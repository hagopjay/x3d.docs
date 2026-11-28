# Live DIS: the six X3D DIS nodes on real IEEE 1278.1 PDU bytes (28 Nov 2026)

Demo 85, x3d.demo `docs/demos/live-dis/v1/`. Learnings are in x3d.loom `LOOM-v1.md`, failure modes 551 to 558.

## What DIS is, in two sentences

Distributed Interactive Simulation (IEEE 1278.1) is the wire format military and training simulators use to tell each other where things are: each simulator broadcasts small binary packets (PDUs) about its own entities, and every other simulator draws them. Because packets are sparse, the receiver moves each entity between packets by dead reckoning, using one of nine standard algorithms named in the packet.

X3D 4.0 has a DIS component with six nodes. This demo makes all six work in a browser.

## The count

| Measure | Result | Grade |
|---|---|---|
| DIS nodes X_ITE 16.8.1 parses, with every specification field | 6 of 6 (233 fields) | C |
| DIS nodes X_ITE 16.8.1 implements itself | 0 of 6 | C |
| Nodes live as reader with the demo's runtime | 6 of 6 | C |
| Nodes live as writer | 4 of 4 that have a writer mode | C |
| Dead-reckoning algorithms checked against a closed form and RK4 | 9 of 9, worst position error 3.9e-11 m | C |
| Codec against opendis 1.1.0 (Python) | 160 PDUs both ways, 0 field mismatches | C |
| Codec against open-dis 1.3.6 (JavaScript) | 160 PDUs, 0 field mismatches | C |
| Tests | 37 of 37 | C |

Rig: X_ITE 16.8.1, headless Chromium 158 on SwiftShader, Node 22.23.5, UDP on loopback. C means confirmed by a run made for the demo.

## The six nodes

| Node | What it does | Live means |
|---|---|---|
| EspduTransform | a Transform that an Entity State PDU moves | position and rotation follow the PDU plus dead reckoning; marking, type and `isActive` are set |
| DISEntityManager | announces entities as they appear and time out | `addedEntities` and `removedEntities` fire and ROUTEs put models in and take them out |
| DISEntityTypeMapping | picks a model by entity type | the ship gets the ship model |
| TransmitterPdu | a radio's state, frequency and power | fields equal the PDU; a ROUTE lights a lamp |
| SignalPdu | the radio's audio or data | 160 mu-law samples per PDU arrive in `data`, are drawn and can be played |
| ReceiverPdu | who is receiving whom | state and received power equal the PDU |

"Live" has four stated points, the same for every node: the file is valid X3D 4.0, X_ITE builds the node, fields with the specification's names take values from decoded PDU octets and read back equal to what was sent, and an X3D author can use the change through a ROUTE.

## How to read it

- **X_ITE parses these nodes and does nothing with them.** No warning, no socket, and the children of an EspduTransform are drawn at the origin. A count of parsed nodes would have called this 6 of 6 before any work was done.
- **Every PDU on the public page is generated.** A static page has no network, so a scripted exercise is encoded to DIS octets in the tab and those octets go through the same decoder a packet would. "Real" refers to the byte format, checked against two independent libraries. No recording and no third-party data is used.
- **The network path was run on one machine only.** A Node gateway relays UDP to WebSocket; a Python sender, the gateway and the browser were tested on loopback. No real network and no other vendor's simulator has seen it.
- **Both reference libraries were wrong somewhere.** opendis writes a 28-octet Receiver PDU where the standard has 36; the JavaScript open-dis misreads Transmitter fields after the frequency. Two references were needed to cover every field.

## Limits

Only PDU types 1, 25, 26 and 27 are decoded, so firing, detonation and collision fields stay at their defaults. The use of two rotation matrices in the body-frame algorithms is one reading of the standard's table (L). The mapping from DIS axes to X3D axes is the demo's choice (S). The runtime sets outputOnly fields through an internal X_ITE call, so it is pinned to 16.8.1.

README, receipt, tests and learnings: x3d.demo `docs/demos/live-dis/v1/` (PR 199).
