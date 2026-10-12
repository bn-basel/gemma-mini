# Q5. Saudi speech baseline

Research date: 2026-10-13. Desk research only: no data, audio, or model weights were downloaded and nothing was run. The only things fetched were web pages plus two small public text files: the leaderboard's `app.py` and its SADA test manifest, which is transcripts only (about 1.8 MB). The manifest was streamed and counted, not kept.

Tags used below:
- **[confirmed]**: read in a primary source (the author's own page, paper, model card or code).
- **[reported]**: secondary source only (news or summaries).
- **[unverified]**: no source found, or derived by me and labelled as such.

Two terms used throughout:
- **WER (word error rate):** (substituted + deleted + inserted words) ÷ number of reference words. Lower is better, and it can go above 100%. **CER** is the same calculation over characters.
- **Normalization:** the text clean-up applied to both the reference transcript and the model output before scoring. For Arabic this usually means removing diacritics and punctuation and unifying letter variants (أ/إ/آ→ا, ى→ي, ة→ه). It can move WER by several points, so two numbers are only comparable when the test set and the normalization are the same.

## Question

The owner's note says: "NVIDIA Nemotron 3.5 ASR fine-tuned on SDAIA's SADA: 55% → 30% WER on Najdi/Hijazi". This note checks every part of that claim. It also looks at:
- what SADA's splits and transcript format are;
- what other published Saudi and Arabic ASR results exist, especially for Gemma 4 E2B/E4B, Gemma 3n and Whisper;
- what the student must replicate to compare fairly.

## Short answer

- **The owner's note is right on the headline, but it is shorthand.** The primary source is NVIDIA's Technical Blog post of 30 Sep 2026 [1]. On a Najdi + Hijazi subset of the SADA test split, WER fell from 55.05% to 29.96%. CER fell from 31.63% to 12.18% [1].
  - **Model:** `nvidia/nemotron-3.5-asr-streaming-0.6b`, a 0.6B-parameter cache-aware FastConformer-RNNT [1][2].
  - **Setup:** greedy decoding, 320 ms streaming setting, no language model [1].
  - **Full SADA test:** WER went from 58.84% to 35.61% [1].
  - **Weights:** no fine-tuned checkpoint has been released. Only the base model is public, under the OpenMDW-1.1 licence [2].
- **The strongest public baseline for Gemma 4 itself** is the Open Universal Arabic ASR Leaderboard, which scores the full SADA test set (6,189 utterances, 10.75 h) zero-shot [7][8]:

  | Model | WER | CER |
  |---|---|---|
  | Gemma 4 E4B-it | 43.40% | 20.96% |
  | Gemma 4 E2B-it | 46.23% | 23.47% |
  | Base Nemotron 3.5 | 53.06% | 29.87% |
  | Whisper large-v3 | 55.96% | 34.62% |

- **NVIDIA's numbers and the leaderboard's numbers use different text normalization and possibly different test subsets.** You cannot put them in one table without re-scoring.

## The NVIDIA/SDAIA result

**Primary source:** NVIDIA Technical Blog, "Fine-Tuning NVIDIA Nemotron for Saudi Arabic Dialects, with a Path to Other Languages", dated 30 Sep 2026 [1]. Some aggregators list 1 Oct 2026 [reported]. Five authors are listed, all shown as NVIDIA [1]. I found no SDAIA-authored paper or announcement about this fine-tune. SDAIA and the Saudi Broadcasting Authority (SBA) appear only as the publishers of the SADA dataset [1][3][4]. So "NVIDIA × SDAIA" means NVIDIA used SDAIA's dataset. It was not shown to be a joint project.

### Model and setup [confirmed, 1][2]

**Model**

| Item | Value |
|---|---|
| Model name | NVIDIA Nemotron 3.5 ASR, Hugging Face id `nvidia/nemotron-3.5-asr-streaming-0.6b`. Base model card release date: 04 Jun 2026 [2]. |
| Size / architecture | 0.6B parameters. Cache-Aware FastConformer encoder with 24 layers and d_model 1024, an RNN-T decoder, and language-ID prompt conditioning. Arabic locale `ar-AR` [1][2]. |
| What was trained | The best run updated all 24 encoder layers. The decoder, joint network and prompt embeddings were always trained [1]. A "top-8 layers" variant had 230.4M trainable and 407.6M frozen parameters [1]. |

**Training data**

| Item | Value |
|---|---|
| Source | SADA 2022 from Kaggle, Najdi + Hijazi only. Started from 125,490 utterances and kept 103,559 (82.5%), which is 133.7 h [1]. |
| Clips kept | 0.5–30 s long, 1.5–35 characters per second, no SADA "unclear speech" tag (both spellings), no "NaN" transcripts [1]. |
| Extra audio-quality filter | A second NeMo Curator pass on UTMOS and SIGMOS speech-quality scores [1]. |
| Training mix | 90% SADA (Najdi + Hijazi), 7% FLEURS English, 3% FLEURS Arabic [1]. |
| Compute | 2× RTX PRO 6000 Blackwell GPUs, 12,000 steps, about 4.5 h [1]. |

**Evaluation**

| Item | Value |
|---|---|
| Normalization | The post's `normalize_arabic` function removes diacritics and punctuation and maps alef variants→ا, ى→ي and ة→ه. Numbers are not handled [1]. **The post shows this function for training transcripts. It does not say it was applied to references and outputs at scoring time** [1]. |
| Scoring tool | "NeMo evaluation script" [1]. NeMo's `word_error_rate` is corpus-level: total errors ÷ total reference words. `strip_lang_tags=True` is used so the locale tag is not counted as an inserted word [1]. |
| Decoding | Headline numbers use greedy decoding at `att_context_size [56,3]`, which is the 320 ms "streaming default". No language model. NGPU-LM fusion was not evaluated [1][2]. |
| Weights / licence | No fine-tuned checkpoint is mentioned in the post, and none was found on Hugging Face (searched 2026-10-13) [1]. The base model is under OpenMDW-1.1 [2]. |

**Linked code** [confirmed]:
- The linked notebook (`nvidia-riva/tutorials`, `asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb`) uses the English AN4 dataset, not SADA [16].
- The linked `NVIDIA/skills` → `nemotron-asr-finetune` skill (Apache-2.0) contains no SADA-specific evaluation code [16].
- So the SADA test-set filter has not been published.

### Exact numbers [confirmed, 1]

Before = pretrained base model. After = fine-tuned model. Settings: greedy decoding, `[56,3]` / 320 ms.

| Test set | WER before → after | CER before → after |
|---|---|---|
| SADA test, Najdi + Hijazi subset | **55.05% → 29.96%** | 31.63% → 12.18% |
| SADA test, full (all dialects) | 58.84% → 35.61% | 35.40% → 15.97% |
| FLEURS English | 11.04% → 10.42% | 6.47% → 4.53% |
| FLEURS Arabic | 12.67% → 11.41% | 5.55% → 3.97% |

The post gives no separate numbers for individual dialects (Najdi alone, Hijazi alone, Khaliji and so on) [1]. The subset's hour and utterance counts are not stated either [1].

**How many encoder layers were updated** (Najdi + Hijazi test) [1]:

| Layers updated | WER | CER |
|---|---|---|
| Base model | 55.05% | 31.63% |
| Top 6 | 33.42% | 14.10% |
| Top 8 | 32.32% | 13.53% |
| All 24 | 29.96% | 12.18% |

**Decoding options** (fine-tuned checkpoint, Najdi + Hijazi test). The second number in brackets is the lookahead, in 80 ms frames [1][2].

| Setting | WER | CER |
|---|---|---|
| Greedy `[56,3]` (320 ms) | 29.96% | 12.18% |
| Greedy `[56,13]` (1.12 s) | 28.65% | 11.39% |
| MALSD beam-4 `[56,3]` | 28.81% | 11.48% |
| MALSD beam-8 `[56,3]` | 28.62% | 11.40% |
| MALSD beam-8 `[56,13]` | **27.25%** | 10.63% |

**Earlier experiment in the same post (not comparable to the tables above):**
- It trained on all SADA dialects and tracked progress on SADA's **validation** split, not the test split.
- The base model scored 49.5% validation WER. The best result reached 46.7% [1].

### Checking the owner's note line by line

| Part of the note | Verdict |
|---|---|
| "NVIDIA Nemotron 3.5 ASR" | **Correct** [1][2]. The full id is `nemotron-3.5-asr-streaming-0.6b`, a 0.6B streaming model. The blog title says only "NVIDIA Nemotron". |
| "fine-tuned on SDAIA's SADA" | **Correct** [1]. Only the Najdi + Hijazi part was used (133.7 h), mixed with 10% FLEURS. |
| "55% → 30%" | **Correct, as WER** [1]: 55.05% → 29.96%. Conditions: greedy decoding, 320 ms setting, no language model, Najdi + Hijazi test subset. |
| "on Najdi/Hijazi" | **Correct**, but it is one combined subset. No separate Najdi or Hijazi number exists [1]. |
| "NVIDIA × SDAIA" | **Not supported as a joint project.** NVIDIA did the work. SDAIA and SBA published the dataset [1][3][4]. |

## SADA splits and format

| Item | Value | Source |
|---|---|---|
| Name / publisher | SADA (صدى), "Saudi Audio Dataset for Arabic". Published by SDAIA's National Center for AI (NCAI) together with the Saudi Broadcasting Authority. | [5][6] confirmed |
| Size | About 667 h of audio from 57+ SBA TV shows, mostly Saudi dialects. Kaggle download is 77.06 GB, version 23, last updated 31 Aug 2023. | [6] confirmed |
| Splits | Train about 418 h, validation about 10 h, test about 10 h. Kaggle says "20 hours for development and testing". | [5][6] confirmed |
| Test split hours per paper | Gerazov et al. count 10.74 h of test: 3.73 h clean, 3.17 h music, 3.84 h noisy. Split totals add up to 437.5 h, not 667 h. | [13] confirmed |
| Test split as the leaderboard uses it | **6,189 utterances, 10.75 h**, clip lengths 0.5–34.81 s. 149 clips are longer than 30 s. 142 references contain the "unclear" tag (`غير واضح` / `غيرواضح`). | I counted [9]; the 142 matches issue #23 [10] |
| Speakers | Not stated. Speaker IDs are only unique within each file. About 45% of segments are labelled "more than one speaker". | [5] confirmed |
| Dialect labels | Najdi, Hijazi, Janubi, Shamali, Khaliji, ModernStandardArabic, Levantine, Egyptian, Iraqi, Yemeni, Maghrebi, More than 1 speaker, Unknown, Notapplicable. | [5] confirmed |
| Test split by dialect | More than one speaker 44.69%, Najdi 19.27%, Hijazi 10.42%, Khaliji 10.51%, Other 15.11%. DataPort does not say whether these are shares of segments or of hours. | [5] confirmed |
| Audio | 4,563 long WAV files (about 10 min each), mono, 16 kHz, 16-bit PCM. Segments are cut out using `SegmentStart` / `SegmentEnd` (in seconds). | [5] confirmed |
| Transcripts | UTF-8 `train.csv`, `valid.csv`, `test.csv`. Columns: FileName, ShowName, FullFileLength, SegmentID, SegmentLength, SegmentStart, SegmentEnd, SpeakerAge, SpeakerGender, SpeakerDialect, Environment, Speaker, **GroundTruthText**, **ProcessedText**, Category. | [5] confirmed |
| `ProcessedText` | A cleaned version of GroundTruthText: letter forms unified; punctuation, emojis, diacritics and special characters removed. Utterances that were empty or contained English words or digits were dropped. | [5] confirmed |
| Leaderboard test references | 0 contain Latin letters or digits. 0 contain أ/إ/آ. 2,624 contain ة and 1,321 contain ى. This looks like `ProcessedText`, which keeps ة and ى. | I counted [9]; the ProcessedText link is my inference [unverified] |
| Official scoring script | **None published by SDAIA** [5][6]. The closest thing to a standard is the leaderboard's `eval.py` [9]. | — |
| Licence | CC BY-NC-SA 4.0 (non-commercial). Details are in the licensing note. | [5][6] confirmed |

## Other published results

**How to read this table:**
- All numbers are % on Arabic speech. ZS = zero-shot (the model was not trained on SADA). FT = fine-tuned on SADA.
- **"LB norm"** means the leaderboard's `eval.py` [9]: removes punctuation and diacritics; أ/إ/آ→ا, ؤ→و, ئ→ي; deletes ء; پ→ب, ڤ→ف; Eastern→Western digits; joins a stand-alone و to the next word. **It does not map ة→ه or ى→ي.**
- "LB" = Open Universal Arabic ASR Leaderboard. Its SADA test set is 6,189 utterances / 10.75 h [8][9].
- The leaderboard does not say which prompt or decoding it used for Gemma or Nemotron. Their inference scripts are not in its repository [9].

**Gemma models**

| Model | Dataset / split | Metric | Number | Normalization | Source |
|---|---|---|---|---|---|
| Gemma 4 E4B-it (ZS) | SADA test (LB) | WER / CER | **43.40 / 20.96** | LB norm | [8] confirmed |
| Gemma 4 E2B-it (ZS) | SADA test (LB) | WER / CER | **46.23 / 23.47** | LB norm | [8] confirmed |
| Gemma 4 E4B-it / E2B-it | Common Voice 18.0 ar test (LB) | WER | 19.65 / 23.76 | LB norm | [8] confirmed |
| Gemma 4 E4B-it / E2B-it | MGB-2 test (LB) | WER | 17.72 / 20.72 | LB norm | [8] confirmed |
| Gemma 4 E4B-it / E2B-it | Casablanca (8 dialects, LB) | WER | 58.63 / 60.87 | LB norm | [8] confirmed |
| Gemma 4 E4B-it / E2B-it | Average over all 6 LB test sets | WER | 32.98 / 35.87 | LB norm | [8] confirmed |
| Gemma 4 E2B / E4B | FLEURS ar | WER | 14.3 / 16.2 | Not stated | [11] confirmed (Table 7) |
| Gemma 3n E2B / E4B | FLEURS ar | WER | 13.1 / 10.1 | Not stated | [11] confirmed (Table 7) |
| Gemma 3n (any) | SADA | — | Not found | — | — |

**NVIDIA models**

| Model | Dataset / split | Metric | Number | Normalization | Source |
|---|---|---|---|---|---|
| Nemotron 3.5 ASR 0.6B base (ZS) | SADA test (LB) | WER / CER | 53.06 / 29.87 | LB norm | [8] confirmed |
| Nemotron 3.5 ASR 0.6B base | FLEURS ar, 320 ms, auto-detect / language-ID prompt | WER | 12.67 / 12.55 | Model card's own normalizer, details not given | [2] confirmed |
| NVIDIA conformer-ctc-large-ar (ZS) | SADA test (LB) | WER / CER | 47.26 / 22.54 greedy; 44.52 / 23.76 with 4-gram LM | LB norm | [7][8] confirmed |

**Whisper, Meta and other open models**

| Model | Dataset / split | Metric | Number | Normalization | Source |
|---|---|---|---|---|---|
| Whisper large-v3 (ZS) | SADA test (LB) | WER / CER | 55.96 / 34.62 | LB norm | [7][8] confirmed |
| Whisper large-v3-turbo (ZS) | SADA test (LB) | WER / CER | 60.36 / 37.67 | LB norm | [7][8] confirmed |
| Whisper large-v2 (ZS) | SADA test (LB) | WER / CER | 57.46 / 36.59 | LB norm | [7][8] confirmed |
| SeamlessM4T v2 large (ZS) | SADA test (LB) | WER / CER | 62.52 / 37.61 | LB norm | [7][8] confirmed |
| MMS-1b-all (ZS) | SADA test (LB) | WER / CER | 77.48 / 37.50 | LB norm | [7][8] confirmed |
| Qwen3-ASR-1.7B (ZS) | SADA test (LB) | WER / CER | 45.53 / 19.90 | LB norm | [8] confirmed |
| omniASR_LLM_7B (ZS) | SADA test (LB) | WER / CER | 41.61 / 24.95 | LB norm | [8] confirmed |
| OmniASR, version not named | 103 SADA clips, human evaluation | Mean WER | 42.2 | Not stated | [15] confirmed (abstract) |
| MMS 1B (FT) + 4-gram LM | SADA test, **clean subset only** (3.73 h) | WER / CER | 40.86 / 17.60 | Not stated | [13] confirmed |
| Whisper medium (ZS) | SADA clean test | WER | 116.69 | Not stated | [13] confirmed |
| Whisper large-v3, Arabic or Saudi fine-tunes | SADA | — | No published SADA number found. `Bruno7/ksa-whisper-model` has no WER. | — | — |

**Commercial and newer Arabic models**

| Model | Dataset / split | Metric | Number | Normalization | Source |
|---|---|---|---|---|---|
| cohere-transcribe-arabic-07-2026 | SADA test (LB) | WER / CER | 37.47 / 23.53 | LB norm | [8] confirmed |
| Audar-ASR-V1-Turbo (2.35B, Qwen3-ASR based) | SADA test (LB) | WER / CER | **28.92 / 13.40** (best on LB) | LB norm | [8][17] confirmed. Whether SADA train was in its training data is not stated [17]. |
| CNTXT Conformer-large (121M, about 15k h of weakly labelled data) | SADA test | WER / CER | 27.71 / 11.65 | "Followed LB settings" | [14] confirmed. Weights not stated. |
| ElevenLabs Scribe / Azure STT / GPT-4o-transcribe | SADA test | WER | 49.44 / 58.5 / 66.47 | "LB settings" | [14] confirmed |

**Searched, nothing found:**
- MGB-3 is Egyptian and MGB-5 is Moroccan, so neither has Saudi results.
- ArTST: no SADA number (it was requested on the leaderboard as issue #2 and not added) [10].
- No published Saudi or SADA WER was found for Fanar, Jais, ALLaM or HUMAIN speech systems.

## Where sources disagree / unverified

1. **CER numbers mis-assigned in the news.** GCC Business News [3] and the Saudi Press Agency story in Arab News [4] give "CER 31.6% → 12.2%" for the broader multi-dialect set. The primary post [1] gives those CER figures for the **Najdi + Hijazi** subset. Full-test CER is 35.40% → 15.97%. Use [1].
2. **The base Nemotron 3.5 on the full SADA test scores differently in two places.** NVIDIA [1] gives 58.84% WER. The leaderboard [8] gives 53.06%. The likely causes are a different normalizer, a different latency setting, or a different test filter. **Unverified:** neither source publishes its full scoring setup for this model.
3. **SADA's size depends on the source.** Kaggle and DataPort say 667 h [5][6]. Gerazov et al. say 668 h, but their split tables add up to 437.5 h [13]. DataPort says 418 + 10 + 10 h [5]. The rest is presumably unsegmented or unlabelled audio [unverified].
4. **Gemma 4 FLEURS averages.** The model card [12] shows 0.08 (E4B) / 0.09 (E2B). The technical report [11] shows 0.075 / 0.090. This is consistent with rounding.
5. **Gemma 4 Arabic on FLEURS is worse than Gemma 3n** [11]. E4B scores 16.2 against 3n E4B's 10.1. Gemma 4 E4B is also worse than Gemma 4 E2B on FLEURS ar, yet better on SADA [8]. These are confirmed as printed. The report gives no explanation.
6. **Leaderboard SADA numbers may be stale relative to its own current scorer.**
   - Gemma 4 was added on 21 Apr 2026 [8]. The scorer changed on 27 Jul 2026: a "fix punctuation regex" commit and the و-joining rule [9][10].
   - Issue #23 (11 Aug 2026, still open) says the SADA numbers were computed without removing the 142 "unclear"-tagged references [10].
   - Issue #22 shows that the scorer's punctuation handling alone moved one model's SADA WER from 41.76 to 37.74 [10].
   - It is not stated whether the Gemma 4 rows were re-scored [unverified].
   - In favour of the leaderboard: a third party (Audar) reported reproducing several of its rows within 0.13 percentage points of average WER [10].
7. **Table error in the CNTXT paper.** Its "Whisper Small" SADA row (78.02 / 33.17) [14] matches the leaderboard's `w2v-bert-2.0` row, not Whisper-small's 87.34 / 56.75 [8]. Prefer [8].
8. **Blog date.** The page shows 30 Sep 2026 [1]; aggregators say 1 Oct 2026 [reported].

## Fair-comparison recipe

**Goal:** measure Gemma 4 E2B/E4B on Saudi speech in a way that can sit next to (a) the leaderboard numbers and (b) NVIDIA's 55.05 → 29.96.

The fine-tuned NVIDIA model is **not public**. The only way to line up with (b) is to rebuild NVIDIA's test subset and normalization, then check that rebuild by re-running the **public base** Nemotron 3.5 and getting close to 55.05.

1. **Fix the test data.** Use only SADA `test.csv`, never train or validation, cut with `SegmentStart` / `SegmentEnd`. Get the audio through the official Kaggle release [6]. The licence is CC BY-NC-SA, as covered in the licensing note.
   - *Done when:* you have a manifest of the full test split that matches the leaderboard's `datasets/sada_test.json`: same 6,189 IDs and 10.75 h [9].
2. **Build the Najdi + Hijazi subset.** Filter the test rows on `SpeakerDialect ∈ {Najdi, Hijazi}`. This is NVIDIA's training filter [1]; their test filter is not published.
   - *Done when:* the subset manifest is saved and its utterance count and hours are written down.
3. **Decide and record exclusions, then score both ways.** Two choices to make:
   - The 142 "unclear"-tagged references [10]: report results with them and without them.
   - The 149 clips longer than 30 s: Gemma 4 accepts at most 30 s of audio [12]. Either chunk them or drop them, and report how many were affected.
   - *Done when:* every result row states the number of utterances scored.
4. **Implement two normalizers and apply each one identically to references and outputs.**
   - **LB-norm:** copy `normalize_arabic_text` from `eval.py` at a pinned commit [9].
   - **NVIDIA-norm:** remove diacritics and punctuation; أ/إ/آ/ٱ→ا; ى→ي; ة→ه [1].
   - In both: remove any language tags.
   - The references contain **no digits** [9], but Gemma 4's recommended ASR prompt asks for digits [12]. Either prompt Gemma to write numbers as words, or convert digits to Arabic words before scoring, and report which you did.
   - *Done when:* a small test file shows both normalizers producing the expected output on hand-made examples (diacritics, ة, ى, hamza forms, a stand-alone و, a digit).
5. **Use the same metric.** Corpus-level WER and CER (total edits ÷ total reference words or characters), as NeMo's `word_error_rate` computes it [9]. Do not average per-utterance WER.
   - *Done when:* your scorer reproduces NeMo's result on a toy example.
6. **Calibrate before measuring Gemma.**
   - Run base `nemotron-3.5-asr-streaming-0.6b` [2] with greedy decoding, `att_context_size [56,3]`, target language `ar-AR`, and `strip_lang_tags=True` [1].
   - Score it on (a) the full test with LB-norm, against 53.06 [8], and (b) the Najdi + Hijazi subset with NVIDIA-norm, against 55.05 [1].
   - Optionally also run Whisper large-v3 against its 55.96 [8].
   - Set your tolerance before you look at the results.
   - *Done when:* both calibration numbers are within your tolerance. If not, the subset or normalizer differs, and the comparison to NVIDIA must be labelled "approximate".
7. **Run Gemma 4 E2B/E4B.** Use one fixed prompt, greedy decoding (no sampling) and the same audio sample rate. Save the raw outputs.
   - *Done when:* each model has WER and CER on both test sets and both normalizers, with the raw outputs kept for re-scoring.
8. **Report like-for-like only.**
   - Zero-shot Gemma compares with NVIDIA's **pretrained** 55.05 / 58.84 and with the leaderboard rows.
   - Only a Gemma that was fine-tuned on SADA *train* is fairly compared with the **fine-tuned** 29.96 / 35.61.
   - For streaming versus offline: NVIDIA's headline numbers are 320 ms streaming, while Gemma processes whole clips, so say so.
   - *Done when:* the results table has these columns: model, ZS/FT, test set, number of utterances, hours, normalizer, decoding/prompt, WER, CER, source.

## Open questions

- What exactly is NVIDIA's "Najdi + Hijazi test" filter (column, values, curation applied or not), and how many utterances and hours does it have? Not published [1].
- Did NVIDIA apply `normalize_arabic` to references and outputs at scoring time? Not stated [1].
- Did NVIDIA's training pool (125,490 → 103,559 utterances) come only from SADA train? The post does not say explicitly [1].
- How did the leaderboard prompt Gemma 4 and the base Nemotron 3.5, and how did it handle clips over 30 s? Scripts not published [9].
- Were the leaderboard's SADA numbers re-scored after the 27 Jul 2026 normalizer change? Unknown [9][10].
- There are no separate per-dialect WERs (Najdi alone, Hijazi alone) for any model on SADA. Issue #16 asks for this and it is still open [10].
- Gemma 3n on SADA: no published number found.

## Sources

1. NVIDIA Technical Blog, Khaouja, El Khair, Alaeena, Al-Kaf, Alkhamees, "Fine-Tuning NVIDIA Nemotron for Saudi Arabic Dialects, with a Path to Other Languages", 30 Sep 2026. https://developer.nvidia.com/blog/fine-tuning-nvidia-nemotron-for-saudi-arabic-dialects-with-a-path-to-other-languages/ (accessed 2026-10-13)
2. Hugging Face model card, `nvidia/nemotron-3.5-asr-streaming-0.6b`, released 04 Jun 2026, OpenMDW-1.1. https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b (accessed 2026-10-13)
3. GCC Business News, "NVIDIA fine-tunes Nemotron 3.5 ASR with Saudi SADA Dataset", 3 Oct 2026. https://www.gccbusinessnews.com/nvidia-fine-tunes-nemotron-3-5-asr-sada/
4. Arab News (Saudi Press Agency), "Saudi dataset cuts AI errors in Arabic dialects", 3 Oct 2026. https://www.arabnews.pk/saudi-arabia/saudi-dataset-cuts-ai-errors-in-arabic-dialects-3003083
5. IEEE DataPort, "SADA Dataset", DOI 10.21227/revt-pa41, 8 Feb 2025. https://ieee-dataport.org/node/14747
6. Kaggle, `sdaiancai/sada2022` "SADA صدى" (NCAI_SDAIA), version 23, 31 Aug 2023. Metadata read via the Kaggle public API. https://www.kaggle.com/datasets/sdaiancai/sada2022
7. Wang, Alhmoud, Alqurishi, "Open Universal Arabic ASR Leaderboard", arXiv:2412.13788, 18 Dec 2024. https://arxiv.org/abs/2412.13788
8. Open Universal Arabic ASR Leaderboard, Hugging Face Space `app.py` results table. Latest update entry 20 Aug 2026; fetched 2026-10-13. https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard
9. Leaderboard GitHub repository: `eval.py` (commits of 27 Jul 2026) and `datasets/sada_test.json`. https://github.com/Natural-Language-Processing-Elm/open_universal_arabic_asr_leaderboard (accessed 2026-10-13)
10. Leaderboard GitHub issues:
    - #2 (ArTST request)
    - #7 (clip durations, Oct 2025)
    - #15 (Gemma 4 added, 21 Apr 2026)
    - #16 (per-dialect columns)
    - #20 (unclear tags and و, 7 Jul 2026)
    - #21 (Audar reproduction, 20 Jul 2026)
    - #22 (normalizer mismatch, 27 Jul 2026)
    - #23 (skip 142 unclear references, 11 Aug 2026)

    https://github.com/Natural-Language-Processing-Elm/open_universal_arabic_asr_leaderboard/issues
11. Gemma Team, "Gemma 4 Technical Report", arXiv:2607.02770v2, 24 Jul 2026, Table 7 and Table 8. https://arxiv.org/abs/2607.02770
12. Hugging Face model card, `google/gemma-4-E4B-it`, including the audio limit and ASR prompt template (accessed 2026-10-13). https://huggingface.co/google/gemma-4-E4B-it
13. Gerazov, Politi, Bratières, "Arabic ASR on the SADA Large-Scale Arabic Speech Corpus with Transformer-Based Models", arXiv:2508.12968, 18 Aug 2025. https://arxiv.org/abs/2508.12968
14. Salhab et al. (CNTXT AI), "Advancing Arabic Speech Recognition Through Large-Scale Weakly Supervised Learning", arXiv:2504.12254, Apr 2025. https://arxiv.org/abs/2504.12254
15. Al-Khalifa, "When Does OmniASR Fail? A Fine-Grained Human Evaluation on Saudi Arabic Dialects", SPEAKABLE workshop at LREC 2026, May 2026. https://aclanthology.org/2026.speakable-1.13/
16. Code linked from [1]:
    - https://github.com/nvidia-riva/tutorials/blob/main/asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb (uses AN4, not SADA)
    - https://github.com/NVIDIA/skills/tree/main/skills/nemotron-asr-finetune (Apache-2.0)

    Both accessed 2026-10-13.
17. Hugging Face model card, `audarai/Audar-ASR-V1-Turbo` (2026). https://huggingface.co/audarai/Audar-ASR-V1-Turbo (accessed 2026-10-13)
