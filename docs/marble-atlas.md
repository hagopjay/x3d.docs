# Marble's successor, Atlas, in X3D: cameras you can check (23 Nov 2026)

Demo: x3d.demo `docs/demos/marble-atlas/v1/` (Demo 76). Code: `kit/atlas2x3d.py` there.
Fold-back: x3d.loom `LEARNINGS-marble-atlas.md`, failure modes 224 to 228; `docs/MARBLE-SPLATS.md` section 5.

## The idea in plain words

World Labs' Marble turned a picture into a 3D world made of Gaussian splats. On 12 Nov 2026 the company opened
**Atlas**, the model it says will power future Marble versions, with a new API. Atlas no longer hands back only a
finished world. Its basic unit is a **posed frame**: a camera (where it stood, which way it looked, how wide its lens
was), the picture, a depth map and a confidence map. From frames it can make splats (SPZ) and turn splats into a mesh
with simple collision boxes (GLB).

Each of those has a natural X3D home:

| Atlas gives | X3D node | Checked how |
|---|---|---|
| camera | `Viewpoint` (position, orientation, fieldOfView) | X_ITE draws the room through each Viewpoint; 99.94% of pixels show the same object the camera saw |
| depth + confidence | `PointSet` or `GaussianSplats` | every point lands within 0.0005 mm of the true surface |
| splats (SPZ) | `GaussianSplats` | SPZ write/read round trip within 0.12 mm |
| mesh + collider boxes (GLB) | `Inline` + `Collision` with `Box` proxies | 19 boxes, exact |

The good news for X3D: Atlas uses the same axes X3D does (Y up, looking down −Z), so unlike raw Marble files no flip is
needed. The bad news is that every easy mistake is huge and silent: reading the depth rows upside down, treating
the pose as the inverse, or relabelling an OpenCV pose without converting it each put points metres away (2.1, 3.3
and 6.4 m on average). The demo measures each one, so a converter can be tested against them.

## Why it matters for the flywheel

A camera is something a validator can hold to account. "The splat looks right" is an opinion; "99.94% of pixels
agree, and these three known mistakes score 49%, 16% and 0%" is a receipt. That is the tether, applied to
generated worlds.

## Cost and rights, briefly

Nothing was spent: the rig is the real one from World Labs' open-source skills (Apache-2.0), the room is ours (CC0).
A refined splat run costs $5 and a draft $0.50 (Atlas docs, 23 Nov). Output made on a free account belongs to World Labs
and is for personal, non-commercial use only, so anything to be published must come from paid access.
