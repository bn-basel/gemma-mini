# Q6. Data and licenses

Research date: 2026-10-13. Desk research only. Nothing was downloaded, cloned or run.
This is not legal advice. It describes what each license or terms page says and flags where a lawyer or the rights holder should confirm.

**How claims are marked**
- **(C) confirmed**: read on the rights holder's own page, or on the official dataset or model page (Kaggle, Hugging Face card or API, Zenodo, GitHub LICENSE).
- **(R) reported**: seen only in a secondary source or a search-engine snippet. The page itself could not be opened.
- **(U) unverified / not found**: no license or terms located.

**License terms in one line each**
- **BY** (Attribution): credit the author, link the license, and say what you changed.
- **NC** (NonCommercial): no use mainly aimed at commercial gain or payment.
- **SA** (ShareAlike): if you share an adaptation, it must carry the same license.
- **ND** (NoDerivatives): you may share only unchanged copies.
- **CC0**: the author waives rights, so the work can be used for anything.

---

## Question

1. What is SADA's license, confirmed on Kaggle and IEEE DataPort, including any extra terms? What does it allow for evaluation, training, publishing fine-tuned weights (with the ShareAlike question) and commercial use?
2. For each test area (plants, food/wood, survival, Islamic references, Nabati poetry, Saudi-dialect text, Arabic TTS): which sources exist, what do they contain, what are their licenses, and can each be used for research only or also for a public release?
3. A summary table and three lists: safe for public release, research only, avoid.

## Short answer

- **SADA is CC BY-NC-SA 4.0.** This is confirmed on SDAIA's own Kaggle dataset (owner `NCAI_SDAIA`, last updated 2023-08-31) and matches the IEEE DataPort entry. Neither page adds terms beyond the license. SADA is fine for private evaluation, training and the portfolio. It is not usable for a commercial product. Publishing weights trained on it is a grey area: if the weights count as an adaptation, ShareAlike would require them to be released under BY-NC-SA (or a compatible license).
- **Public-release friendly sources:**
  - iNaturalist and GBIF photos filtered to CC0 or CC BY.
  - Wikimedia Commons.
  - Tanzil Quran text (verbatim only).
  - The adhan libraries (MIT).
  - US Army ATP 3-50.21 (a US government work).
  - Common Voice Arabic (CC0).
  - Piper and ArTST code and weights (MIT), with their training data checked separately.
- **Research only:**
  - SADA, WHO guidance, MADAR, SaudiBERT, MMS-TTS, XTTS-v2, Food-101.
  - The Pl@ntNet API.
  - IslamQA and most fatwa or Saudi government websites.
- **Gaps:**
  - No open dataset fits food doneness or Saudi firewood.
  - No Nabati-specific dataset and no open Saudi-dialect TTS corpus were found.
  - Fatwa sites (alifta.gov.sa, Islamway) have no readable terms.
  - Saudi Arabia's new 2026 Copyright Law has an AI-training exception whose rules are not yet published.

---

## SADA license

| Item | Kaggle (SDAIA's own account) | IEEE DataPort |
|---|---|---|
| Page | [kaggle.com/datasets/sdaiancai/sada2022](https://www.kaggle.com/datasets/sdaiancai/sada2022). The page loads by JavaScript, so it was read through [Kaggle's public API for the same dataset](https://www.kaggle.com/api/v1/datasets/view/sdaiancai/sada2022). | [ieee-dataport.org/node/14747](https://ieee-dataport.org/node/14747) |
| Publisher | Owner `NCAI_SDAIA`: the National Center for AI at SDAIA, with the Saudi Broadcasting Authority (SBA). **(C)** | Uploaded by an individual account, "Raghad Almutairi", with [no affiliation shown](https://ieee-dataport.org/user/1317217). It credits SBA and SDAIA. **(C)** |
| License | `CC BY-NC-SA 4.0` in the license field. **(C)** | The page says the work is licensed CC BY-NC-SA 4.0. **(C)** |
| Extra terms | None in the description. Kaggle needs a (free) account to download. **(C)** | Access needs an IEEE DataPort subscription. The page also says files have not been uploaded. **(C)** |
| Attribution | The description has no citation. | Cite "SADA - SBA & SDAIA Audio Dataset for Arabic" (2023), or the DataPort DOI 10.21227/revt-pa41 (2025-02-08). **(C)** |
| Size | About 77 GB (77,055,385,134 bytes). About 667 h of audio, mostly Saudi dialects, from more than 57 SBA TV programmes. 20 h are held out for dev and test. **(C)** | About 667 h: 418 h train plus about 10 h validation and about 10 h test. 4,563 wav files, 16 kHz mono. **(C)** |
| Stated uses | ASR, TTS, speaker diarization, and dialect, gender or age identification. **(C)** | Not stated. |

**The two sources do not disagree on the license.** They differ on the split: 418 h of training data on DataPort versus "most of the 667 h" on Kaggle. Kaggle is the rights holder's own channel, so treat it as authoritative. The [community HF card for the MSA subset](https://huggingface.co/datasets/badrex/arabic-speech-SADA22-MSA/blob/main/README.md) also states CC BY-NC-SA 4.0 and points to the same Kaggle page **(C, for that card)**.

**What CC BY-NC-SA 4.0 allows**, per the [license legal code](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en) **(C)**. This describes the text, not a legal opinion.

| Use | What the text says | Our reading |
|---|---|---|
| Private evaluation (WER tests) | Non-commercial reproduction and use is allowed. | Allowed. |
| Fine-tuning for research or portfolio | Allowed if NC, with attribution. | Allowed. |
| Publishing a WER table or write-up citing SADA | No adaptation is shared. Attribution applies. | Allowed. |
| Re-uploading SADA audio or transcripts (e.g. a cleaned subset on HF) | Allowed only under BY-NC-SA, with attribution. No extra restrictions may be added (Section 3(b)(3)). | Possible, but must stay BY-NC-SA. |
| Publishing fine-tuned weights on HF | The license defines "Adapted Material" as material derived from the work in a way that needs copyright permission. If weights count as that, Section 3(b) requires sharing them under BY-NC-SA or a compatible license. Creative Commons' own [AI-training guidance](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/) **(C)** does not say whether a model is Adapted Material. It says the license applies only where copyright permission is needed, which varies by country. It calls following SA for models the conservative approach. | **Grey area. Lawyer or SDAIA to confirm.** The conservative option is to release SADA-trained weights as CC BY-NC-SA 4.0 and say so. That clashes with any base-model license that allows commercial use, so check compatibility. |
| Commercial product | NC means no use mainly aimed at commercial gain or payment. | **Not allowed** without separate permission from SDAIA/SBA. |
| Database rights (Section 4) | Extracting a substantial part is allowed for NC only. A database built from it becomes Adapted Material. | Same NC/SA limits apply. |

Further notes:
- NVIDIA is reported to have fine-tuned a commercially licensed ASR model on SADA ([Origami, secondary](https://origami.sa/en/blog/saudi-dialect-call-transcription/) **(R)**). Whether NVIDIA had a separate agreement is **not found**. Do not treat it as a precedent.
- The audio is broadcast TV with identifiable speakers. Saudi personal-data rules may also apply to redistribution. **(U, ask a lawyer)**

---

## Sources by area

### 1. Plant photos from Saudi Arabia

| Source | Link | Contents / size | License (from source) | Verdict |
|---|---|---|---|---|
| iNaturalist (API) | [api.inaturalist.org](https://api.inaturalist.org/v1/observations?place_id=7358&iconic_taxa=Plantae&photo_license=cc0,cc-by&quality_grade=research&per_page=1) | Saudi Arabia is `place_id=7358` ([place lookup](https://api.inaturalist.org/v1/places/autocomplete?q=Saudi%20Arabia) **(C)**). There are 3,879 research-grade plant observations in total ([query](https://api.inaturalist.org/v1/observations?place_id=7358&iconic_taxa=Plantae&quality_grade=research&per_page=1)), and 836 of them have CC0 or CC BY photos (queried 2026-10-13) **(C)**. | Set per item. The default is CC BY-NC. Users can choose CC BY, CC0 or all rights reserved ([iNat help](https://help.inaturalist.org/en/support/solutions/articles/151000173511), modified 2025-11-20) **(C)**. Filter with `photo_license=cc0,cc-by`. | **CC0/CC BY photos: public release OK** with credit. CC BY-NC photos: research only. |
| iNaturalist Open Data (AWS) | [github.com/inaturalist/inaturalist-open-data](https://github.com/inaturalist/inaturalist-open-data) | More than 400 M photos in total. Monthly metadata tables (observations, photos, taxa). Photos up to 2048 px. | CC0 and other CC licenses. Each photo's license is in the photos table and must be honoured, with the credit format given **(C)**. The repo does not document place filtering, so join on observation coordinates. | Same split as above. Use the metadata tables, not bulk images, until needed. |
| GBIF | [GBIF iNat research-grade dataset](https://api.gbif.org/v1/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) | GBIF finds 29,379 Saudi plant records with images: 15,329 CC BY, 11,309 CC0, 2,741 CC BY-NC ([facet query](https://api.gbif.org/v1/occurrence/search?country=SA&kingdomKey=6&mediaType=StillImage&limit=0&facet=license), 2026-10-13) **(C)**. | GBIF allows CC0, CC BY and CC BY-NC per dataset ([gbif.org/terms](https://www.gbif.org/terms); page returned 403, read via search snippet) **(R)**. The iNat dataset on GBIF is CC BY-NC 4.0 at dataset level **(C)**, but each record carries its own license. **Image licenses can differ from record licenses: check the multimedia license field** (U). | CC0/CC BY records: public release OK, with a GBIF download DOI citation. Otherwise research only. |
| Pl@ntNet-300K | [zenodo.org/records/5645731](https://zenodo.org/records/5645731) | 31.7 GB, about 300 K images, mainly European flora. | The Zenodo record says CC BY 4.0 **(C)**. A later v2 lists per-image CC BY-SA, CC BY-NC or CC BY-NC-SA (search snippet) **(R)**. | Possibly public release under CC BY, but per-image licenses are unclear and it has little Saudi flora. **Unclear.** |
| Pl@ntNet API | [my.plantnet.org/terms_of_use](https://my.plantnet.org/terms_of_use) | Online identification API. | Free up to 500 requests a day. Commercial use needs a contract. Images are "usually CC BY-SA" with credit (search snippets; the site refused connection) **(R)**. | **Research only** for labelling help. It does not fit an offline app. |
| Wikimedia Commons | [Commons:Licensing](https://commons.wikimedia.org/wiki/Commons:Licensing) | Mixed photos. Each file has its own license. | Only free licenses (CC BY, CC BY-SA, CC0, public domain). NC-only and ND files are not accepted **(C)**. | **Public release OK** with per-file credit. Note SA on CC BY-SA files. |
| Regional poisonous-plant references | e.g. [Al-Kharj field study (Plant Science Today, 2022)](https://psau.sa.elsevierpure.com/en/publications/a-field-study-to-restricted-poisonous-wild-plants-grown-in-alkhar) | 16 toxic species, including *Calotropis procera* and *Rhazya stricta* (search snippet) **(R)**. | Journal license **not found**. | Use as a cited fact source for a hand-written list. Do not copy the text. **Unclear.** |

### 2. Food doneness/safety photos and wood/fuel photos

| Source | Link | Contents / size | License | Verdict |
|---|---|---|---|---|
| Food-101 | [ETH page](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/), [HF card](https://huggingface.co/datasets/ethz/food101) | 101 dishes, 101 K images, about 5 GB. These are dish types, not doneness. | The ETH page states no license **(C)**. The HF card says "unknown". Images are from Foodspotting and not owned by ETH. Uses beyond scientific fair use must be negotiated with each photo owner **(C)**. | **Research only.** It also does not fit the task. |
| Roboflow "Cooking Classification and detection" | [universe.roboflow.com/…/cooking-classification-and-detection](https://universe.roboflow.com/school-4kceq/cooking-classification-and-detection) | About 3,942 images labelled cooked, overcooked or undercooked (search snippet). | CC BY 4.0 (search snippet; the page returned 403) **(R)**. Image provenance is unknown. | **Unclear.** Check the image sources before use. |
| GOIMAI wood macro images | [Zenodo 11092208](https://zenodo.org/doi/10.5281/zenodo.11092208) | Macroscopic end-grain images of 37 protected timber species. | CC BY-SA 4.0 (search snippet) **(R)**. | Not a fit: not firewood, and not Saudi species. |
| Wood/fuel photos of Saudi species (samr/acacia, ghada, arta) | None found. | | | **No open dataset fits.** Build an own set: own photos, plus iNaturalist/GBIF CC0 or CC BY photos of those species. |

### 3. Survival guides

| Source | Link | Contents | License / status | Verdict |
|---|---|---|---|---|
| US Army ATP 3-50.21 *Survival* (2018) | [FAS mirror PDF](https://irp.fas.org/doddir/army/atp3-50-21.pdf) (official copy on armypubs.army.mil) | Survival medicine, water, fire, shelter, navigation, desert chapters. | Marked "Approved for public release; distribution is unlimited" (search snippet of the mirror) **(R)**. US federal works have no US copyright ([17 U.S.C. §105](https://www.copyright.gov/title17/92chap1.html)) **(C)**. | **Public release OK** in the US sense. Lawyer to confirm status outside the US. Check figures credited to third parties. |
| FM 21-76 (1992) / FM 3-05.70 (2002) | [FM 3-05.70 PDF](https://biotech.law.lsu.edu/blaw/DOD/fm3-05-70.pdf) | Older editions. FM 3-05.70 says it supersedes FM 21-76 **(R)**. | Same §105 status. | **Public release OK** (as above). Prefer the 2018 edition. |
| WHO guidance (heat-health, drinking-water) | [WHO copyright policy](https://www.who.int/about/policies/publishing/copyright), [GDWQ 4th ed. + addenda (2022)](https://www.who.int/publications/i/item/9789240045064), [Heat-health action plans](https://www.who.int/publications/i/item/heat-health-action-plans) | Heat illness and water treatment. | WHO's default is CC BY-NC-SA 3.0 IGO. Commercial use needs WHO permission. Adaptations and translations need a disclaimer that WHO did not make them **(C)**. GDWQ 2022 is CC BY-NC-SA 3.0 IGO **(C)**. Heat-health plans are the same (search snippet) **(R)**. | **Research only** for verbatim or adapted text. Facts can be restated in own words with a citation (lawyer to confirm). |
| Saudi Civil Defense (998.gov.sa), Saudi Red Crescent (srca.org.sa) | [998.gov.sa](https://998.gov.sa) | Awareness material. | **Not found.** Both sites refused connection and no terms page was found. Other Saudi government sites restrict copying, e.g. [SFDA terms](https://www.sfda.gov.sa/en/terms-of-use) (written consent needed) **(R)**. | **Unclear.** Assume all rights reserved. Ask the agencies. |
| Saudi MOH heat-stroke pages | [MOH Heat-Stress page](https://www.moh.gov.sa/en/HealthAwareness/Pilgrims-Health/Pages/Heat-Stress.aspx) | Arabic and English first-aid advice. | Terms page **not found** (404). | **Unclear.** Cite as a fact source only. |
| Arabic Wikipedia / Wikibooks | [Wikimedia Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use) | Arabic survival and first-aid articles. Quality varies. | CC BY-SA 4.0 and GFDL **(C)**. | **Public release OK** with credit. SA applies to adapted text. |

### 4. Trusted Islamic references

| Source | Link | Contents | License / terms | Verdict |
|---|---|---|---|---|
| Tanzil Quran text | [tanzil.net/docs/text_license](https://tanzil.net/docs/text_license) | Verified Uthmani and simple Arabic Quran text. | Labelled CC BY 3.0, **plus** conditions: verbatim copies only (no changes), credit Tanzil, link to tanzil.net, keep the notice **(C)**. The no-change condition is stricter than plain CC BY. | **Public release OK** when shipped verbatim with the notice. Lawyer to confirm whether training counts as "changing" the text. |
| Tanzil translations | [tanzil.net/trans](https://tanzil.net/trans/) | Many translations. | Non-commercial use only. Other uses need the translator's or publisher's permission **(C)**. | **Research only.** |
| sunnah.com | [sunnah.com/about](https://sunnah.com/about), [/developers](https://sunnah.com/developers) | Hadith with English translations. | The pages returned 403. The API needs a key and covers part of the data. An offline dump is "not available yet" (search snippets) **(R)**. The reproduction/scraping section **could not be read** (U). | **Unclear.** Ask the maintainers. |
| fawazahmed0/hadith-api | [github.com/fawazahmed0/hadith-api](https://github.com/fawazahmed0/hadith-api) | Many editions and languages, with grades. | The repo is the Unlicense **(C)**. Texts are compiled from other projects (see its References.md). The upstream rights to translations are not shown. | **Unclear.** The Arabic matn is likely fine. Translations need provenance checks. |
| Open-Hadith-Data | [repo](https://github.com/mhashim6/Open-Hadith-Data), [LICENSE](https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/LICENSE) | 9 books in Arabic, with and without tashkeel. | ODbL 1.0 (database) plus DbCL 1.0 (contents) **(C)**. ODbL is share-alike for databases. | **Public release OK** for the Arabic text. Derived databases must stay ODbL. |
| LK-Hadith-Corpus | [github.com/ShathaTm/LK-Hadith-Corpus](https://github.com/ShathaTm/LK-Hadith-Corpus) | 39,038 hadith from the six books, Arabic and English, with grades. | No license file found **(U)**. English translation source not stated. | **Research only** until clarified. |
| Sanadset 650K | [Mendeley Data](https://data.mendeley.com/datasets/5xth87zwb5/5) | 650,986 hadith records with narrator chains, from 926 books. | CC BY 4.0 **(C)**. | **Public release OK** with credit. |
| alifta.gov.sa (Permanent Committee) | [alifta.gov.sa](https://www.alifta.gov.sa) | Official Saudi fatwas. | Terms **not found**. The page only rendered a loading message. | **Unclear.** Quote short passages with a link. Ask before any bulk use. |
| IslamQA | [islamqa.info/en/terms](https://islamqa.info/en/terms) | Fatwa Q&A. | Personal, non-commercial use only. No redistribution or repurposing without consent. No commercial use **(C)**. No date (footer 1997-2025). | **Research only** for reading and evaluation prompts. **Avoid** for training data or bulk quoting. |
| Islamway | islamway.net | Lectures and fatwas. | Terms **not found** (U). Related site islamweb.net says its material is copyrighted and usable non-commercially with credit ([islamweb fatwa](https://www.islamweb.net/en/fatwa/379009/islwmweb-material-is-copyrighted)) **(R)**. | **Unclear.** |
| Tafsir texts (QUL / spa5k) | [QUL tafsir list](https://qul.tarteel.ai/resources/tafsir), [spa5k/tafsir_api](https://github.com/spa5k/tafsir_api) | Ibn Kathir, Tabari, Qurtubi, Muyassar, Sa'di and more, as JSON or SQLite. | QUL shows **no license** on the page (U). Its FAQ says resources come from external sources (snippet) **(R)**. spa5k's code is MIT, but it does not license the texts. One edition is CC BY-ND 4.0 **(C)**. Classical authors (Ibn Kathir, Tabari) are long dead. Modern editions and al-Muyassar (King Fahd Complex) may carry edition rights (U). | Classical tafsir likely OK, with edition rights unclear. **Lawyer or publisher to confirm.** |
| Prayer times: Umm al-Qura method + adhan libraries | [adhan-swift](https://github.com/batoulapps/adhan-swift), [adhan-java](https://github.com/batoulapps/adhan-java) | Computes prayer times and Qibla. Umm al-Qura uses Fajr at 18.5° and Isha 90 min after Maghrib; add 30 min in Ramadan **(C)**. | MIT **(C)**. | **Public release OK** (keep the MIT notice). |

### 5. Nabati poetry

| Source | Link | Contents / size | License | Verdict |
|---|---|---|---|---|
| Ashaar dataset | [HF card](https://huggingface.co/datasets/arbml/Ashaar_dataset), [HF API](https://huggingface.co/api/datasets/arbml/Ashaar_dataset), [paper](https://arxiv.org/abs/2307.06218) | About 212 K poems, mostly classical meters, scraped from aldiwan.net. Nabati content not confirmed. | **No license tag** in the card metadata (last modified 2024-07-21) **(C: absence)**. | **Research only.** |
| APCD | [source page](https://hci-lab.github.io/ArabicPoetry-1-Private/#PCD) | About 1.8 M verses, 3,701 poets, 12 eras (snippet). | **Not found** (U). | **Research only.** |
| Tarab corpus (2026) | [HF](https://huggingface.co/datasets/drelhaj/Tarab), [arXiv 2603.16601](https://arxiv.org/abs/2603.16601) | 2.56 M verses of lyrics and poetry. 308 K Gulf-labelled verses; 197 K verses of Saudi origin. 1.6 GB. | Card tag CC BY 4.0 **(C)**. However, the content is crawled song lyrics and poetry from websites. A CC BY tag from the compiler cannot grant rights to living lyricists' work. | **Research only.** Treat the CC BY tag as covering annotations only. Lawyer to confirm. |
| Dedicated Nabati dataset | None found. | | | Build an own set from dead poets' texts (see below), credited. |

**Copyright of classical versus living poets**
- The 2003 Saudi Copyright Law gave life plus 50 years. A new Copyright Law, Royal Decree M/169, took effect on 2026-08-12. It keeps the same term (Art. 22(1)) and adds "cultural heritage", defined as works passed down through generations. Art. 6 makes that heritage State property ([Commons summary](https://commons.wikimedia.org/wiki/Commons:Copyright_rules_by_territory/Saudi_Arabia)) **(R)**.
- The new law also adds an exception for copying works to develop AI, subject to conditions in an Implementing Regulation that SAIP has 180 days to issue ([Baker McKenzie, 2026-07-20](https://www.bakermckenzie.com/en/insight/publications/2026/07/saudi-arabia-new-copyright-law-modernises-ksa-ip-framework)) **(R)**.
- Official text: [WIPO Lex](https://www.wipo.int/wipolex/en/legislation/details/19412) (holds the earlier consolidated version).
- **Practical reading, for a lawyer to confirm:**
  - Poets who died more than 50 years ago are likely free to use.
  - Living or recently deceased poets are protected.
  - Anonymous oral Nabati heritage may fall under the new State-owned "cultural heritage" concept. That is a new, untested question.

### 6. Saudi-dialect conversation text

| Source | Link | Contents | License / terms | Verdict |
|---|---|---|---|---|
| SADA transcripts | see the SADA section | About 667 h of transcribed TV speech, mostly Saudi. | CC BY-NC-SA 4.0 **(C)**. | **Research only.** |
| MADAR | [CAMeL Lab page](https://camel.abudhabi.nyu.edu/madar-parallel-corpus/) | 2,000 sentences in 25 city dialects, including Riyadh and Jeddah, plus 12 K in 6 cities. | Internal research and evaluation only. No redistribution or modification. Commercial use via CMU **(C)**. | **Research only** (evaluation). Cannot be republished. |
| NADI shared tasks | [NADI 2024 paper](https://arxiv.org/abs/2407.04910), [NADI 2021](https://arxiv.org/abs/2103.08466) | Tweets labelled by country or dialect. | Data given to registered teams via private links (2021/22, per paper) **(R)**. 2024 terms **not found** (U). | **Research only.** |
| SaudiBERT (corpus not released) | [model card](https://huggingface.co/faisalq/SaudiBERT), [paper](https://arxiv.org/abs/2405.06239) | Model trained on 141 M Saudi tweets plus forum text. The corpora are not public. | Model: CC BY-NC 4.0 (HF API, 2024-05-23) **(C)**. | **Research only.** No usable text. |
| SauDial | [Mendeley Data](https://data.mendeley.com/datasets/mzdwkb2t6d) | English, MSA and 4 Saudi dialects. Expressions generated by GPT-4o, then refined. | License field empty (snippet) **(U)**. | **Unclear.** Synthetic, so weak as a dialect reference. |
| SADSLyC (Saudi song lyrics) | [ACL Anthology](https://aclanthology.org/2025.wacl-1.4) | 31 K lyric lines across 5 Saudi dialects. | **Not found** (U). Lyrics are copyrighted. | **Research only** at best. |
| Saudi-Dialect-ALLaM data | [arXiv 2508.13525](https://arxiv.org/abs/2508.13525) | 5,466 synthetic Najdi/Hijazi pairs. | Authors say private and not shared **(R)**. | **Neither.** |
| Twitter/X-derived sets | [X developer policy](https://docs.x.com/developer-terms/agreement-and-policy) | Any Saudi tweet corpus. | Only Post/User IDs may be redistributed, capped at 1.5 M IDs per 30 days **(C)**. Since June 2025 the Developer Agreement bars using X content to fine-tune or train foundation or frontier models ([TechCrunch](https://techcrunch.com/2025/06/05/x-changes-its-terms-to-bar-training-of-ai-models-using-its-content)) **(R)**. | **Avoid** for training and release. Evaluation only, using IDs. |
| Common Voice Arabic (speech, with transcripts) | [Mozilla Data Collective](https://datacollective.mozillafoundation.org/datasets/cmflnuzw47jng4x81tavetpul) | v23: about 158 h, 1,654 speakers. Optional accent field; no Saudi split. | CC0. Users must agree not to identify speakers (snippet) **(R)**. | **Public release OK.** It is MSA-heavy. |

### 7. Arabic text-to-speech voices

| Source | Link | Contents | License | Verdict |
|---|---|---|---|---|
| Piper `ar_JO-kareem` | [HF piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main/ar/ar_JO/kareem), [MODEL_CARD](https://huggingface.co/rhasspy/piper-voices/raw/main/ar/ar_JO/kareem/medium/MODEL_CARD) | Jordanian male voice, low and medium quality. 127 MB folder. | Repo MIT **(C)**. The model card points to the [training data repo](https://github.com/AliMokhammad/arabicttstrain), which has **no license** **(U)**. | **Unclear.** Training data rights are unknown. Not Saudi. |
| MMS-TTS `ara` | [facebook/mms-tts-ara](https://huggingface.co/facebook/mms-tts-ara) | 36 M parameters. Variety not stated. | CC BY-NC 4.0 **(C)**. | **Research only.** |
| XTTS-v2 | [HF card](https://huggingface.co/coqui/XTTS-v2), [LICENSE](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt) | Multilingual voice cloning, including Arabic. | Coqui Public Model License 1.0.0. Non-commercial only, and it covers outputs too. It excludes training other models for commercial use **(C)**. Coqui shut down in Jan 2024, so no commercial license can be bought **(R)**. | **Research only.** |
| ArTST (MBZUAI) | [HF commit showing license](https://huggingface.co/MBZUAI/ArTST/commit/4689f88d50819c33ba06e7c2ef0040494a7934a3) | SpeechT5-style Arabic ASR/TTS. The TTS checkpoint is trained on ClArTTS. | MIT (snippet of the card) **(R)**. | **Public release likely OK.** Confirm on the card. Classical Arabic, not Saudi. |
| ClArTTS | [HF API](https://huggingface.co/api/datasets/MBZUAI/ClArTTS), [paper](https://arxiv.org/abs/2303.00069) | 12 h, one male speaker, Classical Arabic from a LibriVox audiobook. | Card CC BY 4.0 (2025-10-01) **(C)**. The paper says "for research purposes" **(R)**. | **Disagreement.** The card is newer and more permissive. LibriVox recordings are generally public domain (U). |
| ArVoice | [HF API](https://huggingface.co/api/datasets/MBZUAI/ArVoice), [arXiv](https://arxiv.org/abs/2505.20506) | 83.5 h, 11 voices (7 human, about 10 h). MSA. | Card CC BY 4.0 **(C)**. The abstract says "available for research use" **(C)**. | **Disagreement.** Ask MBZUAI. |
| Arabic Speech Corpus (Halabi) | [HF API](https://huggingface.co/api/datasets/halabi2016/arabic_speech_corpus) | Single-speaker MSA TTS corpus. | Card CC BY 4.0 **(C, card only)**. | **Public release likely OK.** Not Saudi. |
| Fasee7 Najdi Small | [HF](https://huggingface.co/Wittify/Fasee7-Najdi-Small) | Najdi TTS LoRA on VoxCPM2 (2B base). | Apache 2.0 **(C)**. Training data in-house and unreleased. | **Public release OK** to use the model. Check whether 2B fits on a phone. |
| Saudi TTS dataset | None open found. SADA lists TTS as an intended use. | | SADA is CC BY-NC-SA. | Research only (SADA). |
| Apple iOS built-in Arabic voices (AVSpeechSynthesizer) | [Apple dev forum thread (Jan/Feb 2026)](https://developer.apple.com/forums/thread/812285), [older macOS SLA](https://www.apple.com/legal/sla/docs/macOS1012.pdf) | System Arabic voices, used live on device. | Older macOS SLAs limit "System Voices" to personal, non-commercial use, and bar recording or redistributing them in commercial or public contexts (snippet) **(R)**. The current iOS 26 SLA clause **could not be read** (U). A non-Apple forum reply says the voices are Apple's IP and must not be resold **(R)**. | Live playback through the public API in an App Store app is normal practice. **Do not record, export or train on the voices.** Lawyer or Apple to confirm. |

---

## Summary: safe for release / research only / avoid

| Area | Best public-release option | Research-only options | Avoid |
|---|---|---|---|
| Saudi speech (ASR eval/train) | Common Voice Arabic (CC0) | **SADA (CC BY-NC-SA)**, MADAR | X/Twitter-derived audio or text |
| Plant photos | iNaturalist/GBIF filtered to CC0 + CC BY (836 iNat / about 26.6 K GBIF records); Wikimedia Commons | CC BY-NC iNat photos; Pl@ntNet API | All-rights-reserved iNat photos |
| Food doneness | None found | Food-101 | Scraped recipe photos |
| Wood/fuel | None found; own photos + CC0/CC BY iNat | GOIMAI (CC BY-SA, poor fit) | |
| Survival | ATP 3-50.21 / FM 3-05.70 (US gov); Arabic Wikipedia (CC BY-SA) | WHO (CC BY-NC-SA 3.0 IGO) | Copying Saudi government pages without permission |
| Quran / prayer | Tanzil text (verbatim); adhan (MIT) | Tanzil translations | Altered Quran text |
| Hadith | Sanadset (CC BY); Open-Hadith-Data (ODbL) | LK-Hadith, sunnah.com | Translations of unknown origin |
| Fatwa / tafsir | Classical tafsir (rights of the edition unclear) | alifta, IslamQA (read and cite only) | IslamQA bulk text as training data |
| Nabati poetry | Poets dead more than 50 years (own collection) | Ashaar, APCD, Tarab | Living poets' work; lyrics |
| Dialect text | Common Voice transcripts (CC0) | SADA, MADAR, NADI, SaudiBERT | X content for training |
| Arabic TTS | Fasee7 Najdi (Apache 2.0); ArTST (MIT); Arabic Speech Corpus | MMS-TTS, XTTS-v2, SADA | Recording Apple system voices; XTTS outputs in a product |

**Safe for public release** (with the conditions shown):
- iNaturalist and GBIF CC0/CC BY photos (credit each one).
- Wikimedia Commons.
- ATP 3-50.21.
- Tanzil Quran text (verbatim, with notice and link).
- Sanadset.
- Open-Hadith-Data (ODbL share-alike).
- adhan libraries.
- Common Voice Arabic.
- Fasee7 Najdi Small.
- ArTST and Arabic Speech Corpus (confirm the cards).

**Research only:**
- SADA.
- MADAR, NADI, SaudiBERT.
- WHO texts.
- Food-101.
- MMS-TTS, XTTS-v2.
- Tanzil translations.
- IslamQA (read and evaluate only).
- Ashaar, APCD, Tarab, LK-Hadith.
- Pl@ntNet API.
- CC BY-NC iNaturalist/GBIF photos.

**Avoid:**
- X/Twitter content for training.
- Recording, exporting or training on Apple system voices.
- Living poets' and lyricists' texts.
- IslamQA or other fatwa text as training data.
- Modified Quran text.
- Any data with no license, when it would go into the public release.

## Where sources disagree / unverified

- **SADA split:** IEEE DataPort says 418 h train plus about 10 h each for dev and test. Kaggle says about 667 h, with 20 h for dev and test. The license matches on both. The DataPort uploader is an individual, not SDAIA's account.
- **ClArTTS and ArVoice:** the HF cards say CC BY 4.0, but the papers say "research use". Ask MBZUAI which applies.
- **Pl@ntNet-300K:** the Zenodo record says CC BY 4.0, while v2 lists per-image NC and SA licenses **(R)**.
- **GBIF:** the iNat dataset is CC BY-NC at dataset level, but records carry CC0 or CC BY. The image license may differ from the record license.
- **Tarab:** CC BY 4.0 tag versus crawled copyrighted lyrics.
- **Tanzil:** says "CC BY 3.0" but forbids changes, which is closer to ND in effect.
- **Unverified:**
  - Terms for sunnah.com, alifta.gov.sa, Islamway, Saudi Civil Defense, Saudi Red Crescent, Saudi MOH and QUL.
  - Licenses for APCD, LK-Hadith, SauDial and the Piper Kareem training data.
  - X's AI-training clause (TechCrunch only).
  - The iOS 26 SLA voice clause.
  - The new Saudi law's articles (secondary summaries only).
  - The ATP 3-50.21 marking (mirror only).
- Several pages blocked automated reading: gbif.org/terms, sunnah.com, Roboflow, PMC, my.plantnet.org, 998.gov.sa. Claims about those pages are marked (R).

## Open questions

1. **SADA weights.** Would SDAIA accept fine-tuned weights published as CC BY-NC-SA 4.0? Would it grant commercial terms later? Ask NCAI/SDAIA in writing. A lawyer should also check how ShareAlike interacts with the Gemma base-model license.
2. **New Saudi Copyright Law (2026).** What conditions will SAIP's Implementing Regulation set for the AI-development exception? Does "cultural heritage = State property" cover anonymous Nabati poetry?
3. Does the US-government public-domain status of ATP 3-50.21 hold outside the US (Saudi Arabia, EU)? Are any figures in it third-party?
4. Do restating WHO, MOH or Civil Defense facts in own words, and training on them, need permission? A lawyer should confirm.
5. Does Tanzil's "no changes" condition allow training or tokenising, or only shipping the text verbatim inside the app?
6. Apple: does the current iOS SLA allow commercial apps to speak with system Arabic voices? (Recording or exporting is likely barred.) Ask Apple Developer Relations.
7. Hadith translations: which upstream translations does fawazahmed0 use, and under what rights?
8. Is there any open Saudi-dialect TTS corpus, or a willing Saudi voice actor for a self-recorded set (own consent form)?

## Sources

All accessed 2026-10-13 unless noted. (C), (R) and (U) as above.

1. Kaggle, SADA صدى dataset: https://www.kaggle.com/datasets/sdaiancai/sada2022. Read via the API https://www.kaggle.com/api/v1/datasets/view/sdaiancai/sada2022 (lastUpdated 2023-08-31). (C)
2. IEEE DataPort, SADA Dataset: https://ieee-dataport.org/node/14747 (created 2025-02-08). (C)
3. IEEE DataPort uploader profile: https://ieee-dataport.org/user/1317217. (C)
4. HF card, badrex/arabic-speech-SADA22-MSA: https://huggingface.co/datasets/badrex/arabic-speech-SADA22-MSA/blob/main/README.md. (C, for that card)
5. Creative Commons, CC BY-NC-SA 4.0 legal code: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en. (C)
6. Creative Commons, Using CC-licensed works for AI training: https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/ (undated, 2025 or later). (C)
7. Origami, NVIDIA and SADA: https://origami.sa/en/blog/saudi-dialect-call-transcription/. (R)
8. iNaturalist Open Data: https://github.com/inaturalist/inaturalist-open-data. (C)
9. iNaturalist help, licensing (modified 2025-11-20): https://help.inaturalist.org/en/support/solutions/articles/151000173511. (C)
10. iNaturalist API, place and observation counts: https://api.inaturalist.org/v1/places/autocomplete?q=Saudi%20Arabia and https://api.inaturalist.org/v1/observations?place_id=7358&iconic_taxa=Plantae&photo_license=cc0,cc-by&quality_grade=research&per_page=1. (C)
11. GBIF, iNaturalist Research-grade Observations dataset (modified 2026-10-06): https://api.gbif.org/v1/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7. (C)
12. GBIF occurrence license facet for Saudi plants with images: https://api.gbif.org/v1/occurrence/search?country=SA&kingdomKey=6&mediaType=StillImage&limit=0&facet=license. (C)
13. GBIF terms: https://www.gbif.org/terms (403; search snippet). (R)
14. Pl@ntNet-300K on Zenodo (2021-04-29): https://zenodo.org/records/5645731. (C)
15. Pl@ntNet API terms: https://my.plantnet.org/terms_of_use (snippet). (R)
16. Wikimedia Commons licensing: https://commons.wikimedia.org/wiki/Commons:Licensing. (C)
17. Al-Kharj poisonous plants study: https://psau.sa.elsevierpure.com/en/publications/a-field-study-to-restricted-poisonous-wild-plants-grown-in-alkhar. (R)
18. Food-101 (ETH): https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/, and HF card https://huggingface.co/datasets/ethz/food101. (C)
19. Roboflow cooking dataset: https://universe.roboflow.com/school-4kceq/cooking-classification-and-detection (403; snippet). (R)
20. GOIMAI wood dataset: https://zenodo.org/doi/10.5281/zenodo.11092208 (snippet). (R)
21. ATP 3-50.21 (2018), FAS mirror: https://irp.fas.org/doddir/army/atp3-50-21.pdf (snippet). (R)
22. FM 3-05.70 (2002): https://biotech.law.lsu.edu/blaw/DOD/fm3-05-70.pdf (snippet). (R)
23. 17 U.S.C. §105: https://www.copyright.gov/title17/92chap1.html. (C)
24. WHO copyright policy: https://www.who.int/about/policies/publishing/copyright. (C)
25. WHO GDWQ 4th ed. with 1st and 2nd addenda (2022-03-21): https://www.who.int/publications/i/item/9789240045064. (C)
26. WHO heat-health action plans: https://www.who.int/publications/i/item/heat-health-action-plans (snippet). (R)
27. Saudi MOH heat stress page: https://www.moh.gov.sa/en/HealthAwareness/Pilgrims-Health/Pages/Heat-Stress.aspx. (terms U)
28. SFDA terms of use (example of the Saudi government pattern): https://www.sfda.gov.sa/en/terms-of-use (snippet). (R)
29. Saudi Civil Defense: https://998.gov.sa (connection refused). (U)
30. Wikimedia Terms of Use: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use. (C)
31. Tanzil Quran text license: https://tanzil.net/docs/text_license. (C)
32. Tanzil translations: https://tanzil.net/trans/. (C)
33. sunnah.com about and developers: https://sunnah.com/about, https://sunnah.com/developers (403; snippets). (R)
34. fawazahmed0/hadith-api: https://github.com/fawazahmed0/hadith-api. (C)
35. Open-Hadith-Data: https://github.com/mhashim6/Open-Hadith-Data, and LICENSE https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/LICENSE. (C)
36. LK-Hadith-Corpus: https://github.com/ShathaTm/LK-Hadith-Corpus. (license U)
37. Sanadset 650K: https://data.mendeley.com/datasets/5xth87zwb5/5. (C)
38. IslamQA terms: https://islamqa.info/en/terms. (C)
39. alifta.gov.sa: https://www.alifta.gov.sa. (terms U)
40. islamweb copyright fatwa: https://www.islamweb.net/en/fatwa/379009/islwmweb-material-is-copyrighted (snippet). (R)
41. QUL tafsir resources: https://qul.tarteel.ai/resources/tafsir, and FAQ https://qul.tarteel.ai/faq (snippet). (U/R)
42. spa5k/tafsir_api: https://github.com/spa5k/tafsir_api. (C)
43. adhan-swift: https://github.com/batoulapps/adhan-swift. (C)
44. adhan-java (Umm al-Qura parameters): https://github.com/batoulapps/adhan-java. (C)
45. Ashaar dataset: https://huggingface.co/datasets/arbml/Ashaar_dataset, API https://huggingface.co/api/datasets/arbml/Ashaar_dataset, paper https://arxiv.org/abs/2307.06218. (C)
46. APCD: https://hci-lab.github.io/ArabicPoetry-1-Private/#PCD (snippet). (U)
47. Tarab: https://huggingface.co/datasets/drelhaj/Tarab, and https://arxiv.org/abs/2603.16601 (2026-03-17). (C)
48. Commons, copyright rules for Saudi Arabia: https://commons.wikimedia.org/wiki/Commons:Copyright_rules_by_territory/Saudi_Arabia. (R)
49. Baker McKenzie on the new Saudi Copyright Law (2026-07-20): https://www.bakermckenzie.com/en/insight/publications/2026/07/saudi-arabia-new-copyright-law-modernises-ksa-ip-framework. (R)
50. WIPO Lex, Saudi Copyright Law: https://www.wipo.int/wipolex/en/legislation/details/19412. (R)
51. MADAR corpus: https://camel.abudhabi.nyu.edu/madar-parallel-corpus/. (C)
52. NADI 2024 and NADI 2021 papers: https://arxiv.org/abs/2407.04910, https://arxiv.org/abs/2103.08466. (R)
53. SaudiBERT: https://huggingface.co/faisalq/SaudiBERT (API lastModified 2024-05-23), and paper https://arxiv.org/abs/2405.06239. (C)
54. SauDial: https://data.mendeley.com/datasets/mzdwkb2t6d (snippet). (U)
55. SADSLyC: https://aclanthology.org/2025.wacl-1.4. (U)
56. Saudi-Dialect-ALLaM: https://arxiv.org/abs/2508.13525. (R)
57. X developer policy: https://docs.x.com/developer-terms/agreement-and-policy. (C)
58. TechCrunch on X barring AI training (2025-06-05): https://techcrunch.com/2025/06/05/x-changes-its-terms-to-bar-training-of-ai-models-using-its-content. (R)
59. Common Voice Arabic 23.0 on Mozilla Data Collective: https://datacollective.mozillafoundation.org/datasets/cmflnuzw47jng4x81tavetpul (snippet). (R)
60. MMS-TTS ara: https://huggingface.co/facebook/mms-tts-ara. (C)
61. Piper ar_JO-kareem: https://huggingface.co/rhasspy/piper-voices/tree/main/ar/ar_JO/kareem, and https://github.com/AliMokhammad/arabicttstrain. (C/U)
62. XTTS-v2 card and CPML text: https://huggingface.co/coqui/XTTS-v2, https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt. (C)
63. ArTST: https://huggingface.co/MBZUAI/ArTST/commit/4689f88d50819c33ba06e7c2ef0040494a7934a3 (snippet). (R)
64. ClArTTS: https://huggingface.co/api/datasets/MBZUAI/ClArTTS (2025-10-01), and https://arxiv.org/abs/2303.00069. (C)
65. ArVoice: https://huggingface.co/api/datasets/MBZUAI/ArVoice (2025-10-31), and https://arxiv.org/abs/2505.20506. (C)
66. Arabic Speech Corpus: https://huggingface.co/api/datasets/halabi2016/arabic_speech_corpus (2024-08-14). (C, card)
67. Fasee7 Najdi Small: https://huggingface.co/Wittify/Fasee7-Najdi-Small. (C)
68. Apple developer forum on system voices and the SLA (2026-01/02): https://developer.apple.com/forums/thread/812285. (R)
69. Apple macOS 10.12 SLA, System Voices clause: https://www.apple.com/legal/sla/docs/macOS1012.pdf (snippet). (R)
