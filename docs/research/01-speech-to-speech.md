# Q1. Speech-to-speech

Research date: 2026-10-13. Labels: **confirmed** = primary source (Google/Apple docs, model card, paper). **Reported** = secondary source only. **Unverified** = claim with no backing found.

## Question

In Google's Gemma 4 announcement and demos, people talk to the model and it seems to talk back. How does that work? Can any Gemma 4 model (E2B, E4B, 12B, others) output audio itself, or does speech go in, text come out, and a separate text-to-speech (TTS) model speak the reply? Is there any Google or Gemma-family model that produces speech on-device, and are its weights open? Briefly: which Arabic TTS voices does iOS have on-device, and is there a Saudi-accented one?

## Short answer

- No Gemma 4 model outputs audio. E2B, E4B and 12B take audio **in** but produce **text only**. 26B A4B and 31B take no audio at all. ([1], [2], [3], [4])
- Every "talk to it and it talks back" setup we found is a chain: speech recognition, then Gemma 4, then a separate TTS model. Example: the Hugging Face + Cerebras demo used Parakeet for recognition, Gemma 4 31B, and Qwen3-TTS. ([9])
- Google has no open-weight, on-device speech output model in the Gemma family. Its native speech output (Gemini Live API) is cloud-only. ([12], [13])
- On iOS, the long-standing built-in Arabic voice is "Maged" (locale ar-SA). We found no Saudi-dialect voice from Apple. Apple's own iOS 27 feature table does not list Arabic for Siri's neural voices. ([16], [15])

## Findings

### 1. What Gemma 4 is, and which models take audio

- **Confirmed.** The current family has five sizes: E2B, E4B, 12B ("12B Unified"), 26B A4B (Mixture-of-Experts, meaning only part of the model runs for each token) and 31B dense. The license is Apache 2.0. ([2], [3])
- **Confirmed.** The first release (2026-04-02) had E2B, E4B, 26B and 31B. That announcement mentions audio input only for E2B/E4B, and says nothing about speech output. ([1])
- **Confirmed.** 12B was added on 2026-06-03. Google calls it "our first mid-sized model to feature native audio inputs." It has no separate audio encoder (the part that turns sound into model-ready numbers). Raw audio goes straight into the language model. ([5], [6])
- **Confirmed.** The official model card lists inputs as "Text, Image, Audio" for E2B, E4B and 12B Unified, and "Text, Image" for 26B A4B and 31B. Output is text. ([3], last updated 2026-07-30)
- **Confirmed.** The Hugging Face model card says the models handle text, image and (on three sizes) audio input, "and generating text output." It never mentions speech generation or TTS. ([2])

### 2. What the audio input actually does

- **Confirmed.** The tasks are automatic speech recognition (ASR: turning speech into text), speech translation into text in another language, and general speech understanding (answering questions about a clip). ([4], last updated 2026-10-10; [2])
- **Confirmed.** Limits: clips up to 30 seconds, mono, 16 kHz. Each second of audio costs 25 tokens. ([4])
- **Confirmed.** Gemma 4 has a ~300M-parameter audio encoder on E2B/E4B. The technical report says 12B drops the encoder and feeds raw 40 ms audio chunks directly into the model. ([2], [6], [7])
- **Confirmed.** The Hugging Face launch post says music and non-speech sounds were not in the training data. ([8], 2026-04-02)
- **Not found.** No official page lists which languages the audio input supports. Arabic is not named anywhere for audio. ([4], [2])

### 3. Technical report

- **Confirmed.** "Gemma 4 Technical Report" (arXiv 2607.02770, v1 2026-07-02, v2 2026-07-24). The abstract describes audio encoders and says 12B takes in raw audio. It does not mention audio output or speech generation. ([6])

### 4. How the "talk back" demos work

- **Confirmed (Google material).** We found no Google demo where Gemma 4 itself speaks.
  - The 2026-04-02 announcement has images and benchmarks but no voice demo. ([1])
  - The 12B announcement's linked video is about wearable robot arms, not voice replies. ([5])
  - The LiteRT-LM blog (2026-05-19) talks about audio input only. LiteRT-LM is Google's on-device runtime for these models. ([10])
  - The 12B developer guide (2026-06-03) covers audio input, ASR and diarization (working out who spoke when). It does not mention TTS. ([11])
- **Confirmed (Google AI Edge Gallery).** Google's demo app runs on Android 12+ and iOS 17+. Its audio feature, "Audio Scribe", transcribes and translates recordings into text. The repo README does not mention spoken replies or TTS. ([14])
- **Reported.** Google's AI Edge Eloquent (iOS, launched 2026-04) is an offline dictation app using Gemma-based speech recognition. It turns speech into text and does not speak back. ([18])
- **Confirmed (partner demo).** Hugging Face + Cerebras built a real-time voice demo (2026-07-01). It chains NVIDIA Parakeet (recognition), Gemma 4 31B on Cerebras (reasoning) and Alibaba's Qwen3-TTS (spoken reply). This is a cascaded pipeline (a chain of separate models). It runs in the cloud, not on-device. ([9])
- **Reported (Google for Developers video, via a news write-up).** "Gemma Playground: Robot Duck" ([video](https://www.youtube.com/watch?v=pLwB_63yUBY)) runs Gemma 4 E2B fully on-device on two robot ducks, one on a Raspberry Pi 5 and one on a Jetson Orin Nano. It is also a chain: NVIDIA Parakeet (speech to text), then Gemma 4 E2B (it also looks through a camera), then Kokoro (text to speech) ([Circuit Digest](https://circuitdigest.com/news/google-gemma-4-e2b-runs-locally-on-robot-duck); code: [Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini), Apache 2.0). Kokoro's voice list has no Arabic ([Kokoro VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md), confirmed). Added 2026-10-13 after the owner asked about this video.
- **Reported.** Community local voice assistants follow the same pattern. Example: microphone, then Whisper for recognition, then Gemma 4 via vLLM, then Piper-TTS. ([19])

### 5. Google / Gemma-family models that do speak

- **Confirmed.** The DeepMind Gemma page lists Gemma 4 (with QAT and MTP variants), DiffusionGemma, EmbeddingGemma 1/2, MedGemma, TranslateGemma, T5Gemma, FunctionGemma, VaultGemma, ShieldGemma 2 and others. None is described as producing speech. The page lists "Gemini Audio" separately, as a Gemini (closed) model, not a Gemma one. ([12])
- **Confirmed.** The Gemini Live API outputs raw audio and supports conversation in 70 languages. It works over a WebSocket connection to Google's servers. The page doesn't mention on-device use or open weights. ([13], updated 2026-10-06)
- **Confirmed.** On Android, Gemini Nano's ML Kit GenAI APIs offer summarization, proofreading, rewriting, image description, speech **recognition** and a prompt API. There is no TTS, and the docs are Android-only. ([17], updated 2026-10-08)
- **Reported.** T5Gemma-TTS-2b-2b is a hobby TTS model built on Google's T5Gemma weights by a third party (Aratako), not by Google. It supports English, Chinese and Japanese, not Arabic. ([20])
- **Not found.** Any Google open-weight TTS or speech-to-speech model that runs on-device.

### 6. On-device Arabic TTS on iOS (brief)

- **Confirmed (old source).** `AVSpeechSynthesizer` (Apple's built-in speech API) offers a voice named "Maged" with language code `ar-SA` and identifier `com.apple.ttsbundle.Maged-compact`. This was seen in a 2018 Apple Developer Forums listing. ([16]) Whether newer or higher-quality ("Enhanced"/"Premium") Arabic voices exist on iOS 26/27 was **not confirmed** from a primary source.
- **Confirmed.** Apple's iOS 27 feature table:
  - Siri's neural text-to-speech voice: no Arabic region listed.
  - Personal Voice (cloning the user's own voice): English (US), Mandarin and Spanish (Mexico) only.
  - "Arabic (Saudi Arabia)" appears for dictation and Voice Control, which are speech input. ([15])
- **Sources disagree.** The same Apple table omits Arabic from "VoiceOver, Live Speech, Read & Speak." That conflicts with the Maged voice above and with long-standing Arabic VoiceOver support. See the next section.
- **Not found.** A Saudi-dialect (Najdi/Hijazi) TTS voice from Apple. The `ar-SA` locale tag is a region label. We found nothing saying the voice speaks with a Saudi accent rather than Modern Standard Arabic (**unverified**).

## Where sources disagree / unverified

- **"Gemma 4 speaks directly."** A blog post by SIVARO (2026-07-07) claims Gemma 4 outputs speech tokens directly with a 200-300 ms response time. It cites no source, and it contradicts Google's model card, docs and technical report. All of those say text output only. Treat it as **wrong / unverified**. ([21] vs [2], [3], [4], [6])
- **Model sizes.** Some early third-party guides list only E2B, E4B, 26B and 31B, because they predate the 2026-06-03 12B release. Google's current pages list five sizes including 12B. ([1] vs [3], [5])
- **Arabic in Apple VoiceOver/Read & Speak.** Apple's iOS 27 feature table omits Arabic from that list. But developer listings show an `ar-SA` Maged voice in `AVSpeechSynthesizer`. The listing is from 2018, so it is old. **Unresolved.** It has to be checked on a real device. ([15] vs [16])
- **Audio in third-party runtimes.** An mlx-vlm issue reports garbled output from Gemma 4 E2B/E4B audio input. Community posts say llama.cpp audio support is incomplete. Status as of today: **unverified**. ([22])
- **Audio on LiteRT-LM for iOS.** The LiteRT-LM Gemma 4 page (updated 2026-09-04) gives iPhone 17 Pro text speeds for E2B/E4B but says nothing about audio input on iOS. It says larger models (12B) are "coming soon". ([10], [23])

## What this means for the project

- Plan a three-part voice pipeline: speech recognition, then Gemma 4 (text), then TTS. A speech-to-speech Gemma does not exist.
- Gemma 4 E2B/E4B can be the speech-recognition stage itself, since audio goes in directly. Watch two limits: the 30-second clip cap, and no stated Arabic audio support. A separate ASR model may still be needed for Saudi Arabic.
- TTS must be a separate component. Options to evaluate: Apple's built-in Arabic voice (free and offline, but quality and accent unknown), or an open on-device Arabic TTS model (not covered by this note).
- The same pipeline carries over to RK3588 / Jetson. Apple's voices won't exist there, so the TTS choice for the board is a separate decision.

## Open questions

Each is a next step with a "Done when".

1. **Does Gemma 4 E2B/E4B audio input understand Saudi Arabic?** Find published Arabic results (e.g. FLEURS Arabic word error rate) in the technical report's appendix or the model card's benchmark tables. Done when: an Arabic audio score from a primary source is recorded here, or "not published" is confirmed.
2. **Does LiteRT-LM on iOS support Gemma 4 audio input today?** Check the LiteRT-LM GitHub repo, the iOS/Swift guide and the AI Edge Gallery iOS release notes. Done when: a primary source says yes or no for audio on iOS.
3. **Which Arabic voices does iOS 26/27 actually ship, and at what quality?** Check Apple developer docs, or run `AVSpeechSynthesisVoice.speechVoices()` on the iPhone 17 Pro later. Done when: a list of `ar-*` voices with quality tiers (default/enhanced/premium) is recorded.
4. **Is any Apple Arabic voice Saudi-accented, or only Modern Standard Arabic?** Done when: an Apple source or a recorded on-device sample settles it.
5. **Which open on-device TTS models speak Arabic, ideally Saudi dialect, with licenses fit for this project?** This is a separate research question. Done when: it has its own research note.

## Sources

1. Google blog, "Gemma 4" announcement. Sizes, audio input on E2B/E4B, Apache 2.0, no speech output. 2026-04-02. https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
2. Hugging Face model card, google/gemma-4-E4B-it. Modalities, text-only output, 30 s audio cap, ~300M audio encoder. Accessed 2026-10-13. https://huggingface.co/google/gemma-4-E4B-it
3. Google AI for Developers, Gemma 4 model card. Per-size input modalities, text output, license. Updated 2026-07-30. https://ai.google.dev/gemma/docs/core/model_card_4
4. Google AI for Developers, Gemma audio capabilities. ASR/translation, 30 s, 16 kHz mono, 25 tokens/s, no output audio. Updated 2026-10-10. https://ai.google.dev/gemma/docs/capabilities/audio
5. Google blog, "Introducing Gemma 4 12B". Encoder-free, first mid-size audio-input model. 2026-06-03. https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/
6. arXiv 2607.02770, "Gemma 4 Technical Report" (Gemma Team). Abstract mentions audio input only. v1 2026-07-02, v2 2026-07-24. https://arxiv.org/abs/2607.02770
7. Hugging Face papers page for the technical report. Discussion of 12B raw-audio input. 2026-07. https://huggingface.co/papers/2607.02770
8. Hugging Face blog, "Welcome Gemma 4". Audio is input only, no music/non-speech training data. 2026-04-02. https://huggingface.co/blog/gemma4
9. Hugging Face blog, Cerebras + Gemma 4 real-time voice AI. Cascaded Parakeet, Gemma 4 31B, Qwen3-TTS pipeline. 2026-07-01. https://huggingface.co/blog/cerebras-gemma4-voice-ai
10. Google Developers Blog, "Blazing-fast on-device GenAI with LiteRT-LM". Audio encoder loaded on demand, no TTS. 2026-05-19. https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/
11. Google Developers Blog, "Gemma 4 12B: The Developer Guide". Audio input, ASR, diarization, no TTS. 2026-06-03. https://developers.googleblog.com/gemma-4-12b-the-developer-guide/
12. Google DeepMind, Gemma models page. Family list, no speech-output Gemma, "Gemini Audio" listed separately. Accessed 2026-10-13. https://deepmind.google/models/gemma/
13. Google AI for Developers, Gemini Live API. Audio output over WebSocket (cloud), 70 languages. Updated 2026-10-06. https://ai.google.dev/gemini-api/docs/live
14. GitHub, google-ai-edge/gallery README. Audio Scribe (speech to text), Android 12+/iOS 17+, no TTS mentioned. Accessed 2026-10-13. https://github.com/google-ai-edge/gallery
15. Apple, iOS & iPadOS 27 Feature Availability. Arabic locales per feature, Siri neural TTS list, Personal Voice list. Accessed 2026-10-13. https://www.apple.com/ios/feature-availability/
16. Apple Developer Forums thread 109572. `speechVoices()` output incl. Maged, ar-SA. 2018-10. https://developer.apple.com/forums/thread/109572
17. Google, ML Kit GenAI APIs overview (Gemini Nano). Feature list incl. speech recognition, no TTS. Updated 2026-10-08. https://developers.google.com/ml-kit/genai
18. Android Authority, Google AI Edge Eloquent dictation app (secondary). 2026-04. https://www.androidauthority.com/google-ai-edge-eloquent-ai-dictation-app-3655274/
19. GitHub, JoergR75 local voice assistant (Whisper, Gemma 4/vLLM, Piper-TTS) (community). Accessed 2026-10-13. https://github.com/JoergR75/Fully-Local-Real-Time-Voice-AI-Assistant-with-Gemma-4-ROCm-vLLM-Whisper-Streaming-TTS-/blob/main/README.md
20. Hugging Face, Aratako/T5Gemma-TTS-2b-2b (third-party TTS on T5Gemma). Accessed 2026-10-13. https://huggingface.co/Aratako/T5Gemma-TTS-2b-2b
21. SIVARO, "Gemma 4 Real-Time Voice AI Changes Everything". Unsourced claim of native speech output. 2026-07-07. https://sivaro.in/articles/gemma-4-real-time-voice-ai-changes-everything/
22. GitHub, Blaizzy/mlx-vlm issue #903. Gemma 4 audio input gives garbled output in mlx-vlm. Accessed 2026-10-13. https://github.com/Blaizzy/mlx-vlm/issues/903
23. Google AI Edge, LiteRT-LM Gemma 4 page (redirects to developers.google.com). iPhone 17 Pro E2B/E4B speeds, E2B/E4B only for now. Updated 2026-09-04. https://developers.google.com/edge/litert-lm/models/gemma-4
