# Status #
We were in the process of designing the "universal" live language. After some progress we decided to start an "exprimenting phase" where we will implement a live programming environment for an existing language. See [LiveC](Implementations.md).

# Background #
Live programming is a **fundamental** idea in Enough. Live programming is proposed as a solution to the [Problems of Syntatic Languages](SyntaxProblems.md). It is applicable in many semantic models, but has some extra advantages when applied on a [functional programming](FunctionalProgramming.md) semantic model.

# What is "Live Programming?" #
Live programming means **editing code directly** instead of using a text editor. The editing environment understands the code as you edit it.
  1. **Editing the program itself and not text** that represents it. Therefore syntax mistakes are impossible, and the program is always runnable. You may still edit a textual representation, if it is more convenient - but the editor understands your actions on the semantic level.
  1. **The editing environment understands your program completely** - because it has access to the semantic structure of the program.
  1. **The code can be edited in multiple representations.** Besides viewing the code as text, you can view it graphically in many different ways. Even for text you may view (and edit) the code in any "syntax language" you want. This is because the editor understands the meaning of the code and can express that meaning in any form, with minor effort.

Here is a short list of ideas that harness live programming. Most of these are possible also with today's "dead" programming, but are significantly easier with live programming.
  * **[Example based](ExampleBasedProgramming.md)** programming - while you code, the environment shows you the result of your function. You supply example input and see the real-time output, which changes as you modify the code. Just this simple idea can help prevent many bugs.
  * **Modularity** - refactoring will become an every-day activity, because it will be very easy. For example, all you will need to do is "grab" that function and pull it out of its current location. The environment will automatically show you what else needs to be changed, and change it. There is no performance hit because the enviornment does not have to perform a text-based search of the whole program. It just follows the existing live connections between objects in the program.
  * **Easier finding** of relevant features or code - for example, to find where the keyboard shortcuts are controlled, you may start from a representation of the program's relation to I/O. Of the few input objects, you will select the keyboard and gradually zoom-in to find the code you want.
  * **Easier understanding** of the code - the environment will display the code differently according to the level of abstractness you want. You may choose to see an outline of the data flow in the program, zoom-in to a specific region, view that code using different representations, etc.
  * **Smarter source control** - merging code is much easier when you understand the meaning of each change. Today, source control systems only see the text, and barely understand the meaning of each textual change.
  * **Intelligent tools** such as automated theorem proving - the editor will prove things about your code. This includes compliance to certain requirements. Because the editor always understands the code, it is much easier to implement (but still hard). An even more advanced idea is that the coding environment will suggest modifications to the code (optimizations, minimizations, changes that increase coherence of the code) or even automatically find alternative implementations on the internet, compare them to yours, and suggest improvements.
  * **"Code surfing"** - the abilitiy to search the internet for code that has the same semantic structure or performs similar tasks. You may start by specifying the required interface, such as "takes picture, returns picture with different size". In addition you will supply "requirements" such as "The new image contains data created using all the pixels of the input image." The "live code" search engine will generically be able to understand such requirements.

In most of today's languages, one edits text characters in a text file, that are later interpreted into semantic models (typically trees with a lot of cross-references).
Instead, a better model is to use a semantic editor that edits the semantic model directly. This has many implications.

# Advantages #

## A semantic editor is simpler ##
Since it does not have to parse and manipulate text in order to aid the programmer, it can actually be much simpler than today's code editors.  The writers of semantic editors can thus focus on adding features that aid the programmer rather than working on parsing and manipulating text.

## The program is runnable at all times ##
By editing the program semantics and not the syntax, the program can have correct semantics at all times. This means it is always runnable, and thus more informative feedback about the program can be given to the programmer. Real-time results of the current code can be shown to the programmer incrementally. This enables [Example Based Programming](ExampleBasedProgramming.md).

## References are real and not by names ##
Instead of encoded programs storing cross-references between objects by names, the cross-references will be stored as real references, which are not broken as names are modified.  The programmer can choose an object from the existing objects via the environment's GUI interface (either by drag&drop, or by a semantic-aware name-based query). Due to semantic editing, lexical scopes are unnecessary and the reference to the actual object can be shown graphically and does not need to be resolved.

## Dynamic Representation ##
One of the reasons there are so many different languages, many of which share their semantic models, is that multiple syntaxes are desirable in existing textual language. The reason is that different programs benefit from being represented in different ways.
More evidence are the tools that try to parse programs and generate flow charts and other representations that help read the program.
A big advantage of LiveProgramming is that the semantic model editor is a GUI, and as such it can expose the program's semantic model in many ways (as a flow chart, as nested expressions, etc). This not only allows to view the same program in multiple ways, according to the current need, but also to **edit** it within that view.

For example, in order to review that the program has proper error handling, one might want to view it as a flow-chart that includes the error handling "jumps". After doing this, and perhaps fixing some of the elements, he can switch back to expression view to review that the expressions are correct. Later, the user may want to verify that the type restrictions of the function are correct, so he can choose to display/hide the types that clutter his view.

Once a single specific syntax is no longer a requirement, one can view and edit the same program in a multitude of ways **at the same time**.

## More powerful code meta-data ##
Code meta-data is extra information about the code that does not directly affect the way the program runs, but adds information about the program that helps to run it faster or verify assumptions about the code.

Today, there is a trade-off between the kinds and amounts of meta-data code can contain (the verifiability and speed of the code), and the amount of clutter this adds to the textual representation of the program, as well as programmer effort in specifying this information textually.

A lot of languages choose different points in this trade-off. Some, like Python, choose the far end of no meta-data, such that the syntax is uncluttered, but no meta-data to verify the program or make it run faster is possible.  Python decorators may change this to allow some optional meta-data to be specified, at a loss of some clutter.
C++, as another example, chooses another point where all typing meta-data is specified explicitly in the textual representation. This point requires a lot of extra textual declarations and extra text in the code.

Other languages choose a middle ground with less clutter where only some of the types are specified explicitly and others are inferred.

Semantic Editing and Live Programming allow avoiding this trade-off altogether while gaining both the meta-data, and lack of clutter.  Programmer effort in specifying the meta-data may still exist, but due to the semantic awareness of the editor, this effort can also be significantly reduced. The Semantic Editor can show/hide the extra meta-data at the user's will, making the clutter a non-issue. Static typing information can be specified by the user but with extra inference and aid from the semantic editor, greatly reducing the work by the user.

Once freed from the burden of having to represent the program via uncluttered syntax, unlimited extra meta-data can be added to the code. As an example, meta-data that proves the correctness of the code to the specifications can be added, allowing for code that is provably correct and allowing to eliminate some time-consuming run-time checks as well.

## Editing vs Running ##
Traditionally, editing the program is done by editing its textual representation, while running the program is done by executing a resulting executable.

Via semantic editing, the program is always executable while it is being edited, and does not need to be explicitly "run" as it is always running.  In order to "run" it with different inputs, one just changes the inputs and the outputs are updated accordingly.
This, along with OrthogonalPersistence unifies 3 of the program's different representations ("source code", "executable" and "running form") into one form that is both editable and running. It also allows the developer and user of the program to share one UnifiedInterface to accessing the program. This UnifiedInterface makes every developer of a program a user, and every user of a program a developer of that program.

# Disadvantages #
A semantic editor would be specific to one language's semantics, while a normal text editor can edit all text and thus edit programs of all languages.

In practice, though, editors are already semantics-aware (or syntax-aware) in an attempt to help developers, using syntax highlighting and various aids that try to parse the program.  Virtually no one uses generic text-editors to edit programs anymore, and most use language-specific editors (like a language mode in emacs or vi) already.

# Live programming is a platform #
Many people argue that visual programming is only "nice" and may be cumbersome, and that it does not represnt any fundamental change in the way we program. **Live** programming is not only (or even neccesarily) visual. It means that program is alive while it is being edited. The revolutionary power of live programming is that it serves as a **platform for many new capabilities that are otherwise impossible.** Only after we begin using live programming, will we begin to discover the full potential. But there are many ideas that are already apparent.



# References #
#### Recent, informal, or reviewing references ####
  1. _[Manifesto of the Programmer Liberation Front](http://alarmingdevelopment.org/?p=5)_ Jonathan Edwards (June 16, 2004)
  1. [Flow-based programming on WikiPedia](http://en.wikipedia.org/wiki/Flow-based_programming)

#### Formal, seminal, or "heavy" references ####
  1. [Flow-Based Programming](http://www.jpaulmorrison.com/fbp/) site of J. Paul Morrison (who wrote a book about FBP).

# Additional resources #
  * [Alice](http://www.alice.org), for an interesting demo watch the first one on this page: http://www.alice.org/Alice_movies/
  * [LabView](http://www.ni.com/labview/), a tool for "virtual instrumentation", including an graphical interface for "block programming" by connecting outputs to inputs. See the [Demos](http://www.ni.com/labview/demos.htm)