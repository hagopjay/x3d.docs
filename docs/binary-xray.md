# Binary X-Ray: reverse engineering as a witnessed investigation (23 Nov 2026)

Code: x3d.xray `x3dray/binary/` (Pass A + Pass B, on main). Demo: x3d.demo `docs/demos/xray-binary/v1/` (Demo 74).
Fold-back: x3d.loom `LEARNINGS-xray-binary.md`, failure modes 199 to 203.
Method credit: ioma8, ["LLM assisted reverse engineering"](https://www.slowchronicle.com/posts/llm-assisted-reverse-engineering), Slow Chronicle, 18 Nov 2026.

## The idea in plain words

x3d.xray already turned a family of repositories into evidence, a graph and an X3D scene. The binary lens does the same
for a compiled program. It reads the program with standard tools (objdump, nm, file, strings), builds its call graph,
finds the function every path must pass through (the gatekeeper), and groups functions by what they can do (a
capability lattice). Then it does the part a reverse engineer actually spends time on: it keeps a **hypothesis ledger**.
Each row says what we think, the one experiment that would prove or disprove it, what we predicted and what happened.
The ledger idea comes from the Slow Chronicle article: it stops an analyst, human or AI, from going round in circles.
Here every row is code, so every verdict can be re-earned on another machine.

## The target: crackme1, and why "the debugger lies"

crackme1 is a small, self-authored teaching program: give it a name and a serial, and it says whether the serial is
right. It has three quiet defences: encrypted strings, a ptrace check that notices a debugger, and a scan of its own
code for breakpoint bytes (0xCC). When it notices a debugger it does not complain. It silently changes a hidden seed, so
the serial you read out of memory under the debugger is wrong in the real world.

| # | hypothesis | experiment | result here |
|---|---|---|---|
| H1 | strings are XOR-encrypted with a rolling key 0x33 + 7i | decode .rodata without running anything | 3 messages recovered; `strings` sees none of them |
| H2 | a constructor's ptrace check poisons the seed under a tracer | strace; read the seed in gdb | `PTRACE_TRACEME = -1 EPERM`; seed 0xa5a5a5a5 |
| H3 | the debugger lies | the serial computed for the poisoned seed, run under gdb and natively | F104-7CB6: accepted under gdb, rejected natively |
| H4 | beating both defences leaves the seed at 0 | LD_PRELOAD shim + no breakpoint inside the scanned bytes | seed 0x00000000 |
| H5 | the serial algorithm is understood well enough for a keygen | 2000 random names judged by the real program | 2000/2000 accepted, 200/200 altered serials rejected |
| H6 | (new) a breakpoint on the scanned function trips only the second defence | gdb with the shim, breakpoint on derive | seed 0x5a5a0000 exactly |

All six were re-run on one Linux x86-64 machine (gcc 13.3.0, GNU objdump 2.42, gdb 15.1, strace 6.8). H1 to H5 came
from an outside agent's ledger and agree with it; H6 is new.

## Four kinds of witness

| kind | what is kept | how it is checked again |
|---|---|---|
| static | the tool's argv and a hash of its output | run it again, compare the hash |
| static-decode | the bytes, the decoder model and a hash of the decoded text | run it again, compare |
| trace | the strace/gdb command, its environment, the extracted value | run it again, extract again, compare the value |
| oracle | the real program, run natively over seeded inputs and altered controls; a hash of the whole transcript | regenerate the inputs from the seed, rerun, compare |

Four gates guard the result: no number in the prose outside a slot filled from a record; every witness re-run (13/13
match); no "confirmed" without a re-run witness; and every drawn building or helix rung has a record, and every record
is drawn.

## The demo (Demo 74)

A city where each function is a building (height = instructions), import stubs are gates, hot roofs mark the
anti-debugging code and a gold spire marks the gatekeeper `main`. Call arcs carry moving packets. A ring of 48 tiles
around `derive` is the code `main` scans; in the "under gdb" world one tile turns red. A double helix holds one rung per
hypothesis, coloured by its re-run verdict, and a capability lattice floats behind the city. The static city was baked
in Blender 5.3.0 (Cycles, 384 samples) and exported by x3d-blender-io 2.7.4; the scene is XSD 4.0 valid with no semantic
warnings (x3d_mcp 4d433af) and was rendered in X_ITE 16.7.1 (SwiftShader).

## Limits

Symbolized build only for the trace probes; one machine and one CPU architecture; the keygen model is specific to this
program; frames come from a software renderer. The lens is for programs you wrote or are authorized to analyse.
