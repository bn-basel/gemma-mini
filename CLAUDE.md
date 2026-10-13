# Code rules: the Offline Saudi Companion (gemma-mini)

<!-- This file lives in the code repo. Helpers read it before every task. Keep it short and factual. -->

## Sources of truth

- **The plan:** `PLAN.md` (Steps 0–10, each with a "done when"). **Decisions:** `docs/DECISIONS.md`.
- **Architecture:** `docs/ARCHITECTURE.md`, if it exists. Writing it is a good first wide feature.
- **Outside facts** (Gemma 4, LiteRT-LM, llama.cpp, SADA, licences, hardware): `docs/research/`, each claim with its
  source. Never invent an API, a model feature, a benchmark number or a licence term. If a detail isn't documented,
  say so instead of guessing.
- **Test set:** `eval/`. Once frozen (project Step 2), it has a checksum and never changes in place.

## Fixed rules

- The stack is fixed: Python 3.13 + pytest on the PC (`core/`, `eval/`); Swift + LiteRT-LM on the iPhone (`apps/ios/`).
  Never add frameworks, libraries, services or packages without BN's approval.
- **Model weights and datasets never go in git** (`.gitignore` blocks `*.litertlm`, `*.gguf`, `*.safetensors`). Never
  download them without BN's yes; name the file, source and size.
- **No GPU jobs or long CPU jobs** (training, quantization, model runs) without BN's yes.
- Secrets come only from environment variables or the tools' own login. Never read the Hugging Face token
  (`~/.cache/huggingface`). Never upload anything.
- User-facing Arabic text (fixed safe answers, prompts, refusals) lives in files under `core/` (one place to review it),
  never inline in logic. Files are UTF-8.
- `core/` and `eval/` stay device-independent: nothing in them may depend on iOS or on one device's runtime.

## Product rules (don't break these)

- **Prayer times and Qibla come from the on-device calculator**, never from the model.
- **Religious questions are answered only by quoting trusted sources, with the reference.** The model never issues a
  ruling of its own.
- **"Is it safe to eat / drink / touch?" always gets the fixed safe answer**, whatever the photo or the model says.
- **Survival answers come from the offline knowledge pack**, quoted, with the source.
- **Replies are in Saudi dialect**; fixed safety answers may be in clear Arabic.
- **Data licences hold:** research-only data (e.g. SADA, CC BY-NC-SA) never goes into a public release, a public repo, or
  weights we publish, without BN's explicit decision. Record each source's licence where it is used.
- **No claim without a number:** results state the test set, its size, the metric and the setup.

## Tests

- Behaviour-defining work gets **tests first**.
- **New tests must fail on `origin/main`.** The orchestrator checks this. Helpers report the names of the tests they added.
- **Mutation walls** for wide and closed work: break the guard on purpose, and the test that protects it must go red.
  The safety rules above each get a test that fails if the guard is removed.
- **Nothing is done until a real path uses it.** A test calling it isn't enough.
- **Two lists that must agree**, where only one fails loudly: add a test that compares them.
- **Scoring:** corpus-level WER/CER (total edits ÷ total reference words or characters), the same normalizer on both
  sides, every result row states how many utterances it scored (`docs/research/05-saudi-speech-baseline.md`).
- **Swift code** can't be built on the PC. It is checked by a code review against the official docs, then by BN's run on
  the iPhone.

**Commands** (from `_worktrees/build`):

- **One test file:** `.venv/Scripts/python -m pytest <test file>`. Run targeted tests per task.
- **Full suite:** `.venv/Scripts/python -m pytest`. Once, before the PR.
- **Type check / lint:** none yet (adding one is a new package: BN's call).

**Known flaky tests.** If only these fail, re-run them once and mention it in your report. **Don't "fix" them** unless the task says so.

- none known
