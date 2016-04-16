# What is Multi-Meta Programming? #

## Background - Metaprogramming ##
[Wikipedia on Meta Programming](http://en.wikipedia.org/wiki/Meta_programming)

In many formal languages, sometimes we want to make a meta-statement. That is, a statement _about_ the language and not _in_ the language. The same goes for programming. Sometimes we want to describe the program on a higher level than the code of the program. For example, in automatic verification we might want to make a meta-state about a function, such as "this function should never return 3". This is obviously not something we can normally code in the function itself (because if we do, we change the function, and now we have to write the same statement again about the new function).

Many languages allow code to access the semantic tree of a live program. This is often called _reflection_. Languages such as LISP go further by being completely first-class. Code in LISP can manipulate other code just like any other data.

To perform the static verification task of proving that a function won't ever return 3, a meta-program could analyze the semantic structure of the function and prove or disprove (or not reach any conclusion about) the requirement. [Static analysis](StaticAnalysis.md) is a very complex issue in it's own right and is one of the BuzzWords.

### Example: Automatic Tracing ###
A more common usage of metaprogramming is to automatically generate code that is hard or tedious work to write manually.

For example, one might want all functions in a program to produce a trace-enter log when the function enters, and a trace-return log on return. Instead of manually adding a call to the trace function with the correct parameters at the beginning and end of each function, the programmer would rather use an automatic meta-program that automatically adds these trace calls in the correct position and with the correct parameters. This meta-program will execute every time the program is compiled and in this way the functions will always be automatically traced. To remove the trace calls, the programmer doesn't have to modify his program - he just needs to disable the meta-program by removing it from the build process.

A compiler might supply automatic tracing or the similar task of profiling, built-in. You turn on a compiler switch and the program comes out traced or profiled. In fact, normal code optimization may be viewed as metaprogramming - the compiler analyzes your program and regenerates an optimized version. The final stage of translation to machine code can also be viewed as metaprogramming.

## Multi-Meta Programming ##
Metaprogramming is not a new concept, and has been successfully employed in various settings. We wish to expand it and call this expansion _multi-meta programming_.
Before continuing we will list some uses of metaprogramming:
  * Generation - metacode that generates code
  * Transformation - metacode that modifies code (similar to generation)
  * Translation - transformation into another language (commonly, into machine language)
  * Analysis - metacode that analyzes code
Of course, a metaprogram could use all three simultaneously, for example analyzing a given program in order to generate a new one (like an optimizing compiler).

### Points missed by common metaprogramming ###
Thanks to complex cases such as [Static analysis](StaticAnalysis.md), several points about metaprogramming come into mind:

#### Different language requirements ####
For some tasks, the meta language may require properties that the language does not supply. For example, in the tracing case if we are tracing a C program we wouldn't want to write the automatic tracing metaprogram in C, even if C allowed us to do so.

In the case of static analysis, the metaprogram might require language features not supplied by the analyzed program's language, such as easy logic-based programming with built-in theorems. Also, it may _not_ need features that _are_ supplied by the analyzed program, which would make the task of meta-programming harder.

This is normally solved by using a completely language altogether for the metaprogramming. For example if we need a high-performance and low-resource program, we might write it in C. For the metaprogramming of automatic tracing we might use Python, and for static analysis we would use some other logic-based programming language. The result of this solution is that a growing multitude of languages have to be used.

The less problematic issue with this is the expertise of programmers. Either the different tasks are separated between different programmers, or each programmer must be well-versed in many languages.

The real problem with having to use so many completely different tools is the management of the program structure and build system. How do you cause the metaprogram to work in the first place? What should run first - the autogenerating Python code or the analysis program? Is the order always the same? How does one easily add a new tool? This huge overhead usually means that nobody takes the time to use these powerful tools.

The solution, as described below, is not to try and create a single programming language for all these varying tasks. Rather, it is to create a single programming _platform_ where different semantic systems can co-exist.

#### Metaprogram management ####
There should be a convenient way to manage metaprograms and their relations to regular programs. Usually, we write the metaprogram in specially formatted comments in the program's source code, or in a completely different file. Both options are not convenient. The metaprogram might be sometimes tightly coupled with the program it analyzes and sometimes very general and we would want a better way to organize this relation. Furthermore, we might want to automatically assign a metaprogram to a class of programs, see next point.

#### Automatic metaprogram assignment and execution ####
Back to the analysis example. Assuming we have solved the issue of analysis for a certain class of functions (or programs), we may want to automatically analyze all functions with this new analyzer. This could mean that every function will be scrutinized and if it matches, it will undergo a specific transformation.

A much more powerful feature would be automatic analysis - while the programmer writes a new function, it is continously analyzed and if the function does not comply to pre-written requirements at any point, he will be warned immediately. Even better, the programmer will be warned if a common bug is spotted. Obviously, this feature places several requirements on both the metaprogramming language and on the programming environment.

# Multi-Meta Programming and Live Programming #
After describing various issues and desirable features of metaprogramming, we will attempt to construct a solution.

In the context of [Live Programming](LiveProgramming.md), metaprogramming can be seen in a new light. Because the program is live (syntax exists only on the screen, and semantics are easily accessible), metaprogramming is much easier. No code parsing is necessary. By removing this single, shallow restriction, every programmer can become a metaprogrammer of his favorite language.

Another of the BuzzWords that aids us is [Unified Interface](UnifiedInterface.md). This one means that the programming environment is itself a program that we can edit (in it's own environment!). Thus we can combine metaprograms with our program easily. We might program the environment to run a metaprogram over every function as it is being edited (remember there are no syntax errors in Live Programming).

The last obstacle to remove is the inherent diversity of languages required to perform different tasks. For the logical reasoning associated with analysis, we would need a logics language. This problem is solved by use of the [Multiple Semantics](MultipleSemantics.md), yet one more of the BuzzWords.