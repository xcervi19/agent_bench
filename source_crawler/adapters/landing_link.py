"""Download a file that a landing page links to, when the filename keeps moving.

The other adapters assume the file's URL is knowable in advance: `static_file`
and `static_pdf` take a fixed endpoint, `opec_assetdb` builds candidates from a
`{month}/{year}` template. Neither fits a statistical agency that keeps a stable
*page* and republishes the file underneath it with a new name every release.

PPAC is the case that forced this. Its sectoral gas consumption lives at a fixed
page, but the file behind it is

    /uploads/page-images/1787815916_4_NG-C-Sectoral-Consumption.xlsx
                         ^^^^^^^^^^ changes on every publication

so a fixed endpoint goes stale within the month and a template cannot guess the
prefix. What *is* stable is the tail of the name, which is how a human finds it
on the page. This adapter does the same thing: fetch the page, match the link,
download it.

Deliberately plain HTTP and a regex over the served HTML — no browser, no
JavaScript execution. That is a design constraint, not a shortcut: an agency
that only exposes its data through a scripted download is one we acquire through
the semi-automatic `browser-fetch` path (see `source_acquisition_pipeline.md`),
where a person saves the file, rather than one we try to out-engineer. If this
adapter's `discover` finds nothing, that is the signal to take that route.

Configuration (`extras`):

    link_pattern   regex matched against the page's href/src values; the first
                   capture group, or the whole match, is the file URL
    extension      expected file extension (".xlsx", ".csv", ".pdf", …)
    prefer         "last" to take the final match rather than the first, for
                   pages that list oldest-first
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

from ..base import SourceAdapter
from ..models import (
    DocRef,
    DownloadedDoc,
    SourceAssessment,
    SourceConfig,
    SourceTarget,
)
from ..registry import register
from ._http import http_get
from .static_file import _guess_content_type, _normalize_ext, _validate_body

# Every run of characters that could form a URL. Deliberately not a quote-pairing
# regex: an earlier attribute without a URL in it (`class="a b"`) consumes the
# opening quote of the next one as its own closing delimiter, and the link that
# follows is then never offered as a candidate. Scanning for URL-legal runs
# cannot drift that way.
#
# Narrowing to <a href> would also miss the files that sit in onclick handlers
# and data- attributes, which is where agency sites keep half of them. The
# caller's `link_pattern` does the filtering, so a generous scan is free.
_URL_TOKEN = re.compile(r"""[^\s"'()<>\\]+""")


def _candidate_links(html: str, base_url: str, pattern: str) -> list[str]:
    """Absolute URLs in `html` whose text matches `pattern`, in document order."""
    matcher = re.compile(pattern, re.IGNORECASE)
    seen: set[str] = set()
    found: list[str] = []
    for raw in _URL_TOKEN.findall(html):
        match = matcher.search(raw)
        if not match:
            continue
        target = match.group(1) if match.groups() else raw
        absolute = urljoin(base_url, target.strip())
        if not urlparse(absolute).scheme.startswith("http"):
            continue
        if absolute not in seen:
            seen.add(absolute)
            found.append(absolute)
    return found


def _require_pattern(config: SourceConfig | SourceTarget) -> str:
    extras = config.extras if isinstance(config, SourceConfig) else config.hints
    pattern = str(extras.get("link_pattern") or "").strip()
    if not pattern:
        raise RuntimeError(
            f"landing_link needs extras['link_pattern'] for {getattr(config, 'source_id', '?')!r}"
        )
    return pattern


def _pick(links: list[str], config: SourceConfig) -> str:
    if str(config.extras.get("prefer") or "first").lower() == "last":
        return links[-1]
    return links[0]


@register
class LandingLinkAdapter(SourceAdapter):
    name = "landing_link"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        """Is there a matching file behind this page, and can we read it?

        Answers the question a register entry cannot: a domain that resolves is
        not the same as a source that hands us data. Reported as `viable` plus a
        reason either way — a hard block is a recorded fact, not a retry loop.
        """
        try:
            pattern = _require_pattern(target)
        except RuntimeError as exc:
            return SourceAssessment(self.name, target.url, False, str(exc))

        resp = http_get(target.url)
        if resp.status_code >= 400:
            return SourceAssessment(
                self.name, target.url, False, f"landing page HTTP {resp.status_code}"
            )
        links = _candidate_links(resp.text, str(resp.url), pattern)
        if not links:
            return SourceAssessment(
                self.name,
                target.url,
                False,
                f"no link matching {pattern!r} — try the browser-fetch path",
            )

        head = http_get(links[0])
        if head.status_code >= 400:
            return SourceAssessment(
                self.name, links[0], False, f"file HTTP {head.status_code}"
            )

        source_id = target.source_id or urlparse(target.url).netloc.replace(".", "_")
        return SourceAssessment(
            adapter=self.name,
            endpoint=target.url,
            viable=True,
            reason=f"{len(links)} match(es); newest {head.headers.get('last-modified', 'undated')}",
            proposed_config=SourceConfig(
                source_id=source_id,
                adapter=self.name,
                endpoint=target.url,
                title=str(target.hints.get("title") or source_id),
                publisher=str(target.hints.get("publisher") or ""),
                interval_hours=int(target.hints.get("interval_hours", 168)),
                commodity=str(target.hints.get("commodity", "natural_gas")),
                region=target.hints.get("region"),
                tier=int(target.hints.get("tier", 1)),
                domain=str(target.hints.get("domain", "official_stats")),
                tags=tuple(target.hints.get("tags", ())),
                label_assignment=target.hints.get("label_assignment"),
                document_type=target.hints.get("document_type"),
                use_for=tuple(target.hints.get("use_for") or ()),
                extras=dict(target.hints),
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        pattern = _require_pattern(config)
        resp = http_get(config.endpoint)
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} for {config.endpoint}")
        links = _candidate_links(resp.text, str(resp.url), pattern)
        if not links:
            raise RuntimeError(
                f"no link matching {pattern!r} on {config.endpoint} — "
                "the page changed, or the file is script-generated (use browser-fetch)"
            )
        url = _pick(links, config)
        ext = _normalize_ext(
            str(config.extras.get("extension") or "") or "." + url.rsplit(".", 1)[-1].lower()
        )
        return [
            DocRef(
                url=url,
                title=config.title or config.source_id,
                extras={"extension": ext, "referer": config.endpoint},
            )
        ]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        ext = _normalize_ext(str(ref.extras.get("extension") or ".bin"))
        resp = http_get(ref.url, referer=str(ref.extras.get("referer") or config.endpoint))
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} for {ref.url}")
        body = resp.content
        # Rejects an HTML error page served with a 200, which is how these sites
        # usually say "gone" — otherwise we would store the error as the dataset.
        _validate_body(body, ext, ref.url)
        return DownloadedDoc(
            ref=ref,
            body=body,
            content_type=_guess_content_type(ext, resp.headers.get("content-type")),
            extension=ext,
            meta={
                "landing": config.endpoint,
                "resolved_url": ref.url,
                "last_modified": resp.headers.get("last-modified"),
            },
        )
