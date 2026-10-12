# gemma-mini: Offline Saudi Companion

An offline assistant that hears Saudi dialect, sees through the camera, and answers in Saudi Arabic.
It is built on Google's Gemma 4 small models, runs first on an iPhone 17 Pro, and later on a small dedicated device.
Facts come from tools and trusted sources (prayer-time calculator, survival and religious references); the model understands and talks.

The full plan, with steps and "done when" checks, is in [PLAN.md](PLAN.md).

| Folder | What it holds |
|---|---|
| `core/` | Model config, prompts, tools, knowledge pack, safety rules (portable) |
| `eval/` | Test sets, scoring, review app, results (portable) |
| `apps/ios/` | Thin iPhone app (Swift) |
| `apps/device/` | Thin app for the dedicated device (later) |
| `docs/` | Research notes (`docs/research/`) and decisions (`docs/DECISIONS.md`) |

Current phase: **research (Step 0)**. No training or model runs yet.
