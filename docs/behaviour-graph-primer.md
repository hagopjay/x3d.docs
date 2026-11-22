# Scripting primer: the X3D behaviour graph methods

This is a primer for the new methods in `x3d-blender-io/source/behaviour_graph.py` and `behaviour_sim.py`. It is not a Blender scripting
primer: everything on this page except the last section runs in plain Python, with no Blender installed. Every code
block here was run before publishing (22 Nov 2026, Python 3.13.18), and the printed output is what it printed.

Set up once. The module is one file with one generated neighbour, and needs nothing but Python:

```python
import sys
sys.path.insert(0, "x3d-blender-io/source")      # the folder that holds behaviour_graph.py
from behaviour_graph import Behaviour, BehaviourError
```

## 1. The whole idea in ten lines

A scene has shapes. A behaviour graph says what happens. You build the graph, then weave it into the scene.

```python
scene = """<?xml version="1.0" encoding="UTF-8"?>
<X3D profile="Immersive" version="4.0"><Scene>
  <Transform DEF="Door"><Shape><Box size="1.5 2.4 0.1"/></Shape></Transform>
  <Transform DEF="Button" translation="-2 1 0"><Shape><Sphere radius="0.3"/></Shape></Transform>
</Scene></X3D>
"""

b = Behaviour()
click = b.add("TouchSensor", "Click", parent="Button")
timer = b.add("TimeSensor", "Timer", cycleInterval=3)
slide = b.add("PositionInterpolator", "Slide", key=[0, 1], keyValue=[(0, 0, 0), (0, 2.5, 0)])
door = b.target("Transform", "Door")

click.touchTime >> timer.startTime
timer.fraction_changed >> slide.set_fraction
slide.value_changed >> door.translation

print(b.explain())
```

```text
TouchSensor Click.touchTime --SFTime--> TimeSensor Timer.startTime
TimeSensor Timer.fraction_changed --SFFloat--> PositionInterpolator Slide.set_fraction
PositionInterpolator Slide.value_changed --SFVec3f--> Transform Door.translation
```

```python
x3d = b.weave(scene)            # the scene with the graph written into it
print(x3d.count("<ROUTE"), "ROUTEs written")
```

```text
3 ROUTEs written
```

Save `x3d` to a file and open it in X_ITE: click the sphere and the box rises.

## 2. The methods

| Method | What it does | Returns |
|---|---|---|
| `Behaviour()` | an empty graph | the graph |
| `b.add(type, name=None, parent=None, **fields)` | a new behaviour node; `name` is its DEF (made up if left out); `parent` is the DEF of the Transform a sensor sits in | a handle |
| `b.target(type, name)` | a part of the scene a wire may start or end at, by the DEF it has in the scene | a handle |
| `handle.field` | one field of the node, ready to be wired | a port |
| `port >> port` | a ROUTE, checked as it is made | the right-hand node's handle |
| `handle.set(**fields)` | give fields a value | the handle |
| `b.get(name)` | the handle of a node already in the graph | a handle |
| `b.connect(port, port)` / `b.disconnect(port, port)` | the same as `>>`, and its undo | a route / True or False |
| `b.remove(name)` | take a node out, with every wire that touches it | nothing |
| `b.check()` | every problem in the graph | a list, empty when all is well |
| `b.explain()` | one sentence per ROUTE | text |
| `b.weave(scene_text)` | the scene with the graph written in | X3D text |
| `Behaviour.from_x3d(text)` | the graph already inside an X3D file | a graph |
| `strip(text)` | an X3D file with its behaviour taken out | X3D text |
| `to_json(b)` / `from_json(data)` | the graph as plain data and back | a dict / a graph |
| `difference(before, after)` | what changed between two graphs | a dict of five lists |
| `route_verdict(type, field, type, field)` | would X3D allow this wire? | `"ok"` or an error code |

## 3. Values: write Python, get X3D

You give field values as ordinary Python. They are turned into the text X3D uses.

```python
from behaviour_graph import to_lexical
print(to_lexical(True))
print(to_lexical(2.5))
print(to_lexical((0, 1, 0)))
print(to_lexical([(0, 0, 0), (0, 2, 0.5)]))
print(to_lexical(["hello", "world"], "MFString"))
```

```text
true
2.5
0 1 0
0 0 0 0 2 0.5
"hello" "world"
```

A string is passed through untouched, so `keyValue="0 0 0 0 2 0"` also works. Numbers are in X3D's own space: Y is up,
lengths are metres, angles are radians, and a rotation is an axis followed by an angle.

## 4. The rule, and what a mistake looks like

A ROUTE joins an output to an input of the same field type. The methods refuse anything else at the line where you
write it, and the message names both types.

```python
try:
    click.isActive >> timer.startTime
except BehaviourError as error:
    print(error.code)
    print(error)
```

```text
type-mismatch
Click.isActive is SFBool but Timer.startTime is SFTime: a ROUTE joins fields of one type
```

```python
try:
    timer.startTime >> click.touchTime
except BehaviourError as error:
    print(error.code)
    print(error)
```

```text
wrong-direction
TouchSensor.touchTime is outputOnly: it cannot be a ROUTE destination
```

```python
try:
    b.add("TimeSensr")
except BehaviourError as error:
    print(error)
```

```text
'TimeSensr' is not a behaviour node; did you mean TimeSensor?
```

```python
try:
    timer.set(isActive=True)
except BehaviourError as error:
    print(error)
```

```text
TimeSensor.isActive is outputOnly: an event carries values while the scene runs, it cannot be given one beforehand
```

| Code | Meaning |
|---|---|
| `unknown-node` | no such node type in the catalogue |
| `unknown-field` | the node has no such field (the message lists the ones it has) |
| `wrong-direction` | the field cannot be a source, or cannot be a destination |
| `type-mismatch` | the two ends have different field types |
| `event-has-no-value` | you tried to give a value to an event |
| `duplicate-def` | two nodes with one name |
| `unknown-def` | a name that is not in the graph, or a target that is not in the scene |

You can ask before you wire:

```python
from behaviour_graph import route_verdict
print(route_verdict("TouchSensor", "isOver", "TimeSensor", "startTime"))
print(route_verdict("TouchSensor", "isOver", "TimeTrigger", "set_boolean"))
print(route_verdict("TimeTrigger", "triggerTime", "TimeSensor", "startTime"))
```

```text
type-mismatch
ok
ok
```

That is the standard pattern for a type that does not fit: find the node that converts it.

| You have | You need | Use |
|---|---|---|
| yes / no (SFBool) | a time (SFTime) | TimeTrigger |
| a time (SFTime) | yes (SFBool) | BooleanTrigger |
| a time (SFTime) | a number running 0 to 1 (SFFloat) | TimeSensor |
| a number (SFFloat) | a place (SFVec3f) | PositionInterpolator |
| a number (SFFloat) | a turn (SFRotation) | OrientationInterpolator |
| a number (SFFloat) | a colour (SFColor) | ColorInterpolator |
| yes / no (SFBool) | a whole number (SFInt32) | IntegerTrigger |

## 5. What fields does a node have?

Ask the catalogue. It is generated from the X3D Unified Object Model, so it is the standard's own list.

```python
from behaviour_graph import field_rows
for name, kind, access, default in field_rows("BooleanFilter"):
    print(f"{name:12} {kind:8} {access}")
```

```text
inputFalse   SFBool   outputOnly
inputNegate  SFBool   outputOnly
inputTrue    SFBool   outputOnly
set_boolean  SFBool   inputOnly
```

`inputOnly` fields are inputs. `outputOnly` fields are outputs. `inputOutput` fields are both: you can wire into
`door.translation` and you can wire out of it, because a Transform sends its translation every time it changes.
`initializeOnly` fields can be set but not wired.

## 6. Change a file that already exists

```python
from behaviour_graph import strip, difference

g = Behaviour.from_x3d(x3d)                      # read the graph out of the file from section 1
g.get("Timer").set(cycleInterval=6)              # slower
spin = g.add("OrientationInterpolator", "Spin", key=[0, 1], keyValue=[(0, 1, 0, 0), (0, 1, 0, 3.14)])
g.get("Timer").fraction_changed >> spin.set_fraction
spin.value_changed >> g.get("Door").rotation

changed = g.weave(strip(x3d))                    # take the old behaviour out, write the new one in
report = difference(Behaviour.from_x3d(x3d), Behaviour.from_x3d(changed))
print(report["fields_changed"])
print(report["nodes_added"])
print(len(report["routes_added"]), "routes added,", len(report["routes_lost"]), "lost")
```

```text
{'Timer': {'cycleInterval': ('3', '6')}}
['Spin']
2 routes added, 0 lost
```

`difference` is how you prove an edit did what you meant and nothing else. An AI agent that edits a graph can be held
to the same proof.

## 7. The graph as data

```python
import json
from behaviour_graph import to_json, from_json

data = to_json(b)
print(data["schema"])
print(json.dumps(data["routes"][0]))
print(from_json(data).explain() == b.explain())
```

```text
x3d-blender-io.behaviour-graph/v0
["Click", "touchTime", "Timer", "startTime"]
True
```

## 8. A complete second example: a counter with no code

Two node types, wired in a chain, count in binary. `BooleanToggle` flips each time it hears yes. `BooleanFilter`'s
`inputNegate` says yes when its input says no, which is the moment a bit rolls over from 1 to 0.

```python
c = Behaviour()
press = c.add("TouchSensor", "Press", parent="Button")
previous = press.isActive
for bit in range(4):
    flip = c.add("BooleanToggle", f"Flip{bit}")
    previous >> flip.set_boolean
    flip.toggle >> c.target("Transform", f"Bit{bit}").visible
    carry = c.add("BooleanFilter", f"Carry{bit}")
    flip.toggle >> carry.set_boolean
    previous = carry.inputNegate
print(len(c.routes), "ROUTEs,", c.check())
```

```text
12 ROUTEs, []
```

A loop builds the chain, which is the point of scripting: four bits or forty is the same six lines.

## 9. Run it without a browser

`behaviour_sim.py` sits beside `behaviour_graph.py` and plays a graph in plain Python. You say what time it is and what
the pointer did; it tells you every value that reached the scene. These blocks reuse `b`, the door from section 1.

```python
from behaviour_sim import Simulation

sim = Simulation(b)
sim.start(0.0)                      # the world loads at time 0
print(sim.step(1.0))                # one second later: nothing has happened
print(sim.click("Click", 2.0))      # the pointer clicks the button at 2 s
print(sim.step(3.5))                # 1.5 s into the 3 s cycle
```

```text
[]
[('Door', 'translation', (0.0, 0.0, 0.0))]
[('Door', 'translation', (0.0, 1.25, 0.0))]
```

Each answer is a list of (target, field, value). The click started the timer in the same instant, so the door got its
first value at once. Half way through the cycle it is half way up.

| Method | What it does |
|---|---|
| `Simulation(graph)` | a graph, ready to run |
| `sim.start(now)` | begin: looping timers start, followers that are not at rest wake up |
| `sim.step(now)` | move time forward to `now`; returns what reached the scene |
| `sim.click(sensor, now, held=0)` | press and release a TouchSensor |
| `sim.press(sensor, now, point)` / `sim.drag(sensor, point, now)` / `sim.release(sensor, now)` | the pointer, one move at a time (a PlaneSensor follows the drag) |
| `sim.hover(sensor, True or False, now)` | the pointer goes over or leaves |
| `sim.send(node, field, value, now)` | deliver a value to an input, as a ROUTE would |
| `sim.post(node, field, value, now)` | send a value out of an output, as the node would |
| `sim.values[(target, field)]` | the last value that reached a target |
| `sim.outputs[(node, field)]` | the last value any node sent |
| `sim.log` | every event sent: (time, node, field, value) |
| `sim.not_simulated` | the nodes this simulator does not run, by name |

The log is the whole story of a step, in order:

```python
for when, node, field, value in list(sim.log)[-4:]:
    print(when, node, field, value)
```

```text
3.5 Timer elapsedTime 1.5
3.5 Timer time 3.5
3.5 Slide value_changed (0.0, 1.25, 0.0)
3.5 Door translation (0.0, 1.25, 0.0)
```

```python
print(sim.values[("Door", "translation")])
print(sim.outputs[("Timer", "isActive")])
print(sim.step(9.0), sim.outputs[("Timer", "isActive")])
```

```text
(0.0, 1.25, 0.0)
True
[('Door', 'translation', (0.0, 2.5, 0.0))] False
```

The counter from section 8, pressed eleven times, with no browser anywhere:

```python
count = Simulation(c)
count.start(0.0)
for presses in range(1, 12):
    count.click("Press", float(presses), held=0.1)
lamps = [count.values.get((f"Bit{bit}", "visible"), False) for bit in range(4)]
print(lamps, sum(1 << bit for bit, lit in enumerate(lamps) if lit))
```

```text
[True, True, False, True] 11
```

A follower, watched closing in. After one `tau` a first-order damper has covered 63% of the distance:

```python
g = Behaviour()
soft = g.add("PositionDamper", "Soft", tau=0.5, order=1)
soft.value_changed >> g.target("Transform", "Ball").translation
s = Simulation(g)
s.start(0.0)
s.send("Soft", "set_destination", (10, 0, 0), 0.0)
for t in (0.5, 1.0, 2.0, 4.0):
    s.step(t)
    print(t, round(s.values[("Ball", "translation")][0], 3))
```

```text
0.5 6.321
1.0 8.647
2.0 9.817
4.0 9.997
```

A drag on a PlaneSensor:

```python
grab = Behaviour()
handle = grab.add("PlaneSensor", "Grab", parent="Head")
handle.translation_changed >> grab.target("Transform", "Head").translation
d = Simulation(grab)
d.start(0.0)
d.press("Grab", 1.0, point=(0, 0, 0))
print(d.drag("Grab", (2, 1, 0), 1.2))
d.release("Grab", 1.3)
```

```text
[('Head', 'translation', (2.0, 1.0, 0.0))]
```

What it cannot run, it says:

```python
g.add("SplinePositionInterpolator", "Curve")
print(Simulation(g).not_simulated)
```

```text
['SplinePositionInterpolator Curve']
```

**Is it right?** The simulator was checked against the X_ITE browser (16.7.1), event by event, with real mouse clicks:
36 of 36 event streams agree on four files (exact nodes within 0.002, followers within 0.08). The recorded traces are in
the add-on's `tests/behaviour/x_ite_traces/` and are replayed by its tests. This is why a script, or an AI agent, can
ask "what will this scene do?" and get the browser's answer without a browser.

## 10. Inside Blender

In Blender the same graph is shown as a node tree. Build the graph exactly as above, then:

| Function | What it does |
|---|---|
| `behaviour_nodes.target(graph, object)` | add a Blender object, camera, light or material to the graph as a wire end |
| `behaviour_nodes.apply(graph, scene)` | show the graph as the scene's X3D Behaviour node tree |
| `behaviour_nodes.read(scene)` | the node tree back as a graph |
| `behaviour_play.Player(scene)` | the simulator, running on the scene's own objects: `start`, `step`, `press(object, now)`, `release`, `click`, and `stop()` to put everything back |

Export then writes the graph into the X3D file. Importing an X3D file with "Behaviour as node graph" ticked builds the
tree from the file. The Play button in the node editor is `Player` driven by the mouse. All of it except the mouse works
without a window, so a script or an AI agent can do it.
