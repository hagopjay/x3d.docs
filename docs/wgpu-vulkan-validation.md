# Vulkan validation in x3d.wgpu receipts

Every x3d.wgpu conformance receipt (`x3d-wgpu-conformance/2`) records what the Khronos validation layer reported while the rows rendered.

- Switch: `X3D_VVL=on` asks for the layer; `X3D_VVL=require` also fails the run if the layer is not loaded or any error outside the known-errors list appears. CI uses `require`.
- Receipt block `api_validation`: layer, layer version, counts of errors and warnings, message ids, known errors, errors wgpu itself hides, and a log hash.
- Known error today: `SYNC-HAZARD-READ-AFTER-WRITE` on wide lines (cause not found).
- Not in receipts: SSIM/PSNR (rows are probes).
- Verified on software Vulkan (lavapipe); a real-GPU run is still to do.

Full details: hagopjay/x3d.wgpu `docs/VVL.md` and `docs/RECEIPT-SCHEMA.md` (PR #7). Learnings: x3d.loom `LEARNINGS-wgpu-vvl.md`.
