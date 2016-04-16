## Libraries ##
In the process of our work, we are developing a (Pythonic) codebase that includes:
  1. A generic library (PackageLibrary), including:
    * Observables - primitives that notify registrars about events, when an underlying object mutates. A basic building block for DifferentialComputing.
      * Observable values (observables that have state (contain data) such as List, Dict, ValuePtr).
      * Expressions - function-like object that represent operations on each other, and that ultimately depend on observable values (through the special Literal expression).
    * Revision control - where every change is understood by the system (unlike current revision control systems where changes are done on the data and the system "guesses" what the diff means).
  1. A GUI toolkit, based on the concepts:
    * Complete separation between model and view - view only contains state that model does not.
    * Model changes 

&lt;--&gt;

 view changes, automatically, using Observables.
    * Keys are processed by a Keymap tree.
    * Based on pygame
  1. Other utility things including:
    * parsing dot output (used in Graphui)
    * Graph objects (Nodes, Edges) and some basic algorithms.
    * etc.

## LiveC ##
LiveC is a demonstration of a LiveProgramming interface for C. It is the current focus of attention.

## NF ##
NF is a gui for functional live programming. A few prototypes were developed.

## Graphui ##
See here: [Graphui](Graphui.md)

## Python Tracer ##
[Python Tracer](http://code.google.com/p/pythontracer)

## Tools ##
  * **videowriter** is a tiny program for **creating a video out of a sequence of images**. Available in the SVN under tools. **Requires**: OpenCV library. Or you can try the [linux binary](http://enough.googlecode.com/svn/trunk/tools/video_writer).

### Some stuff that may be useful ###
This includes even trivial stuff that we haven't seen in many other places.
  * **Bezier curves in Python** - the Graphui gui includes an implementation of n-order bezier curves in Python. See the file Bezier.py under graphui/Lib in the svn trunk.