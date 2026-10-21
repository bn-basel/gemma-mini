# gemma-mini: Offline Saudi Companion

> **Status: work in progress.** The research phase is finished. Nothing is trained, built or measured yet, so this page
> makes no performance claims. This is a private repository.

An offline assistant for people in the Saudi desert with no signal. You talk to it in Saudi dialect and it answers in Saudi
dialect. It can also look through the camera. It is built on Google's Gemma 4 small models (E2B and E4B), runs first on an
iPhone 17 Pro, and later on a small, cheap handheld device.

The model understands and talks. **Facts come from tools and trusted sources**, because a small model is sometimes
confidently wrong, and out in the desert a wrong answer can hurt someone.

## What we want to build

| You ask… | It is answered by |
|---|---|
| Something by voice, in Saudi dialect | Speech goes into Gemma 4, the text answer is spoken back by a separate text-to-speech voice |
| "What plant is this?", "Does this look cooked?" (a photo) | The model describes what it sees. "Is it safe to eat?" always gets a fixed, safe answer |
| Prayer times and Qibla | An on-device calculator (GPS and date). Exact, and offline |
| A religious question | Quotes from trusted sources, with the reference. The model never gives a ruling of its own |
| Survival help (fire, water, heat, navigation) | An offline knowledge pack of trusted guides, searched and quoted |
| Poetry, conversation, general questions | The model itself, in Saudi dialect |

## The plan

Every step has a "done when" check, and no claim goes in without a number.

| Step | What | Status |
|---|---|---|
| 0 | Research: voice design, which model, iOS runtime, fine-tune to phone, speech baseline, data licences, device | done |
| 1 | Setup: Gemma 4 E2B and E4B answer text, image and audio on the PC | planned |
| 2 | A small test set, fully reviewed by a person, then frozen with a checksum | planned |
| 3 | Baseline: score the unchanged models, including speed, memory and heat on the iPhone | planned |
| 4 | Tools and knowledge pack: prayer times, Qibla, survival and religious references, safety rules | planned |
| 5 | Fine-tune (LoRA) for Saudi dialect. First a tiny test to prove it can run on the iPhone | planned |
| 6 | Compress (8, 4 and 2 bits) and measure quality, speed and size at each | planned |
| 7 | iPhone app: hold to talk or send a photo, works in airplane mode | planned |
| 8 | Release: public repo, models, write-up in Arabic and English, demo video | planned |
| 9 | Dedicated handheld device (a 16 GB RK3588 board first) with a button, camera and battery | planned |
| 10 | A text-to-speech voice that speaks Saudi dialect (stretch goal) | planned |

The full plan is in [PLAN.md](PLAN.md). The research decisions, each with its sources, are in
[docs/DECISIONS.md](docs/DECISIONS.md).

## What the research found so far

- No Gemma 4 model speaks. They take speech in and give text out, so voice replies need a separate text-to-speech step.
- E2B is the first model to build on because it is the one that is fast enough on the phone. E4B stays as the quality
  candidate, and both get scored.
- Running a fine-tuned Gemma 4 on an iPhone with audio and vision both working is **not yet proven by anyone**. It is the
  biggest technical risk, so it gets tested first with a tiny test model.
- The public reference for Saudi speech recognition is NVIDIA's fine-tune on SDAIA's SADA dataset. We will report against it
  with a fixed, written recipe.
- Some of the best Saudi speech data is research-only (non-commercial), which limits what can be released publicly.

## Layout

| Folder | What it holds |
|---|---|
| `core/` | Model config, prompts, tools, knowledge pack, safety rules (portable) |
| `eval/` | Test sets, scoring, review app, results (portable) |
| `apps/ios/` | Thin iPhone app (Swift) |
| `apps/device/` | Thin app for the dedicated device (later) |
| `docs/` | Research notes (`docs/research/`) and decisions (`docs/DECISIONS.md`) |

The core is kept separate from the device, so moving to a new device means writing a new thin app, not rebuilding the brain.

## How to run the tests

Python 3.13. From this folder:

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest
```

(On macOS/Linux use `.venv/bin/` instead of `.venv/Scripts/`.) CI runs the same tests on every pull request and push to `main`.
