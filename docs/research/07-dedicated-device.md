# Q7. Dedicated device

Research date: 2026-10-13. Labels: **confirmed** = primary source (manufacturer page, official repo, official model card, regulator). **Reported** = secondary source only (news site, forum user, reseller). **Unverified** = no backing found. **Calc** = my own arithmetic from sourced numbers, not a measurement. Prices change fast in 2026 (memory shortage), so every price has a date.

Jargon used below:
- **NPU** (neural processing unit): a small AI accelerator inside the chip. Rockchip's NPU needs its own model format (`.rkllm`); it cannot run normal llama.cpp files.
- **TOPS**: trillions of simple (INT8) operations per second. A marketing ceiling; for chat models, memory speed matters more.
- **MIPI CSI**: the flat-ribbon camera connector used by phone-style camera modules. "4-lane" = more bandwidth.
- **Prefill** = reading the prompt (and image/audio tokens); sets the wait before the first word. **Decode** = writing the answer, word piece by word piece.
- **W8A8 / W4A16 / Q4_K_M**: quantisation (compression) levels. Smaller = less RAM, sometimes lower quality.

## Question

For an offline, push-to-talk handheld (mic, camera, screen, battery) running Gemma 4 E2B/E4B with audio and image input: compare RK3588 boards (Orange Pi 5 family, Radxa ROCK 5 family, plus RK3576 and newer Rockchip chips) with NVIDIA Jetson Orin Nano Super 8 GB (and Orin NX 16 GB, Thor-family). Cover RAM/price, Gemma 4 runtime support, speed, power/cooling/camera/audio, and buying in Beijing/Harbin and bringing it to Saudi Arabia.

## Short answer

- **Both platforms now run Gemma 4 E2B with image and audio input, officially.** Rockchip's own `rknn-llm` added Gemma 4 in v1.3.0 and a Gemma 4 *audio* demo in v1.3.1 (29 Sep, year inferred 2026) ([1], [2], [4]). NVIDIA's Jetson AI Lab has a Gemma 4 page with vLLM and llama.cpp containers and says E2B/E4B take audio ([11]).
- **Jetson Orin Nano Super is about 2x faster at writing and about 5x faster at reading prompts** for Gemma 4 E2B (Google's official numbers: 24.2 tok/s decode, 1,142 tok/s prefill, GPU) ([8]) than RK3588 on its NPU (Rockchip's numbers: 11.1 tok/s decode, about 214 tok/s prefill derived) ([3]). These two tests use different prompt lengths, so treat the ratio as rough.
- **But the Jetson kit now costs $399** (raised from $249 in July 2026) ([19], [20]), draws more power (7–25 W modes) ([18]) and has no built-in audio jack. RK3588 boards are made in Shenzhen, cheaper, use about 8 W during NPU chat (reported) ([34]), and some have an onboard mic ([27]).
- **Gemma 4 E4B is the weak spot on both.** NVIDIA recommends only E2B for the Orin Nano ([11]), though staff say E4B works on JetPack 6.2.2 ([14]). For RK3588, nobody has published an E4B number.
- **Recommendation:** start with a 16 GB RK3588 board (Orange Pi 5 Pro or 5 Max, or Radxa ROCK 5B+/5C) running E2B through RKLLM. Add a Jetson Orin Nano Super only if E2B is too slow or E4B quality is required.

## Comparison table

Prices are USD list prices unless noted. "Not found" = searched, nothing reliable. CNY retail prices could not be found on official stores (Orange Pi's site refused connections from here; JD/Taobao pages were not reachable by search).

| Board | Chip / AI unit | RAM options | Price (date) | Gemma 4 E2B speed (best published) | Power | Camera (MIPI CSI) | Audio onboard |
|---|---|---|---|---|---|---|---|
| **Jetson Orin Nano Super dev kit** | Orin Nano 8 GB, Ampere GPU 1024 CUDA cores, 67 TOPS sparse INT8 ([18]) | 8 GB only (102 GB/s) ([18], [23]) | **$399** since July 2026, was $249 (confirmed [19]; [20]). ~CNY 2,704 by exchange rate, not a shop price (reported [21]) | 24.2 decode / 1,142 prefill tok/s, 2.7 GB, GPU, LiteRT-LM (confirmed, Google [8]) | Modes 7/15/25 W + MAXN SUPER ([18]); idle 4.7 W measured by a user, 2.5 W after tuning ([24]) | 2x 22-pin MIPI CSI-2 (reported, resellers) | None found; USB mic or I2S via 40-pin header ([49]) |
| **Jetson Orin NX 16 GB** (module, needs carrier board) | 157 TOPS sparse ([18]) | 16 GB (102 GB/s) ([18]) | **$999** module (1KU), was $599 ([19], [20]); carrier extra | Not found for Gemma 4. NVIDIA says E2B and E4B are "natural choices" ([11]) | 10/15/25/40 W + MAXN SUPER ([18]) | Depends on carrier | Depends on carrier |
| **Jetson T2000 / T3000** (Thor family, small) | Blackwell GPU | 16 GB / 32 GB (reported [26]) | Not announced; ship Q1 2027 (reported [26]) | Not found | ~40 W / ~70 W (reported, sources differ [26]) | n/a | n/a |
| **Orange Pi 5 Pro** | RK3588S, 6 TOPS NPU | 4 / 8 / 16 GB LPDDR5 ([27]) | Launch 2024: $60 / $80 / $109+ ([27]); 2026 price not found | Same NPU as RK3588: see RK3588 row below | Not measured for this board | **2x 4-lane** ([27]) | **ES8388 codec, 3.5 mm jack, onboard mic** ([27]) |
| **Orange Pi 5 Max** | RK3588, 6 TOPS | 4 / 8 / 16 GB LPDDR5 ([28]) | Launch 2024: 8 GB $95, 16 GB $125 on AliExpress (reported, Liliputing via search); 2026 not found | RK3588 NPU: 11.1 decode / ~214 prefill, 2.5 GB, W8A8 (confirmed, Rockchip [3]) | Not measured for this board | 3 camera inputs (reported [28]) | Not confirmed |
| **Orange Pi 5 Plus** | RK3588, 6 TOPS | 4 / 8 / 16 / 32 GB LPDDR4X ([29], [45]) | China launch: CNY 699 / 799 / 999 for 4/8/16 GB (reported [45], year of article not shown) | as RK3588 above | Idle about 4–5 W (reported, user [35]) | 1x 4-lane ([29]) | ES8388, 3.5 mm jack with mic, onboard mic, speaker header ([29]) |
| **Orange Pi 5 (original)** | RK3588S | up to 32 GB LPDDR4X ([29]) | not found (2026) | as RK3588 | not found | not checked | not checked |
| **Radxa ROCK 5B+** | RK3588 | 4–32 GB LPDDR5 ([30], [44]) | Launch $75 (4 GB) / $95 (8 GB) ([44]); April 2026: 8 GB $129.99 at Radxa's store, sold out ([22]) | as RK3588 | USB-C PD in; Radxa sells 30 W PD adapter ([30]) | 2x 4-lane or 4x 2-lane ([30]) | Not stated on product page |
| **Radxa ROCK 5C** | RK3588S2 class (page says quad or dual A76) | 4 / 8 / 16 / 32 GB ([32]) | not found (USD); India reseller only | as RK3588 (if the quad-A76 version; not confirmed) | not found | MIPI CSI, count not stated ([32]) | Headphone jack with mic input ([32]) |
| **Radxa ROCK 5T** | RK3588 | LPDDR5, sizes not listed on page ([31]) | not found (USD) | as RK3588 | **9–20 V DC barrel** ([31]) | 2x 4-lane ([31]) | Not stated |
| **Radxa ROCK 4D** (RK3576 sibling) | RK3576, 6 TOPS NPU | 2 / 4 / 8 / 16 GB LPDDR5 ([33]) | Launch: $31 / $37 / $58 / $100 on AliExpress (reported, CNX via search) | **9.2 decode / ~105 prefill, 1.46 GB, W4A16** (confirmed, Rockchip [3]) | not measured | 1 or 2 (sources disagree) | not checked |

## Runtime support for Gemma 4

### RK3588 / RK3576

| Runtime | Gemma 4? | Image in | Audio in | Status |
|---|---|---|---|---|
| **RKLLM (`airockchip/rknn-llm`)** on the NPU | Yes. README lists "Gemma2/Gemma3/Gemma3n/Gemma4" ([1]). Added in v1.3.0 (17 Jun) ([2]) | Yes. `multimodal_model_demo` lists Gemma-4-E2B-it with a vision encoder converted to RKNN ([4]) | **Yes**. v1.3.1 (29 Sep) "Added multimodal audio input interface and Gemma4 audio inference demo" ([2]). Steps: export audio tower to ONNX, convert with `--target-platform rk3588`, run `./audioenc` on a WAV file ([4]) | **Official** (Rockchip). Release page shows day/month only; year 2026 inferred from Gemma 4's April 2026 launch. Demo output in README is a placeholder, so real audio quality is not shown ([4]) |
| RKLLM, Gemma 4 **E4B** | Not listed separately; benchmark has E2B only ([3]) | not found | not found | **Unverified** |
| Pre-converted Gemma 4 E2B `.rkllm` (Seeed SenseCraft) | Yes, E2B, W8A8 for RK3588, W4A16 for RK3576 ([5]) | Page says text input only ([5]) | No ([5]) | Community/vendor (Seeed), not Rockchip |
| llama.cpp on the CPU (Cortex-A76) | Yes, llama.cpp supports Gemma 4; audio encoder added in PR #21421, merged 2026-04-12, tested on CPU, Vulkan and CUDA ([16]) | Yes (mmproj) | Yes, from April 2026, with caveats: BF16/Q8_0 mmproj, very low-bit quants fail ([16]) | Official llama.cpp; **no RK3588 Gemma 4 speed number found** |
| llama.cpp Vulkan on Mali-G610 GPU | not found | not found | not found | No RK3588 Gemma results found |
| MLC LLM (Mali OpenCL) | Not found. Last RK3588 work is 2024 (Llama 3) ([MLC blog](https://blog.mlc.ai/2024/04/20/GPU-Accelerated-LLM-on-Orange-Pi)) | — | — | Unverified for Gemma 4 |
| LiteRT-LM (Google) on Linux ARM64 CPU | Yes, E2B/E4B; README lists "IoT (e.g. Raspberry Pi)" and a Raspberry Pi CLI example ([7]); Google benchmarks a Raspberry Pi 5 ([10]) | Model card says vision/audio parts "loaded on demand" ([8]) | same | **Official for Pi 5 (same A76 cores as RK3588); no RK3588 test found.** Linux audio/image support not explicitly confirmed ([10]) |

### Jetson (Orin Nano / Orin NX)

| Runtime | Gemma 4? | Image in | Audio in | Status |
|---|---|---|---|---|
| **llama.cpp (CUDA)** in NVIDIA container `ghcr.io/nvidia-ai-iot/llama_cpp:latest-jetson-orin` | Yes ([11]) | Yes ([11]) | Supported in llama.cpp ([16]), but NVIDIA lists "a currently known E2B audio issue under llama.cpp on Orin" ([11]) | **Official** (NVIDIA Jetson AI Lab). E4B Q4_K_M ran out of GPU memory on JetPack r36.4.7; NVIDIA staff say fixed in r36.5 / JetPack 6.2.2 ([14]). A user got E2B Q4_K_S working with `--no-mmproj -c 4096` ([15]) |
| **vLLM** `ghcr.io/nvidia-ai-iot/vllm:gemma4-jetson-orin` | Yes ([11]) | Yes | Yes, "enabled by default" ([11]) | **Official**. Older `latest-jetson-orin` image (vLLM 0.16) did not know `gemma4` in April 2026 ([15]); use the gemma4 tag |
| Ollama | "Does not work on Orin Nano right now" ([11]) | — | — | Official statement: not working on Nano; works on other Jetsons ([11]) |
| **LiteRT-LM** | Yes. Google's E2B model card benchmarks "Jetson Orin Nano" on CPU and GPU ([8]) | not confirmed on Jetson | not confirmed on Jetson | **Official benchmark (Google)**; no Jetson E4B row ([9]) |
| TensorRT Edge-LLM | Docs list "Gemma" family and Jetson Orin targets (FP16/INT8/INT4 only on Orin) ([17]); a Gemma 4 audio-encoder kernel is reported in the repo docs (search snippet) | not confirmed | reported | Gemma 4 entry in its Supported Models page **not verified** |
| TensorRT-LLM / MLC | not found for Gemma 4 on Jetson | — | — | Not found |

Jetson AI Lab's device table: Orin Nano → E2B "best fit"; Orin NX → E2B and E4B; AGX Orin and Thor → full family ([11]). Requires JetPack 6 (L4T r36.x); recommends an NVMe SSD ([11]).

## Speed numbers

All numbers below are **published by others**. Nothing here was run by us. Prompt length differs between sources, so compare within a table, not across.

### Gemma 4 (direct)

| Device | Runtime / backend | Model, quant | Prefill tok/s | Decode tok/s | Memory | Source |
|---|---|---|---|---|---|---|
| RK3588 | RKLLM NPU | Gemma 4 E2B, W8A8 | ~214 (derived: 128 tokens / 599 ms TTFT) | **11.12** | 2,499 MB | confirmed [3] |
| RK3576 | RKLLM NPU | Gemma 4 E2B, W4A16 | ~105 (derived) | 9.23 | 1,463 MB | confirmed [3] |
| RK3576 | RKLLM NPU | Gemma 4 E2B, W8A8 | ~110 (derived) | 5.56 | 2,549 MB | confirmed [3] |
| Jetson Orin Nano | LiteRT-LM GPU | Gemma 4 E2B (LiteRT format) | **1,142** | **24.2** | 2,739 MB | confirmed, Google [8] |
| Jetson Orin Nano | LiteRT-LM CPU | Gemma 4 E2B | 109 | 12.2 | 3,681 MB | confirmed [8] |
| Raspberry Pi 5 16 GB (A76 CPU, like RK3588's big cores) | LiteRT-LM CPU | Gemma 4 E2B | 133 | 7.6 | 1,546 MB | confirmed [8] |
| Raspberry Pi 5 16 GB | LiteRT-LM CPU | Gemma 4 E4B | 51 | 3.2 | 3,069 MB | confirmed [9] |
| Raspberry Pi 5 | LiteRT-LM CPU | Gemma 4 E2B | 99 | 9 | 1,432 MB peak | confirmed, Google blog [50] (differs from [8]) |

Test settings: Rockchip uses a 128-token prompt and 64 new tokens at max CPU/NPU clocks ([3]); Google uses 1,024 prompt tokens, 256 new tokens, 2,048 context, 4 CPU threads ([8], [9]).

**Not measured anywhere (as of 2026-10-13):** Gemma 4 **E4B** on RK3588 (any runtime), Gemma 4 E4B on Orin Nano (speed), any Gemma 4 on Orin NX, llama.cpp Gemma 4 speed on RK3588, image-encoder or audio-encoder time on either platform, and end-to-end "press button → first word" latency.

### Proxies (clearly not Gemma 4)

| Device | Runtime | Model (proxy) | Prefill | Decode | Memory | Source |
|---|---|---|---|---|---|---|
| RK3588 | RKLLM W8A8 | Gemma 3n E2B | ~114 (derived) | 9.91 | 2,703 MB | confirmed [3] |
| RK3588 | RKLLM W8A8 | Qwen3.5 4B (size proxy for E4B) | ~62 (derived) | 6.22 | 4,576 MB | confirmed [3] |
| Orin Nano Super | Ollama | Gemma 3n E2B | 135.7 | 16.55 | not stated | reported, forum user [25] |
| Orin Nano Super | Ollama | Gemma 3 4B | 471.5 | 10.11 | not stated | reported [25] |
| Orin Nano Super | MLC, INT4 | Gemma 2 2B | — | 35.0 | — | confirmed, NVIDIA [18] |
| Orin NX 16 GB Super | MLC, INT4 | Gemma 2 2B | — | 39.0 | — | confirmed [18] |

What this means for the device (calc): a 30-word spoken answer is roughly 40–50 tokens. At 11 tok/s (RK3588) that is about 4 s of writing; at 24 tok/s (Orin Nano GPU) about 2 s. Audio in costs 25 tokens per second of speech (from Q1 note), so a 10 s question is ~250 tokens: about 1.2 s of prefill on RK3588 at ~214 tok/s, about 0.2 s on Orin Nano GPU at 1,142 tok/s. An image adds more tokens (count depends on settings; not measured here).

## Power, cooling, camera, audio

### Power and battery

- **Jetson Orin Nano Super:** power modes 7 W, 15 W, 25 W and uncapped MAXN SUPER (confirmed [18]). One user measured 4.7 W idle and 6.2 W with two cameras running a small vision model in 7 W mode, using `tegrastats`; NVIDIA staff said that reading is close to real power (reported [24]). After disabling display/audio/PCIe and using microSD: 2.5 W idle ([24]). **No published watt figure for LLM chat on Orin Nano was found.** The kit ships with a 19 V supply (reported, reseller [48]), so a battery build needs a 19 V boost or a different carrier.
- **RK3588:** a user reports Orange Pi 5 Plus idle about 4–5 W (reported [35]). A video-based test reports about 8 W whole-board when an LLM runs on the NPU and about 12 W on the CPU (reported, informal USB meter [34]). No official Rockchip power figure for LLM load was found. Radxa notes nobody has measured all engines at full load (reported, Radxa forum via search).
- **Battery sizing (calc, not measured):** a common 10,000 mAh / 3.7 V pack is 37 Wh. At an average of 5 W (mostly idle, short bursts of chat) that is about 7 h before conversion losses; at a constant 8 W, about 4.5 h; at 15 W (Jetson mid mode), about 2.5 h. Anything under 100 Wh can fly in carry-on (see below).
- **Solar (calc):** a phone-sized 5 W panel in full sun gives about the board's idle draw at best, so solar can top up a battery but cannot run either board on its own.
- **Cooling:** the Jetson dev kit comes with a heatsink and fan as part of its 21 mm height (reported, reseller). MAXN SUPER throttles if heat exceeds the design budget (confirmed [18]). For RK3588 boards under sustained NPU load, no throttling test was found; plan for a heatsink at minimum (unverified).

### Camera

- Jetson Orin Nano Super kit: two MIPI CSI-2 22-pin connectors (reported, resellers; NVIDIA China page does not list ports [23]).
- Orange Pi 5 Pro: 2x 4-lane MIPI CSI ([27]). Orange Pi 5 Max: three camera inputs (reported [28]). Orange Pi 5 Plus: 1x 4-lane ([29]). ROCK 5B+: 2x 4-lane or 4x 2-lane ([30]). ROCK 5T: 2x 4-lane, 31-pin ([31]).
- Check that the exact camera module has a driver for your board's OS image before buying (Rockchip boards use vendor kernels; unverified per module).

### Microphone / audio

- **Orange Pi 5 Pro and 5 Plus have an onboard microphone and a 3.5 mm jack** (ES8388 codec) ([27], [29]). ROCK 5C has a headphone jack with mic input ([32]).
- **Jetson Orin Nano dev kit: no onboard audio codec found.** Options are a USB microphone (easiest) or an I2S microphone on the 40-pin header; users report I2S MEMS mics being hard to get working (reported [49]).
- For push-to-talk, a GPIO button works on all boards (40-pin header). Not tested.

## Buying in Beijing / Harbin

- **Who makes them:** Orange Pi = Shenzhen Xunlong Software Co. (reported [47]). Radxa sells only through "Approved Partners" and lists China as a region (confirmed [30]); ALLNET China and Arace Tech were named sellers at the ROCK 5B+ launch (reported [44]). Both are Chinese brands, so Taobao/JD flagship stores are the normal channel (store names not verified here).
- **Jetson in China:** NVIDIA's FAQ lists **CN** among sale regions for Orin Nano 8 GB and Orin NX 16 GB modules, and says the dev kit and modules are made in "China, USA, or Vietnam" (confirmed [19]). Arrow lists the Orin Nano Super kit as "for US, CA, CN, JP, PH Regions" (reported [36]). NVIDIA's China page sends buyers to partners but names none (confirmed [23]).
- **US export rules:** NVIDIA states the ECCN (export class) is **5A992.C** (confirmed [19]). BIS says 5A992.c mass-market items only carry anti-terrorism controls and need no licence for most destinations (confirmed [37]); China and Saudi Arabia are not in the embargo groups named there. A 2022 rule added China licence needs for 5A992 items that exceed the 3A090 performance thresholds (reported, law firm summary [38]). Orin Nano's 67 TOPS INT8 looks far below those data-centre thresholds, but **no source was found that does this comparison**, so this is unverified. No source was found saying Jetson Orin retail sales in China are blocked.
- **China prices (CNY):** not found on official stores. IT Home gives ~CNY 2,704 for the $399 kit by exchange rate only (reported [21]). Orange Pi 5 Plus launch: CNY 699/799/999 (reported [45]). Memory prices pushed many boards up 44–148% between 2024 and April 2026 (reported [22]).
- **Warranty:** not found for Orange Pi or Radxa. NVIDIA: dev kits have "no guarantee of availability" (confirmed [19]); warranty terms not found. Buying from a grey seller likely means no warranty outside China (unverified).
- **Plugs and power:** China sockets take Type I and Type A plugs, 230 V 50 Hz ([43]). Saudi Arabia uses **Type G** (UK-style), 230 V **60 Hz** ([42]). USB-C PD adapters and the Jetson 19 V brick are normally 100–240 V, 50/60 Hz, so a plug adapter is enough (check the label; unverified per adapter).
- **Flying China → Saudi Arabia:**
  - Lithium batteries: up to 100 Wh in devices or as spares; spares and power banks in carry-on only, terminals protected; 100–160 Wh needs airline approval, max 2 spares (confirmed IATA [40]; PDF could not be rendered here, details via IATA-quoting search summary).
  - China domestic flights (e.g. Harbin → Beijing): power banks without a **3C mark** are banned since 2025-06-28 (reported [41]). Buy 3C-marked power banks in China.
- **Saudi customs (ZATCA):** personal luggage and gifts are duty-free up to **SAR 3,000** total, must be non-commercial with receipts, and not prohibited/restricted (confirmed [39]). Keep receipts; several boards for a project could look commercial (unverified how officers judge this).
- **Saudi radio approval:** CST (telecom regulator) requires type approval for imported wireless equipment; boards with Wi-Fi/Bluetooth may count. No traveller-specific rule found (unverified [51]).

## Where sources disagree / unverified

- **RKLLM Gemma 4 support:** some search summaries and Radxa's docs list only Gemma 2/3 ([Radxa RKLLM doc](https://docs.radxa.com/en/rock5/rock5b/app-development/rkllm_usage)); the upstream README and release notes clearly add Gemma 4 and its audio demo ([1], [2]). Upstream wins; Radxa docs are out of date.
- **Seeed vs Rockchip on multimodal:** Seeed's ready-made Gemma 4 `.rkllm` is text-only ([5]); Rockchip's demo adds vision and audio encoders you must convert yourself ([4]).
- **Pi 5 Gemma 4 E2B speed:** Google's blog says 99 prefill / 9 decode ([50]); the model card says 133 / 7.6 ([8]).
- **Orin Nano memory bandwidth:** NVIDIA says 102 GB/s in Super mode ([18], [23]); some resellers still print 68 GB/s (old mode).
- **E4B on Orin Nano:** Jetson AI Lab recommends E2B only ([11]); NVIDIA forum staff say E4B Q4_K_M works on JetPack 6.2.2 ([14]). Both can be true (works, but tight on 8 GB).
- **Thor T2000/T3000 power:** 40 W / 70 W vs. 40–75 W range (reported, different outlets [26]).
- **ROCK 4D camera count:** dual vs single CSI in different sources (reported).
- **Unverified:** RK3588 power under NPU LLM load (one informal video); RK3588 cooling needs; Jetson LLM power draw; CNY retail prices; warranty terms; whether llama.cpp's Orin E2B audio issue is fixed.

## Recommendation

**Build the first handheld prototype on a 16 GB RK3588 board running Gemma 4 E2B through Rockchip's RKLLM (W8A8).** Best fits: **Orange Pi 5 Pro** (onboard mic, 3.5 mm jack, 2 cameras, small RK3588S) or **Radxa ROCK 5B+** (USB-C PD power, 2x 4-lane cameras). Reasons:
1. Rockchip ships an official Gemma 4 E2B demo with **both image and audio input** on the NPU ([2], [4]).
2. ~11 tok/s writing and ~2.5 GB RAM are published by Rockchip ([3]); 16 GB leaves room for speech-to-text, text-to-speech and the camera pipeline.
3. Made in Shenzhen, easy to buy in China, lower power (about 8 W reported during NPU chat [34]), USB-C power suits a battery pack.

**Buy a Jetson Orin Nano Super (8 GB, $399) as a second board only if** E2B on RK3588 feels too slow (Google's numbers show ~2x decode and ~5x prefill on Orin Nano GPU [8]) or if the faster Jetson tools (vLLM audio by default [11]) save a lot of work.

What would change this:
- **Saudi-dialect quality needs E4B** → Orin NX 16 GB (E4B is a "natural choice" there [11]) but $999 for the module alone ([19]); or test E4B on RK3588 first (expect around 6 tok/s by the Qwen3.5 4B proxy [3]; not measured).
- **Rockchip's audio demo fails on real speech** (its README shows no real output [4]) → Jetson, where vLLM audio is on by default ([11]).
- **Jetson prices fall back, or a used Orin Nano is cheap in Beijing** → Jetson becomes the easier first choice.
- **Battery life is the top priority** → look at RK3576 (ROCK 4D): Gemma 4 E2B W4A16 at 9.2 tok/s in 1.46 GB ([3]); power not measured.

## Open questions

Each step is a check the student (or a later research task) can do. No timings given.

1. **Check E4B on RKLLM.** Search `airockchip/rknn-llm` issues and the Rockchip model zoo for "Gemma4 E4B". Done when: an official benchmark row or a dated issue/answer is found, or "not supported" is confirmed.
2. **Check whether llama.cpp's E2B audio issue on Orin is fixed.** Re-read the Jetson AI Lab Gemma 4 page and llama.cpp issues. Done when: the "known issue" note is gone or a linked fix is found.
3. **Get real CNY prices.** In China, open JD/Taobao flagship stores for Orange Pi (香橙派), Radxa (瑞莎) and an NVIDIA partner; note price, RAM, seller name, invoice (发票), warranty. Done when: a dated table of at least 3 listings per board exists.
4. **Confirm Saudi rules.** Ask ZATCA (call centre 19993) whether 2–3 dev boards with Wi-Fi count as personal items, and check CST for traveller exemptions. Done when: a written or recorded answer is saved.
5. **Measure on hardware (after purchase).** Run Rockchip's Gemma 4 audio demo with a 10 s Saudi-dialect clip; log time to first word, tok/s, watts (USB-C meter) and board temperature. Done when: one results table exists for the bought board.
6. **Check Gemma 4 12B (audio-capable) fit.** Jetson AI Lab lists it for AGX Orin only; not for 16 GB boards. Done when: a published RAM figure for 12B at 4-bit is found.

## Sources

All accessed 2026-10-13 unless noted.

1. Rockchip, `rknn-llm` README (support list incl. Gemma4). https://github.com/airockchip/rknn-llm
2. Rockchip, `rknn-llm` releases (v1.3.0 17 Jun; v1.3.1 29 Sep; year not shown). https://github.com/airockchip/rknn-llm/releases
3. Rockchip, `rknn-llm` benchmark.md (RK3588/RK3576 Gemma4 E2B rows; undated). https://github.com/airockchip/rknn-llm/blob/main/benchmark.md
4. Rockchip, `multimodal_model_demo` README (Gemma-4-E2B vision + audio). https://github.com/airockchip/rknn-llm/tree/main/examples/multimodal_model_demo
5. Seeed SenseCraft AI Lab, Gemma 4 E2B RKLLM page (undated). https://sensecraft.seeed.cc/ai-lab/en/models/gemma-4-e2b-it
6. Seeed SenseCraft, RK LLM benchmark (undated). https://sensecraft.seeed.cc/ai-lab/tutorials/rk/benchmark/llm
7. Google, LiteRT-LM README (v0.18.0 highlighted). https://github.com/google-ai-edge/LiteRT-LM
8. Google / litert-community, Gemma 4 E2B LiteRT-LM model card (benchmark table incl. Jetson Orin Nano). https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm
9. Google / litert-community, Gemma 4 E4B LiteRT-LM model card. https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm
10. Google AI Edge, LiteRT-LM Gemma 4 page (last updated 2026-09-04). https://developers.google.com/edge/litert-lm/models/gemma-4
11. NVIDIA Jetson AI Lab, "Gemma 4 on Jetson" tutorial (undated, © 2026). https://www.jetson-ai-lab.com/tutorials/gemma4-on-jetson/
12. NVIDIA Jetson AI Lab, Gemma 4 E2B model page. https://www.jetson-ai-lab.com/models/gemma4-e2b
13. NVIDIA Jetson AI Lab, Gemma 4 E4B model page. https://www.jetson-ai-lab.com/models/gemma4-e4b
14. NVIDIA Developer Forums, "Gemma4 e4b on Jetson Orin Nano fails due to CUDA out of memory" (2026-04-05 to 04-08). https://forums.developer.nvidia.com/t/gemma4-e4b-on-jetson-orin-nano-fails-due-to-cuda-out-of-memory-issue/365641
15. NVIDIA Developer Forums, "No luck with Gemma 4 on Jetson Nano Super" (2026-04-04 to 05-05). https://forums.developer.nvidia.com/t/no-luck-with-gemma-4-on-jetson-nano-super/365620
16. llama.cpp PR #21421, Gemma 4 audio conformer encoder (merged 2026-04-12). https://github.com/ggml-org/llama.cpp/pull/21421
17. NVIDIA, TensorRT Edge-LLM 0.10.1 overview. https://nvidia.github.io/TensorRT-Edge-LLM/0.10.1/overview.html
18. NVIDIA Technical Blog, "JetPack 6.2 Brings Super Mode…" (2025-01-16). https://developer.nvidia.com/blog/nvidia-jetpack-6-2-brings-super-mode-to-nvidia-jetson-orin-nano-and-jetson-orin-nx-modules
19. NVIDIA, Jetson FAQ (prices, ECCN 5A992.C, regions, origin). https://developer.nvidia.com/embedded/faq
20. CNX Software, "NVIDIA increases the price of Jetson modules and devkits by up to 101%" (2026-07-22). https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/
21. IT之家 (IT Home), Jetson price rise report (2026-07-22). https://www.ithome.com/0/979/840.htm
22. CNX Software, "Comparing SBC prices in 2024 and 2026" (2026-04-28). https://www.cnx-software.com/?p=169435
23. NVIDIA China, Jetson Orin Nano Super Developer Kit page. https://www.nvidia.cn/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/
24. NVIDIA Developer Forums, "Reducing idle power on Orin Nano Super Dev Kit" (2026-01-23 to 02-06). https://forums.developer.nvidia.com/t/reducing-idle-power-on-orin-nano-super-dev-kit/358482
25. NVIDIA Developer Forums, "Gemma 3 and Gemma 3n on Jetson Orin Nano Super" (2025-08-19, 2025-09-23 posts). https://forums.developer.nvidia.com/t/gemma-3-and-gemma-3n-on-jetson-orin-nano-super/337513
26. CNX Software, "NVIDIA Jetson T2000 and T3000 modules" (2026-07-16). https://www.cnx-software.com/2026/07/16/nvidia-jetson-t2000-and-t3000-modules-for-edge-ai-and-robotics-applications/
27. CNX Software, "Orange Pi 5 Pro…" (2024-04-12). https://www.cnx-software.com/2024/04/12/orange-pi-5-pro-low-cost-rockchip-rk3588s-sbc-16gb-lpddr5-ram-dual-hdmi/
28. CNX Software, "Orange Pi 5 Max…" (2024-08-01); TechSpot/Hackster for camera count. https://www.cnx-software.com/2024/08/01/rockchip-rk3588-powered-orange-pi-5-max-sbc-features-up-to-16gb-lpddr5-2-5gbe-onboard-wifi-6e-and-bluetooth-5-3/ · https://hackster.io/news/orange-pi-launches-the-orange-pi-5-max-boasting-a-6-tops-npu-four-lane-pcie-gen-3-and-more-8a1761b372e5
29. CNX Software, "Orange Pi 5, 5B, and 5 Plus… 32GB RAM" (2023-10-13). https://www.cnx-software.com/2023/10/13/orange-pi-5-5b-and-5-plus-sbc-32gb-ram/
30. Radxa, ROCK 5B+ product page. https://radxa.com/products/rock5/5bp/
31. Radxa, ROCK 5T product page. https://radxa.com/products/rock5/5t/
32. Radxa, ROCK 5C product page. https://radxa.com/products/rock5/5c/
33. Radxa, ROCK 4D docs. https://docs.radxa.com/en/rock4/rock4d · CNX launch article https://www.cnx-software.com/?p=151062
34. Lilys.ai note on a video, "Running LLMs on the Rockchip RK3588 NPU" (2025-11-10; informal power readings). https://lilys.ai/en/notes/ai-semiconductor-20251110/running-llms-rockchip-rk3588-npu
35. Armbian forum user post, Orange Pi 5 Plus idle power (undated). https://forum.armbian.com/profile/4443-thewonderer/content
36. Arrow, Jetson Orin Nano Super kit listing (945-13766-0000-000). https://www.arrow.com/de/products/945-13766-0000-000/nvidia.html
37. US BIS, "Mass market (Section 740.17)". https://www.bis.gov/learn-support/encryption-controls/mass-market
38. ArentFox Schiff, "Summary of ECCN Changes" (2022-10). https://www.arentfox.com/sites/default/files/2022-10/Summary-of-ECCN-Changes.pdf
39. ZATCA, travellers' luggage and gifts exemption. https://zatca.gov.sa/en/RulesRegulations/Taxes/Pages/customs-individual/Travel-pages/luggage.aspx
40. IATA, passenger lithium battery guidance (PDF, undated). https://www.iata.org/contentassets/6fea26dd84d24b26a7a1fd5788561d6e/passenger-lithium-battery.pdf
41. Executive Traveller, China airlines power bank (3C) ban (2025). https://www.executivetraveller.com/news/china-airline-powerbank-battery-ban · Techlicious https://www.techlicious.com/tip/flying-within-china-your-power-bank-needs-a-3c-label/
42. WorldStandards, Saudi Arabia plugs/voltage (updated 2025-07-12). https://www.worldstandards.eu/electricity/plug-voltage-by-country/saudi-arabia/
43. WorldStandards, China plugs/voltage. https://www.worldstandards.eu/electricity/plug-voltage-by-country/china/
44. Notebookcheck, ROCK 5B+ launch, sellers ALLNET China / Arace Tech. https://www.notebookcheck.net/Radxa-releases-Rock-5B-Plus-with-up-to-32-GB-LPDDR5-RAM-to-compete-against-Raspberry-Pi-5.869506.0.html
45. IT之家, Orange Pi 5 Plus China launch prices (year not shown). https://www.ithome.com/0/692/295.htm
46. CNX Software, Rockchip RK3668 and RK182X LLM co-processor (2025-07-18). https://cnx-software.com/2025/07/18/rockchip-unveils-rk3668-10-core-arm-cortex-a730-cortex-a530-soc-with-16-tops-npu-rk182x-llm-vlm-co-processor
47. Wikipedia, Orange Pi (Shenzhen Xunlong). https://en.wikipedia.org/wiki/Orange_Pi
48. Mouser / Seeed, Jetson Orin Nano dev kit listing (19 V supply included). https://www.mouser.in/new/seeed-studio/seeed-studio-nvidia-jetson-orin-nano-dev-kit/
49. NVIDIA Developer Forums, "I2S MEMS Microphone not working with Jetson Orin Nano Devkit" (2025). https://forums.developer.nvidia.com/t/i2s-mems-microphone-not-working-with-jetson-orin-nano-devkit/340782
50. Google Developers Blog, "Mastering Edge AI on Raspberry Pi with LiteRT and Gemma". https://developers.googleblog.com/en/mastering-edge-ai-on-raspberry-pi-with-litert-and-gemma/
51. CST (Saudi Communications, Space & Technology Commission), special wireless devices registrar page. https://www.cst.gov.sa/en/business/services/Special-Telecommunication-Devices-Registrar-Qualification-and-Accreditation

Newer Rockchip note: RK3668 (16 TOPS NPU) and the RK1820/RK1828 LLM co-processors were announced in July 2025; the only devkit found is Firefly's at $889/$1,029 with an RK3588 host, and no Gemma 4 support was found (reported [46]). Not a fit for this project yet.
