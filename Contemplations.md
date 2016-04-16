## World Library ##
  * with LiveProgramming + theorem provers or other intelligent tools, we can use the internet to find similair code according to structure, types, requirements, input/output relations, etc.
  * use something like imagesynth (tm) (c) (etc) to find similar code to yours, and explore the world of software in many directions according to criterions (types, requirements, etc.)

## Different models of abstractions ##
This sections deals with MultipleSemantics (we should put the results of this discussion in that page).

The question is which model of abstraction is the best, and do we need more than one.

For a program module that simulates an object such as a car, traditional object-oriented modelling is the most intuitive. We don't think of a car as a function that "in comes gas, wheel direction, gear position, ..., out comes speed". We think of it as an object. These sort of objects prevail computer simulations of real systems. This includes computer games and more importantly many scientific tools.

On the other hand, for input processing programs such as a video decoder, the functional (or rather, flow or actor-based) model is best. Although we may have a "video decoder" sitting on our desk (a real-life object), it is easier to think of it as a black box where "in comes DVD, out go video frames and Audio".

**Todo:** Find if there are other abstraction models that may interest us.

My (Noam) conclusion is that we may want to have a "model space" composed of many different abstraction models, each complementing the others. The question is how to connect all these together and how to edit them together.


# Various Points #
When trying to revolutionize programming, it is best to keep in mind its goals.

Some points:
  * A programming language should allow the most natural (easy to express and understand) description of the system.
  * Readability/editability is a bigger problem than "writability" and that's where the focus should be.
  * For a general description of a system, natural language is the easiest to understand but lacks the exactness required for a program.
    * I am not sure I agree about this one (Eyal)
  * A system can be described in many different ways, and the best way is the one that is easiest for the programmer to use.
    * I think as above, the best way is the one that will be easiest to later read and maintain. Its less important if it takes 5 minutes or 10 minutes to write. Reading and editing and scaling it later are much much more expensive.
  * Many times, we think of a thing in many different ways. We may think of a table as a piece of wood (material), as an easy-to-reach place to put things (tool A), as a flat surface good for writing (tool B), or even as an obstruction (environment?), depending on the context.
  * Any system or part of a system can also be described in several ways, depending on the context.
  * As humans we usually describe **tasks** in an object oriented and procedural (order list of actions) way. For example, to tie shoe laces one could use the following instructions:
    1. Put the shoe on your foot (the verb "put" is a method of you - an object, shoe is another object, and your foot is a third object).
    1. Grab the laces with your hands
    1. etc.
  * It is less intuitive to describe systems in functional terms. We think of a car (a very complex system) as an object with parts, states and capabilities. We don't think of a car as set of highly-complex functions.
    * I disagree about this (Eyal). I think it depends. In one-to-one processing, functional is just as understandable as any other description, perhaps more.
    * (Noam) I agree that a "flow model" is also intuitive, where "actors" change input into output, with internal state. But globally stateless, mathematical, functions are hard to visualize and think about. See "Different models of abstractions" below.
  * Functional programming is easy for the computer to "understand", because side effects are concentrated in specific points.
    * I would say its a higher-level/more declarative description of the program, that allows a lot of extra features than lower-level descriptions like stateful languages.