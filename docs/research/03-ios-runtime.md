# Q3. iOS runtime

Research date: 2026-10-13. This area changes weekly, so every claim carries the date of its source. Labels: **confirmed** means a primary source (official docs, release notes, the PR or issue itself). **Reported** means a secondary source only. **Unverified** means there is a claim but no source that checks it.

## Question

Which runtimes can run Gemma 4 E2B or E4B inside an iOS app (Swift, iPhone 17 Pro first) with **both** audio input (speech) and image input (camera) working? For each runtime: does it load the model, does image work, does audio work, is that official or a community fork, what speeds are published on iPhone, what licence applies, and how hard is the Swift integration?

## Short answer

- **No runtime has image and audio for Gemma 4 that is both official and proven bug-free on iPhone today.** LiteRT-LM (Google) comes closest. Its Swift API officially documents `Content.imageFile` and `Content.audioFile` ([Swift docs, updated 2026-09-04][s5]). Google's own iPhone app added image and audio chat on 2026-09-04 ([App Store][s9]). However, the Swift API is still "Early Preview" ([repo][s3]), and open GitHub issues report iPhone vision failures ([#2979][s7]) and audio returning null ([#3850][s6]).
- **llama.cpp** officially lists Gemma 4 E2B and E4B with audio and vision ([multimodal.md][s14]). Its iOS XCFramework has included the multimodal library since 2026-06-25 ([PR #21935][s16]). I found no public report of Gemma 4 audio running on an iPhone through it.
- **MLX Swift** has Gemma 4 text and vision. Audio is still an unmerged PR ([#392][s12]).
- **CoreML-LLM** (one community developer) claims all four modalities on iPhone 17 Pro.
- **Cactus** documents image and audio for Gemma 4, but its licence charges larger companies.

## Runtime table

| Runtime | (a) Loads E2B/E4B on iOS | (b) Image on iOS | (c) Audio on iOS | (d) Official or community | (f) Licence (runtime) | (g) Swift integration |
|---|---|---|---|---|---|---|
| **LiteRT-LM** (Google AI Edge) | Yes, both. Google benchmarks both on iPhone 17 Pro ([model page][s1]). Confirmed. | **Partial.** The API exists ([Swift docs][s5]). Open bug: the E2B vision encoder fails on a physical iPhone ([#2979][s7], opened 2026-07-24, still open). It works in Google's Gallery app ([App Store][s9]). | **Partial.** The API exists ([Swift docs][s5]). Open report of null output ([#3850][s6]); the maintainer suggests a missing `audioBackend: .cpu()` setting. A user report says audio needs the CPU backend ([#1959][s8]). Gallery has audio since v1.0.10 ([App Store][s9]). | Official, Google. The Swift API is labelled "Early Preview" ([repo][s3]). | Apache-2.0 ([repo][s3]) | Medium. SPM package from the repo root, merged about 2026-10-09 ([#1959][s8]). One `Engine`/`Conversation` API with a vision backend and an audio backend ([s5]). |
| **MediaPipe LLM Inference API** | Not found for Gemma 4 | Not found for iOS | Not found for iOS | Official, but "maintenance-only mode"; Google says to migrate to LiteRT-LM ([guide, 2026-10-01][s10]) | Apache-2.0 | Don't start here |
| **MLX Swift** (`mlx-swift-lm`) | Yes. Gemma 4 E2B/E4B text and vision added in 3.31.3 ([releases][s11]). Confirmed. iPhone numbers come from a third-party bench ([s4]). | **Yes (official).** Gemma 4 VLM is in the library ([releases][s11]). I found no iPhone-specific image test. | **No.** Gemma 4 audio encoder PR [#392][s12] is open and unmerged (last activity 2026-09-14). Two earlier PRs were closed without merging ([issue #207][s13]). | Official Apple ml-explore project for text and vision; audio only in a community PR | MIT ([repo][s11b]) | Easy for text and vision: SPM plus Hugging Face downloads. Audio would mean merging an unreviewed PR. |
| **mlx-vlm** (Python) | Mac only, not iOS | n/a on iOS | Gemma 4 audio works on a Mac ([Willison][s27], reported) | Official ml-explore project, Python | MIT | Not usable in an iOS app |
| **llama.cpp** + libmtmd | Yes. GGUF of E2B loads on iPhone ([bench][s4], reported). The official QAT q4_0 GGUF "did not load" in that bench. | **Yes in the library** ([multimodal.md][s14]). No iPhone image test of Gemma 4 found. | **Yes in the library.** Gemma 4 audio was merged 2026-04-12 ([PR #21421][s15]). Not tested on iPhone (not found). | Official, ggml-org. Multimodal entered the iOS XCFramework 2026-06-25 ([PR #21935][s16]); typechecked for iOS, but no device test was posted. | MIT ([README][s17]) | Hard-ish. C API through `import llama`; you write the Swift wrapper for mtmd yourself. No official Swift sample for mtmd (not found). |
| **Core ML: CoreML-LLM** (community, john-rocky) | Yes, E2B and E4B on iPhone 17 Pro ([README][s18]). Reported (single developer). | Yes, claimed ([releases v1.7.0/v1.9.0][s19]) | Yes, claimed. A Conformer audio encoder was added in v1.9.0 ([releases][s19]) | Community, one maintainer | Code MIT; weights keep their own licence ([README][s18]) | Easy: SPM, `CoreMLLLM.load(model: .gemma4e2b)`, `image:`/`audio:` parameters ([README][s18]). Needs iOS 18+. Very large bundle (5.4 GB E2B multimodal). |
| **Apple Core AI** (WWDC26) | Not found for Gemma 4 | Not found | Not found | Official Apple, but no Gemma 4 path documented. A third-party bench used a "patched engine" ([s4]). | Apple SDK | Unknown |
| **ExecuTorch** (Meta/PyTorch) | Gemma 4 E2B/E4B example exists ([examples/models/gemma4][s20]), but it covers a host/C++ build and has **no iOS instructions** | Yes in the export (not on iOS) | Yes in the export (16 kHz WAV, ≤30 s); not on iOS | Official example; iOS path not documented. The MLX delegate is "experimental" and Mac-focused ([PyTorch blog, 2026-05-15][s21]). | BSD-3 (ExecuTorch); not checked this session | Hard. Export yourself, then use the C++ runtime from Swift. |
| **React Native ExecuTorch** (Software Mansion) | A Gemma 4 E2B multimodal `.pte` constant appears in the "next" (unreleased) docs ([search result][s22], page now 404) | Unverified | Unverified | Community/company, unreleased | MIT (reported) | Not Swift (React Native) |
| **MLC LLM** | E2B text and audio merged 2026-09-29 ([PR #3559][s23]) | **No.** Vision is "out of scope" ([s23]) | Web/WebGPU path only; "the native engine cannot serve it yet" ([s23]) | Official, but not usable natively | Apache-2.0 | Not viable now |
| **Cactus** | Yes, E2B is its main reference model on iPhone ([README][s24]) | Yes, documented ([Apple docs v1.14][s25]) plus an iPhone VLM benchmark ([s24]) | Yes, documented: `"audio": [...]` for Gemma 4 ([s25]). No iPhone audio number for Gemma 4 (the transcription benchmark uses Parakeet). | Company SDK. One bench reports its shipped default quant scored 3% on GSM8K ([s4]). | **Source-available, not open source.** Free only for individuals, education, non-profits and small orgs (<$2M funding and revenue) ([LICENSE][s26]) | Easy: XCFramework plus `Cactus.swift`; iOS 13+ ([s25]) |
| **Nexa SDK (iOS)** | Not found for Gemma 4 | VLM class exists; Gemma 4 not found ([docs][s28]) | ASR only (e.g. Parakeet); no audio-language model on iOS found ([s28]) | Company | Not checked | Unknown for Gemma 4 |
| **PocketPal AI** (app, llama.rn) | Gemma 4 not in release notes ([releases][s29]) | Not found | Not found | Community app, not a library | MIT | Not a Swift library |
| **Enclave AI, Ollama on iOS, Locally AI** | Enclave: not found. Ollama: no official iOS app found. Locally AI runs Gemma 4 through MLX ([talk][s30], reported). | Not found | Not found | Closed apps | n/a | Not libraries |
| **Google AI Edge Gallery** (app, reference only) | Yes, E2B/E4B ([App Store][s9]) | Yes, "Ask Image" ([s9]) | Yes, "Audio Scribe"; AI Chat gained images and audio in v1.0.10 (2026-09-04) ([s9]) | Official Google app; Google's blog says it shows LiteRT-LM multimodal ([blog][s2]) | Apache-2.0 ([gallery repo][s31]) | It is an app. iOS source not found in the public repo. |

(e) Speeds are in the next section.

## Findings per runtime

### LiteRT-LM (Google AI Edge)

- **Models:** It supports E2B and E4B today ([Gemma 4 page, updated 2026-09-04][s1]). Confirmed.
- **Swift API:** Google's May 2026 blog announces "a fully open-source iOS Swift API" ([blog, 2026-05-19][s2]). The repo still marks Swift as "Early Preview", while Kotlin, Python and C++ are "Stable" ([repo README][s3]). Confirmed. Official SPM support in the root `Package.swift` was merged about 2026-10-09, according to a maintainer comment ([#1959][s8]).
- **Image and audio API:** The Swift docs show `Content.imageFile(path)` and `Content.audioFile(path)`. Both need `visionBackend` and/or `audioBackend` set in `EngineConfig`, and the docs' example sets them to `.cpu()` ([Swift docs][s5]). Confirmed (documentation).
- **iOS GPU:** The docs say the GPU path uses Metal ([s5]). An older feature request says no iOS Metal accelerator was shipped and the source is closed ([#1050][s32], opened 2025-12-03, still open). A newer issue lists `prebuilt/ios_arm64/libLiteRtMetalAccelerator.dylib` as shipping in v0.17.x ([#3863][s33], 2026-10-06). The two disagree on timing; the newer one suggests GPU prebuilts now ship. The GPU accelerator itself is still closed source ([#1050][s32]).
- **Known iOS problems (all open on 2026-10-13):**
  - Vision: on a physical iPhone (iPhone17,2, iOS 26.5), E2B's first image message fails inside the CPU vision executor, and `sendMessage` returns nil ([#2979][s7]). The reporter says Google's Gallery app handles the same image on the same phone. #2979 cites a related E4B report, #2370, with the same error. A community workaround replaces Gemma vision with Apple Vision OCR plus text input.
  - Audio: `Content.audioFile` makes `sendMessage` return null, on the simulator, v0.17.1 ([#3850][s6], opened 2026-10-04). On 2026-10-07 the maintainer said `audioBackend` was not set and asked the reporter to retry. Not yet confirmed fixed.
  - Audio backend: a user on iPhone 17 reported "Audio backend constraint mismatch" on GPU; the model requires the CPU backend for audio ([#1959][s8], 2026-04-17). Reported.
  - E4B on GPU can hang permanently mid-prefill on iOS ([#3087][s34], opened 2026-08-03, open). Title only seen.
  - App Store hygiene: the iOS binaries ship no `PrivacyInfo.xcprivacy`; the maintainer has reproduced this ([#3863][s33]).
- **Proof that the full stack can work:** Google's Gallery iOS app added "images and audio" to AI Chat in v1.0.10 (Sep 4), and has Ask Image and Audio Scribe ([App Store][s9]). Google's blog says the Gallery app shows LiteRT-LM multimodal on Android and iOS ([s2]). That the iOS Gallery is built on the public Swift API is **unverified**: its iOS source was not found in the public repo ([s31]).
- **Memory design:** vision and audio encoders load on demand, and the text-only footprint can be as low as 0.8 GB ([HF model card][s35]). Confirmed (vendor claim).
- **Apple adapter:** v0.15.0 added an "Apple FM adapter" for text and multimodal execution of Gemma 4 through Apple's Foundation framework, credited to john-rocky ([release v0.15.0][s36]). How this relates to the Swift API is not documented (not found).

### MediaPipe LLM Inference API

The API is in "maintenance-only mode" for Android, iOS and Web, and Google recommends LiteRT-LM ([guide, updated 2026-10-01][s10]). The page lists no Gemma 4 model and no iOS multimodal files. Confirmed. Not a candidate.

### MLX Swift (mlx-swift-lm, mlx-swift-examples) and mlx-vlm

- Gemma 4 text (E2B, E4B), vision and MoE were added in 3.31.3 (15 Apr). 3.31.4 (30 Jun) added Gemma 4 MTP speculative decoding and an iOS build fix. 3.32.3 (30 Sep) added video input to the Gemma 4 VLM ([releases][s11]). Confirmed.
- **Audio is not merged.** PR [#392][s12] ports the Gemma 4 USM-Conformer audio encoder. It is open with no formal review. It was tested only on macOS, and long-audio chunking is not implemented. Earlier PRs #192 and #343 were closed unmerged. The maintainer agreed audio "belongs in mlx-swift-lm" ([issue #207][s13]). The 3.31.4 item "support for audio resources" (#298) is not explained in the notes ([s11c]).
- mlx-vlm (Python) runs Gemma 4 audio on a Mac ([Willison][s27]). Reported. It is not an iOS runtime.
- Memory on iPhone is high in one bench: 3,010 MB (4-bit PTQ) and 4,592 MB (OptiQ int4) ([s4]). Reported.

### llama.cpp (libmtmd)

- PR #21309 added Gemma 4 vision and MoE "no audio", merged 2026-04-02 ([search summary][s37], reported). PR [#21421][s15] added the Gemma 4 E2B/E4B Conformer audio encoder, merged 2026-04-12. Confirmed. Its notes: use a BF16 mmproj (the multimodal projector file), because F16/Q8_0 caused repetitions. Clips are handled in 30 s chunks. Some quants failed on long audio. Input that is not 16 kHz is resampled linearly.
- The official multimodal doc lists gemma-4-E2B-it and E4B-it under mixed modalities, audio and vision ([multimodal.md][s14]). Confirmed.
- iOS: PR [#21935][s16] put `libmtmd` and `mtmd.h` into the Apple XCFramework, merged 2026-06-25. It was typechecked for iphoneos; an iPhone device test was offered but not posted. Confirmed.
- No public report found of Gemma 4 **audio** or **image** through llama.cpp on an iPhone. A bench loaded E2B Q4_K_M text on iPhone 17 Pro, but the official QAT q4_0 "did not load" ([s4]).

### Core ML / Apple

- **CoreML-LLM** ([README][s18], [releases][s19]) is one developer's Swift package, the same author as the bench repo. It is aimed at the Apple Neural Engine (ANE, Apple's low-power AI chip). It claims Gemma 4 E2B (5.4 GB multimodal bundle) and E4B (8.16 GB) with text, image, video and audio on iPhone 17 Pro. v1.9.0 (3 May) added the E4B audio encoder and fixed garbled E4B audio. Known issues: one prefill path gives degenerate output on iPhone, and a stateful multimodal engine crashes on the iPhone ANE. Reported (single source, not independently tested).
- **Apple Core AI** (WWDC26) is reported as Core ML's successor for running third-party models ([Callstack][s38], reported). Apple's documentation page returned no readable content to my fetch. No Gemma 4 support found. The bench repo's "Core AI (patched engine)" arm jetsammed (was killed by iOS for memory) under its standard protocol ([s4]).

### ExecuTorch

- The official folder `examples/models/gemma4` covers E2B and E4B with text, vision and audio (16 kHz mono WAV, up to 30 s). It has no iOS instructions and only Samsung S25 performance numbers ([README][s20]). Confirmed.
- The MLX delegate (Apple GPU) is "experimental", is framed around Macs, and does not list Gemma 4 ([PyTorch blog, 2026-05-15][s21]). Confirmed.
- React Native ExecuTorch "next" docs listed a `GEMMA4_E2B_MLX_MM` multimodal `.pte` ([search result][s22]). The page returned 404 when fetched, and no release mentions Gemma 4 ([releases][s39]). Unverified.

### MLC LLM

E2B text and audio support was merged 2026-09-29. Vision is out of scope, and "the native engine cannot serve it yet", so it is tested only on WebGPU ([PR #3559][s23]). Confirmed. Not usable for an iOS app now.

### Commercial SDKs and apps

- **Cactus:** documents Gemma 4 image and audio in messages for Swift ([v1.14 Apple docs][s25]). It publishes iPhone 17 Pro numbers for Gemma-4-E2B-CQ4 ([README][s24]). The licence is source-available: companies over $2M funding or revenue need a paid licence ([LICENSE][s26]). A third-party bench found its shipped default CQ4 scored 3.0% on GSM8K, versus 87% for an uncalibrated build ([s4]). This is a quality red flag. Reported.
- **Nexa SDK iOS:** has LLM/VLM/ASR classes; no Gemma 4 found ([docs][s28]).
- **PocketPal:** a llama.cpp app (llama.rn). No Gemma 4, image or audio input in its release notes ([releases][s29]).
- **Enclave, Ollama:** no Gemma 4 multimodal iOS evidence found. No official Ollama iOS app found.
- **Locally AI:** runs Gemma 4 on iPhone through MLX, demoed at about 40 tok/s ([AI Engineer talk][s30]). Reported. Image and audio not confirmed.

## Published speed numbers

All numbers are iPhone 17 Pro unless stated. "Decode" means tokens generated per second after the first. "Prefill" means prompt tokens read per second. TTFT means time to first token.

| Runtime | Model / quant | Device | Prefill tok/s | Decode tok/s | TTFT | Memory | Source (date) | Label |
|---|---|---|---|---|---|---|---|---|
| LiteRT-LM GPU | E2B (official .litertlm) | iPhone 17 Pro | 2,878 | 56 | 0.3 s | 1,450 MB peak CPU | [Gemma 4 page][s1] (upd. 2026-09-04) | Confirmed |
| LiteRT-LM CPU | E2B | iPhone 17 Pro | 532 | 25 | 1.9 s | 607 MB | [s1] | Confirmed |
| LiteRT-LM GPU | E4B | iPhone 17 Pro | 1,189 | 25 | 0.9 s | 3,380 MB | [s1] | Confirmed |
| LiteRT-LM CPU | E4B | iPhone 17 Pro | 159 | 10 | 6.5 s | 961 MB | [s1] | Confirmed |
| LiteRT-LM GPU | E2B wNa8o8 QAT | iPhone 17 Pro, iOS 27.0 | 3,513 (p=1024) | 61.1 | not given | 497 MB | [bench][s4] (2026-07-28) | Reported |
| MLX Swift | E2B 4-bit PTQ | iPhone 17 Pro | 3,274 (quant not stated) | 49.1 | not given | 3,010 MB | [s4] (2026-07-28) | Reported |
| MLX Swift | E2B OptiQ int4 | iPhone 17 Pro | not given | 36.0 | not given | 4,592 MB | [s4] | Reported |
| llama.cpp | E2B Q4_K_M | iPhone 17 Pro | not given | 38.8 | not given | 191 MB (mmap, not comparable) | [s4] (2026-07-27) | Reported |
| Cactus | E2B CQ4 (shipped default) | iPhone 17 Pro | not given | 50.0 | not given | 632 MB | [s4] (2026-07-29) | Reported |
| Cactus (vendor) | Gemma-4-E2B-CQ4 | iPhone 17 Pro | 729 | 37 | not given | 644 MB; VLM 256 px encode 0.5 s, then 39 tok/s | [Cactus README][s24] (undated) | Confirmed (vendor) |
| Cactus (vendor) | Gemma-4-E2B-CQ4 | iPhone 15 Pro | 517 | 26 | not given | 633 MB; VLM encode 1.15 s | [s24] | Confirmed (vendor) |
| CoreML-LLM (ANE) | E2B 4-bit (3-chunk) | iPhone 17 Pro | not given | 34.2 | not given | not given | [releases v1.7.0][s19] | Reported |
| CoreML-LLM (ANE) | E4B multimodal | iPhone 17 Pro | not given | 15.7 | not given | not given | [releases v1.9.0][s19] | Reported |
| Core AI (patched) | E2B own int4 | iPhone 17 Pro | not given | 47.1 | not given | 755 MB | [s4] | Reported |

**Sustained (10-minute) decode, E2B, iPhone 17 Pro** (owner's note to verify):

| Runtime | Burst → sustained tok/s | Retained | Source |
|---|---|---|---|
| LiteRT-LM GPU | 56 → 27 | 48% | [bench][s4] (run undated) and [CoreML-LLM README][s18]. Same author. |
| MLX GPU | 48 → 18 | 38% | same |
| CoreML ANE | 33 → 22 | 67% | same |
| Re-measured 600 s energy run (2026-07-30) | — | LiteRT 76%, MLX-PTQ 64%, Cactus 57%, llama.cpp 54% | [s4] |

**Verdict on the owner's note:** the "≈ 56 tok/s E2B, ≈ 25 tok/s E4B" figures are **confirmed** by Google ([s1]). The drop to ≈ 27 tok/s after 10 minutes is **reported**: it appears in one undated run by one author ([s4], [s18]). That author's later 600 s run shows LiteRT keeping 76%, which is about 43 tok/s if applied to 56. No independent second source found.

**Speed with image or audio input on iPhone:** not found for any runtime, except Cactus's vendor image-encode time above.

## Where sources disagree / unverified

1. **LiteRT-LM iOS GPU availability.** [#1050][s32] says there is no iOS Metal accelerator and that its source is closed (comments through 2026-09). [#3863][s33] (2026-10-06) lists an iOS arm64 Metal dylib in v0.17.x, and Google publishes iPhone GPU numbers ([s1]). Likely now shipped as a closed binary; confirm in the SPM package.
2. **LiteRT-LM iOS vision.** The docs say it is supported ([s5]) and Gallery does it ([s9]). Developers on the public build report failure ([#2979][s7]). Unresolved.
3. **LiteRT-LM iOS audio.** The docs say it is supported ([s5]). [#3850][s6] got null output, possibly from a configuration mistake. Unresolved.
4. **Sustained throttling.** 48% retained ([s4] undated) versus 76% retained ([s4], 2026-07-30, energy protocol). The same author used different protocols.
5. **Gemma 4 licence.** Google says Apache-2.0 ([s1], [s35]). The CoreML-LLM README says Gemma weights use the Gemma Terms of Use ([s18]). Google's statement is primary, so treat Apache-2.0 as correct for Gemma 4.
6. **MLX Swift on iPhone speed.** 49.1 tok/s ([s4]) versus 12–14 tok/s from an early sidecar port ([Apple forum][s40], reported, probably before official support).
7. **CoreML-LLM multimodal.** Claimed by its author only; no independent test found. Unverified.
8. **Whether Google's Gallery iOS uses the public LiteRT-LM Swift API.** Unverified.

## Recommendation

**Start with LiteRT-LM (Swift API, E2B, GPU for text, CPU for the vision and audio encoders).** Reasons:

- It is the only official runtime whose Swift API documents both image and audio for Gemma 4 ([s5]).
- Google publishes the best iPhone numbers: 56 tok/s, TTFT 0.3 s ([s1]).
- Google's own iPhone app does image and audio on it ([s9], [s2]).
- It is Apache-2.0.

Treat it as **preview software**. The first job is to prove image and audio on the physical iPhone 17 Pro, given open issues [#2979][s7] and [#3850][s6].

**Fallback: llama.cpp XCFramework with libmtmd.** It has official, merged Gemma 4 audio and vision ([s14], [s15]) and an MIT licence, and its iOS packaging includes mtmd ([s16]). The costs: you write the Swift wrapper yourself, decode is slower in the one published bench (38.8 tok/s, [s4]), and iPhone multimodal is untested in public.

Keep **CoreML-LLM** as a second fallback to test only if both fail. It claims all modalities on iPhone and has the best sustained speed, but it has one maintainer and very large bundles. Skip **Cactus** unless its licence fits the project's funding. Skip **MLX Swift** for now, because audio is unmerged.

### Next steps

1. Read the LiteRT-LM root `Package.swift` and the Swift sample (if any) on GitHub. Confirm the iOS GPU dylib and the minimum iOS version. **Done when:** the note records the SPM product names, the minimum iOS version, and whether `libLiteRtMetalAccelerator` ships for `ios_arm64`.
2. Build the smallest Swift test app with E2B: one text prompt, one camera photo, and one 5-second Arabic WAV at 16 kHz. Set `visionBackend: .cpu()` and `audioBackend: .cpu()`. **Done when:** all three return a sensible answer on the physical iPhone 17 Pro, or the exact failure is logged and matched to #2979/#3850.
3. Watch issues #2979, #3850 and #3087. **Done when:** each is closed with a fix version, or a workaround is confirmed in the test app.
4. Measure the 10-minute sustained decode yourself on the iPhone 17 Pro (E2B, GPU, MTP on and off). **Done when:** there is a burst and sustained tok/s pair with the phone's thermal state noted, replacing the unverified 27 tok/s figure.
5. If step 2 fails for image or audio, repeat step 2 with the llama.cpp XCFramework, E2B GGUF and a BF16 mmproj. **Done when:** the same three inputs work or fail on the device, with the result logged.

## Open questions

- Does Google's iPhone Gallery app use the public Swift API or a private build? (iOS source not found.)
- Image and audio latency on iPhone for Gemma 4 E2B: encoder time per photo and per 5–30 s clip. Not published for LiteRT-LM, llama.cpp or MLX.
- Is Saudi Arabic speech understood well by Gemma 4 E2B audio? Not covered by this question; see the speech research note.
- Is the iPhone 17 Pro GPU used for audio and vision, or only the CPU? The docs show `.cpu()` for both, and one report says audio requires CPU.
- Does MTP (multi-token prediction, a speed-up that drafts several tokens at once) work through the Swift API on iPhone? The Swift docs mark it experimental ([s5]). No iPhone MTP numbers found.
- Memory with all encoders loaded on iPhone, for both E2B and E4B. Not found.

## Sources

1. [s1] Google, LiteRT-LM Gemma 4 model page (iPhone 17 Pro E2B/E4B table, Apache-2.0), updated 2026-09-04. https://developers.google.com/edge/litert-lm/models/gemma-4
2. [s2] Google Developers Blog, "Blazing fast on-device GenAI with LiteRT-LM" (Swift API, Gallery multimodal), 2026-05-19. https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/
3. [s3] google-ai-edge/LiteRT-LM repo README (Swift "Early Preview", Apache-2.0, v0.18.0), read 2026-10-13. https://github.com/google-ai-edge/LiteRT-LM
4. [s4] john-rocky/apple-silicon-llm-bench (iPhone 17 Pro E2B runtime comparison and throttle test), sessions 2026-07-18 to 07-30. https://github.com/john-rocky/apple-silicon-llm-bench
5. [s5] Google, LiteRT-LM Swift API docs (`Content.imageFile`, `Content.audioFile`, backends), updated 2026-09-04. https://developers.google.com/edge/litert-lm/swift
6. [s6] LiteRT-LM issue #3850, iOS Swift `audioFile` returns null, opened 2026-10-04. https://github.com/google-ai-edge/LiteRT-LM/issues/3850
7. [s7] LiteRT-LM issue #2979, Gemma 4 E2B vision fails on iPhone (XNNPack), opened 2026-07-24 (refers to #2370 for E4B). https://github.com/google-ai-edge/LiteRT-LM/issues/2979
8. [s8] LiteRT-LM issue #1959, community Swift wrapper; official SPM merged about 2026-10-09; audio backend report, 2026-04-14 to 10-09. https://github.com/google-ai-edge/LiteRT-LM/issues/1959
9. [s9] App Store, Google AI Edge Gallery (v1.0.10 adds images and audio to AI Chat, Sep 4; iOS 17+), read 2026-10-13. https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337
10. [s10] Google, MediaPipe LLM Inference guide (maintenance-only mode), updated 2026-10-01. https://developers.google.com/edge/mediapipe/solutions/genai/llm_inference
11. [s11] ml-explore/mlx-swift-lm releases (Gemma 4 in 3.31.3; 3.31.4; 3.32.3), read 2026-10-13. https://github.com/ml-explore/mlx-swift-lm/releases
12. [s11b] ml-explore/mlx-swift-lm README (MIT, SPM 3.32.3). https://github.com/ml-explore/mlx-swift-lm
13. [s11c] mlx-swift-lm release 3.31.4 notes (#298 audio resources, iOS build fix). https://github.com/ml-explore/mlx-swift-lm/releases/tag/3.31.4
14. [s12] mlx-swift-lm PR #392, Gemma 4 native audio input, open, last activity 2026-09-14. https://github.com/ml-explore/mlx-swift-lm/pull/392
15. [s13] mlx-swift-lm issue #207, Gemma 4 audio encoder request, opened 2026-04-12. https://github.com/ml-explore/mlx-swift-lm/issues/207
16. [s14] llama.cpp docs/multimodal.md (Gemma 4 E2B/E4B audio and vision), read 2026-10-13. https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
17. [s15] llama.cpp PR #21421, Gemma 4 audio Conformer encoder, merged 2026-04-12. https://github.com/ggml-org/llama.cpp/pull/21421
18. [s16] llama.cpp PR #21935, libmtmd in Apple XCFramework, merged 2026-06-25. https://github.com/ggml-org/llama.cpp/pull/21935
19. [s17] llama.cpp README (MIT). https://github.com/ggml-org/llama.cpp
20. [s18] john-rocky/CoreML-LLM README (Gemma 4 multimodal on iPhone, sustained test, SPM), read 2026-10-13. https://github.com/john-rocky/CoreML-LLM
21. [s19] CoreML-LLM releases (v1.7.0 Apr 27, v1.9.0 May 3). https://github.com/john-rocky/CoreML-LLM/releases
22. [s20] pytorch/executorch examples/models/gemma4 README (text, vision, audio; no iOS), read 2026-10-13. https://github.com/pytorch/executorch/tree/main/examples/models/gemma4
23. [s21] PyTorch blog, ExecuTorch MLX delegate (experimental), 2026-05-15. https://pytorch.org/blog/running-pytorch-models-on-apple-silicon-gpus-with-the-executorch-mlx-delegate/
24. [s22] React Native ExecuTorch "next" docs, `GEMMA4_E2B_MLX_MM` (seen in search, page 404 on fetch), 2026-10-13. https://docs.swmansion.com/react-native-executorch/docs/next/api-reference/variables/GEMMA4_E2B_MLX_MM
25. [s23] mlc-ai/mlc-llm PR #3559, Gemma 4 E2B text and audio (no vision; native engine not yet), merged 2026-09-29. https://github.com/mlc-ai/mlc-llm/pull/3559
26. [s24] cactus-compute/cactus README (iPhone 17 Pro/15 Pro Gemma-4-E2B-CQ4 benchmarks), undated, read 2026-10-13. https://github.com/cactus-compute/cactus
27. [s25] Cactus docs v1.14, Apple/Swift (Gemma 4 images and audio in messages), undated. https://docs.cactuscompute.com/v1.14/apple/
28. [s26] Cactus LICENSE (source-available; commercial licence above $2M thresholds), © 2025. https://github.com/cactus-compute/cactus/blob/main/LICENSE
29. [s27] Simon Willison, Gemma 4 audio with mlx-vlm on macOS (tag feed), 2026. https://simonwillison.net/tags/gemma/
30. [s28] Nexa SDK iOS docs overview, read 2026-10-13. https://docs.nexa.ai/nexa-sdk-ios/overview
31. [s29] PocketPal AI releases (v1.19.0, Oct 4; no Gemma 4), read 2026-10-13. https://github.com/a-ghorbani/pocketpal-ai/releases
32. [s30] AI Engineer Europe 2026 talk, "Running Gemma 4 on-device, 40 tokens/s on iPhone with MLX" (Locally AI), 2026. https://ai.engineer/talks/running-gemma-4-on-device-40-tokens-s-on-iphone-with-mlx
33. [s31] google-ai-edge/gallery repo (Apache-2.0, iOS 17+), read 2026-10-13. https://github.com/google-ai-edge/gallery
34. [s32] LiteRT-LM issue #1050, GPU accelerator source / iOS prebuilt, opened 2025-12-03, activity to 2026-09-30. https://github.com/google-ai-edge/LiteRT-LM/issues/1050
35. [s33] LiteRT-LM issue #3863, iOS binaries lack PrivacyInfo.xcprivacy (lists iOS Metal dylibs), opened 2026-10-06. https://github.com/google-ai-edge/LiteRT-LM/issues/3863
36. [s34] LiteRT-LM issue #3087, E4B GPU prefill hang on iOS, opened 2026-08-03 (title seen in issue search only). https://github.com/google-ai-edge/LiteRT-LM/issues/3087
37. [s35] Hugging Face, litert-community/gemma-4-E2B-it-litert-lm model card (Apache-2.0, on-demand encoders, benchmarks), read 2026-10-13. https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
38. [s36] LiteRT-LM release v0.15.0 (Apple FM adapter, multimodal), 4 Aug (2026). https://github.com/google-ai-edge/LiteRT-LM/releases/tag/v0.15.0
39. [s37] llama.cpp PR #21309, Gemma 4 vision and MoE, no audio, merged 2026-04-02 (seen via search summary only). https://github.com/ggml-org/llama.cpp/pull/21309
40. [s38] Callstack, "On-device AI after WWDC 2026" (Core AI), 2026. https://callstack.com/blog/on-device-ai-after-wwdc-2026-whats-new
41. [s39] software-mansion/react-native-executorch releases (no Gemma 4 mention), read 2026-10-13. https://github.com/software-mansion/react-native-executorch/releases
42. [s40] Apple Developer Forums, "Sharing a Swift port of Gemma 4 for mlx-swift-lm" (12–14 tok/s claim), 2026. https://developer.apple.com/forums/thread/822084

[s1]: https://developers.google.com/edge/litert-lm/models/gemma-4
[s2]: https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/
[s3]: https://github.com/google-ai-edge/LiteRT-LM
[s4]: https://github.com/john-rocky/apple-silicon-llm-bench
[s5]: https://developers.google.com/edge/litert-lm/swift
[s6]: https://github.com/google-ai-edge/LiteRT-LM/issues/3850
[s7]: https://github.com/google-ai-edge/LiteRT-LM/issues/2979
[s8]: https://github.com/google-ai-edge/LiteRT-LM/issues/1959
[s9]: https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337
[s10]: https://developers.google.com/edge/mediapipe/solutions/genai/llm_inference
[s11]: https://github.com/ml-explore/mlx-swift-lm/releases
[s11b]: https://github.com/ml-explore/mlx-swift-lm
[s11c]: https://github.com/ml-explore/mlx-swift-lm/releases/tag/3.31.4
[s12]: https://github.com/ml-explore/mlx-swift-lm/pull/392
[s13]: https://github.com/ml-explore/mlx-swift-lm/issues/207
[s14]: https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
[s15]: https://github.com/ggml-org/llama.cpp/pull/21421
[s16]: https://github.com/ggml-org/llama.cpp/pull/21935
[s17]: https://github.com/ggml-org/llama.cpp
[s18]: https://github.com/john-rocky/CoreML-LLM
[s19]: https://github.com/john-rocky/CoreML-LLM/releases
[s20]: https://github.com/pytorch/executorch/tree/main/examples/models/gemma4
[s21]: https://pytorch.org/blog/running-pytorch-models-on-apple-silicon-gpus-with-the-executorch-mlx-delegate/
[s22]: https://docs.swmansion.com/react-native-executorch/docs/next/api-reference/variables/GEMMA4_E2B_MLX_MM
[s23]: https://github.com/mlc-ai/mlc-llm/pull/3559
[s24]: https://github.com/cactus-compute/cactus
[s25]: https://docs.cactuscompute.com/v1.14/apple/
[s26]: https://github.com/cactus-compute/cactus/blob/main/LICENSE
[s27]: https://simonwillison.net/tags/gemma/
[s28]: https://docs.nexa.ai/nexa-sdk-ios/overview
[s29]: https://github.com/a-ghorbani/pocketpal-ai/releases
[s30]: https://ai.engineer/talks/running-gemma-4-on-device-40-tokens-s-on-iphone-with-mlx
[s31]: https://github.com/google-ai-edge/gallery
[s32]: https://github.com/google-ai-edge/LiteRT-LM/issues/1050
[s33]: https://github.com/google-ai-edge/LiteRT-LM/issues/3863
[s34]: https://github.com/google-ai-edge/LiteRT-LM/issues/3087
[s35]: https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
[s36]: https://github.com/google-ai-edge/LiteRT-LM/releases/tag/v0.15.0
[s37]: https://github.com/ggml-org/llama.cpp/pull/21309
[s38]: https://callstack.com/blog/on-device-ai-after-wwdc-2026-whats-new
[s40]: https://developer.apple.com/forums/thread/822084
[s39]: https://github.com/software-mansion/react-native-executorch/releases
