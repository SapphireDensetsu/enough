# Status #
We have re-implemented the [PackageLibrary](PackageLibrary.md) - so now we need a major re-write of Graphui as well.

## Download ##
The latest version (BEFORE the anticipated rewrite) is: [Latest Version](http://enough.googlecode.com/files/graphui488_only.tar.gz)

# Features #
Graphui (pronounced grafoo-ee) is an attempt at a generic graph editing gui. The code is in the svn under [graphui](http://enough.googlecode.com/svn/trunk/graphui/).

Short **[Demo video](http://www.youtube.com/watch?v=RT87JfTYIvo)** (or try this: [demo video](http://enough.googlecode.com/svn/trunk/media/graphui_sneak_2.mp4) and if you experience problems with QuickTime, use something else.)

[Screenshot](http://enough.googlecode.com/svn/trunk/media/graphui_screenshot_2.jpg):

![http://enough.googlecode.com/svn/trunk/media/graphui_screenshot_2_thumb.jpg](http://enough.googlecode.com/svn/trunk/media/graphui_screenshot_2_thumb.jpg)

Here are the current "features":
  * Automatic layout using [Dot, Neato & Twopi](http://www.graphviz.org) (Graphviz). You can switch layout engines in real time
  * Cross-platform - tested on Linux (ubuntu) and Windows
  * Save and load graphs
  * Connect, disconnect, add and remove nodes
  * Zoom & pan
  * Stretch or keep DOT's aspect ratio
  * Undo/redo
  * Multi-line text labels for nodes and edges
  * Record animation - makes a series of BMP files you can later turn into a movie using videowriter or some other tool.
  * All changes are animated to make it easy to see what is changing (and to make it cooler!)

More coming soon!

**Requirements**: [Python](http://www.python.org) 2.5, [Pygame](http://www.pygame.org), [Twisted](http://www.twistedmatrix.com), and [Graphviz](http://www.graphviz.org) (aka dot). On Windows you will need also [pywin32](http://sourceforge.net/projects/pywin32/).

For better performance get Pyrex too (and run setup.py build make sure to use the .so files).

Here is a short animation showing Graphui switching between layout engines:

![http://enough.googlecode.com/svn/trunk/media/graphui_switch_layouts.gif](http://enough.googlecode.com/svn/trunk/media/graphui_switch_layouts.gif)


# Applications #
Graphui is still under development. Here are some ideas for applications.
  * Diagram editor - the simplest most obvious application. Use Graphui instead of manual-layout programs (such as Visio and Dia) to easily create flow charts, state machine diagrams, etc.
  * Graph visualization - because Graphui's format is simply pickled Python objects, you can easily create tools that make graphs from any dataset and then view/edit the graph in Graphui.
  * Graph algorithms demonstration and visualization - a researcher/student may easily extend Graphui's code to work on graph algorithms in a live environment, instead of iterating between running his algorithm test program and viewing the result seperately.


## Future applications ##
Graphui may be suitable for testing a [Live programming](LiveProgramming.md) environment. We will have to add features for viewing the code in different ways (not just as a Dot graph), especially as a compact tree (like the one used in graphical file managers to represent the directory tree).
