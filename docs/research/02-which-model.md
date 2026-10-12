# Q2. Which model

Research date: 2026-10-13. Desk research only: nothing was downloaded or run.
Labels: **[confirmed]** = primary source (Google, Apple, the benchmark's own data file). **[reported]** = secondary or independent source only. **[unverified]** = claim found but not checked against a primary source, or my own arithmetic.

## Question

Which Gemma 4 model should the offline Saudi-dialect voice + camera assistant start with: E2B, E4B, or the "12B"? The comparison covers Arabic and Saudi-dialect quality, audio input, image input, memory, and speed on an iPhone 17 Pro. It also names the other Gemma 4 sizes.

## Short answer

- **"12B" is a real model.** Its official name is **Gemma 4 12B Unified** (`google/gemma-4-12B-it`). It was released on 2026-06-03, two months after E2B/E4B ([2], [5]). The full family is E2B, E4B, 12B Unified, 26B A4B and 31B. Only E2B, E4B and 12B accept audio ([3]).
- **Start with E4B on LiteRT-LM (GPU), and keep E2B as a drop-in fallback.** E4B has the better Saudi-dialect speech score: 43.4% word error rate (WER) on the Saudi TV test set SADA, against 46.2% for E2B ([22]). Its multilingual knowledge score is also higher: MMMLU 76.6% vs 67.4% ([3]). It fits on the phone (about 3.4 GB measured), and Google publishes iPhone 17 Pro numbers for it: 25 tok/s decode ([12]).
- **12B is not an option on iPhone yet.** Google's on-device build targets macOS, Linux, Windows and web only. It needs about 7.3–7.9 GB of GPU memory, and nobody has published an iPhone measurement ([13]).
- **No published benchmark measures Saudi-dialect *text* quality for E2B, E4B or 12B.** The only Saudi-dialect number is the speech-recognition score above, and both small models get roughly 4–5 words wrong in every 10 on Saudi TV speech ([22]).

## Comparison table

| | **Gemma 4 E2B** | **Gemma 4 E4B** | **Gemma 4 12B Unified** |
|---|---|---|---|
| Official ID | `google/gemma-4-E2B-it` [4] | `google/gemma-4-E4B-it` [3] | `google/gemma-4-12B-it` [5] |
| Released | 2026-03-31 [2] | 2026-03-31 [2] | 2026-06-03 [2] |
| Parameters (total / effective) | 5.1B / 2.3B effective [3] | 8B / 4.5B effective [3] | 11.95B, dense [3] |
| Inputs | text, image, audio, video [3] | text, image, audio, video [3] | text, image, audio, video; no separate encoders [3][5] |
| Context (model / LiteRT-LM file) | 128K / up to 32K [3][11] | 128K / up to 32K [3][12] | 256K / up to 128K [3][13] |
| MMMLU (multilingual knowledge; not Arabic-specific) | 67.4% [3] | 76.6% [3] | 83.4% [3] |
| Arabic speech, FLEURS (read Arabic, WER, lower is better) | 14.3% [6] | 16.2% [6] | 7.0% [6] |
| **Saudi speech, SADA (Saudi TV, WER)** | **46.2%** [22] | **43.4%** [22] | not tested |
| Arabic ASR leaderboard average WER (6 test sets) | 35.87 [22] | 32.98 [22] | not tested |
| Arabic text leaderboards (OALL, AraGen, BALSAM) | not listed [23][24] | not listed [23][24] | not listed [23][24] |
| LiteRT-LM file size | 2,583 MB [11] | 3,654 MB [12] | 6,883 MB [13] |
| Peak memory, iPhone 17 Pro, GPU (LiteRT-LM) | 1,450 MB [11] | 3,380 MB [12] | no iOS build [13] |
| iPhone 17 Pro decode, GPU (LiteRT-LM, Google) | 56.5 tok/s [11] | 25.1 tok/s [12] | not measured |
| iPhone 17 Pro prefill, GPU (LiteRT-LM, Google) | 2,878 tok/s [11] | 1,189 tok/s [12] | not measured |
| iPhone 17 Pro time to first token, GPU | 0.3 s [11] | 0.9 s [12] | not measured |
| Sustained 10 min, iPhone 17 Pro, LiteRT-LM GPU | 56 → 27 tok/s (48% kept) [16] | not measured | not measured |

## Findings

### 0. Which Gemma 4 sizes exist (exact names)

- **[confirmed]** The Gemma release log lists "Release of Gemma 4" (E2B, E4B, 31B, 26B A4B) on 2026-03-31, MTP drafters on 2026-04-16, and "Release of Gemma 4 12B Unified" on 2026-06-03 ([2]). MTP (multi-token prediction) is a small helper model that guesses several tokens at once to speed up output. The Google blog post announcing the first four sizes is dated 2026-04-02 ([1]).
- **[confirmed]** Model card names: **E2B, E4B, 12B Unified, 26B A4B** (a mixture-of-experts model with 25.2B total and 3.8B active parameters), and **31B** (dense) ([3]). The Hugging Face card calls them "five sizes" ([5]).
- So "12B" is correct as a size. The full name is "Gemma 4 12B Unified". Do not confuse it with **Gemma 3 12B**, an older model that still shows up in 2026 Arabic papers ([30]).
- **[confirmed]** 26B A4B and 31B have no audio input ([3]), so they cannot serve a voice assistant without a separate speech model.

### 1. Arabic and Saudi-dialect quality

**Text (understanding and writing Arabic)**
- **[confirmed]** Google claims pre-training on 140+ languages and "out-of-the-box support" for 35+. Neither list is published, and Arabic is not named on the model card ([3], [4]).
- **[confirmed]** The only official multilingual text score is MMMLU (MMLU questions translated into many languages, averaged): E2B 67.4%, E4B 76.6%, 12B 83.4% ([3], [6] Table 5). No per-language (Arabic) breakdown is published ([6]).
- **[confirmed] Not on the Arabic leaderboards.** The Open Arabic LLM Leaderboard (OALL) results store has no Gemma 4 folder. Its newest Google entries are Gemma 2 ([24]). The AraGen v3 data file (last sync 2026-04-06) lists only **31B (3C3H score 0.727, 10th of 69)** and **26B A4B (0.674, 14th)**. E2B, E4B and 12B are not in it ([23]). 3C3H is a judge-scored mark of correctness, completeness, conciseness, helpfulness, honesty and harmlessness. For scale, Jais-2-8B scored 0.340 on the same file ([23]). I found no Gemma 4 results on BALSAM ([25]).
- **[confirmed] No dialect-specific text numbers exist** for E2B, E4B or 12B. I found no paper or leaderboard that scores any Gemma 4 model on Saudi (Najdi, Hijazi, Gulf) text. The closest work uses other models, for example a June 2026 study of small models on Arabic in which Gemma **3** 12B scored best ([30]).
- **[reported]** The bigger Gemma 4 models score well on AraGen. That suggests the family handles Arabic, mostly Modern Standard Arabic, but it says nothing direct about the small models or about Saudi dialect.

**Speech (Arabic speech recognition)**
- **[confirmed] Google FLEURS Arabic WER** (FLEURS is read-aloud speech, mostly Modern Standard Arabic): E2B 14.3%, **E4B 16.2%**, 12B 7.0%. Older Gemma 3n scored E2B 13.1% and E4B 10.1% ([6] Tables 7–8). Arabic is the one language in the table where Gemma 4 small models are *worse* than Gemma 3n, and where E4B is worse than E2B ([6]).
- **[confirmed] Open Universal Arabic ASR Leaderboard** (hard-coded data in the leaderboard's own code, 37 models) ([22]):

  | Model | Avg WER | SADA (Saudi TV) WER | Common Voice | MGB-2 (broadcast) | Casablanca (dialects) |
  |---|---|---|---|---|---|
  | gemma-4-E4B-it | 32.98 | 43.40 | 19.65 | 17.72 | 58.63 |
  | gemma-4-E2B-it | 35.87 | 46.23 | 23.76 | 20.72 | 60.87 |
  | whisper-large-v3 (reference) | 36.86 | 55.96 | 17.83 | 16.26 | 71.81 |
  | Audar-ASR-V1-Turbo (best average) | 23.17 | 28.92 | 8.09 | 11.08 | 47.02 |

  A third-party page dates the Gemma 4 rows to 2026-05-06 ([26], [reported]).
- **[reported]** SADA is a public set of about 667 hours of Saudi TV audio, mostly in Saudi dialects, built by SDAIA with the Saudi Broadcasting Authority ([27]). It is the closest public proxy for "Saudi dialect speech".
- Takeaways: on Saudi speech **E4B beats E2B** (43.4 vs 46.2 WER), and **both beat Whisper-large-v3**. Both are still far behind a dedicated Arabic recogniser (28.9). No 12B row exists ([22]).

### 2. Audio input

- **[confirmed]** Audio works on **E2B, E4B and 12B Unified** only ([3], [7]). E2B and E4B use a ~300M-parameter audio encoder (305M in the report). 12B has none and feeds raw 40 ms audio chunks straight into the language model ([6] §2.2–2.3, Table 1).
- **[confirmed]** Maximum clip length is **30 seconds**. Input is **16 kHz, mono, 32-bit float**, and each second costs **25 tokens** (Gemma 3n used 6.25) ([7], updated 2026-10-10). The E2B processor config agrees: 16,000 Hz, 128 mel bins, 750 audio tokens, 40 ms per token ([9]). A full 30 s clip is therefore 750 tokens.
- **[confirmed]** Supported tasks are speech recognition (ASR) and speech-to-translated-text. Google says "multiple languages" and publishes no language list ([3], [7]). The FLEURS tables include Arabic ("ar") ([6]).
- **[confirmed]** WER numbers: see Section 1. Model-card summary FLEURS WER: E2B 0.09, E4B 0.08, 12B 0.069 (12B excludes Chinese) ([3]).
- **[confirmed]** The LiteRT-LM files for E2B and E4B include audio. The audio and vision parts load only when needed ([11], [12]). The Swift (iOS) API of LiteRT-LM is labelled "Early Preview" ([15]). Google's own iPhone app, AI Edge Gallery, advertises on-device audio transcription ("Audio Scribe") and photo questions ("Ask Image") ([29]).
- **[unverified]** I found no published test confirming that audio input works through the LiteRT-LM **Swift API** on iPhone, as opposed to Google's own app.

### 3. Image input

- **[confirmed]** All Gemma 4 sizes accept images ([3]). E2B and E4B use a ~150M vision encoder, 26B/31B use ~550M, and 12B has no separate encoder ([3], [6] Table 1).
- **[confirmed]** Images use a **token budget** you pick: 70, 140, 280, 560 or 1120 visual tokens per image. Any aspect ratio and resolution is accepted, and the image is resized to fit the budget ([3], [8]). Low budgets suit classification and captioning; high budgets suit reading small text ([3]). The default is **280** in the E2B processor config ([9]). Video is sampled as frames, up to 60 s at 1 fps ([3]).
- **[confirmed]** The model makes 9 small patches per budget token and merges each 3×3 group into one token ([8]). Patch size is 16 px with pooling kernel 3 ([9]).
- **[unverified, my arithmetic]** One token therefore covers about 48×48 px. A 280-token image is about 645,000 pixels (around 800×800), and 1120 tokens is about 2.6 megapixels.
- No plant, food or wood recognition benchmark exists for any size. The general vision scores rise with size, for example MMMU Pro 44.2 / 52.6 / 69.1 for E2B / E4B / 12B ([3]).

### 4. Memory

- **[confirmed] Per-Layer Embeddings (PLE):** E2B and E4B give every layer its own small lookup table of token embeddings. These tables can be kept in storage and memory-mapped, so the "effective" size that must sit in fast memory is much smaller than the total ([3]). Embedder size: E2B 400M + 2,340M PLE; E4B 670M + 2,820M PLE; 12B 1,000M with no PLE ([6] Table 1).
- **[confirmed] Text-only weights at 32K context** ([6] Table 3):

  | | bf16 (full precision) | quantized | + int8 KV cache |
  |---|---|---|---|
  | E2B | 4.6 GB | 0.8 GB (mobile int2/int4 mix) | +0.05 GB |
  | E4B | 9.0 GB | 2.3 GB (mobile) | +0.14 GB |
  | 12B | 24.0 GB | 7.65 GB (Q4_0) | +0.28 GB |

  The KV cache is the model's working memory of the conversation so far.
- **[confirmed] LiteRT-LM files:** E2B is 2,583 MB, a mix of 2-, 4- and 8-bit weights; its text part can be as small as 0.8 GB, with 1.12 GB of embeddings memory-mapped ([11]). E4B is 3,654 MB, including a 2.24 GB text decoder and 0.67 GB of embeddings ([12]). 12B is 6,883 MB and needs LiteRT-LM v0.17 or later ([13]).
- **[confirmed] Peak memory measured on iPhone 17 Pro (LiteRT-LM, `phys_footprint`, 2K context):** E2B uses 607 MB on CPU and 1,450 MB on GPU. E4B uses 961 MB on CPU and 3,380 MB on GPU ([11], [12]).
- **[confirmed] 12B memory on Macs:** about 7,300–7,900 MB of GPU memory with LiteRT-LM at 4K context ([13]). One MLX 4-bit run reported 13.8 GB peak Metal memory and 9.1 GB process memory on a 48 GB Mac mini (2026-10-03) ([18], [reported]).
- **[confirmed] iPhone 17 Pro RAM:** Apple's tech-specs page lists only storage, not RAM ([19]). **12 GB** comes from MacRumors reading Xcode 26 (2025-09-09) ([20], [reported]). Apple does not publish the per-app memory limit. Apps can request a higher limit through the `increased-memory-limit` entitlement ("on supported devices") and should check `os_proc_available_memory` at runtime ([21]).
- **[unverified]** Whether a ~7–8 GB 12B model would stay under the iPhone's per-app limit is unknown. No source has tested it.

### 5. Speed on iPhone 17 Pro

**Google's numbers (LiteRT-LM; 1,024 tokens in, 256 out, 2K context, warm cache, load time excluded)** ([10], [11], [12]):

| Model | Backend | Prefill tok/s | Decode tok/s | Time to first token |
|---|---|---|---|---|
| E2B | GPU | 2,878 | 56.5 | 0.3 s |
| E2B | CPU | 532 | 25.0 | 1.9 s |
| E4B | GPU | 1,189 | 25.1 | 0.9 s |
| E4B | CPU | 159 | 9.7 | 6.5 s |

- Prefill = reading the input (prompt, audio and image tokens). Decode = writing the answer.
- **[confirmed] The owner's notes are correct:** E2B ≈ 56 tok/s and E4B ≈ 25 tok/s on GPU ([10], [11], [12]). The figures are single-run snapshots with no thermal (heat) conditions stated ([10]).
- **[reported] Sustained run, E2B, iPhone 17 Pro, 600 s, unplugged** ([16], independent benchmark, iOS 27.0, July 2026):

  | Runtime | Start tok/s | After 10 min | Kept |
  |---|---|---|---|
  | LiteRT-LM / GPU | 56 | **27** | 48% |
  | MLX / GPU | 48 | 18 | 38% |
  | Core ML / Neural Engine | 33 | 22 | 67% |

  This confirms the owner's "≈27 tok/s after 10 minutes". The same repo's warm, best-build table gives LiteRT-LM 61.1 tok/s, 497 MB memory and 3,513 tok/s prefill. It ranks LiteRT-LM fastest and most energy-efficient (0.147 J/token) of the runtimes tested ([16]).
- **[reported] Other E2B runtimes on iPhone 17 Pro:** MLX about 40 tok/s (developer post) ([28]). Core AI GPU 30.3 tok/s, and a hand-written Metal build about 55 tok/s, all measured on iOS 27 betas ([17]).
- **[reported] E4B, other runtimes on iPhone 17 Pro:** Core AI GPU 15.1 tok/s ([17]). **No sustained or thermal E4B result exists.**
- **[confirmed] Speculative decoding (MTP):** Google reports up to 2.2× faster decoding on mobile GPUs ([10]). Measured gains are for an Android phone only, for example E4B GPU going from 21.9 to 36.7–49.4 tok/s by task ([12]). **No iPhone MTP numbers are published.**
- **12B:** **No iPhone measurement found.** Google's 12B LiteRT-LM build lists only desktop and web platforms, and Google's launch post for it talks only about laptops ([14]). On a 16 GB MacBook Air M4 it ran at 15 tok/s decode with a 9.1 s time to first token ([13]). The Core AI model zoo marks 12B "Mac-only" ([17]).
- **[unverified, my arithmetic from [11]/[12]]** A full 30 s voice clip (750 tokens) plus one 280-token photo is about 1,030 input tokens. At Google's GPU prefill rates that is about 0.4 s of reading for E2B and about 0.9 s for E4B, before any answer text appears.
- Nearby iPhones: none of the primary sources publish Gemma 4 numbers for iPhone 16 Pro or older.
- For the later small board ([11], [12], Google): on a Raspberry Pi 5 (CPU), E2B decodes at 7.6 tok/s and E4B at 3.2 tok/s. On a Jetson Orin Nano GPU, E2B decodes at 24.2 tok/s.

## Where sources disagree / unverified

1. **Which small model is better at Arabic speech?** Google's FLEURS table puts E2B ahead: 14.3% vs 16.2% WER ([6]). The Arabic ASR leaderboard puts E4B ahead on all six sets, including Saudi SADA: 43.4 vs 46.2 ([22]). FLEURS is read, mostly Modern Standard Arabic speech, while SADA is real Saudi TV speech, so for this project the SADA result is the more relevant. Our own Saudi test is still needed.
2. **CoVoST translation scores differ between Google sources.** The model card gives E2B 33.47 and E4B 35.54 ([3]). The technical report's average gives 35.4 and 38.2 ([6]). This is probably a different language set or setup. The source does not explain it.
3. **FLEURS average for E4B** is 0.08 on the model card ([3]) but 0.075 in the technical report ([6]). This is likely rounding.
4. **12B LiteRT-LM image support.** A search snippet (secondary) said the 12B file supports text and audio only, with images "in a future update". The live model card (read 2026-10-13) says the file supports "text, vision and audio" plus MTP ([13]). The card was probably updated. Rely on the live card.
5. **12B Mac memory.** LiteRT-LM reports about 7.3–7.9 GB GPU memory ([13]). An MLX 4-bit run reports 13.8 GB peak Metal and 9.1 GB process memory ([18]). They use different runtimes and measurements.
6. **iPhone 17 Pro RAM (12 GB)** is reported, not Apple-published ([19], [20]).
7. **Sustained throttling (56 → 27 tok/s)** comes from one independent repo, measured on iOS 27.0 ([16]). It is not from Google.
8. **E2B decode on iPhone 17 Pro varies by source:** 56.5 (Google, [11]), 61.1 (independent warm protocol, [16]), and about 40 with MLX (social post, [28]). The runtime and measurement method differ in each case.

## Recommendation and what would change it

**Start with Gemma 4 E4B on LiteRT-LM (GPU backend) for Steps 1–3, and keep E2B wired in as a one-line swap.** Reasons:
- It has the best published **Saudi-dialect speech** result of the models that can run on an iPhone today ([22]).
- It has a clearly higher multilingual knowledge score than E2B: 76.6 vs 67.4 MMMLU ([3]).
- Google has measured it on the exact target phone: 25 tok/s decode, 0.9 s time to first token, 3.4 GB peak ([12]). That fits well within the reported 12 GB of RAM ([20]).
- It uses the same file format, runtime and audio/image inputs as E2B, so switching later is cheap ([11], [12]).
- 12B is the strongest on paper (FLEURS Arabic 7.0%, MMMLU 83.4%), but it has **no iOS build and no iPhone measurement**, and it needs about 7–8 GB ([13]).

**What would change it:**
- **Switch to E2B** if:
  - our own Saudi test (see Open questions) shows E2B is about as good as E4B;
  - E4B's sustained speed on the phone becomes too slow to feel like a conversation (no sustained E4B data exists yet; E2B kept 48% of its speed after 10 min [16]);
  - E4B's 3.4 GB footprint triggers memory kills alongside the camera and audio pipeline;
  - the later small board is CPU-only, like a Raspberry Pi 5, where E4B decodes at 3.2 tok/s vs 7.6 for E2B ([12], [11]).
- **Consider 12B Unified** if Google ships an iOS/Android LiteRT-LM build of 12B, or another runtime publishes an iPhone 17 Pro measurement, and it stays under the per-app memory limit ([21]). Its Arabic speech score is about half the error of E2B/E4B on FLEURS ([6]).
- **Add a separate speech recogniser** if both small models stay above about 40% WER on our Saudi recordings. The leaderboard shows a dedicated Arabic recogniser at 28.9% on SADA ([22]). That would be a design change, not a model swap.
- **Watch Gemma 3n E4B as a comparison point:** it has a better FLEURS Arabic WER than Gemma 4 E4B (10.1% vs 16.2%) ([6]), but it is the older generation and has no SADA score.

## Open questions

Each is written as a step with a "Done when".

1. **Build a small Saudi-dialect test set** of short voice clips (Najdi, Hijazi, Gulf; quiet and noisy) with reference transcripts, plus matching text prompts.
   *Done when:* the set exists with written references and a WER script, and E2B and E4B each have a WER and a short human rating of the Saudi-Arabic replies.
2. **Confirm audio and image input through the LiteRT-LM Swift API on iPhone 17 Pro**, not only in Google's Gallery app.
   *Done when:* a minimal iOS build sends one 30 s, 16 kHz clip and one photo to E4B and gets a correct answer, or the blocking issue is identified in the LiteRT-LM repo.
3. **Measure E4B sustained speed and heat** on iPhone 17 Pro over 10 minutes with the GPU backend, logging decode tok/s and `ProcessInfo.thermalState`.
   *Done when:* there is a start/after-10-minutes table for E4B comparable to the E2B one in [16].
4. **Measure whether MTP speculative decoding works and helps on iOS.**
   *Done when:* tok/s with and without MTP are recorded on iPhone 17 Pro for E2B and E4B.
5. **Check whether 12B Unified can load on iPhone at all** (memory available to the app, any iOS build).
   *Done when:* there is either a published iPhone 17 Pro 12B measurement, or `os_proc_available_memory` with the increased-memory entitlement is recorded and compared with 12B's ~7–8 GB need.
6. **Check plant, food and wood photo quality** at budgets 280 and 560 for E2B vs E4B.
   *Done when:* 20–30 labelled photos have been run and scored for each model and budget.

## Sources

1. Google blog, "Gemma 4" announcement: sizes, 140+ languages, Apache 2.0. 2026-04-02. https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
2. Google, Gemma releases log: E2B/E4B/26B/31B on 2026-03-31, MTP on 2026-04-16, 12B Unified on 2026-06-03. https://ai.google.dev/gemma/docs/releases
3. Google, Gemma 4 model card: sizes, parameters, audio/image specs, benchmark table. Updated 2026-07-30. https://ai.google.dev/gemma/docs/core/model_card_4
4. Hugging Face, google/gemma-4-E2B-it model card. https://huggingface.co/google/gemma-4-E2B-it
5. Hugging Face, google/gemma-4-12B-it model card ("Gemma 4 12B Unified", five sizes). https://huggingface.co/google/gemma-4-12B-it
6. Gemma Team, "Gemma 4 Technical Report", arXiv:2607.02770 v2 (2026-07-24): parameter table, memory table, FLEURS/CoVoST per-language tables. https://arxiv.org/html/2607.02770v2
7. Google, Gemma audio understanding docs: 30 s, 16 kHz, 25 tokens/s. Updated 2026-10-10. https://ai.google.dev/gemma/docs/capabilities/audio
8. Google, Gemma vision understanding docs: token budgets, 9 patches per token. Updated 2026-04-02. https://ai.google.dev/gemma/docs/capabilities/vision
9. Hugging Face, gemma-4-E2B-it `processor_config.json`: default 280 image tokens, patch 16, 16 kHz, 750 audio tokens. https://huggingface.co/google/gemma-4-E2B-it/raw/main/processor_config.json
10. Google AI Edge, LiteRT-LM Gemma 4 page: per-device benchmark tables, MTP claims. https://developers.google.com/edge/litert-lm/models/gemma-4 (redirected from ai.google.dev)
11. Hugging Face, litert-community/gemma-4-E2B-it-litert-lm: file size, quantization, method, iPhone 17 Pro table. https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
12. Hugging Face, litert-community/gemma-4-E4B-it-litert-lm: same, for E4B, plus Android MTP table. https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm
13. Hugging Face, litert-community/gemma-4-12B-it-litert-lm: desktop/web only, 6,883 MB, Mac/PC benchmarks. https://huggingface.co/litert-community/gemma-4-12B-it-litert-lm
14. Google Developers Blog, "Bringing Gemma 4 12B to your laptop": no phone mention. 2026-06-03. https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/
15. GitHub, google-ai-edge/LiteRT-LM README: Swift API "Early Preview", vision and audio support, v0.18.0. https://github.com/google-ai-edge/LiteRT-LM
16. GitHub, john-rocky/apple-silicon-llm-bench: iPhone 17 Pro cross-runtime and 600 s sustained tests. Captures 2026-07-18 to 07-30. https://github.com/john-rocky/apple-silicon-llm-bench
17. GitHub, john-rocky/coreai-model-zoo: Core AI tok/s on iPhone 17 Pro (iOS 27 betas); 12B "Mac-only". https://github.com/john-rocky/coreai-model-zoo
18. Rapid-MLX, Gemma 4 12B 4-bit on Mac mini M4 Pro: speed and memory. 2026-10-03. https://rapidmlx.com/models/gemma-4-12b-4bit
19. Apple Support, iPhone 17 Pro tech specs: A19 Pro, storage only, no RAM figure. https://support.apple.com/en-us/125090
20. MacRumors, "iPhone 17, Air, and iPhone 17 Pro: Here's How Much RAM": 12 GB via Xcode 26. 2025-09-09. https://www.macrumors.com/2025/09/09/iphone-17-pro-iphone-air-ram-amounts/
21. Apple Developer, `com.apple.developer.kernel.increased-memory-limit` entitlement. https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.kernel.increased-memory-limit
22. Hugging Face Space, Open Universal Arabic ASR Leaderboard (elmresearchcenter): results hard-coded in `app.py`. Read 2026-10-13. https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard/raw/main/app.py
23. Hugging Face Space, inceptionai/Leaderboards, `aragen_v3_results.json` (AraGen v3, 69 models; last sync 2026-04-06). https://huggingface.co/spaces/inceptionai/Leaderboards/tree/main/assets/results
24. Hugging Face dataset, OALL/results, `google/` folder: no Gemma 4 entries. Read 2026-10-13. https://huggingface.co/datasets/OALL/results/tree/main/google
25. BALSAM paper (Arabic benchmark platform), arXiv:2507.22603, ArabicNLP 2025. https://arxiv.org/abs/2507.22603
26. BenchmarkList, Gemma 4 E2B page: ASR leaderboard rows dated 2026-05-06 (secondary). https://benchmarklist.com/models/google-gemma-4-e2b-it/
27. Arab News, on SADA, the Saudi dialect speech dataset (secondary). https://www.arabnews.pk/saudi-arabia/saudi-dataset-cuts-ai-errors-in-arabic-dialects-3003083
28. Adrien Grondin (Locally AI) on X: E2B ~40 tok/s with MLX on iPhone 17 Pro (secondary, April 2026). https://x.com/adrgrondin/status/2040512861953270226
29. Apple App Store, Google AI Edge Gallery: Ask Image, Audio Scribe, iOS 17+. https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337
30. "Evaluation of Small Language Models for Arabic Language Processing", arXiv:2606.21460 (2026-06-19): Gemma 3 12B, not Gemma 4. https://arxiv.org/abs/2606.21460
