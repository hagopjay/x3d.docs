# x3d.docs

AST teardowns of six X3D code bases, published with GitHub Pages: **x3d-blender-io, x3d_mcp, x3d.loom, x3d.onto, x3d.demo and X_ITE 16.7.0**.
Site files live in `docs/`; open `docs/index.html` or the Pages site, https://hagsmac.github.io/x3d.docs/. Each folder holds the write-up (`MASTERCLASS.md`, also as `MASTERCLASS.html`), a scene index,
a viewer (`view.html?scene=…`) and validated X3D 4.0 scenes under `scenes/`.

* Analysis: Python `ast`, the TypeScript compiler's parser, an XML walk over every `.x3d` file, git and the GitHub API; X3D vocabulary from the X3D Unified Object Model 4.1.
* Labels: measured numbers are plain; heuristics are marked *inferred*; PR statements are marked *claimed*.
* Rendering: bundled X_ITE 16.7.0 (MIT, `vendor/x_ite/LICENSE.md`). Every scene passes the x3d_mcp validator (XSD 4.0, 0 errors, 0 warnings).

## X3D Elucidation (`docs/learn/`)

The deep-learning base for people who already believe in X3D: twenty-three chapters (one of them the methods chapter) and seven appendices. Every number names its validator, renderer
or rig; every claim carries a grade (Confirmed, Likely, Suspected); every chapter ends in drills with answer keys. Start at `docs/learn/00-start-here.md`
(site: `learn/index.html`). Rules for writing and growing it: `docs/learn/AUTHORING.md`. Rebuild and lint:

```bash
pip install markdown-it-py mdit-py-plugins
python3 docs/tools-shared/check_learn.py --warn --summary
python3 docs/tools-shared/build_learn.py
```

See also: [x3d.gobbler field notes](docs/x3d.gobbler/FIELD-NOTES.md): how this repo's `tools-shared` helpers are pinned by the Gobbler Atlas witness.
