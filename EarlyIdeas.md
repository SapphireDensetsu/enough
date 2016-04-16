# The Ideas #
## General computing ideas ##
  * No address space separation: Use safe languages! Objects suddenly all see each other, yay!
  * No "applications", the user directly manipulates high-level functions and objects to connect them to one another. Menus and Toolbars are simple user-adjustable configurations that can trigger these high-level functions. You can use your "Photoshop" filter functions on the movie you're watching, or connect your mp3 decoder to a file instead of the speaker if you want to rip an mp3.
  * No "security permission checks" necessary. If you don't explicitly give the functions you run references to internet connections and your secret documents, they can't express operations on them, or request them.
  * No more textual representation for code. No more merge problems, difficult renaming, refactoring, allowing a huge set of new features that are difficult because of syntax issues, i.e:
    * Static typing in Python, via incremental type-inference as you program. The benefits of type-inference without the slowness of compilation, as everything is delta-based. The types can be shown/hidden/colorized without obscuring the display.
    * Static assertions on code, that integrate into the type-verification system and statically verify properties of the program. i.e: This pointer I'm given is not NULL -> propagating this demand automatically to all callers, who have to "prove" it by getting such a non-NULL pointer in the first place or via an explicit cast that requires a NULL check.
    * Using software from others and writing software become almost identical processes, yet very easy, exposing everyone to the power programmers have.
  * Defragmenting the computing world as a spreadsheet and a build system become the same program!
  * Speed up execution by using diff-oriented execution (A user changed a slot in a 6-million-entry array? Don't rerun the sort function after it, send it a "slot changed"
event, which will cause it to send a "slot moved" event which will show it animated in the GUI.

  * The RAM is cache for the disk. The disk is cache for the network. You should be able to transparently instantiate objects from the network and call functions on the network, as if they were on your computer. Assuming ofcourse, you were given secure crypto-signed references to them (capabilities).
An explicit copy to your own storage should be possible ofcourse, to allow offline work. That principle, though, is not special to the network. You may want to control the physical medium your data is stored at (i.e: Move data from one disk to another) in the same way.
Implicit copies will also be made from slow storages to
fast storages for performance's sake, but those should be
transparent(?).
  * The above actually "unites" a lot of concepts together, and makes the entire world just one happy borderless computing platform. Not only borderless because of the
lack of processes, but because objects from one computer see objects from another computer.

## FileSystem ideas ##
  * Orthogonal persistency means there is no filesystem in the traditional sense
  * "Deletion" is silly. Marking something as a lower priority is better, because it allows prioritizing between data and overwriting less important data first, making more important data restorable.

## GUI ideas ##
  * Almost everything is "undo'able". Now that "deletion" became reprioritize, it is also undo'able!
A global undo key should always work. Localized undo's should also be possible, but that may be complex or even impossible!
  * Only external computer side effects (such as sending on the network or some other device) should not be undoable, and thus require confirmation. Confirmation should ALWAYS
be meaningful, or people will auto-confirm.
  * No "dialog boxes":
    * Presenting information is done by appending to some sort of information to user pane, which can be viewed by some global hotkey.
    * Requiring information should be done "locally" to the operation, meaning that it does not hide, halt or otherwise annoy you when trying other things. For example, the word processor should not halt all of its functions and disallow continuation if the spell checker wants your input on a word. It can use a small pane which is similar, but does not steal focus or hide things.
    * The "overlapping window" model is stupid. A better model is due. What that exact model is is not clear, but even Emacs's window model is better.
    * I think each widget should know to say which parts of it are of which importance, such that a "dead gray" area NEVER hides important text.
    * The equivalent of "alt-tab" would be saying "this is more important to me now". Maybe more data can fit the screen? Let the computer do the window arrangement work...
    * The main problem is how to easily convey (from the user) which data is important.
    * Relating to the above, "buttons", especially small ones, are very annoying to click, especially as there's the entire screen-worth of space. Perhaps all buttons should
be replaced with a nicer concept I once saw, where you drag the mouse cursor from some spot into the correct angle (i.e: 0..30 degrees is option A, 30..60 is B, etc). This is displayed nicely as a cut-pie. This allows you to move further for more precision or move a little carefully.
  * Let logic be logic and widgets be widgets. The WYSIWYG "word processing" widget should be available for the user to connect to any function or object.
  * "Widgets" are just object manipulators/viewers or action invokers that the user can connect to objects.

## General bugs to fix ##
  * NEVER jump, always animate (Made possible due to diff oriented flow of information). The human brain finds it very difficult to follow these jumps.
  * Keyboard shortcuts are KEY SHORTCUTS, not symbol shortcuts. Alt-f should always mean the same, no matter what language I'm currently using.
  * Radio buttons suck! All multi-choice options should use the same widget, that doesn't force you to hit a small spot in the screen to choose what you want, especially when the entire screen is available.

## Misc UI ideas ##
  * Via some hotkey (i.e Ctrl+Capslock) map the keyboard to the screen, displaying a transparent keyboard image on screen, allowing the keyboard to serve as a sort of "rough
mouse". Letting you jump to any geographical position with any key. Since the keyboard is wider than the screen, you can use up/down to move the transparent keyboard on screen
over the parts of the screen...


MORE IDEAS LATER... :-)


# Q&A #


> RE: Brainstorming Lotex' Ideas
> Questions by ncryptor, answers by lotex

### Q ###
> static typing in python - but in many cases you operate on a variable while allowing it to be many types: for example, you activate a method of it:

> result = moshe.do\_stuff()

> and still, moshe could be any object the implements do\_stuff how does static typing work with this? Maybe you mean that the type/assertion inference can infer that all callers to this function must pass a "moshe" that is of a type that has the do\_stuff method implemented. but this is impossible since the do\_stuff method could be created in many different ways!

### A ###
> Yes, "static typing" here means that it infers which "protocols" must be supported, and not which exact type it is. In implementation this might be implemented via subclassing most of the time, but there's some thought work...
> do\_stuff's signature here should be decided from the code here, I believe, and not from the code inside the function. i.e: if I use result in one way or the other, I make "demands" of do\_stuff. Thus I deduce that the protocol that defines do\_stuff also defines that the type returned has the protocols I use. It propagates correctly..But maybe if you give a more details example I can try to see if it really works.
> I have not thought about static typing enough, and I think nobody ever tried incremental static typing before (i.e: Applying static typing on an incrementally growing program, and not re-establishing all the types from a dead textual representation every time..), so maybe what we think about as "inconvinient" and such is actually fine in such a case. Specifying each and every type in C++ is a chore, but in this case it may not be so...


### Q ###
> spreadsheet and a build system become the same program - what do you mean? explain and example

### A ###
> A spreadsheet just attaches a GUI to view/edit cells and graphs, and then it propagates changes through the functions according to the relationships you establish (dependency tree updates).
> A build system doesn't attach a GUI to view/edit "cells" because the cells are "files" and you can edit them with the filesystem, but like the spreadsheet, it "detects" changes via mtimes and propagates them in the same way through the functions according to the relationship you establish.

> When you update a cell in a spreadsheet, the dependent cells are updated and recalculated because the GUI knows when it changes. When you update a file, the build system scans its mtime to know it changes, and knows to recalculate. Because of these superficial differences (Spreadsheet has cells/GUI, build system has files), both of these programs, while doing the exact same thing, have to be implemented completely differently because of the redundant concepts ("file" vs "gui object").

> Also note that a build system has a "live tree" of dependencies that is encoded in a "dead textual format". It keeps translating the dead representation to live, and lets you edit only the dead representation. A spreadsheet has only a live tree, which would also be better in a build system -- much faster (Remmember monk-daemon idea?) and editing it with a GUI is much nicer than editing a textual representation.

> You want to add another preprocessing on the source? "Splice" the arrow between the source object and the function that processes it and put another function on it instead.

### Q ###
  * peeding up the 6 million entry array**: I didnt understand. do you mean that the sort function NEVER occurs? or does it occur in idle time and in the mean time how does everything work (If i need to find an entry before the sort, what happens?)**

### A ###
> It NEVER occurs. "sort" looks like a sort function onscreen, that takes elements and returns ordered elements. But under the hood, "sort" in fact takes DELTAs and yields DELTAs in the other end. i.e, input is "Entry at index #3 changed from X to Y", output is "Entry at index #88 moved to #99 + Entry at index #99 changed from X to Y".
> Note that delta-based change propagation is not only faster, but lets you do nice GUI animations and not have yucky jumpy GUIs like today. Also makes other features like undo's and stuff possibly more powerful...

### Q ###
> lack of processes - we should describe the problems with that. In fact we should make a list of problems with everything we think about - critical thinking is important!!!

### A ###
> The problem is basically choosing between safety and optimized inner loops. Unsafe language code can still be used, if you can prove it to be safe :-) Proof-carrying-code is a nice concept, and possibly even practical for small inner loops. I think the idea though, that all objects communicate via the exact same protocols without imaginary
"process" boundaries simplifies and defragments the computing world a lot.
> But if today you can take an OpenGL engine with highly-optimized ASM stuff, with this new world, the highly-optimized ASM stuff would be installed just like a driver today is. And in a way, it is: a "cpu driver" :-)



