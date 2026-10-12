# Offline Saudi Companion — Plan

An offline assistant that hears Saudi dialect, sees through the camera, and answers in Saudi Arabic,
running on an iPhone 17 Pro with no signal, and later on a small dedicated device.

Built by one student on one RTX 5080. Goal: it works, and every claim is measured.

## The end goal

Someone in the desert, with no service, can:

- **Ask by voice in Saudi dialect** and get an answer in Saudi dialect.
- **Send a photo** ("what plant is this?", "does this wood burn?", "does this look cooked?").
- **Get exact prayer times and Qibla** for where they are.
- **Ask religious questions** and get answers quoted from trusted sources, never invented rulings.
- **Get survival help** (fire, water, heat, navigation) from a trusted offline knowledge pack.
- **Just talk**: poetry (Nabati), conversation, general questions.

And it comes with numbers: speech accuracy against the strongest public Saudi-dialect baseline
(NVIDIA Nemotron 3.5 ASR fine-tuned on SDAIA's SADA: 55% → 30% word error rate on Najdi/Hijazi),
quality per area, speed, memory and heat on the phone.

## Core design decisions

### The model understands; tools and sources supply the facts

A 2–4B model will sometimes be confidently wrong. In this project, wrong can hurt someone. So:

| Request | Answered by |
|---|---|
| Prayer times, Qibla | **On-device calculator** (GPS + date). Exact, offline. |
| Survival | **Offline knowledge pack** of trusted guides, searched and quoted |
| Religious questions | **Trusted sources on the device**, quoted with references. The model never issues rulings of its own. |
| Plants / food from a photo | Model describes what it sees. **"Is it safe to eat" always gets a fixed, safe answer.** |
| Poetry, conversation, general | The model itself, in Saudi dialect |

### Keep the core separate from the device

```
core/        model config, prompts, tools, knowledge pack, safety rules   ← portable
eval/        test sets, scoring, review app, results                      ← portable
apps/ios/    thin iPhone app (Swift)
apps/device/ thin app for the dedicated device (later)
```

Moving to a new device means writing a new thin app, not rebuilding the brain.

### Hardware roles

- **RTX 5080 PC (Windows)**: everything — data, evaluation, training, compression.
- **MacBook Air**: only for Xcode builds to the iPhone. Nothing else.
- **iPhone 17 Pro**: first target device.
- **Dedicated device (later)**: an RK3588 board (Orange Pi 5 / Radxa Rock 5, up to 32 GB, NPU) or
  NVIDIA Jetson Orin Nano. Can be sourced in China (e.g. Beijing's Zhongguancun electronics area).

## Open questions — investigate first (Step 0)

1. **Speech-to-speech.** Google's Gemma 4 demo appeared to show talking to the model and it talking back.
   Find out exactly how: does any Gemma 4 model output audio natively, or was the demo
   speech-in → text → separate text-to-speech? This decides the voice design.
2. **Which model.** E2B vs E4B vs Gemma 4 12B (unified multimodal, audio + images) for this use.
   Trade-off: quality vs speed/memory/heat on the iPhone 17 Pro.
3. **iOS runtime.** Which runtime runs Gemma 4 on iOS **with audio and image input**: LiteRT-LM,
   MLX Swift, llama.cpp, Core ML? Known: LiteRT-LM on iPhone 17 Pro GPU ≈ 56 tok/s (E2B),
   ≈ 25 tok/s (E4B); one independent test saw E2B drop to ≈ 27 tok/s after 10 minutes sustained.
4. **Fine-tune → phone.** Can a LoRA fine-tune be merged and converted to the iOS runtime's format
   with audio and vision still working? **Biggest technical risk — prove it early.**
5. **Data licenses.** SADA is listed as CC BY-NC-SA 4.0 (non-commercial — fine for research and
   portfolio, not for Mujawib). Confirm on Kaggle. Check licenses for every other source.

**Done when:** each question has a written answer with sources in `docs/DECISIONS.md`.

## Steps

### Step 1 — Project setup
New folder, GitHub repo (private until release), the layout above.
**Done when:** Gemma 4 E2B and E4B both run and answer (text, image, audio) on the PC.

### Step 2 — Test set (built by Claude Code, reviewed by me)
I don't write cases. Claude Code collects and generates them; I approve, reject or edit.

- **Test set: small, fully reviewed.** A few hundred cases covering all five areas, dialects,
  photos, speech and safety. Each case states the *expected behaviour* (a rubric), not an exact answer.
- **Sources:**
  - Speech: SADA test split (transcripts already verified).
  - Plants/photos: openly licensed, species-identified photos (e.g. iNaturalist observations
    from Saudi, filtered by license).
  - Prayer/Qibla: generated from the exact calculation — correct by construction.
  - Religious: questions paired with a quote + reference from a trusted source.
  - Survival: drafted from established guides, source attached.
  - Poetry/conversation: drafted in Saudi dialect; real Nabati poems where the license allows.
  - Safety: drafted from a list of dangers (poisonous plants, undercooked food, invented rulings).
- **Automatic filtering before I see anything:** duplicates removed, a second model checks
  dialect and facts, doubtful cases flagged.
- **Review app** (build this first): one case at a time, keyboard-driven —
  A approve · R reject · E edit · F flag for second opinion. Doubtful cases first. Progress saved.
- **I check the source supports the answer** — not answer from my own memory.
- **Add:** my own desert photos taken while in Saudi; one or two other native speakers
  blind-review a dialect sample.
- **Freeze** the reviewed test set with a checksum.

**Done when:** one command scores any model on the frozen test set.

### Step 3 — Baseline
Score unchanged E2B and E4B on everything. Speech vs NVIDIA's 55% → 30%.
Also measure on the iPhone: speed, time to first word, memory, heat over sustained use,
and the Arabic token tax (tokens per Arabic word vs English).
**Done when:** a table showing exactly where Gemma 4 fails at Saudi Arabic — first publishable result.

### Step 4 — Tools and knowledge pack
Prayer-time/Qibla calculator, searchable offline survival + religious references, safety rules.
**Done when:** unchanged model + tools beats the model alone on the Step 2 tests.

### Step 5 — Fine-tune
LoRA on the 5080. Speech: SADA training split. Text: Saudi-dialect conversation, tool use,
Nabati poetry, when to call each tool, when to refuse.
**First:** a small fine-tune → convert → run on the iPhone (Open Question 4) before training at scale.
Training data: generated in bulk; I review a random sample per batch. Too many bad → fix the
generator and regenerate, don't fix items one by one.
**Done when:** beats Steps 3 and 4 in every area, no area worse.

### Step 6 — Compress
Quantize at 8 / 4 / 2 bits. Measure quality, memory, speed, battery, heat at each.
**Done when:** quality-vs-size table; the phone setting chosen.

### Step 7 — iPhone app
Offline. Hold to talk, or send a photo; reply in Saudi dialect.
- Show the transcript ("سمعتك تقول: …") so the user can correct it before it answers.
- Compare two speech setups on SADA: **direct** (audio → Gemma) vs **two-stage**
  (Whisper / Apple's on-device Arabic recognition → text → Gemma).
- Voice replies: built-in iOS Arabic voice to start (offline, but likely MSA-sounding).
**Done when:** works on the iPhone 17 Pro in airplane mode.

### Step 8 — Release
Public repo, models on Hugging Face, write-up in Arabic and English with the numbers,
demo video (ideally filmed in the desert). Send to SDAIA, HUMAIN and others.

### Step 9 — Dedicated device
Port the core to the RK3588 or Jetson board. Case, screen, push-to-talk button, camera,
battery (solar is a bonus). Simple, clean, retro.
**Done when:** someone can hold it, no phone, no signal, and ask it something.

### Step 10 — Saudi voice (stretch)
An on-device text-to-speech voice that speaks Saudi dialect, replacing the built-in voice.

## Rules for working on this

- Measure before and after every change. No claim without a number.
- Plans are steps with a "done when", not time estimates.
- Uni comes first (scholarships). The project fits around it.

## References

- NVIDIA × SDAIA SADA ASR: https://www.gccbusinessnews.com/nvidia-fine-tunes-nemotron-3-5-asr-sada/
- SADA dataset (hours, license): https://ieee-dataport.org/node/14747
- Gemma 4 announcement: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Gemma 4 E2B LiteRT-LM (iPhone numbers): https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
- Gemma 4 E4B LiteRT-LM: https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm
- LiteRT-LM blog: https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/
- Sustained iPhone benchmark: https://github.com/john-rocky/apple-silicon-llm-bench
- Google AI Edge, Gemma 4: https://ai.google.dev/edge/litert-lm/models/gemma-4
