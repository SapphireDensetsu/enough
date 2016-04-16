# Purpose of this page #

**Update**: _See the ObjectModel page for a much deeper examination of this topic._

This page is meant to discuss various models of concurrent systems, and their relation to our BuzzWords.

# Imperative model #
In traditional imperative programming models, concurrency is represented as explicit threads of execution. Each thread sequentially executes code and interaction occurs via explicit synchronization mechanisms and shared memory.

#### Problems ####
The main problem with this model is its engineerability. Threads can interact in exponentially large number of possible ways. Synchronization is explicit and depends on the good will of the programmer and on luck. Debugging and testing is extremely hard because so many different states are possible that it is sometimes impossible to re-create a bug.

# Imperative with promises #

See [Promises](Promises.md).

#### Problems ####
Although this is much better than traditional synchronization techniques, the concurrency of the system is still "hidden" from the programmer. With LiveProgramming, perhaps this can be solved - the environment can analyze the system and allow editing in a view that emphisizes the concurrency of the system, but this should be demonstrated.

# Flow/actor based model #
The flow or actor based model describes a system in terms of data flow between active components. Here is a simple example:

![http://enough.googlecode.com/svn/wiki/images/simple_concurrent_system.jpg](http://enough.googlecode.com/svn/wiki/images/simple_concurrent_system.jpg) A video processing system

The system processed inputs from two cameras, and eventually performs some logic on it. To construct this system using traditional object oriented languages, one would have to waste time to define the basic, repeating building blocks (network of actors, what each actor is, etc.), and to define what is concurrent and how is synchronization performed.

Note: GStreamer is a library that implements exactly this model, and even has a graphical editor for constructing pipelines. See [Gst Editor](http://gstreamer.freedesktop.org/modules/gst-editor.html).


It would be much easier to program this system with a language (or environment...see LiveProgramming) that allows us simply to build each of the actors (processing blocks) and then connect them. The language will then supply the ability to automatically parallelize the system by finding parallel branches in the flow graph, and by analyzing the behaviour of the actors. Furthermore, with AdaptiveProfiling the system will auto-adjust itself to different resource conditions (such as running on a computer with less memory and more CPU) or different input conditions (such as when suddenly a given actor becomes much slower).

#### Problems ####
On the good side, this model does not let the program deal with threads and low-level synchronization explicitly. The only synchronization required is on a high-level scale. The actors are stateful but because they are completely seperated and the only interaction is via the "pipes", the state of each actor has no implications on the concurrent system.

However, not every system is easily modelled as a flow graph. (_Examples?_) Furthermore, the actors themselves are "atomic" and cannot be parallelized internally, because the model does not deal with non-flowing objects (the internal structure of an actor may be non-flowing, perhaps imperative).

# Functional model #
This model is related to, but not identical, to the flow model above. In the flow model, each actor may have an internal state. With a purely functional model, this is not possible.

#### Problems ####
How do you design a stateful system with a functional model?

_Expand!_