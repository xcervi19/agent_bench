"""One oversized stdout line must not end the run.

A WebFetch tool result can carry a whole page body on a single stream-json line.
That line is unreadable either way, but killing the process over it discards every
event that would have followed — the whole topic run for one large page.
"""

import asyncio
import json

import pytest

from apps.claude_agent.runner import MAX_OVERSIZED_LINES, stream_lines

LIMIT = 128
RESULT = json.dumps({"type": "result", "subtype": "success"})


def _reader(*chunks: bytes) -> asyncio.StreamReader:
    reader = asyncio.StreamReader(limit=LIMIT)
    for chunk in chunks:
        reader.feed_data(chunk)
    reader.feed_eof()
    return reader


async def _drain(reader: asyncio.StreamReader, killed: list[bool]) -> list[str]:
    deadline = asyncio.get_running_loop().time() + 30
    return [
        line
        async for line in stream_lines(
            reader, deadline=deadline, limit=LIMIT, kill=lambda: killed.append(True)
        )
    ]


@pytest.mark.asyncio
async def test_oversized_line_is_skipped_and_the_stream_continues():
    killed: list[bool] = []
    lines = await _drain(
        _reader(b"x" * (LIMIT * 4) + b"\n", RESULT.encode() + b"\n"),
        killed,
    )

    assert not killed
    assert RESULT in lines, "the event after the oversized line must still arrive"
    assert any(json.loads(line).get("warning") == "oversized_line_skipped" for line in lines)


@pytest.mark.asyncio
async def test_events_before_an_oversized_line_are_kept():
    killed: list[bool] = []
    first = json.dumps({"type": "assistant"})
    lines = await _drain(
        _reader(first.encode() + b"\n", b"y" * (LIMIT * 4) + b"\n", RESULT.encode() + b"\n"),
        killed,
    )

    assert not killed
    assert lines.index(first) < lines.index(RESULT)


@pytest.mark.asyncio
async def test_a_stream_of_nothing_but_oversized_lines_gives_up():
    killed: list[bool] = []
    # One oversized line costs exactly one skip — `readline` drops that line and
    # keeps the rest of the buffer — so the cap is reached only by a stream that is
    # oversized lines all the way down.
    oversized = [b"z" * (LIMIT * 2) + b"\n"] * (MAX_OVERSIZED_LINES + 1)
    lines = await _drain(_reader(*oversized), killed)

    assert killed
    errors = [json.loads(line) for line in lines if json.loads(line).get("type") == "error"]
    assert errors and "line limit" in errors[-1]["error"]


@pytest.mark.asyncio
async def test_normal_lines_pass_through_untouched():
    killed: list[bool] = []
    lines = await _drain(_reader(RESULT.encode() + b"\n"), killed)

    assert not killed
    assert lines == [RESULT]


@pytest.mark.asyncio
async def test_the_oversized_counter_resets_after_a_good_line():
    """Otherwise a long run accumulates skips and trips the cap on unrelated lines."""
    killed: list[bool] = []
    chunks: list[bytes] = []
    for _ in range(MAX_OVERSIZED_LINES):
        chunks.append(b"x" * (LIMIT * 2) + b"\n")
        chunks.append(RESULT.encode() + b"\n")
    lines = await _drain(_reader(*chunks), killed)

    assert not killed
    assert lines.count(RESULT) == MAX_OVERSIZED_LINES
