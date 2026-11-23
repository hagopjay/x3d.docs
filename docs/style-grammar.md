# A style vocabulary and grammar for X3D (23 Nov 2026)

Code and spec: x3d.loom `x3d.style/` ([SPEC.md](https://github.com/hagopjay/x3d.loom/blob/main/x3d.style/SPEC.md)). Demo: x3d.demo `docs/demos/style-loom/v1/` (Demo 75, Style Loom).
Fold-back: x3d.loom `LEARNINGS-style-loom.md`, failure modes 205 to 210.

## The idea in plain words

Our data demos kept coming out as a neon city at night. Nobody chose that; it was copied forward. This kit makes the look
a separate, small piece of data, so the same scene can be dressed many ways and each way can be checked before it is drawn.

- The **scene** says what is there: a ground, plates, masses, alerts, a hero, links, labels. Each mark has a *role* and data. No colour.
- The **style** is one sentence with ten parts: palette, surface, light, air, line, form, type, motion, encode, view.
- The **grammar** is 14 rules. Each is a measurement: a contrast ratio, a colour distance, a count.
- The **compiler** joins scene and style into X3D 4.0, and writes the style back into the file as Metadata.

It is the HTML and CSS split, with two additions: the style rides inside the X3D file, and it has a linter.

## The ten parts of speech

| part | answers | example tokens |
|---|---|---|
| palette | which colours, for which role | `ground`, `plate`, `mass`, `ink`, `accent`, `alert`, `haze`, `sky[]`, `categorical[]`, `sequential[]` |
| surface | how a body answers light | `model: unlit / phong / physical`, `tint`, `roughness`, `metallic`, `glow` |
| light | where from, how hard, how much baked shade | `azimuth`, `elevation`, `intensity`, `ambient`, `shadow`, `contact`, `relief` |
| air | what is between eye and distance | `fog: none / linear / exp`, `range` |
| line | what is drawn as line | `edges: none / ink / data`, `links: line / tube`, `grid: none / lines / rings` |
| form | the shape of a mass | `sides`, `taper`, `tiers`, `inset`, `cap: flat / spike` |
| type | how labels are set | `family`, `size`, `case`, `density` |
| motion | what moves | `pulse`, `flow` (seconds) |
| encode | data channel → visual channel | `hue: category / value / mono`, `alert: color / glow` |
| view | first look | `projection: perspective / ortho`, `start: hero / plan / street` |

## A style, whole

```json
{ "@id": "xst:maquette", "@type": "Style", "label": "Paper Maquette",
  "intent":  { "key": "high", "mood": ["calm", "honest"], "use": "form and proportion first, one thing flagged" },
  "palette": { "ground": "#e9e4d8", "plate": "#f3efe6", "mass": "#ffffff", "ink": "#3a3632", "accent": "#c8a04a", "alert": "#e4572e",
               "haze": "#ece9e2", "sky": ["#cfd9e2", "#ece9e2"], "categorical": ["#3d6f9e", "…"], "sequential": ["#f4f1ea", "…"] },
  "surface": { "model": "phong", "tint": 0.0, "roughness": 0.95 },
  "light":   { "azimuth": 215, "elevation": 38, "ambient": 0.55, "shadow": 0.55, "contact": 0.7 },
  "air":     { "fog": "linear", "range": 4 },
  "line":    { "edges": "none", "links": "tube" },
  "form":    { "sides": 4, "tiers": 1, "fill": 0.78 },
  "encode":  { "hue": "mono", "alert": "color" },
  "view":    { "projection": "perspective", "start": "hero" } }
```

Anything left out takes a default. `intent.key` is a promise: "this is a bright style". The linter holds the palette to it and the render receipt holds the frame to it.

## The rules, as questions

| rule | question it asks | number it needs |
|---|---|---|
| G1 | Did the style say all ten parts? | 0 missing tokens |
| G2 | Can the labels be read? | contrast ≥ 4.5:1 |
| G3 | Do the bodies stand off the plate? | colour distance ≥ 0.10, or an edge line, or shade on a light body |
| G4 | Can the categories be told apart, also by colour-blind readers? | ≥ 0.08, and ≥ 0.04 in simulation |
| G5 | Does more look like more? | lightness ramp in one direction, span ≥ 0.30 |
| G6 | Does the alert jump out? | ≥ 0.15 from every body |
| G7 | Are alerts rare enough to mean something? | ≤ 15% of marks |
| G8 | If something glows, is it dark enough to see? | ground lightness ≤ 0.35 |
| G9 | Does the light fit the surface? | unlit casts no shadow |
| G10 | Does the fog match the horizon? | within 0.08 |
| G11 | Is the motion calm? | pulse ≥ 0.5 s |
| G12 | Is the plate a quiet step? | 0.02 to 0.2 off the ground |
| G13 | Can this palette be lent to another style? | ≥ 4 categories, ≥ 3 ramp stops |
| G14 | Is the declared key honest? | ground lightness in the declared band |

Distances are Delta E in OKLab; about 0.02 is one just-noticeable step.

## Four ways to get a new style without writing one

| operator | plain words | what the 288-sentence run showed |
|---|---|---|
| transpose | wear another style's colours | 71 of 144 valid as written, 98 after repair |
| invert | day becomes night | 33 of 144 valid: not a free night mode |
| mix | halfway between two styles | a continuum; many midpoints are invalid, and the linter says which |
| repair | nudge lightness until the rules pass | fixes 54 of 184 failures; the rest need a new alert colour or key |

## What the first run found

- **4 of 12 hand-written styles broke a rule**, including the neon look every demo used: two of its category colours merge for red-green colour-blind readers (0.020 apart in simulation; 0.04 needed). Fix: two colours moved by about one noticeable step.
- **A frame overruled a rule.** A sentence passed all 10 applicable rules and drew a black picture. The rule was wrong, was tightened, and has a test.
- **The first scoring formula rewarded cheating.** Throwing the input away scored 0.70, repairing it 0.67. Fixed before any optimizer saw it.

## Tag your own X3D so a style can address it

```xml
<Group DEF='XST_World'>
  <MetadataSet containerField='metadata' name='xst:Style' reference='https://hagopjay.github.io/x3d.loom/ns/style#maquette'>
    <MetadataString containerField='value' name='xst:palette_ground' value='"#e9e4d8"'/>
    <!-- 47 more tokens -->
  </MetadataSet>
  <Group DEF='Role_alert'>
    <MetadataString containerField='metadata' name='xst:role' reference='https://hagopjay.github.io/x3d.loom/ns/style#' value='"alert"'/>
    <!-- shapes -->
  </Group>
</Group>
```

Put the style on the root `Group`, not on `WorldInfo`: metadata on `WorldInfo` is lost on the way to glTF. Use `_` in names, not `.`: the validator warns about dots.

The same name, `xst:palette_ground`, is the X3D Metadata name, the JSON-LD term and the RDF predicate. The vocabulary is published as OWL + SKOS with SHACL shapes, all generated from the code, and the style survives X3D → glTF (`KHR_xmp_json_ld`) → X3D for 12 of 12 worlds.

## For an optimizer (DSPy or other)

`node bin/eval.mjs tasks` gives 196 tasks; `node bin/eval.mjs score <task-id> < style.json` gives one number in 0..1. The deterministic repair scores 0.646 on the 87 dev tasks; a perfect answer scores 1.0. `evals/dspy_socket.py` is the seam for MIPROv2 or GEPA. It is switched off and has never called a model.

## Numbers and their instruments

| number | instrument |
|---|---|
| 12 of 12 worlds XSD 4.0 valid, 0 warnings | x3d_mcp fork 4d433af |
| 22 frames, 12 of 12 styles in their declared luminance band | X_ITE 16.7.1, Chromium 157 (Playwright), SwiftShader; no hardware GPU |
| 288 sentences: 104 valid, 158 after repair | x3d.style `lint` and `repair`, Node 22 |
| colour-blind distances | Machado, Oliveira, Fernandes 2009 simulation at severity 1.0: a model, not readers |
| 555 + 455 triples, SHACL conforms, 6 of 6 broken styles rejected | rdflib 7.6.0, pyshacl 0.40.2 |
| glTF round trip 12 of 12 | x3d.loom `x3dsem 0.1.0`, rules S0..S6 |
