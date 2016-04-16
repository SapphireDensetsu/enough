**This represents our old ideas. A new document will be written soon.**

# Credits #

## Jonathan Edwards' Subtext ##
This is heavily based on the work of **Jonathan Edwards** (See [Subtext](http://www.subtextual.org)). The majority of the ideas presented here are actually directly taken from Edwards' work in Subtext (with some modifications).

# Introduction #

This document represents the core of our understanding of how the new computing world should function.

There is an inherent complexity in the relationship between side-effects and immutable functions. In the following we describe a possible way to reconcile these two conflicting terms and also try to deal with related issues.

# Terminology #

A short list of fundamental terms in the new computing world:

  * **Reference**: A universal link to a value, mutable or function.
  * **Value**: An immutable thing like an integer or a string - these exist "out of" the computer, and will never change.
  * **Mutable**: A stateful object. Typically a container, but can also be "built-in" (i.e implemented via a lower-level mechanism, e.g console).
> The following mutable objects exist:
    * **Data**: e.g: Arrays, structures (containing fields) and other arbitrary data containers.
    * **Function**: Transforms values into new values, in a side-effect free way. A function is mutable because it can be edited (modified to perform a different calculation).
    * **Action**: Modify a Mutable or use other Actions.
    * **Event**: Triggered when a Mutable modification or built-in event occurred, and can be used to invoke Actions.
    * **State**: The entire "world" (all the objects that exist, anywhere) in a certain exact moment.
  * **Now**: The current **State**. From this moment, any changes will be based on this State.
  * **History**: The collection of all **States**.

Additional terms:
  * **World**: The new computing world in which all these objects are defined and exist. No other types of objects exist in this new world.
  * **Root Event**: An Event that causes computations and invokations to occur. Without Root Events, the computer would be waiting indefinately.
  * **Chain reaction**: The propagation from a Root Event through all the Events and Actions that are triggered because of it.

# State #

At any time, the (new computing world) will have a State. The entire "platform state" of **all** the computers in the world (or State) at a given moment is composed of all the Objects, Values, Functions, etc. and the inter-relations (i.e references) between them.

**Mutables** only have state due to their part in the entire "world". When a Mutable is changed, a new State of the entire world is created in which that Mutable exists in its new state. This makes it possible to undo back to previous States in **History**. If some Mutable exists in some other computer, and does not interact with any known Mutable, it's individual state is irrelevant for us (the local machine) and therefore not included in the State.

A new state of a Mutable (and therefore the entire world) is created when a Mutable changes. The **root cause** for any change in State (change of any Mutable) is always an Event. When an Event occurs it may trigger one or more Actions which by definition modify the state of Mutables. Furthermore, the mere occurance of an Event means that some Mutable has changed.

Any State must be **coherent**. All changes that have the same originating Event are part of a single State (the same version). For example, if an Event of Mutable "A" has triggered a chain reaction that caused some other Mutable "B" to change, the new State will contain the version of both Mutables **after** the change. (Recursive chain reactions are TBD).

## Timing issues ##
In theory, all Functions compute their results immediately, and all Actions take no time at all to invoke. In practice, Functions may take a long time to compute their values during which Events may arise. For example, the user may want to continue interacting with the system.

It is important that the entire chain changes all of the objects and creates a single new State for all of these changes. The reason is that letting some of the changes occur in an earlier State than others would create an incoherent world state and may break assumptions about the relation between various computations of the same inputs.

During long computations and action invocations, we would like to:
  1. Expose to the user that the objects affected by the chain are in the process of changing.
  1. Disallow or queue up further changes to the affected objects.

In order to expose the user to the fact that the objects are being processed, a new version of each Mutable affected by the chain must be created immediately (before computation completes).

When a Chain Reaction starts, **before** the Event is actually processed through the whole chain, all

## Implementation ##

There is no actual data structure that stores the entirety of the **State**. It is more of a logical construct to facilitate understanding of object versions.

Every **Mutable** has an associated version number, that refers to the **State** it belongs to. A **State** is actually the collection of all **Mutables** of a certain version number or the latest one older than it.

Modifications of remote **Mutables** (that live on other computers) are associated with a local version number so that a remote object version can be associated with a local **State**. The implementation of this TBD.

# Values #

Immutable values exist in thin air, and are referred to by other objects via