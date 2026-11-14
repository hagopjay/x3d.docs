# x3d.docs

AST teardowns of six X3D code bases, published with GitHub Pages: **x3d-blender-io, x3d_mcp, x3d.loom, x3d.onto, x3d.demo and X_ITE 16.7.0**.
Open `index.html` (or the Pages site). Each folder holds the write-up (`MASTERCLASS.md`, also as `MASTERCLASS.html`), a scene index,
a viewer (`view.html?scene=…`) and validated X3D 4.0 scenes under `scenes/`.

* Analysis: Python `ast`, the TypeScript compiler's parser, an XML walk over every `.x3d` file, git and the GitHub API; X3D vocabulary from the X3D Unified Object Model 4.1.
* Labels: measured numbers are plain; heuristics are marked *inferred*; PR statements are marked *claimed*.
* Rendering: bundled X_ITE 16.7.0 (MIT, `vendor/x_ite/LICENSE.md`). Every scene passes the x3d_mcp validator (XSD 4.0, 0 errors, 0 warnings).
