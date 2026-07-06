# Source catalog — multi-agent runs

Každý model/agent, který plní [source-catalog-brief.md](../../../.cursor/skills/trading-geopolitical-analyst/source-catalog-brief.md),
ukládá výstupy **vlastní podsložku** pod `agents/<agent_slug>/`.

| Soubor / složka | Účel |
|-----------------|------|
| `agents/<agent_slug>/meta.json` | Identita agenta, model, časové razítko |
| `agents/<agent_slug>/catalog.json` | Kumulativní katalog + progress pro daného agenta |
| `agents/<agent_slug>/batches/<agent_slug>_<seq>_<phase>.md` | Jednotlivé dávky k review |

Sloučený whitelist (`source_whitelist.json`) vzniká až po schválení uživatele — není per-agent.
