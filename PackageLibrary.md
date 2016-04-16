# Outline #
The current design is the result of our current livec/graphui implementation efforts, where we learned important lessons.

  * **Purpose:** to allow development of enough projects (e.g. LiveC, Graphui) using a design based on ideas in Enough.
  * **Design:** Currently, the library's design reflects:
    * [Differential computing](DifferentialComputing.md) using deltas and observation
    * [Lazy Evaluation](LazyEvaluation.md) using "expression objects"
    * [Object-based revision control](ObjectRevisionControl.md) using deltas, histories, and hierarchical baselines.
    * [Retroactive macros](RetroactiveMacros.md) made possible by history recording and visualization.

  * **Future features** that will become possible after we complete this phase:
    * [Intelligent memory management (recomputability)](MemoryManagement.md): Deciding which objects should be cached (in-memory), swapped (cached in disk), or discarded (recomputed when necessary) according to the computation costs, storage costs, access frequency and importance. This requires developing some algorithms...
    * [Orthogonal persistence](OrthogonalPersistence.md) (or a variant thereof): Transparent swapping of unused objects to disk (due to current LCW implementation, objects will be serialized to files).

# Layer 1: Observation and deltas #

### In short ###
This layer provides the basic building blocks of the library. **Observation** means that objects subscribe (_observe_) on each other for notifications. In this layer, observation notifications are "deltas" (modifications to objects). When a modification occurs in one object, it notifies its observers. **Deltas** provide control over changes. All changes are done via deltas.

## Glossary ##

  * **Value**: an entity that holds a piece of data that can be accessed in some way (read, sliced, etc). Examples: `List`, `Dict`, `ValuePtr`.

  * **Observable**: an object that sends **notifications** to **observers**. A single object can have multiple "observation ports". A typical observation pattern is typically used by mutable objects to send notifications to observers about mutations. Some examples of observable objects:
    * **Values** are always observable:
      * `List` (notifies when items are added, removed or replaced)
      * `Dict` (notifies when keys are added, removed or a value is replaced)
      * `ValuePtr` (notifies when the ptr is changed to point at another object)
    * **Expressions** are always observable - because their inputs may be mutable.

  * **Notifications**: in the case of observable mutable objects, a notification is actually  a **delta**. Mutations are always done via deltas, and the delta is sent to **observers**.

  * **Observer**: an entity that is registered to receive notifications about changes in an observable object.

  * **Expression**: represents computations on inputs (inputs are other expressions). Expressions are "light" objects that do not cost a lot of memory, and represent the necessary computation required to create the value that they represent.
    * **Literal**: a special kind of expression that contains a mutable value. It does not have inputs but allows changes to take place directly on the value via a special interface.  Only literal expressions are actually mutable, and are not redundant to their inputs.

  * **Delta**: represents a change in a class of objects (e.g. `ListItemAdd` represents the adding of an item to a List). Deltas do not refer to a specific object that has changed - rather, they represent the change that _can be applied_ to an object. Each object type (`List`, `Dict`, etc.) has its own set of delta classes specific to that type. A delta is always reversible. This means that some deltas hold more information than is necessary to just perform the change, but also information required to reverse it (e.g DictItemReplace also holds the previous value).  Deltas are also combinable via **delta arithmetic**.

  * **Delta arithmetic**: Deltas can be combined in various ways. Operations are:
    * **Addition**: applying `a+b` is equivalent to applying `a`, and then applying `b`.
    * **Negation**: reversal - `-a` is the reverse of a (applying `a` and then `-a` yields no change).
    * Example: The delta `-((-b)+(-a))` is equivalent to the delta `a+b`.
    * For a formal discussion see **[Delta Algebra](DeltaAlgebra.md)**.

## Observables ##
### Motivation for Observation ###
It might seem that observation is a by-product of the mutability of some base objects (such as `List`). Can we do without observation, and only use deltas on immutable objects? The answer is no. The main reason is that expressions need to know if their inputs changed. Otherwise, an expression will have to re-calculate itself every time somebody tries to use its value. Also, however uses its value, does not know if that value has changed a moment later, it has to keep checking.

### Open/Close of Observables ###
**TODO**

## Expressions ##

Expression represent and evaluate to an "output value".

### Non-literal expressions ###

Expressions that are not literals have certain properties:

  * **Immutability:** Expressions are not themselves mutable, but they are observable for mutations in their value (because the input may be mutable).
  * **Redundancy:** They are always redundant to their inputs. ("a+b" is redundant to a and b, because it adds no additional data besides the operator +)
  * **Observing the inputs:** When expressions are observed, they observe their inputs, so that when the input has changed, it may notify its own observers of changes.
  * **Caching**: Normally, an expression doesn't store the result of its operation. It calculates the result lazily (see _Open/Close_). Storing the result is called _caching_, and in principal this can be done "intelligently", considering performance tradeoffs, resources, etc.
    * Some example expressions are:
      * `Literal` - the expression that simply represents a value
      * `DictValue` - an expression that represents a single value in a dictionary. It is created by `DictMap`.
      * `WithDelta` - see _revision control_, below.

## Example ##
**TODO**

# Layer 2: Revision control #
Since all changes in layer 1 are represented by deltas and expressions on which they occur, the revision control can understand not only _how the change looks_ but also _what the change was_. For further discussion see [Object-based revision control](ObjectRevisionControl.md).

### Viewing the revision world ###
An important aspect of this design is that revisioned objects' values may not really "exist", in memory or otherwise, until they are viewed. A revisioned object can be computed from the set of deltas that comprise it, plus some base revision's value. This means that there should be a clear seperation between things in the design that are vital to revisioning, as opposed to things that are used for viewing revisioned things. Therefore, we define two "worlds":
  * **Revisioned world** contains all things that are required for managing the revisions.
  * **View world** contains things that are used for viewing a version of the world.

**Object representation**: every object in the revision world is represented by a pair - the `ObjectHistory` and `Baseline` of that object.

## Glossary ##

### The revision world ###
  * `WithDelta` - an **expression** that takes (expression, delta) and represents the given expression with the delta applied. `WithDelta` does not actually _apply_ the delta, it only _represents_ the combination: value+change. The given expression can be thought of as a "base revision" and the `WithDelta` object as a "new revision" which is equal to "base revision" + delta.
  * A **Revision** of an object is basically a `WithDelta` of that object. Later we might have a specific pythonic object that represents a revision, and that contains the appropriate `WithDelta`.
  * A **Delta path** is the difference between two revisions of the same object.
    * The "sum" of a delta path is a delta that reflects the canonical change that the path represents.
    * If an object has some revision tree, including revisions A and B, the delta path from A to B is the accumulation of all deltas one needs to apply to A, in order to get to revision B.

  * `ObjectHistory` - contains a tree of all revisions of an object. There is one `ObjectHistory` per object. The "revisions" here differ by changes to the object itself - not by changes in other objects. For example, if A references B, the `ObjectHistory` of A will not contain a new revision if only B changes. The `ObjectHistory` can be used to calculate a **delta path** between two revisions of the same object. This is used in the `RevisionGetter`.

  * **Baseline** is a "freeze" of a set of objects in specific revisions.
    * Baselines are revisioned, so a baseline object has its own `ObjectHistory`.
    * Every revisioned object has exactly one Baseline. Only Baselines don't have a Baseline.
    * The Baseline of an object A is a map:
      * for A itself: map (`ObjectHistory` of A, Baseline of A) -> (Revision of A)
      * for each object X that is contained by A: map (`ObjectHistory` of X, Baseline of X) -> (Revision of Baseline of X)
    * For an object A that doesn't contain other objects, the baseline will have only one entry: (`ObjectHistory` of A, Baseline of A) -> (Revision of A).
    * Baselines are hierarchial, meaning that a big baseline maps objects to their local baselines. There is a **global baseline** that maps all the top-level objects to a revision of their respective baselines.
    * When accessing objects (usually using a `RevisionGetter` on a DictMap of the baseline) we access a specific revision of the baseline.

  * **MRCA** means Most Recent Common Ancestor. For two revisions B and C, the MRCA is the most recent (newest) revision that is a parent of both B and C.
  * **Conflicting deltas** - when the order of applying the deltas matter.
    * Assume two deltas d0, d1 and a revision A0 of an object A.
    * If applying the deltas on A0 in a different order (d0 and then d1, or d1 and then d0) results in two different values, the deltas are defined to be **conflicting on revision A0 of A**.
    * Revisions of the same object are said to conflict, if the delta paths from their MRCA to each of them evaluates to two conflicting deltas.
  * **Merge** - Creating a revision from a pair of base revisions.
    * If the base revisions don't conflict, the merge can be resolved automatically by simple applying the two corresponding deltas (from the MRCA to each base revision), in an arbtirary order.
    * If the base revisions conflict, some special interaction must take place to decide how to resolve this. The interaction for resolving may be done manually, or automatically by some intelligent code, but it is not "straightforward" - it is heuristical.

### The view world ###
  * `RevisionGetter` - an object that looks like a specific revision of an object.
    * From the user's point of view, the `RevisionGetter` looks just like the revision itself.
    * If the `RevisionGetter` detects that it should now point to a different revision, it automatically generates (notifies) its users with deltas that represent the change (using a **delta path** from the old to the new revision).

  * `BaselineView` is an object that manages accesses to revisioned objects. `BaselineView` creates `RevisionGetter`s that match the revision that it happens to watch (not the "latest" revision). If the `RevisionGetter`s make a change, they tell observers about new baseline revisions being made.

  * `ObjectAccessor` encapsulates work that is always done in the view world to access objects. It allows access to a versioned object, while recursively supplying `ObjectAccessor`s when you reference a sub-object.


## Detailed usage of objects ##
When an outside component (such as a GUI) accesses an object in the revisioned world, it uses some revision of a baseline of the world to do so. Now, the GUI needs to reference objects "universally" - meaning, it shouldn't need to keep updating references to objects every time a new revision of an object is created. For this purpose the GUI uses RevisionGetters

**TODO** _Continue this...._


## Propogation of modifications ##
When an object is modified via some view, the modification causes two propogation chains:
  1. The modification causes the object to emit a delta towards its containers (expressions that use that object as an input). These, in turn, progpogate deltas further up. For each object in the hierarchy, a new revision is created and added to it's `ObjectHistory`.
  1. Modifications are always made in some view of the world - meaning, the object that was modified was accessed through some baseline. A new baseline can be created, where the difference with the old baseline is that the modified object is mapped to it's new revision.

**TODO** _describe in detail_

### Example ###
**TODO** _describe in further detail, add BaselineView and make it correct!_

  * Assume hierarchy of objects, A->B->C. Each object initially has one revision: A0, B0, C0.
  * Assume a revision of A's baseline, called "Baseline A0" that maps: A->A0, B->"Baseline B0"
  * "Baseline B0" maps: B->B0, C->C0.

The object A is accessed via "Baseline A0". Because the baseline maps A->A0 we are actually viewing revision A0 of A. Since this revision contains a reference to B, we consult "Baseline A0" and find that B has a baseline revision "Baseline B0" in this baseline. Now, using "Baseline B0" we find that B has the specific revision B0, and using B0 we find that it contains a single object - C. Using "Baseline B0" again we find that C is mapped to C0. So far we have only used the baselines to access some objects in the revisioned world.

Now, we wish to apply a change, or: create a new revision of C, that is based on C0. Let's call this new revision C1. We create the new revision and add it to C's `ObjectHistory`. However, since we are viewing C through B, we must update B's baseline history to reflect that there is a new version of C.

It is **important** to understand that this is completely _view dependent_. In principal, B shouldn't care if C got a new revision - but since we are now _viewing_ the world (and making changes), it is desirable to update our view to reflect the new version we have created. To do this, we must modify B's baseline to point to C1 instead of the old C0. Modifying B's baseline means creating a new revision of it, namely "Baseline B1" which based on "Baseline B0".

The change propogates upwards and also A's baseline needs to be modified. This is because now, in this new version of the world, _in our view_ we want to access C and get to C1 instead of the old C0. Therefore, A's baseline should now map B->"Baseline B1" instead of the old "Baseline B0". Since this is a change in A's baseline, a new revision of it must be created, called "Baseline A1".

**Summary**:
  1. We accessed A->B->C viewed via "Baseline A0"->"Baseline B0"->C0.
  1. We created a new revision C1.
  1. We created new revisions "Baseline B1" and "Baseline A1" to reflect this.
  1. The view is now: A->B->C, via "Baseline A1"->"Baseline B1"->C1.


## Merge ##
Merged revisions are represented as children of their MRCA. If A is the parent revision of children B and C (meaning A->B and A->C), and D is the merge of B and C, in the revision tree the merge will be represented as A->D. This is in contrast to making D have two parents (B and C) which complicates the design. For this reason, the revision tree is always a tree (and not a DAG).