# What is Multiple Semantics? #
_this needs to be developed further_ see discussion in [Contemplations](Contemplations.md)

## Choosing semantics ##
With every new programming language, new semantics are introduced. Naturally, most new programming languages use semantics similar or identical to a previous language's. Programming languages may even be categorized by their semantics into groups, as is often done (arguably). These categorizations are called "programming paradigms":
  * Functional
  * Imperative
  * Procedural
  * Object-oriented (state-method semantics)
  * High level (closer to human-level semantics)
  * Low level (closer to machine-level semantics)
  * Numerical
  * Logical
  * Many more
Some of these overlap, and some conflict. Most programming languages use a combination of varying degrees of each category. Most languages are a total mess (C++, and even likeable Python has an identity problem).

In [Live Programming](LiveProgramming.md) the goal is to seperate syntax from meaning, syntax from semantics. However, one may ask - _is this enough_? Even if we get rid of syntactical restrictions by allowing any syntax, we still need to choose semantics for our language. Obviously this time we can't simply get rid of it (unless we want to get rid of programming!). Obviously, _want_ semantics, but we don't know which to choose.

There are several options:
  * Study different programming languages, paradigms, and semantics, to finally design or choose existing semantics that will solve all our problems (highly unlikely)
  * Try to combine as many as possible different (often conflicting) semantic sets into a single language that will feature them all (very difficult or impossible)
  * Try to perform translation of program content from one semantic structure to another. Althought the possibility of this is questionable, we wish to explore it.

## Semantic translation ##
Some "paradigms" are easly translated: a simple imperative program can be transformed into a function program and vice verse (as is done by the functional language compiler). It is also obviously easy to translate _any_ language to machine-level semantics - this is _always_ done. The reverse is exceedingly hard. What about object-oriented to procedural? Easy. Reverse? Probably impossible. Functional high-level to low-level object oriented? This one doesn't even make sense. (OK, we get the point.) This is an idea that must be developed further.

# Goal of Multiple Semantics #
The goal is to allow the programmer to edit his logical program structure using different semantic structures. For example, the program itself is numerical, but when analyzing it with a metaprogram a logical semantic structure is more appropriate.

The **key point** is: despite having different semantic structures, with **integrated** multiple sematics, all these differing languages live in the same world.