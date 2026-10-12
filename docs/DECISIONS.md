# Decisions: research phase (Step 0)

Written 2026-10-13. Each decision links to its research note in `docs/research/`, where every claim has its source.
Key numbers marked ✔ were re-checked against the primary source by a second pass on 2026-10-13.
Status words: **decided** (go with this), **provisional** (go with this until a named measurement says otherwise), **open**.

| # | Question | Decision | Status |
|---|---|---|---|
| D1 | Speech-to-speech | Speech in → Gemma 4 → text → separate TTS. No Gemma 4 model speaks. | decided |
| D2 | Which model | Prove the pipeline on **E2B**; keep **E4B** as the quality candidate; 12B is not a phone option | provisional |
| D3 | iOS runtime | **LiteRT-LM** (Swift, preview); fallback **llama.cpp + libmtmd**; second fallback CoreML-LLM | provisional |
| D4 | Fine-tune → phone | Train the language model only, keep Google's audio/vision parts, splice into Google's bundle. **Not proven: test first.** | provisional, biggest risk |
| D5 | Speech baseline | Report against both NVIDIA's numbers and the Open Arabic ASR leaderboard, with a fixed recipe | decided |
| D6 | Data and licenses | SADA is research only. Public release uses only the "safe" list. | decided (legal grey area flagged) |
| D7 | Dedicated device | **16 GB RK3588** board running E2B on its NPU via RKLLM; Jetson Orin Nano Super only if needed | provisional |

---

## D1. Voice design: speech in, text out, separate TTS

- **Finding.** All Gemma 4 models output text only. E2B, E4B and 12B Unified accept audio (max 30 s per clip); 26B A4B and 31B
  don't ✔ ([model card](https://ai.google.dev/gemma/docs/core/model_card_4)). The voice demos chain three models, e.g.
  Parakeet → Gemma 4 31B → Qwen3-TTS in the cloud ([HF + Cerebras](https://huggingface.co/blog/cerebras-gemma4-voice-ai)).
  Google's native speech output (Gemini Live) is cloud-only. → [01-speech-to-speech.md](research/01-speech-to-speech.md)
- **Decision.** Voice reply = Gemma's text → a TTS engine. Start with iOS's built-in Arabic voice (the long-standing one is
  "Maged", ar-SA; no Saudi-dialect Apple voice found). Saudi TTS stays Step 10.
- **Candidate for Step 10:** Fasee7 Najdi Small (Apache 2.0, a LoRA on a 2B TTS base). Whether it fits on the phone next to
  Gemma is unknown. → [06](research/06-data-and-licenses.md)
- **Consequence.** Clips over 30 s must be cut before Gemma sees them (Step 7's hold-to-talk needs a 30 s limit or chunking).

## D2. Model: prove the pipeline on E2B, keep E4B as the quality candidate

The notes disagree, and this is how they're reconciled:

| | E2B | E4B | 12B Unified |
|---|---|---|---|
| SADA speech WER, zero-shot (leaderboard) ✔ | 46.2% | **43.4%** | not listed |
| FLEURS Arabic WER (Google tech report, read MSA) | 14.3% | 16.2% | 7.0% |
| iPhone 17 Pro GPU decode / time to first token ✔ | **56 tok/s / 0.3 s** | 25 tok/s / 0.9 s | not measured; on-device build is desktop/web only |
| LiteRT-LM file | 2.58 GB | 3.65 GB | 6.88 GB |
| RK3588 board (RKLLM) ✔ | 11.1 tok/s, about 2.5 GB | no published number | — |
| Fine-tune export on a 31 GB PC | reported feasible with workarounds | reports of 48–92 GB+ RAM needed | — |

Sources: [leaderboard data](https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard),
[LiteRT-LM Gemma 4 page](https://developers.google.com/edge/litert-lm/models/gemma-4),
[Rockchip benchmark](https://github.com/airockchip/rknn-llm/blob/main/benchmark.md). → [02](research/02-which-model.md), [04](research/04-finetune-to-phone.md), [07](research/07-dedicated-device.md)

- **Decision.** Build and prove everything (phone app, fine-tune → phone, board) on **E2B** first: it is the only size that is
  fast on the phone, runs on the board, and exports on this PC. Score **both** in Step 3, as the plan already says.
  Switch the main model to E4B only if Step 3 shows a clear gain on the Saudi test set that is worth half the speed.
- **No Saudi-dialect text benchmark exists** for any Gemma 4 size. Step 3 will be the first.
- **12B is out** for the phone. It stays a possible "teacher" on the PC for generating training data.

## D3. iOS runtime: LiteRT-LM first

| Runtime | Image on iPhone | Audio on iPhone | Status |
|---|---|---|---|
| **LiteRT-LM** (Google) | API exists; open bug on a physical iPhone ([#2979](https://github.com/google-ai-edge/LiteRT-LM/issues/2979)) | API exists; open null-output report ([#3850](https://github.com/google-ai-edge/LiteRT-LM/issues/3850)), likely needs `audioBackend: .cpu()` | Official; Swift API is "Early Preview" |
| **llama.cpp + libmtmd** | official | official ([PR #21421](https://github.com/ggml-org/llama.cpp/pull/21421)) | No public iPhone multimodal report; write your own Swift wrapper |
| **MLX Swift** | yes | **no** (audio PR #392 unmerged) | skip for now |
| **CoreML-LLM** | claimed | claimed | One developer; claims unverified |

- Google's own Gallery app does image + audio on iPhone, so the runtime can work. → [03-ios-runtime.md](research/03-ios-runtime.md)
- The "27 tok/s after 10 minutes" figure in PLAN.md comes from one undated run. The same author's later 600 s run kept 76%
  of burst speed. **Measure it ourselves** (Step 3).

## D4. Fine-tune → phone: plausible, not proven. Prove it first.

- **Verdict.** Every piece exists, but nobody has published a fine-tuned Gemma 4 running on an iPhone with audio **and**
  vision working. → [04-finetune-to-phone.md](research/04-finetune-to-phone.md)
- **Key facts:**
  - Google's converter (`litert-torch`) added Gemma 4 audio export on 2026-09-24, nightly builds only. It needs Linux, so
    **WSL2** on this PC, and lots of RAM.
  - LiteRT-LM accepts a LoRA file at runtime for the Gemma 4 bundle, but it **silently has no effect** ✔
    ([#3173](https://github.com/google-ai-edge/LiteRT-LM/issues/3173), open). So we **merge**.
  - Closest precedent: a Swahili ASR fine-tune of E2B ships as a `.litertlm` whose audio sections appear to come from Google's
    bundle ([Ndizi](https://huggingface.co/smutuvi/ndizi-gemma4-e2b-african-asr-litert)). It has no vision and names no tested device.
  - Unsloth trains on Windows directly. llama.cpp converts merged fine-tunes with both audio and vision.
- **Decision.** LoRA on the **language model only**; freeze the audio and vision parts. Merge, export the text part, and splice
  it into Google's `.litertlm` (keeping Google's audio/vision sections). Fallback: llama.cpp GGUF + BF16 mmproj.
- **Prove it with a "canary" LoRA** before any real training: a tiny adapter that makes every answer start with "أبشر".
  Done when the iPhone shows the canary word **and** transcribes a clip **and** describes a photo. The steps are in note 04.
- **Unproven:** whether training only the language model is enough to improve Saudi speech recognition.

## D5. Speech baseline: report against both references, same recipe

- **NVIDIA** ✔ ([blog, 2026-09-30](https://developer.nvidia.com/blog/fine-tuning-nvidia-nemotron-for-saudi-arabic-dialects-with-a-path-to-other-languages/)):

  | Model | Test set | WER | CER |
  |---|---|---|---|
  | `nemotron-3.5-asr-streaming-0.6b`, base | Najdi + Hijazi subset of SADA test | 55.05% | 31.63% |
  | same, fine-tuned (133.7 h Najdi + Hijazi) | Najdi + Hijazi subset | 29.96% | 12.18% |
  | same, fine-tuned, beam-8 | Najdi + Hijazi subset | 27.25% | 10.63% |
  | base → fine-tuned | full SADA test | 58.84% → 35.61% | 35.40% → 15.97% |

  The main table uses greedy decoding and 320 ms streaming. **The subset's size and filter are not published**, and the
  fine-tuned weights are not released (base model: OpenMDW-1.1). NVIDIA did the work; SDAIA published the dataset.
- **Open Arabic ASR leaderboard**, full SADA test (6,189 clips, 10.75 h), zero-shot ✔: Gemma 4 E4B 43.40%,
  E2B 46.23%, base Nemotron 53.06%, Whisper large-v3 55.96%. Best on SADA: Audar-ASR-V1-Turbo 28.92%.
- **Watch out:** the two sources clean up text differently, so their numbers don't line up (base Nemotron is 58.84% at NVIDIA
  and 53.06% on the leaderboard).
- **Decision.** Use the 8-step recipe in [05-saudi-speech-baseline.md](research/05-saudi-speech-baseline.md):
  - the full test split plus a Najdi + Hijazi subset;
  - two text normalizers (one matching the leaderboard, one matching NVIDIA);
  - corpus-level WER and CER;
  - calibrate by re-running the public base Nemotron;
  - compare zero-shot only with zero-shot, and fine-tuned only with fine-tuned.

## D6. Data and licenses

- **SADA is CC BY-NC-SA 4.0** ✔ (Kaggle `sdaiancai/sada2022`, owner NCAI_SDAIA, 77 GB, about 667 h). It is fine for research and
  the portfolio, and not for a commercial product.
- **Grey area:** if model weights trained on SADA count as an "adaptation", ShareAlike would force those weights to be released
  BY-NC-SA. This affects Step 8 ("models on Hugging Face"). SDAIA or a lawyer should confirm.
  → [06-data-and-licenses.md](research/06-data-and-licenses.md)
- **Safe for public release** (with credit/conditions):
  - iNaturalist / GBIF photos filtered to CC0 + CC BY (836 iNat / about 26.6k GBIF Saudi plant records);
  - Wikimedia Commons;
  - US Army ATP 3-50.21;
  - Tanzil Quran text (verbatim only);
  - Sanadset (CC BY) and Open-Hadith-Data (ODbL);
  - adhan libraries (MIT);
  - Common Voice Arabic (CC0);
  - Fasee7 Najdi, ArTST.
- **Research only:**
  - SADA, MADAR, NADI, SaudiBERT;
  - WHO guidance;
  - Ashaar / APCD / Tarab poetry sets;
  - MMS-TTS, XTTS-v2, Food-101.
- **Avoid:**
  - X/Twitter content for training;
  - living poets' work;
  - IslamQA bulk text for training;
  - recording Apple system voices.
- **No fitting dataset** for food doneness or wood/fuel photos: build our own.
- **Unknown:**
  - the terms of alifta.gov.sa, sunnah.com, Saudi Civil Defense, Red Crescent and the Ministry of Health;
  - the rules for the AI-training exception in Saudi Arabia's new Copyright Law (in force 2026-08-12).

## D7. Dedicated device: 16 GB RK3588 first

| | RK3588 (e.g. Orange Pi 5 Pro / 5 Max, Radxa ROCK 5B+) | Jetson Orin Nano Super |
|---|---|---|
| Gemma 4 E2B with audio + image | official in RKLLM v1.3.0 / v1.3.1 ✔ | official Jetson AI Lab page; E4B "works" per staff |
| E2B decode | 11.1 tok/s on the NPU, about 2.5 GB ✔ | 24.2 tok/s on the GPU (Google) |
| Power while chatting | about 8 W (one informal reading) | 7–25 W modes |
| Price | cheaper (CNY shop prices not found) | **$399** since July 2026 (was $249) |
| Audio / camera | some boards have a mic; MIPI CSI camera ports | no audio jack; 2 × CSI |

→ [07-dedicated-device.md](research/07-dedicated-device.md)

- **Decision.** Start with a 16 GB RK3588 board running E2B through RKLLM. Add a Jetson only if E2B is too slow there or the
  model has to be E4B.
- **Buying in China:**
  - Both board makers sell in China. NVIDIA lists China as a sales region (export class 5A992.C).
  - Saudi customs allows SAR 3,000 duty-free in personal luggage, with receipts.
  - Power banks need a **3C mark** on Chinese domestic flights.
  - Lithium batteries of up to 100 Wh are fine; spare batteries go in carry-on only.
  - Saudi Arabia uses Type G plugs.
- **Unknown:**
  - E4B on RK3588;
  - any end-to-end measurement with real audio and camera input;
  - CNY shop prices and warranty;
  - whether Wi-Fi boards need CST type approval in Saudi Arabia.

---

## Corrections to PLAN.md suggested by this research

(PLAN.md is the owner's; these are proposals, not edits.)

1. "Gemma 4 12B" is officially **Gemma 4 12B Unified**. It is not an iPhone option today (D2).
2. The "27 tok/s after 10 minutes" figure is a single undated run; a later run by the same author kept 76% (D3).
3. The NVIDIA result is NVIDIA's own work on SDAIA's dataset. Its 55% → 30% is on a Najdi + Hijazi **subset** with greedy
   decoding, and the fine-tuned model is not public (D5).
4. Step 1 and Step 5 need **WSL2** on the PC for Google's converter (D4).
5. Step 8 "models on Hugging Face": weights trained on SADA may have to be released as BY-NC-SA, or not at all (D6).
6. Step 7: Gemma takes at most 30 s of audio per clip (D1).

## First steps for Step 1 (no GPU)

Each step is written so it can be checked. Downloads are named with their size, and nothing gets downloaded without the owner's yes.

1. **Scoring code first (no download).** In `eval/`, write both Arabic text normalizers and a corpus-level WER/CER scorer, with
   unit tests on hand-made examples (diacritics, ة, ى, hamza forms, a digit).
   *Done when:* the tests pass, and the scorer matches NeMo's `word_error_rate` on a toy example.
2. **SADA test manifest (small download).** Fetch the leaderboard's `sada_test.json` (a small text file), and read SADA's file
   list from the Kaggle metadata, without downloading audio.
   *Done when:* the manifest has 6,189 IDs and 10.75 h, the Najdi + Hijazi subset is counted, and we know whether the test audio
   can be downloaded on its own (the whole dataset is 77 GB). If it can, its size goes to the owner for a yes.
3. **Phone baseline (on the Mac and iPhone, not the PC).** A minimal Swift app with the LiteRT-LM package and Google's E2B
   `.litertlm` (**2.58 GB download**, needs a yes). Run it with one text prompt, one photo, and one 10 s Arabic WAV, with
   `audioBackend` and `visionBackend` set to `.cpu()`.
   *Done when:* all three answer sensibly on the physical iPhone 17 Pro, or the failure is logged and matched to #2979 / #3850.
4. **WSL2 readiness check (no download).** Check whether WSL2 is installed, and how much RAM and swap it gets.
   *Done when:* this is written down next to the converter's reported needs (D4), with a proposed `.wslconfig`.
5. **PC run of E2B and E4B, the plan's Step 1 "done when"** (needs the PC to be free, plus **2.58 GB + 3.65 GB** of downloads,
   and a yes). Use the LiteRT-LM CLI, which runs on Windows. Test text, one image and one audio clip.
   *Done when:* both models answer all three on the PC.
