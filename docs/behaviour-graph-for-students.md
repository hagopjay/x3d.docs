# How a 3D scene comes alive: a student's guide to X3D behaviour graphs

You do not need to know any programming to read this. You need curiosity and about half an hour. Open the
[Wire Lab](https://hagopjay.github.io/x3d.demo/demos/wire-lab/v1/?world=door) in another tab and try each thing as you
read it. Nothing you do there can break anything, and "Start over" puts it back.

## 1. A scene that does nothing

A 3D file can describe a door: a flat box, this wide, this tall, this colour, standing here. That is a picture of a
door. It will never open. Most 3D file formats stop here.

X3D is an international standard for 3D scenes (ISO/IEC 19775), and it goes one step further. An X3D file can also say
what happens: when someone clicks the button, the door rises. That part of the file is called its behaviour. This guide
is about how behaviour is written, why it is written that way, and how you can rewire it yourself.

## 2. Events: small messages with a kind

When something happens in a scene, a small message is sent. X3D calls it an event. Every event has a kind.

| Kind | X3D name | Dot colour in the lab | An example |
|---|---|---|---|
| yes or no | SFBool | red | "the pointer is over the button": yes |
| a time | SFTime | amber | "the button was clicked at 14:03:07.25" |
| a number | SFFloat | grey | "the timer is 40% done": 0.4 |
| a place | SFVec3f | blue | "be at 0, 3.7, 0" |
| a turn | SFRotation | purple | "turn a quarter circle around the up axis" |
| a colour | SFColor | yellow | "be orange": 1, 0.5, 0 |
| a whole number | SFInt32 | green | "show picture number 3" |

Here is the first surprise. A click is not a yes. A click is a time: the exact moment it happened. That turns out to be
far more useful, because the next thing in line usually wants to know when to start.

## 3. Nodes: little machines with labelled plugs

The things that send and receive events are called nodes. Each node is a small machine that does one job. Its plugs
are called fields. Some plugs only send (outputs, on the right of a node in the lab). Some only receive (inputs, on the
left). Some do both.

| Node | Its one job | Hears | Says |
|---|---|---|---|
| TouchSensor | notices the pointer on a shape | nothing | `touchTime` (a time), `isOver` (yes or no) |
| TimeSensor | a stopwatch | `startTime` (a time) | `fraction_changed`: a number that runs from 0 to 1 |
| PositionInterpolator | turns a number into a place | `set_fraction` (a number) | `value_changed` (a place) |
| Transform | holds a shape somewhere | `translation` (a place) | `translation` (a place), whenever it moves |

An interpolator is worth a second look, because the idea is everywhere in animation. You give it a few key moments
and where the object should be at each one:

| When (key) | Where (keyValue) |
|---|---|
| 0 | on the ground |
| 0.4 | up high |
| 0.6 | still up high |
| 1 | on the ground again |

Now feed it any number between 0 and 1 and it answers with the place in between. At 0.2 it is halfway up. You wrote
four lines and got smooth motion for every instant.

## 4. ROUTEs: the wires

A wire from one plug to another is called a ROUTE. A ROUTE has one rule:

> A ROUTE joins an output to an input of the same kind.

Time goes to time. Place goes to place. That is the whole rule. Here is the door, all of it:

```text
TouchSensor Click.touchTime        --a time-->    TimeSensor Timer.startTime
TimeSensor Timer.fraction_changed  --a number-->  PositionInterpolator Slide.set_fraction
PositionInterpolator Slide.value_changed --a place-->  Transform Door.translation
```

Read it aloud. The click tells the stopwatch when to start. The stopwatch counts from 0 to 1. The interpolator turns
that count into a height. The height moves the door. Three wires.

**Try it.** In the lab, click the red button and watch the wires flash as the events go by. The list under the picture
shows every event as it happens.

## 5. The rule is a teacher

Try to make the door open when the pointer only hovers over the button. The TouchSensor has an output called `isOver`.
Drag a wire from `isOver` to the timer's `startTime`.

It is refused. `isOver` says yes or no. `startTime` wants a time. A yes is not a time.

This is not the lab being fussy. It is the rule doing its job: it caught a mistake before the scene ever ran. The
question becomes, what turns a yes into a time? X3D has a node for exactly that, called TimeTrigger. Add one, wire
`isOver` into it and its `triggerTime` into the timer, and hovering opens the door.

Engineers call this a type system. You have just used one. The same idea keeps spacecraft software and bank software
from mixing up things that must not be mixed up.

| I have | I need | The node that converts |
|---|---|---|
| a yes | a time | TimeTrigger |
| a time | a yes | BooleanTrigger |
| a time | a number that runs | TimeSensor |
| a number | a place | PositionInterpolator |
| a number | a turn | OrientationInterpolator |
| a number | a colour | ColorInterpolator |

## 6. Wires can compute

Open [world 2, the Ripple Counter](https://hagopjay.github.io/x3d.demo/demos/wire-lab/v1/?world=counter). Press the
red button a few times and watch the lamps. They are counting in binary.

There is no program in this scene. There are only two kinds of node.

- A **BooleanToggle** flips each time it hears yes. On, off, on, off. It remembers which. That is one bit of memory.
- A **BooleanFilter** has an output called `inputNegate`. It says the opposite of what it hears. So it says yes at
  the exact moment its input says no.

Now chain them. The first toggle shows lamp 1. Its output also goes to a filter. When lamp 1 goes from on to off, the
filter says yes, and that yes flips the second toggle. That is carrying, the same carrying you do when 9 + 1 becomes 10.

| Presses | Lamp 2 | Lamp 1 | Number |
|---|---|---|---|
| 0 | off | off | 0 |
| 1 | off | on | 1 |
| 2 | on | off | 2 (lamp 1 rolled over and carried) |
| 3 | on | on | 3 |
| 4 | off | off | 0 (both rolled over, and there is no lamp 3 to carry into) |

**Try it.** Lamps 3 and 4 are dark because nobody wired them. Copy the pattern twice and count to 15. Then swap
`inputNegate` for `inputTrue` and work out why the counter now runs backwards. (Hint: counting down borrows when a bit
goes from 0 to 1.)

This circuit is called a ripple counter and it is inside real computers. You built it out of messages in a 3D file.

## 7. Wires can feel alive

Open [world 3, the Follower](https://hagopjay.github.io/x3d.demo/demos/wire-lab/v1/?world=snake). A golden ball flies
a figure of eight and a tail of beads follows it. There is no physics engine here.

A **PositionDamper** chases a place. It never jumps; it closes part of the remaining distance each moment, so it
arrives smoothly. Its `tau` is how lazy it is: a small tau is eager, a big tau is sleepy.

Bead 1 chases the head. Bead 2 chases bead 1. Each one is a little late, and the lateness adds up along the chain into
something that looks like a living tail. Nobody told the tail how to curve.

**Try it.** Wire in beads 3 and 4. Then add a PlaneSensor so you can drag the head with the mouse. Then make the green
beacon light only while the tail is still catching up: a damper's `isActive` says yes while it is moving and no when it
has arrived.

## 8. Three ways to see one thing

Under the graph in the lab are three tabs. They all show the same behaviour.

| Tab | What you see | Who it is for |
|---|---|---|
| Script | a few lines of Python that would build this graph | people who like to type |
| X3D | the actual file, with the ROUTE lines lit | the web browser, and anyone checking the work |
| Sentences | one plain sentence per wire | reading aloud, and comparing two versions |

Change a wire and all three change. A picture, a program and a file that always agree with each other are rare and
valuable. It means a person, a script and an AI can work on the same scene and each can check the others.

## 9. From the lab to Blender

Blender is a free 3D program used to make films and games. It has an excellent node editor, and no idea what a ROUTE
is. The add-on `x3d-blender-io` now closes that gap as a proof of concept:

1. Press "Download .x3d" in the lab.
2. In Blender, import the file with "Behaviour as node graph" ticked.
3. Open the node editor and choose "X3D Behaviour". Your graph is there, with the same nodes and the same wires.
4. Change it, export, and open the file in a browser.

The three lab worlds have each made that trip in a test and come back with every node, every field and every wire
unchanged.

## 10. Things to try, from easy to hard

1. Make the door take ten seconds instead of three. (Which node knows about seconds?)
2. Make the door open sideways. (Which numbers are "where"?)
3. Make the lamp in world 1 glow while the door moves.
4. Make the counter count by itself, twice a second.
5. Make the follower's tail stiff at the front and lazy at the back.
6. Build a combination lock: three buttons that must be pressed in order. You will need to think about what
   "remember" means, and which node can do it.
7. Hard: make a lamp that blinks faster the closer the head gets to it. Which kinds of event would you need, and is
   there a node for each conversion?

## Words

| Word | Meaning |
|---|---|
| X3D | an open international standard for 3D scenes that can include behaviour |
| node | one small machine in the scene |
| field | a named plug on a node |
| event | a small message sent from one field to another |
| ROUTE | a wire that carries events from an output to an input of the same kind |
| DEF | a node's name, so wires can find it |
| sensor | a node that notices something: a click, a drag, a moment in time |
| interpolator | a node that turns a number from 0 to 1 into a place, a turn or a colour |
| follower | a node that chases a value smoothly (dampers and chasers) |
| type | the kind of value a field carries; the rule that wires must match kinds is a type system |

## What is true and what is not yet tested

The lab was driven by a real mouse in a test: the door opened, the counter counted to 15 and back down, and the tail
followed a real drag (30 of 30 checks, X_ITE 16.7.1, headless Chromium with software drawing). It has not been tried on
a phone or with a real graphics card. In Blender, the graph was built, changed and exported by script; nobody has yet
looked at it on a real screen.
