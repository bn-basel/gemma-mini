# Q4. Fine-tune to phone

Research note, written 2026-10-13. Read-only desk research: no weights downloaded, nothing installed or run.
Labels: **[confirmed]** = primary source (official docs, source code, maintainer comment); **[reported]** = secondary source
or a user's report; **[unverified]** = could not check. Numbers in square brackets like [S12] point to the Sources list.

Jargon used below:
- **LoRA**: a small add-on set of weights trained on top of a frozen model. "Merging" folds it back into the full weights.
- **Audio tower / vision tower**: the encoders that turn sound or pictures into vectors the language model can read.
  The small **adapter** or **projector** (`embed_audio`, `embed_vision`) maps those vectors into the language model's space.
- **PLE (Per-Layer Embeddings)**: Gemma 4 E2B/E4B keep an extra, very large embedding table per layer. It is why "E2B" has far
  more stored parameters than 2B.
- **`.litertlm`**: Google's LiteRT-LM bundle. One file holding several sections (text decoder, embedder, per-layer embedder,
  audio encoder, vision encoder, tokenizer, metadata).
- **GGUF + mmproj**: llama.cpp's format. The language model is one `.gguf`; the audio/vision encoders go in a separate "mmproj" `.gguf`.
- **PTQ / QAT**: quantising after training (PTQ) vs. training with quantisation in the loop (QAT).

---

## Question

Can a LoRA fine-tune of Gemma 4 E2B/E4B (trained on an RTX 5080 Windows PC, with Saudi speech and text) be merged and converted
to a format that runs on an iPhone 17 Pro, with **audio and vision input still working**? Which tools support it, who has done
it, what breaks, and what is the smallest experiment that would settle it?

## Short answer

**Verdict: plausible with gaps. Not proven for our exact case.** Every piece exists on its own. Audio LoRA training works
(Unsloth, PEFT). llama.cpp converts a merged fine-tune with both audio and vision encoders. Google's converter gained Gemma 4 audio
export on 2026-09-24, in nightly builds only. One public fine-tune (Swahili/Amharic/Oromo ASR) ships a `.litertlm` that pairs a
fine-tuned text decoder with Google's original audio sections. **But I found no public report of a fine-tuned Gemma 4 running on an
iPhone with audio and vision both working.** Google's iOS runtime also has open bugs on vision. The safest plan is to fine-tune only
the language model, keep Google's audio/vision encoders unchanged, and test early on the phone.

## Official path

**Fine-tuning docs (Google)**
- Google's Gemma docs list text QLoRA, vision QLoRA and full fine-tune guides. **No audio fine-tuning guide** appears in the
  navigation, and the audio page links none [S7][S8]. [confirmed]
- The vision QLoRA guide uses `google/gemma-4-E2B`. It leaves `target_modules` unset because PEFT's Gemma 4 defaults cover
  only the language-model layers, so the vision tower stays frozen. It saves `lm_head` and `embed_tokens` in full, merges with
  `merge_and_unload()`, and warns the merge needs over 30 GB of CPU RAM (page updated 2026-06-19) [S7]. [confirmed]
- Audio input limits: 30 s maximum, 16 kHz mono, 25 tokens per second of audio for Gemma 4. The page names no ASR languages and
  does not mention Arabic (updated 2026-10-10) [S8]. [confirmed]

**Conversion to `.litertlm` (Google's `litert-torch`, formerly ai-edge-torch)**
- The official route for a custom checkpoint is `litert-torch export_hf --model=<local safetensors dir>`. It produces a
  `.litertlm`. Gemma 4 (`Gemma4ForConditionalGeneration`) is listed, but only **vision** is documented as an extra encoder
  (`--task=image_text_to_text --export_vision_encoder`). Audio is not mentioned (page updated 2026-09-02) [S2]. [confirmed]
- Google's Gemma 4 page says to use `litert-torch-nightly` with `--externalize_embedder` and
  `--jinja_chat_template_override` (updated 2026-09-04) [S1]. The only official "convert a fine-tuned model" tutorial uses a
  Gemma 3 270M **text** model, Android only, with no vision, audio or iOS steps (updated 2026-06-01) [S3]. [confirmed]
- **Audio export now exists in the code, but only in nightly builds.** A commit on 2026-09-24 added Gemma 4 audio-encoder
  export: a new `multimodal_lm` task with `export_audio_encoder` and `audio_encoder_quantization_recipe` options [S11][S12]. It
  came after the last stable release (v0.9.4, 2026-08-24). The nightly wheel `0.10.0.dev20261012` (2026-10-12) should contain
  it [S13]. [confirmed] I found **no report from anyone using it on a fine-tuned model**, and the docs do not mention it yet.
  [unverified]
- Before that commit, a maintainer said on 2026-06-15 that audio-encoder and MTP-drafter export were still being open-sourced,
  and that Google's pre-built Gemma 4 bundles come from QAT "mobile" checkpoints that `litert-torch` cannot convert [S16].
  [confirmed]
- **Linux only.** The `litert-torch` README lists Linux as its operating system [S14]. Its dependency `litert-converter` ships
  wheels only for macOS arm64 and Linux x86_64, with none for Windows [S15]. So on the RTX 5080 PC, conversion needs **WSL2**.
  [confirmed for the wheel list; WSL2 working is unverified]
- **Splicing is possible with official tools.** `litert-lm-builder unpack` extracts a bundle's sections and writes an editable
  `model.toml`, which can be repacked. `litert-lm-peek` lists the sections [S6]. [confirmed] The page gives no rules for mixing
  sections from different sources. [confirmed]

**Runtime LoRA instead of merging (LiteRT-LM)**
- The runtime code has LoRA hooks. Swift `EngineConfig` has `loraRank` and `audioLoraRank`, and `ConversationConfig` has
  `loraPath` and `audioLoraPath` [S25]. On 2026-10-06 a merged change taught the runtime to load **Gemma 4 audio-encoder LoRA**
  inputs under their own names [S26]. [confirmed] None of this is in the Swift guide [S4]. [confirmed]
- **But it does nothing with the public Gemma 4 bundle.** A user trained a rank-16 attention LoRA and converted it to a
  `.tflite` sidecar with `litert-torch`'s `LoRA.from_safetensors().to_tflite()`. Loaded into the official E2B bundle, it ran
  without error and gave **identical output** in 54 of 54 tests. A second user confirmed that the runtime silently accepts LoRA
  for bundles built without LoRA inputs (issue opened 2026-08-07, still open) [S23]. [reported] `export_hf` has no LoRA option;
  LoRA appears only in the older Generative API (attention-only) and on its roadmap [S23][S31]. [confirmed] Whether Google's
  audio-encoder section has LoRA inputs: not found. **For now, plan to merge.**

**iOS runtime facts relevant here**
- Swift API: audio goes in with `Content.audioFile(path)` and images with `Content.imageFile(path)`. The guide shows only the CPU
  backend for the vision and audio encoders (`visionBackend: .cpu()`, `audioBackend: .cpu()`) [S4]. [confirmed]
- Google's E2B bundle card says vision and audio models load on demand. It gives iPhone 17 Pro text speeds (GPU decode
  56.5 tok/s, CPU 25 tok/s) but no audio or vision timings [S9]. [confirmed]

## Third-party tools

| Tool | Gemma 4 support | Audio | Vision | Output format | Source |
|---|---|---|---|---|---|
| **Unsloth** (training) | E2B/E4B/26B/31B; E2B LoRA about 8–10 GB VRAM | Yes. Official E2B/E4B audio notebooks. The guide says audio can be fine-tuned, but there is no separate audio on/off flag yet. Data-collator bug that silently dropped audio was fixed 2026-06-10 | Yes, `finetune_vision_layers`. The guide advises keeping it off at first for E2B/E4B | merged 16-bit safetensors, GGUF (`q4_k_m`, `q8_0`, `f16`); no LiteRT/Core ML export | [S39][S40] confirmed |
| **HF PEFT + TRL** (training) | Yes. Gemma 4 support fixed 2026-04 | Can target the audio tower (`.linear` inside `Gemma4ClippableLinear`, by regex) | Same as audio | adapter or merged safetensors | [S42][S7] confirmed |
| **Axolotl** | not checked | not found | not found | — | not found |
| **mlx-lm / mlx-vlm** (Mac training) | mlx-vlm has a Gemma 4 model with `audio.py` and `vision.py` | LoRA docs say nothing on audio training | `--train-vision` option | MLX safetensors. MLX itself runs on macOS or Linux, not Windows | [S44][S46] confirmed |
| **MLX Swift** (`mlx-swift-lm`, iPhone runtime) | E2B/E4B `gemma4` model | **No.** Code comment says the port supports text and vision only, and drops the audio weights (main, 2026-10-12) | Yes | MLX safetensors | [S45] confirmed |
| **llama.cpp** (`convert_hf_to_gguf.py` + mtmd) | Yes | Yes. Gemma 4 audio encoder merged 2026-04-12. The converter has a `Gemma4VisionAudioModel` mmproj class. BF16 mmproj recommended | Yes | GGUF + mmproj. iOS XCFramework build includes mtmd | [S32][S35][S36][S37] confirmed |
| **litert-torch `export_hf`** | Yes (nightly needed) | Nightly only, since 2026-09-24; untested by the public | Yes (`--export_vision_encoder`), with bugs reported | `.litertlm` | [S2][S11] confirmed |
| **Core ML: CoreML-LLM** (one developer, MIT) | E2B/E4B; iPhone 17 Pro E2B 34.2 tok/s (claimed) | Claimed (Conformer audio encoder, from base weights) | Claimed | `.mlmodelc` bundles. Has a documented "local fine-tune to iPhone" workflow for merged text weights | [S47] reported |
| **coremltools** (needed for Core ML) | — | — | — | wheels for macOS and Linux only, no Windows | [S15b] confirmed |

Which tools freeze or train the towers:
- **Frozen by default:** Google's PEFT recipe [S7]; Unsloth with `finetune_vision_layers=False` [S39].
- **Can be trained:** PEFT, by targeting `audio_tower...linear` [S42]. Unsloth's audio notebooks also train audio parts, but which
  modules are unclear [S39]. The Khmer ASR adapter says it targets audio-encoder projection parts [S56]. The Ndizi ASR model trains
  LoRA plus the `embed_audio` adapter [S49].

## Who has done it

None of these is exactly "Gemma 4 + LoRA + audio + vision + iPhone".

| Who / what | Pipeline | Audio after conversion | Vision after conversion | Device | Status |
|---|---|---|---|---|---|
| **Ndizi African ASR** (smutuvi) [S49] | LoRA plus `embed_audio` on Sunbird's Sunflower-Gemma4-E2B, then merged. Shipped as merged safetensors, a community GGUF with mmproj, and a 2.7 GB `.litertlm` | **Yes in the bundle.** The header I read lists `tf_lite_audio_encoder_hw`, `tf_lite_audio_adapter`, `tf_lite_end_of_audio`, plus tags `finetuned_export_plus_audio` and `base_litert: litert-community/gemma-4-E2B-it-litert-lm`. The audio sections appear to be **spliced from Google's bundle**. Swahili WER on in-domain test fell from 0.655 to 0.484 "with on-device prompt" | **No vision sections** (Google's bundle has `tf_lite_vision_encoder`/`_adapter`; this one does not) | Not named | Published 2026-09-21. Closest evidence that a fine-tuned text slice plus Google's audio encoder works in LiteRT-LM. I inferred the splice from header strings (a 64 KB range read, not a download). Unclear whether the trained `embed_audio` made it into the bundle |
| **Sunbird Sunflower-Gemma4-E2B** [S50] | Continued pretraining, then speech SFT, then mixed SFT and GRPO, covering 69 African languages | Works in Transformers (server) | — | Server (vLLM/Transformers) | Shows that low-resource-language ASR fine-tuning of E2B works. No phone build |
| **QuadraKev** (litert-torch #998) [S16] | E4B QLoRA, merged, then export_hf 0.9.0 | — | Vision encoder quantised after a quantizer fix [S22] and "runs correctly on-device" | Not named | Their own exports segfaulted. They got it working by **binary-patching their sections into Google's pre-built bundle** (2026-04-28) [reported] |
| **TinmanLab companion** [S48] | Fine-tuned E4B, then patched `litert-torch-nightly` 0.10.0 | Not stated | Vision encoder kept FP32 | Not tested on phone; bundle "pending upload" | Needs Linux and 92+ GB RAM [reported] |
| **EchoRead (wundr-ai)** [S52] | E4B LoRA SFT and DPO, merged, re-exported with nightly plus patches | **Audio did not survive conversion** | Sections present, untested on GPU | Targets iOS Metal; device test deferred | 2026-07 [reported] |
| **Luigi meeting-agent-zh** [S51] | LoRA trained on Google's mobile QAT weights, merged, and written **into Google's own file** (GPTQ onto Google's integer grid), using a forked engine | Text only | Text only | Android (OPPO Reno7) | Shows splice-into-Google's-file works for quality and size [reported] |
| **SafeRide (esherialabs)** [S53] | PEFT LoRA, merged, export `dynamic_wi8_afp32`. Chat-template metadata had to be replaced | Not claimed | Not claimed | One Android phone | 2026-08 [reported] |
| **jdshah (dev.to)** [S54] | QLoRA, merged, export_hf `dynamic_wi4_afp32` | Disabled | Disabled ("vision encoder not found" until turned off) | Snapdragon 8 Elite (Android) | Failed on chat template until replaced (2026-07) [reported] |
| **aelhajj (Kaggle notebook, Medium)** [S55] | Says they got both vision and text working (comment on litert-torch #998, 2026-05-18) | — | Claimed | Android | Could not read the notebook (Kaggle page empty, Medium 403). [unverified] |
| **Gemma 3n precedent** | Fine-tuned 3n to `.litertlm`: request open since 2025-09 [S30]. 3n E4B export gives only pad tokens on device (open) [S18] | — | — | Android | Official tooling never covered fine-tuned 3n well |

Also found: many Gemma 4 ASR LoRAs on Hugging Face (Khmer, Vietnamese, Luganda, Kannada, Twi, Lithuanian). Most stop at a PEFT
adapter, with no phone build [S56]. One Yemeni-Arabic E2B assistant fine-tune ships GGUF plus a BF16 mmproj (text task; audio
not tested) [S57]. **Nothing for Saudi or Gulf Arabic speech on Gemma 4 was found.**

## Known failures and pitfalls

**Conversion (`.litertlm`)**
1. **Pre-built bundles are better than what you can export yourself.** For stock E4B, `export_hf` gave a 4.0 GB text-only file.
   Google's bundle is 3.66 GB and also has vision, audio and MTP (12 sections vs 5). Per-layer embedder: 1.41 GB vs 837 MB
   (2026-06-07) [S16]. [reported] Reason: Google's bundles come from QAT mobile checkpoints with int2/int4 weights, which
   `litert-torch` cannot convert [S16]. [confirmed by maintainer]
2. **Exports that load but crash or babble.** Self-exported Gemma 3n/4 bundles gave pad tokens or SIGSEGV on Android. Reported
   causes: float32 KV cache and mask where Google uses int8 and bool, and no `param_tensor` input (open since 2026-04) [S18][S16].
   [reported]
3. **Wrong model type in metadata.** Gemma 4 fell back to `generic_model`, causing a template error at runtime. It was fixed
   only on certain paths (2026-06-15) [S17]. Check with `litert-lm-peek` that the type is `gemma4`. [confirmed]
4. **Chat template.** LiteRT-LM's template engine (minijinja) cannot run the Hugging Face Gemma 4 template, which uses `.get()`.
   Use `--jinja_chat_template_override=litert-community/gemma-4-E2B-it-litert-lm` [S16][S54]. [confirmed by maintainer]
5. **Missing audio section breaks apps.** A text-only export failed in AI Edge Gallery with "TF_LITE_AUDIO_ENCODER_HW not found"
   (issue #1039, open, last activity 2026-09-21) [S19]. [reported] Before 2026-09-24, `export_hf` could not write audio sections
   at all [S11]. [confirmed]
6. **Vision quantisation crash.** The quantizer failed on the Gemma 4 vision encoder's 3D position table. A fix PR was filed
   2026-04-28 [S22]. Workaround: keep vision FP32 [S48]. [reported] A user reported a fine-tuned vision export giving
   gibberish images through `litert-torch` while the same merged model worked in Unsloth (2026-04-27) [S16]. [reported]
7. **Quality loss from PTQ.** PTQ int4/int8 exports of the unmodified E2B gave malformed JSON in 1–13 of 20 cases, where Google's
   QAT bundle gave none (2026-08-22) [S21]. A fine-tuned E2B lost tool-call accuracy after export [S20]. Google suggests
   `dynamic_wi4c_hr_afp32` or `dynamic_wi4b32_afp32` to limit the damage [S16]. [reported / maintainer advice]
8. **RAM.** E4B export needed 48 GB or more (one user used 400 GB of swap) [S16], 62 GB RAM plus 50 GB swap [S16], or
   92 GB or more [S48]. `--experimental_lightweight_conversion` helps [S16]. **Our PC has 31 GB, and WSL2 gets only part of
   that by default.** Plan on E2B, the lightweight flag and a big WSL swap file. [reported]
9. **Weight names after merge.** Merged checkpoints may save tower weights as `.weight` where `litert-torch` expects
   `.linear.weight` (ClippableLinear) [S16]. MLX-fused models use a different key layout (`language_model.model.*`) [S20][S47].
   [reported]

**iOS runtime (LiteRT-LM)**
10. **Vision on iOS is buggy even with Google's own bundles.** Open issues report: E2B vision fails with an XNNPack reshape error
    on a physical iPhone (2026-07-24) [S28a]; E4B vision fails on iOS v0.12.0 while E2B works (2026-05-26) [S28b]; E4B crashes
    on image prefill (2026-04-12) [S28c]. [reported]
11. **Audio on iOS:** a report that `Content.audioFile()` returns null on CPU and GPU (iOS 27 Simulator, v0.17.1). The maintainer
    replied the user forgot `audioBackend: .cpu()` (2026-10-07) [S27]. No confirmed bug, but **no public report of Gemma 4 audio
    on a physical iPhone through the Swift API either.** [reported]
12. **GPU fp16 output errors on iOS:** E4B repeats digits at long context; CPU and float32 are correct (2026-10-10) [S29]. [reported]

**Training**
13. **Unsloth audio data silently ignored** before the collator fix of 2026-06-10. Training "worked", but the audio tower never
    ran [S40]. Use versions after that date and check that batches contain `input_features`. [confirmed]
14. **`use_cache=False` gave garbage logits** in Gemma 4 (KV-shared layers). Fixed in Transformers 2026-04-09; Unsloth patched it
    too [S43][S39]. [confirmed]
15. **PEFT and `Gemma4ClippableLinear`:** you must target `.linear` inside it. A loose `q_proj` target can catch tower layers by
    accident [S42]. [confirmed]
16. **PLE and embeddings:** Google's recipe trains and saves full `embed_tokens` and `lm_head` [S7]. That changes the embedder
    section and enlarges what has to be converted. Not saving them is likely fine for dialect adaptation. [unverified]
17. **Audio fp16 overflow on T4 GPUs** in the audio attention (not an issue on an RTX 5080 with bf16) [S39]. [confirmed]

**GGUF path**
18. **Audio needs higher precision.** The llama.cpp authors recommend a BF16 mmproj [S32]. An unmerged PR's tests showed Q4_K_M
    text weights repeating themselves on audio longer than about 17 s, while Q5_K_M and up passed [S34]. [reported]
19. Older Unsloth mmproj files had **no audio encoder** (April 2026) [S38]. Re-convert yourself with the current converter, which
    has an audio-capable class [S35]. [confirmed for the converter]

**Windows**
20. Unsloth trains natively on Windows [S41]. `litert-torch` needs Linux (WSL2) [S14][S15]. coremltools has no Windows wheel
    [S15b]. MLX does not run on Windows [S46]. llama.cpp's converter is plain Python and works on Windows. [confirmed]

## Where sources disagree / unverified

- **Audio export in `litert-torch`:** the docs (2026-09-02) mention vision only [S2], and issue #1039 is still open [S19], but
  the code has had audio export since 2026-09-24 [S11]. The code is newer. Whether it produces a bundle the iOS runtime accepts:
  **unverified**.
- **Vision export:** a maintainer said in May that vision export was unsupported, but showed a working command in June [S16].
  Users still call it "flaky" [S16].
- **TinmanLab cites issue #998** for the vision-quantizer bug [S48]. #998 is the general "how to convert" thread; the bug is
  discussed in its comments and fixed via ai-edge-quantizer PR #482 [S16][S22]. Minor citation mismatch.
- **Unsloth VRAM:** the same guide gives 10 GB and 17 GB for E4B LoRA [S39].
- **CoreML-LLM's multimodal claims** (audio + vision at 34 tok/s on iPhone 17 Pro) come from the author only [S47]. Unverified.
- **The Ndizi bundle's audio adapter:** the model trained `embed_audio`, but the bundle tag says the audio sections came from
  Google's base bundle [S49]. Which adapter is inside is **unverified**.
- **Runtime LoRA for the audio encoder:** the runtime can now name-match audio-encoder LoRA inputs [S26]. Whether Google's public
  bundle has such inputs: **not found**.
- **Kaggle/Medium "fine-tuned Gemma 4 on mobile" write-up:** content unreadable [S55]. **Unverified.**

## Most likely pipeline

The key design choice: **train only the language model (LoRA on the text decoder). Leave the audio and vision towers and their
adapters frozen.** Then Google's own audio/vision encoder sections stay valid, and conversion only has to handle the text part,
which is the best-trodden path. Dialect ASR improvement must then come from the decoder. Sunflower and Ndizi suggest that can work
[S49][S50], but it is not proven for Saudi Arabic.

**Primary route: LiteRT-LM, splicing into Google's bundle**
1. Train a LoRA with Unsloth (native Windows) or PEFT on `google/gemma-4-E2B-it`, language layers only, bf16. Use the Gemma 4 chat
   template unchanged. Use Unsloth after 2026-06-10 [S40]. Done when: a held-out Saudi clip transcribes better with the adapter
   than without it, in Transformers on the PC.
2. Merge to 16-bit safetensors (`save_pretrained_merged`, or `merge_and_unload` + `save_pretrained`). Fix key names if needed.
   Done when: the merged folder loads in Transformers, gives the same output as base+adapter, and transcribes one audio clip.
3. In WSL2 (Ubuntu, big swap), install `litert-torch-nightly` from 2026-10-12 or later. Export:
   `export_hf --model=<merged> --task=text_generation --externalize_embedder --jinja_chat_template_override=litert-community/gemma-4-E2B-it-litert-lm --quantization_recipe=dynamic_wi4b32_afp32 --experimental_lightweight_conversion`.
   Done when: a `.litertlm` exists and `litert-lm-peek` shows `gemma4` model type.
4. Splice. `litert-lm-builder unpack` Google's `gemma-4-E2B-it.litertlm` and your export. In Google's `model.toml`, swap in your
   `prefill_decode`, `embedder` and `per_layer_embedder`. Keep Google's audio, vision, end-of-audio/vision, tokenizer and metadata
   sections, and drop the MTP drafter. Repack [S6]. Done when: peek lists the text sections plus Google's audio and vision sections.
   (Ndizi did a version of this [S49]; QuadraKev binary-patched [S16].) Risk: graph differences between `export_hf` output and
   Google's metadata (KV-cache type, `param_tensor`) [S16].
   - Alternative to splicing: try `--task=multimodal_lm` (audio + vision export, nightly) [S12]. This is untested publicly.
5. Desktop check with `litert-lm` CLI or Python (it runs on Windows [S1]): text, one Saudi audio clip, one image. Done when: all
   three give sensible answers and match step 2 closely.
6. iPhone 17 Pro with the LiteRT-LM Swift package (v0.18.0, 2026-10-06), `audioBackend: .cpu()`, `visionBackend: .cpu()` [S4].
   Done when: on a physical phone, the app answers about a spoken Saudi question and a camera photo.

**Fallback route: llama.cpp (GGUF + mmproj)**
1. Same training and merge as above.
2. On Windows: run `convert_hf_to_gguf.py` on the merged folder twice, once for the text model and once with `--mmproj` (the
   `Gemma4VisionAudioModel` class [S35]). Keep the mmproj in BF16 and the text at Q5_K_M or higher for audio [S32][S34].
3. Test with `llama-mtmd-cli` on the PC (audio + image).
4. Build the llama.cpp XCFramework (needs a Mac with Xcode, since `build-xcframework.sh` includes mtmd [S37]). Embed it in the
   iOS app.

**Third option: Core ML via CoreML-LLM** [S47]. It has a written fine-tune-to-iPhone workflow (merged text weights; audio and
vision taken from base). It needs macOS or Linux for coremltools and a Mac for the iOS build. It is a one-developer project.

## Smallest proving experiment

Goal: prove that a fine-tune survives conversion **and** that audio and vision still work on the iPhone, before spending effort on
real Saudi training. Use a "canary" LoRA: a tiny adapter that teaches one obvious, checkable behaviour.

1. **Baseline on the phone, no fine-tune.** Run Google's `gemma-4-E2B-it.litertlm` in a minimal Swift test app on the iPhone
   17 Pro with one 10 s Arabic WAV and one photo.
   Done when: both audio and image prompts give sensible answers on the physical device. If this fails, the runtime is the
   blocker, not the fine-tune. Then try the llama.cpp route's baseline instead.
2. **Canary LoRA.** Train a small text-only LoRA (language layers, a few hundred examples) that makes the model start every answer
   with a fixed Saudi word, for example "أبشر". Optionally add about 50 Saudi audio→transcript pairs.
   Done when: in Transformers on the PC, the merged model shows the canary word for text, audio and image prompts, and still
   transcribes the test clip.
3. **Convert (primary route, steps 3–4 above)** in WSL2.
   Done when: `litert-lm-peek` shows `gemma4` type, your text sections, and Google's audio and vision sections.
4. **Desktop run.**
   Done when: the CLI gives the canary word plus a correct transcript of the WAV plus a correct image description.
5. **Phone run** with the same app as step 1, swapping only the model file.
   Done when: on the iPhone, the canary word appears **and** the WAV is transcribed **and** the photo is described. That proves
   the pipeline end to end.
6. **If step 3 or 5 fails:** repeat steps 3–5 with the llama.cpp route (GGUF + BF16 mmproj).
   Done when: the same three checks pass with llama.cpp on the iPhone, or you have a written list of exactly which check failed
   in each route.

## Open questions

- Does the 2026-09-24 `multimodal_lm` audio export produce bundles the iOS runtime accepts? No public report yet.
- Is the spliced bundle (your text sections plus Google's QAT audio and vision sections) stable on iOS, given the graph
  differences reported between `export_hf` output and Google's bundles?
- Can decoder-only LoRA fix Saudi dialect ASR enough, or must the audio tower or `embed_audio` be trained? If so, they must be
  exported too, and Google's audio section can't be reused.
- Does Google's public bundle accept runtime audio-encoder LoRA (`audioLoraPath`)? This would avoid merging the audio part.
- How much does PTQ int4 of a fine-tune lose versus Google's QAT int2/int4 bundle, in size, speed and Arabic accuracy?
- Will Gemma 4 E2B vision run reliably on a physical iPhone 17 Pro with the current LiteRT-LM (v0.18.0)? The iOS vision issues
  are still open.
- Will `litert-torch` export E2B within 31 GB RAM plus swap under WSL2?
- Is there a Gemma 4 audio path in MLX Swift coming? Today it drops audio.

## Sources

Accessed 2026-10-13 unless noted. "upd" = page's own last-updated date.

- [S1] Google, LiteRT-LM Gemma 4 page, upd 2026-09-04. https://developers.google.com/edge/litert-lm/models/gemma-4
- [S2] Google, Convert PyTorch GenAI models (`export_hf`), upd 2026-09-02. https://developers.google.com/edge/litert/conversion/pytorch/genai
- [S3] Google, LiteRT-LM tutorial "Convert and run a fine tuned model on device", upd 2026-06-01. https://developers.google.com/edge/litert-lm/tutorials/convert-and-run
- [S4] Google, LiteRT-LM Swift guide, upd 2026-09-04. https://developers.google.com/edge/litert-lm/swift
- [S5] Google, LiteRT-LM overview, upd 2026-10-06. https://developers.google.com/edge/litert-lm/overview
- [S6] Google, LiteRT-LM File Builder, upd 2026-07-02. https://developers.google.com/edge/litert-lm/file_builder
- [S7] Google, Vision fine-tune with HF Transformers and QLoRA, upd 2026-06-19. https://ai.google.dev/gemma/docs/core/huggingface_vision_finetune_qlora
- [S8] Google, Gemma audio understanding, upd 2026-10-10. https://ai.google.dev/gemma/docs/capabilities/audio
- [S9] litert-community, gemma-4-E2B-it-litert-lm model card. https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
- [S10] Google Developers Blog, "Blazing fast on-device GenAI with LiteRT-LM", 2026-05-19. https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/
- [S11] litert-torch commit ed83bf8 "Support Gemma 4 audio encoder export for multimodal LLM", 2026-09-24. https://github.com/google-ai-edge/litert-torch/commit/ed83bf8fe5b9b9256a915a4dc30a6b7c41f6ad27
- [S12] litert-torch `exportable_module_config.py` (main). https://github.com/google-ai-edge/litert-torch/blob/main/litert_torch/generative/export_hf/core/exportable_module_config.py
- [S13] litert-torch releases (v0.9.4, 2026-08-24) https://github.com/google-ai-edge/litert-torch/releases and PyPI litert-torch-nightly 0.10.0.dev20261012 https://pypi.org/project/litert-torch-nightly/
- [S14] litert-torch README (OS: Linux). https://github.com/google-ai-edge/litert-torch
- [S15] PyPI litert-converter 0.5.0 wheels (macOS arm64, manylinux x86_64). https://pypi.org/project/litert-converter/
- [S15b] PyPI coremltools 9.0 wheels (macOS, manylinux). https://pypi.org/project/coremltools/
- [S16] litert-torch issue #998 "How to convert Gemma-4 safetensors model to LiteRT-LM format?", 2026-04-13 to 2026-07-01 (comments by QuadraKev, stawils, sirakiin). https://github.com/google-ai-edge/litert-torch/issues/998
- [S17] litert-torch issue #1005 (missing gemma4 metadata case), 2026-04-26, open. https://github.com/google-ai-edge/litert-torch/issues/1005
- [S18] litert-torch issue #994 (Gemma 3n/4 exports: pad tokens / SIGSEGV), 2026-04-03, open. https://github.com/google-ai-edge/litert-torch/issues/994
- [S19] litert-torch issue #1039 "Support audio encoder export for gemma-4-E2B-it", 2026-06-02, open. https://github.com/google-ai-edge/litert-torch/issues/1039
- [S20] litert-torch issue #1013 (fine-tuned E2B tool-call regression after export), 2026-05-01, open. https://github.com/google-ai-edge/litert-torch/issues/1013
- [S21] litert-torch issue #1183 (PTQ exports emit malformed JSON), 2026-08-22, open. https://github.com/google-ai-edge/litert-torch/issues/1183
- [S22] ai-edge-quantizer PR #482 (3D tensor quantisation fix), 2026-04. https://github.com/google-ai-edge/ai-edge-quantizer/pull/482
- [S23] LiteRT-LM issue #3173 (runtime LoRA loads but has no effect on gemma-4-E2B), 2026-08-07, open. https://github.com/google-ai-edge/LiteRT-LM/issues/3173
- [S24] LiteRT-LM issue #1188 (public LoRA API), 2026-01-07, open. https://github.com/google-ai-edge/LiteRT-LM/issues/1188
- [S25] LiteRT-LM `swift/Config.swift` and `swift/Engine.swift` (main). https://github.com/google-ai-edge/LiteRT-LM/blob/main/swift/Config.swift
- [S26] LiteRT-LM PR #3868 "Load Gemma 4 audio encoder LoRAs under the encoder's own input names", merged 2026-10-06. https://github.com/google-ai-edge/LiteRT-LM/pull/3868
- [S27] LiteRT-LM issue #3850 (iOS `Content.audioFile()` returns null), 2026-10-04. https://github.com/google-ai-edge/LiteRT-LM/issues/3850
- [S28a] LiteRT-LM issue #2979 (iOS E2B vision XNNPack error), 2026-07-24, open. https://github.com/google-ai-edge/LiteRT-LM/issues/2979
- [S28b] LiteRT-LM issue #2370 (iOS E4B vision fails, v0.12.0), 2026-05-26, open. https://github.com/google-ai-edge/LiteRT-LM/issues/2370
- [S28c] LiteRT-LM issue #1933 (iOS E4B crash on image prefill), 2026-04-12, open. https://github.com/google-ai-edge/LiteRT-LM/issues/1933
- [S29] LiteRT-LM issue #3913 (iOS GPU fp16 digit duplication), 2026-10-10, open. https://github.com/google-ai-edge/LiteRT-LM/issues/3913
- [S30] LiteRT-LM issue #547 "Converting Gemma3n to litertlm", 2025-09-09, open. https://github.com/google-ai-edge/LiteRT-LM/issues/547
- [S31] litert-torch Generative API README (roadmap lists "LoRA support") and `layers/lora.py` (attention-only). https://github.com/google-ai-edge/litert-torch/blob/main/litert_torch/generative/README.md
- [S32] llama.cpp PR #21421 "mtmd: add Gemma 4 audio conformer encoder support", merged 2026-04-12. https://github.com/ggml-org/llama.cpp/pull/21421
- [S33] llama.cpp PR #21824 (causal attention for Gemma 4 audio), merged 2026-04-13. https://github.com/ggml-org/llama.cpp/pull/21824
- [S34] llama.cpp PR #21599 (warn below Q5_K_M for Gemma 4 audio; closed, not merged). https://github.com/ggml-org/llama.cpp/pull/21599
- [S35] llama.cpp `conversion/gemma.py` (`Gemma4VisionAudioModel`). https://github.com/ggml-org/llama.cpp/blob/master/conversion/gemma.py
- [S36] llama.cpp `docs/multimodal.md` (Gemma 4: audio input, vision input). https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
- [S37] llama.cpp `build-xcframework.sh` (mtmd enabled). https://github.com/ggml-org/llama.cpp/blob/master/build-xcframework.sh
- [S38] HF discussion "Include Audio Encoder in mmproj GGUFs", unsloth/gemma-4-E2B-it-GGUF, April 2026. https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF/discussions/1
- [S39] Unsloth, Gemma 4 fine-tuning guide (no page date). https://unsloth.ai/docs/models/gemma-4/train
- [S40] Unsloth issue #6004 (collator ignored audio), fixed 2026-06-10. https://github.com/unslothai/unsloth/issues/6004
- [S41] Unsloth Windows installation (no page date). https://unsloth.ai/docs/get-started/install/windows-installation
- [S42] PEFT issue #3130 (LoRA for `Gemma4ClippableLinear`), 2026-04-02/03. https://github.com/huggingface/peft/issues/3130
- [S43] Transformers issue #45242 (`use_cache=False` garbage logits), closed 2026-04-09. https://github.com/huggingface/transformers/issues/45242
- [S44] mlx-vlm `models/gemma4` and `LORA.MD`. https://github.com/Blaizzy/mlx-vlm/tree/main/mlx_vlm/models/gemma4
- [S45] mlx-swift-lm `Libraries/MLXVLM/Models/Gemma4.swift` (main, last commit 2026-10-12). https://github.com/ml-explore/mlx-swift-lm/blob/main/Libraries/MLXVLM/Models/Gemma4.swift
- [S46] MLX install docs (macOS ≥ 14; Linux CUDA/CPU). https://github.com/ml-explore/mlx/blob/main/docs/src/install.rst
- [S47] CoreML-LLM README and `docs/LOCAL_FINETUNE_WORKFLOW.md` (doc dated 2026-04-22). https://github.com/john-rocky/CoreML-LLM
- [S48] Tinman-Lab gemma4-companion-litert-lm model card (no date). https://huggingface.co/TinmanLabSL/gemma4-companion-litert-lm
- [S49] smutuvi Ndizi African ASR: LiteRT bundle (created 2026-09-21) https://huggingface.co/smutuvi/ndizi-gemma4-e2b-african-asr-litert ; merged https://huggingface.co/smutuvi/ndizi-gemma4-e2b-african-asr-merged ; GGUF + mmproj (2026-09-20) https://huggingface.co/mradermacher/ndizi-gemma4-e2b-african-asr-merged-GGUF . Section names read from the first 64 KB of the bundle file (own inspection, 2026-10-13).
- [S50] Sunbird, Sunflower-Gemma4-E2B model card (created 2026-07-19). https://huggingface.co/Sunbird/Sunflower-Gemma4-E2B
- [S51] Luigi, gemma-4-E4B-meeting-agent-zh-LiteRT model card. https://huggingface.co/Luigi/gemma-4-E4B-meeting-agent-zh-LiteRT
- [S52] wundr-ai, echoread-gemma4-e4b-v3.2.1-litertlm-gpu model card (2026-07). https://huggingface.co/wundr-ai/echoread-gemma4-e4b-v3.2.1-litertlm-gpu
- [S53] esherialabs, saferide-gemma-4-e2b litertlm model card (2026-08). https://huggingface.co/esherialabs/saferide-gemma-4-e2b-v058-original-419806-litertlm
- [S54] jdshah, "My Fine-Tuned Gemma 4 Loaded Fine, Then Broke on the First Message", dev.to, 2026-07-06 (edited 2026-10-01). https://dev.to/jdshah/my-fine-tuned-gemma-4-loaded-fine-then-broke-on-the-first-message-1nef
- [S55] aelhajj, Kaggle notebook (unreadable) https://www.kaggle.com/code/aelhajj/fine-tuned-gemma-4-on-mobile-lite-rt-solution and Medium post (HTTP 403) https://medium.com/@amanie.elhajj/how-i-got-a-fine-tuned-gemma-4-working-on-android-51484e6369ed
- [S56] Sothay, Gemma 4 E2B Khmer ASR LoRA (no date). https://huggingface.co/Sothay/gemm4-E2B-khmer-asr
- [S57] yemeni-ai-lab, gemma-4-e2b-yemeni-arabic-assistant-GGUF (created 2026-05-03). https://huggingface.co/yemeni-ai-lab/gemma-4-e2b-yemeni-arabic-assistant-GGUF
- [S58] Google AI Edge Gallery README (Ask Image, Audio Scribe; Android 12+, iOS 17+). https://github.com/google-ai-edge/gallery
