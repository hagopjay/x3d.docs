# 27. Shaders and Vulkan: what the explicit APIs teach an X3D renderer

> **Say it:** An X3D renderer is trustworthy only where its colour encode, depth range and timing scope are named and tested, and X_ITE 16.7.1 encodes output with a plain 2.2 power (byte 186 for linear 0.5, where sRGB gives 188) for the materials its `ColorSpace` option selects. **[C]**

| field | value |
|---|---|
| chapter code | `SVK` |
| prerequisites | [01 The tether](01-the-tether.md); [06 X_ITE the oracle](06-xite-the-oracle.md); [20 Compute on the GPU](20-webgpu-compute.md) |
| after this you can | (1) say which materials X_ITE encodes under each `ColorSpace` value and what byte to expect; (2) decode X_ITE bytes without faking an energy loss; (3) write a white-furnace fixture; (4) write a Vulkan dependency sentence and pick its stage and access pair; (5) say why an image hash binds one driver |
| sources read | `x3d.loom@90f9862:LEARNINGS-shader-vulkan.md`, `runs/shader-vulkan-20261117/`; `x3d.loom@32f5ae7:x3d.webgpu/{SPEC,BENCHMARK,ARCHITECTURE}.md`, `x3d.gltf/render/README.md`, `x3d.threejs/bridge/ESTIMATE.md`; the Shader-Vulkan Fieldbook and the Vulkan Light Lab (uploaded packages, read and re-run, not in a public repository) |
| instruments used | `X_ITE 16.7.1`, Chromium 153.0.8010.12, Playwright 1.63.0, SwiftShader (software); CPython 3.13.18 and GCC on Linux x86_64, 4 vCPU; Mesa 25.2.8 lavapipe (LLVM 20.1.2), Vulkan 1.4.318, validation layer 1.3.275; no physical GPU |

Two teaching packages about shaders and Vulkan were re-run and one measurement of X_ITE was added. The packages teach a method that matches ours (a small CPU reference, a visible intermediate, one controlled fault, a named measurement) and they supply facts a renderer's receipt should carry. The measurement found a colour-encode difference that explains small parity gaps between engines.

---

## 1. The map

```text
   X3D scene value (linear)    engine shader                     screenshot byte
   emissive 0.5 ---+--> X_ITE: pow(c, 1/2.2) ------------------>  186  (PhysicalMaterial)
                   +--> X_ITE: no encode (unlit, legacy) ------>  128  (default ColorSpace)
                   +--> exact sRGB, piecewise ----------------->  188  (the Fieldbook's rule)
   decode with the INVERSE of the writer: 186 -> 0.4995 (2.2 inverse), 0.491 (sRGB inverse)
```

```text
   Vulkan hand-off, one dependency sentence per arrow
   host init --flush--> [particles] --simulate--> [particles] --render--> [pixels]
   [pixels] --reduce--> [partials] --fence wait--> host stats
   [pixels] --copy--> swapchain or readback
   arrow = producer stage/access -> consumer stage/access (sync2 names)
```

| in scope | out of scope |
|---|---|
| X_ITE output encode and `ColorSpace` contract; a white furnace on PhysicalMaterial; the Fieldbook's rules; the Light Lab re-run; what each means for the bridges and the WebGPU spec | a physical GPU, WSL, a native window, Babylon / three.js / Blender / Unreal encode functions (read, not run), prefiltered IBL energy compensation |

| fieldbook label | meaning | our grade |
|---|---|---|
| Identity | follows from stated maths | [C] if derived and run, else [L] |
| Guarantee | an API or spec obligation | [L]; [C] if a validator layer ran |
| Approximation | a substitute with a limited domain | [C] only with its error measured |
| Observation | a result on one workload and system | [C] on the named rig only |

Read next: deeper, [20 Compute on the GPU](20-webgpu-compute.md) for the twins and the three clocks; wider, [18 Path-tracing X3D](18-three-pathtracer.md) for the same colour traps in a path tracer.

---

## 2. The X_ITE colour contract

The encode is in the shader source: `x_ite.js` 16.7.1 line 67921 reads `const float GAMMA=2.2; ... linearToSRGB(color) { return pow(color, vec3(INV_GAMMA)); }`. Rendering emissive 0.5 on a sphere with no lights and `toneMapping=NONE` (centre 5x5 mean, 128x128 canvas) gave:

| material, emissive 0.5 | default (`LINEAR_WHEN_PHYSICAL_MATERIAL`) | `ColorSpace=LINEAR` | `ColorSpace=SRGB` | `DisplayColorSpace=DISPLAY_P3` |
|---|---|---|---|---|
| UnlitMaterial | 128 | 186 | 128 | 128 |
| legacy Material | 128 | 186 | 128 | 128 |
| PhysicalMaterial | 186 | 186 | 128 | 186 |

Byte 128 is a raw pass-through of 0.5; 186 is `255 * 0.5^(1/2.2) = 186.08`; exact sRGB would give 187.52, byte 188. The two curves differ by about 2 bytes at linear 0.5 and by about 8.5 bytes near linear 0.002 (2.2 power 15.1, sRGB 6.6), so engine gaps are larger in darks. `DisplayColorSpace=DISPLAY_P3` changed nothing in a headless Chromium screenshot; that is this rig only.

## 3. A white furnace on PhysicalMaterial

The only light is an `EnvironmentLight` whose diffuse and specular cube maps are six identical 1x1 white PNG faces, headlight off, white background. With no `EnvironmentLight`, or intensity 0, the sphere is byte 0 although the background is 255.

| case | byte | linear (2.2 inverse) | reading |
|---|---|---|---|
| dielectric, baseColor 0.5, roughness 1, intensity 1 | 187 | 0.5054 | diffuse about 0.5 |
| dielectric, baseColor 0.5, roughness 0.5 or 0 | 189 | 0.5174 | +0.012 from the specular lobe (inferred) |
| metal, baseColor 1, intensity 0.5, roughness 0, .25, .5, .75, 1 | 186 each | 0.4995 | flat in roughness |
| any baseColor 1, intensity 1 | 255 | 1.0 | clipped; shows nothing |

Flat metal output fits energy compensation or a lookup with no roughness-dependent term; a uniform environment cannot tell them apart, and one byte of quantisation is about 0.3 percent here. The first reading of these bytes used the exact sRGB inverse and gave 0.491, a fake 1.8 percent loss. The decode must be the inverse of what wrote the bytes.

## 4. What the Fieldbook adds, as a checklist

| topic | rule | grade |
|---|---|---|
| depth | forward-Z with `w_clip = -z_view`: `z_ndc = (A z + B)/(-z)`, `A = f/(n-f)`, `B = fn/(n-f)`; n=0.1, f=100: z=-n gives 0.0, z=-f gives 0.9999999999999999, z=-1 gives 0.9009. Reversed-Z (the WebGPU spec's choice, R-RENDER-07) swaps the ends. | [C] arithmetic |
| NDC y | depth [0,1] is shared by Vulkan, WebGPU and D3D; NDC y is up in WebGPU and D3D and down in Vulkan | [L] |
| sRGB | piecewise, not 1/2.2; linear 0.5 is 0.7354 encoded; averaging encoded 0 and 1 gives linear 0.2140 | [C] |
| dependency | write the sentence first ("A writes this range, B reads it as storage"), then choose stage and access; order alone is neither an execution nor a memory dependency | [L] |
| sync2 names | transfer write to compute storage read is COPY/TRANSFER_WRITE to COMPUTE/SHADER_STORAGE_READ; compute to vertex attribute fetch uses VERTEX_ATTRIBUTE_INPUT/VERTEX_ATTRIBUTE_READ; sync1 names differ | [L] |
| memory | coherent memory removes flush and invalidate, not execution synchronisation; flush ranges are multiples of `nonCoherentAtomSize` from the start of the `VkDeviceMemory` | [L] |
| barriers | a workgroup barrier is not a dispatch barrier; tail lanes carry identities and still reach every barrier | [L] |
| timing | submit plus fence wait is latency; kernel time needs timestamp queries; report `null`, never CPU time, when unsupported | [L] |
| presentation | a frame fence alone does not prove a render-finished semaphore is free; `VK_KHR/EXT_swapchain_maintenance1` present fences are the formal proof (optional extension) | [L] |

## 5. Re-running the two packages

| check | authors (Mesa 25.0.7, LLVM 19.1.7) | here (Mesa 25.2.8, LLVM 20.1.2) |
|---|---|---|
| Fieldbook lab, C vs Python cases | 745, max diff 1.665e-16 | 745, max diff 1.6653345369377348e-16 |
| particle oracle, 257 particles | 9.313e-10 | 9.313e-10, with and without `--validate` |
| luminance reduction oracle, 65x33 | 2.260e-7 | 1.660e-7 |
| integration checks | 15 PASS | 15 PASS |
| GPU ms median, 160x90, 128 particles: simulate, render, reduce | 0.117, 0.493, 0.377 | 0.078, 0.480, 0.484 |
| same 1440x900 4 spp render, bytes differing from the shipped image | reference | 258 of 3,888,000, max 14 of 255 |

The timings are lavapipe numbers and demonstrate a measurement pipeline, not GPU throughput. The same shader bytes gave a bit-identical particle result and a different image tail on another LLVM: a hash of an image binds one driver, the same rule the Math Lab found for float hashes across runtimes.

---

## Heuristics

| ID | Rule | Grade | Evidence | Instrument |
|---|---|---|---|---|
| H-SVK-1 | Name each engine's output encode function in every parity receipt; a 2-byte mid-grey gap and a larger gap in darks are expected between a 2.2 power and exact sRGB. | C | `x_ite.js` line 67921; byte 186 vs 188 | X_ITE 16.7.1, Chromium 153.0.8010.12, SwiftShader |
| H-SVK-2 | Test a scene that mixes material kinds under each `ColorSpace`; under the default, unlit and legacy materials are not encoded and PhysicalMaterial is. | C | section 2 table, 12 cells | X_ITE 16.7.1, Chromium 153.0.8010.12, SwiftShader |
| H-SVK-3 | Decode bytes with the inverse of the function that wrote them; a mismatched decode fakes a loss. | C | 0.491 vs 0.4995 on the same byte 186 | Python 3.13.18, X_ITE 16.7.1 |
| H-SVK-4 | Put a furnace fixture (uniform white environment, albedo 0.5, no tone map) in every renderer's suite; expected diffuse output is the albedo, within byte quantisation. | C | byte 187 (0.5054) and 186 (0.4995) | X_ITE 16.7.1, SwiftShader |
| H-SVK-5 | Never set intensity so a furnace result clips; keep a half-intensity control. | C | baseColor 1 at intensity 1 read 255 for every roughness | X_ITE 16.7.1, SwiftShader |
| H-SVK-6 | Compare images across drivers with a stated tolerance and the driver named; never by hash. | C | 258 of 3,888,000 bytes differ, max 14 | Mesa 25.2.8 vs shipped LLVM 19.1.7, `imgdiff.py` |
| H-SVK-7 | Write the depth test in the spec's convention; reversed-Z swaps the expected ends, and use a tolerance at the far plane in f32. | C | forward-Z values 0.0 and 0.9999999999999999 | Python 3.13.18 |
| H-SVK-8 | Write a dependency sentence for every compute-to-render hand-off; it documents why the pass order is legal. | L | Fieldbook section 10, Light Lab ledger | read, not run |
| H-SVK-9 | Report a missing timestamp as `null`, never as CPU time, and keep device interval, CPU frame time and process latency apart. | L | Light Lab metrics `timing_scope` | read; `bench.py` run on lavapipe |
| H-SVK-10 | Treat a model-written primer as a lead; publish the corrected canon and keep the retractions as a ledger. | C | Fieldbook ledger, 19 rows | `Fieldbook.md` section 17 counted |
| H-SVK-11 | Do not read double-precision agreement as float32 GPU agreement; give the float32 twin its own tolerance. | L | Fieldbook VALIDATION.md; chapter 20 particle twin | read |

## Drills

### D-SVK-1 Find the X_ITE encode
- **Level:** L1 (look it up)
- **Task:** find the function that converts linear to display in the X_ITE 16.7.1 distribution and say its exponent.
- **Verify:** `grep -n "const float GAMMA" node_modules/x_ite/dist/x_ite.js` after `npm install x_ite@16.7.1`.
- **Answer:** line 67921, `GAMMA=2.2`, `linearToSRGB = pow(color, vec3(1./GAMMA))`.
- **Checked:** 2026-11-17 `X_ITE 16.7.1`, line 67921 read.

### D-SVK-2 Predict the three bytes
- **Level:** L2 (run a tool and compare)
- **Task:** before running, predict the centre byte of an emissive-0.5 sphere for UnlitMaterial and PhysicalMaterial under the default `ColorSpace`, then run `runs/shader-vulkan-20261117/probe/xite-furnace-colour.js` in `x3d.loom`.
- **Verify:** the `exp2_a_unlit_default` and `exp2_c_physical_default` rows of `xite-furnace-colour.json`.
- **Answer:** 128 and 186; exact sRGB would give 188.
- **Checked:** 2026-11-17 `X_ITE 16.7.1`, Chromium 153.0.8010.12, SwiftShader.

### D-SVK-3 Undo the fake loss
- **Level:** L2
- **Task:** the metal half-intensity rows read byte 186. Compute the linear value with the exact sRGB inverse and with the 2.2 inverse, and say which is right for X_ITE.
- **Verify:** `python3 -c "print(((186/255+0.055)/1.055)**2.4, (186/255)**2.2)"`.
- **Answer:** 0.4910 and 0.4995; the 2.2 inverse is right because it undoes what the shader wrote.
- **Checked:** 2026-11-17 Python 3.13.18.

### D-SVK-4 Write the depth test
- **Level:** L3 (break it, fix it, extend it)
- **Task:** implement forward-Z `z_ndc = (A z + B)/(-z)` and test z=-n and z=-f; then swap n and f for reversed-Z and say which two outputs change.
- **Verify:** the closed form in section 4 with n=0.1, f=100.
- **Answer:** forward gives 0.0 and 0.9999999999999999; reversed-Z gives about 1.0 and 0.0.
- **Checked:** 2026-11-17 Python 3.13.18 (forward values); reversed case reasoned.

### D-SVK-5 Same shader, other driver
- **Level:** L3
- **Task:** build the Light Lab, render 1440x900 at 4 samples with default flags on two Mesa/LLVM versions, and diff the images.
- **Verify:** `python3 -I runs/shader-vulkan-20261117/imgdiff.py beauty.png mine.ppm`.
- **Answer:** 258 of 3,888,000 bytes differ, max 14 of 255, against the shipped LLVM 19.1.7 image.
- **Checked:** 2026-11-17 Mesa 25.2.8 lavapipe, LLVM 20.1.2.

### D-SVK-6 Reproduce the Fieldbook lab
- **Level:** L2
- **Task:** run `run_lab.py` from the Fieldbook package and report case count and maximum difference.
- **Verify:** `labs/output/validation.json`.
- **Answer:** 745 cases, 1.6653345369377348e-16.
- **Checked:** 2026-11-17 CPython 3.13.18, GCC.

## Honest limits

- [C] No physical GPU, no WSL, no native window, in the authors' run or here; Light Lab timings are lavapipe numbers.
- [C] The X_ITE numbers are SwiftShader only; the furnace cube maps have no mip chain, so prefiltered IBL energy compensation was not tested.
- [C] `DisplayColorSpace=DISPLAY_P3` had no effect in a headless Chromium screenshot; this rig only.
- [S] The three.js, Babylon, Blender and Unreal encode functions were not re-read; statements about them are carried from reading, not run.
- [S] The WebGPU synchronisation and NDC-y statements were not re-read in the WebGPU specification.
- [L] The Fieldbook's Vulkan helper file was never compiled by its authors and not by us.
- [S] The 2.2-power encode is a candidate for the X_ITE maintainer and has not been reported upstream.

## Numbers register

| ID | Quantity | Value | Grade | Instrument | Source |
|---|---|---|---|---|---|
| N-SVK-1 | byte for linear 0.5 under X_ITE's 2.2 encode | 186 | C | X_ITE 16.7.1, Chromium 153.0.8010.12, SwiftShader | `x3d.loom@90f9862:runs/shader-vulkan-20261117/xite-furnace-colour.json` |
| N-SVK-2 | byte for linear 0.5 under exact sRGB | 187.52 (byte 188) | C | Python 3.13.18 | closed form |
| N-SVK-3 | X_ITE `GAMMA` constant | 2.2 | C | X_ITE 16.7.1 | `x_ite.js` line 67921 |
| N-SVK-4 | Unlit and legacy emissive 0.5, default `ColorSpace` | 128 | C | X_ITE 16.7.1, SwiftShader | `x3d.loom@90f9862:runs/shader-vulkan-20261117/xite-furnace-colour.json` |
| N-SVK-5 | rows in the X_ITE probe result | 41 | C | X_ITE 16.7.1, SwiftShader | `x3d.loom@90f9862:runs/shader-vulkan-20261117/xite-furnace-colour.json` |
| N-SVK-6 | largest 2.2-power vs sRGB gap, bytes (near linear 0.002) | 8.5 | C | Python 3.13.18 | closed form |
| N-SVK-7 | metal furnace, intensity 0.5, linear (2.2 inverse) | 0.4995 | C | X_ITE 16.7.1, SwiftShader | `x3d.loom@90f9862:runs/shader-vulkan-20261117/xite-furnace-colour.json` |
| N-SVK-8 | same bytes with exact sRGB inverse | 0.4910 | C | Python 3.13.18 | same |
| N-SVK-9 | dielectric 0.5 rough, intensity 1, linear | 0.5054 | C | X_ITE 16.7.1, SwiftShader | same |
| N-SVK-10 | Fieldbook lab C vs Python cases | 745 | C | CPython 3.13.18, GCC | Fieldbook `labs/output/validation.json`, re-run |
| N-SVK-11 | Fieldbook lab max difference | 1.6653345369377348e-16 | C | CPython 3.13.18, GCC | same |
| N-SVK-12 | Light Lab integration checks passed | 15 | C | Mesa 25.2.8 lavapipe, LLVM 20.1.2 | `x3d.loom@90f9862:runs/shader-vulkan-20261117/lightlab-rerun.json` |
| N-SVK-13 | image bytes differing across LLVM 19.1.7 and 20.1.2 | 258 of 3,888,000 | C | `imgdiff.py`, Mesa 25.2.8 | same |
| N-SVK-14 | Lambert furnace, 32 elevation bins | 0.500201 | C | Python 3.13.18; Light Lab guide | Light Lab `furnace.json` |
| N-SVK-15 | Fieldbook correction ledger rows | 19 | C | counted | Fieldbook `Fieldbook.md` section 17 |

## Sources and provenance

Public: `x3d.loom@90f9862` (this change) and the files cited in the table at the top, read at `x3d.loom@32f5ae7`. The two teaching packages were uploaded by the project owner, are not in a public repository, and were read and re-run in a scratch directory; their MIT-licensed Light Lab was not modified. X_ITE was installed from npm at 16.7.1 for the probe. Nothing was sent to any upstream project.
