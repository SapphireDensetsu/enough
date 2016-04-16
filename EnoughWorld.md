# The web #

The web is used to access many types of things. Each thing is replaced by something else in the Enough world.

## Static content ##

Static content should be replaced by remote read-only references to document, text, sound or image objects.

## Dynamically generated content ##

Dynamically generated content should be replaced by functions that return documents.

## Web applications ##

Web applications should be replaced by remote references to factories that make instances that can be conveniently used by the GUI.

## Flash applications ##

Flash applications should be replaced by GUI widget implementations that run locally (via AdaptiveProfiling).

## Search engines ##

Search engines should be replaced by "object databases" that hold many objects and can search them quickly. These databases can "spider"-walk documents and any object which can be walked, much like existing search engines.
Unlike search engines, an "object database":
  * Can be created and used over any scope of objects, local, remote or a hybrid.
  * Can get change notifications from the objects inside it, rather than having to poll these objects periodically. Thus the "Google" equivalent would receive notifications of updates rather than poll millions of unchanging websites, and be permanently out of date.
For extra efficiency, site update aggregators can be used to collect notifications about updates and notify all who are interested in those updates.

This aggregator can let millions of sites send updates to a single entity, rather than many different spiders. It can also be a central place to allow multiple search engines or content aggregators to watch the same site listing. It would allow sites to register with one large index, rather than many small ones.

This approach also makes implementing a [Web Archive](http://www.archive.org) much easier.

### Questions ###
  1. Why should a user spend his resources on updating a global search engine he doesn't care about? On the other hand, if the search engine DOES care about the user's data, how will the search engine index it, if the user doesn't care to update himself?
    * The user spends resources on that because he wants his pages to appear up-to-date in the search results, and because otherwise, he's forcing the engine to poll him regularly (which will waste more of his resources!)
  1. Who will be responsible for hosting such a huge database? It costs tons of money and some sort of profit will have to cover it. If there are several competing databases, will every user have to register his data with all databases to make sure he can be found?
    * Same as today, a company like Google. It will still use "spidering" so you don't have to register with anyone or anything.


# Processes #

Processes are not required, as address space separations are not required.

# Threads #

Threads may still exist, as explicit entities. Hopefully, threads will be implicitly used for independent functional (side-effect-free) paths.

# Applications #

Applications today are a collection of multiple things.
Enough does not have "Applications" as such. Instead, it uses the existing simpler primitives of objects, references and the uniform GUI to achieve the same and far more.

## Executables ##

Executables are replaced with objects and types. Some objects contain functions and actions, which contain code. These functions and actions can be serialized transparently and efficiently. More importantly, they can be deserialized efficiently.
Currently, executing an executable incurs a large penalty of deserializing an ad-hoc executable format, copying various things from the executable, and so on.
Instead, the executable can be replaced by a singleton object in some cases, or an instance factory in others.
References to library functions and such are direct references to either proxies or function objects of other libraries.
Thus, the penalties of execution, including those of dynamic linkage to various libraries, loading of much code into memory, and so on, are eliminated.

## GUI ##

Applications contain mainly two types of GUI code:
  * GUI glue code (This is the vast majority of "application code")
  * GUI widgets (Some applications implement their own user interface features)

GUI glue code generally consists of defining which widget layout to use in order to feed inputs and events into functions and actions. This can be replaced by either:
  * Nothing - Let the GUI heuristics sort out the layout to interface with the functions and actions automatically
  * Hints - The developers of the actions/functions (or others!) can write hints about the various functions, actions and their inputs and outputs (beyond metadata such as type that exists already), that helps the GUI heuristics build a sensible layout.
  * Layout configurations - If hints are difficult, or not good enough, full layout configurations specifying which widgets are to be used and how to access the actions and functions can be provided. Unlike existing glue code, multiple such configurations can exist, and be provided from multiple sources. The configuration of the GUI widgets should be directly editable from within the GUI.

GUI widgets are generally used to provide novel user interfaces. For example, one of the core components of a "word processor" is a marked-up-text editor widget. It consists of code that specifies how to respond to user interface events, and how to draw the user interface.

These GUI widgets are ordinary objects in Enough, and can be distributed as well.

## Scripting ##

Many applications today integrate "scripting engines" that try to expose their internal objects to a "scripting language".
In Enough, all objects are already exposed to the user interface, which is fully scriptable. For example, any object can be taken and given to any function or action.
There is no need for "scripting languages" or any extra work to expose objects and the interfaces.

# Email #

The "Email" concept is composed of several things.

## The inbox ##

The inbox, and various other "folders" or labels used, is basically a container for "messages". Each message in Enough is simply a document object. The "Inbox" can be implemented as an "Object Database", but one that also exports actions/methods to add items into the inbox.


## POP/IMAP ##

These message retrieval protocols are replaced simply by network-transparent reference to a remote object database object.

## SMTP/email addresses ##

These can be replaced by handing out a network-transparent reference to the append/add method of the object database. By creating trivial append/add wrapper actions and handing out references to them, one can know more about the source of the message (equivalent to Gmail's username+identifier@gmail.com feature, except its more secure).

## Mail browsing GUIs ##

Webmail is very popular, and so are various desktop mail readers.
These various GUI's would be replaced by a configuration of functions and widgets.
For example, a Sort function can be used on the object database containing the mail items, and the output of Sort can be attached to a GUI widget. The object database can have some metadata about the fields within it (such as containing of "send time", "receive time") which allow the display widget to sensibly display the messages.

## Calendaring ##

A calendar in Enough is the mapping of Time objects to arbitrary TimeRange objects. In the case of typical calendaring, these arbitrary objects would be "Meeting" objects that contain various data about the meeting.
An action that adds to the calendar (after whatever prompts necessary) can be used on any "Meeting" objects that are in the inbox. A specific action that adds to a specific calendar can be specified as a default action for Meeting objects (Allowing double clicking on any Meeting object from any context, not just email, to add it to that calendar).
In addition, an action that processes all messages that go into inbox could apply them automatically on the calendar according to arbitrary conditionals (as to allow exposure to the information in those Meeting objects in the Calendar viewer immediately).

## Availability issues ##

Much of the point of email is the availability of the mail servers, and the resending features they use to overcome downtime in various mail servers. The typical client pulls his mail from the mail server at his uptime, allowing him to be down most of the time.
If handing out network references to methods of objects on the local machine, downtime could make message sending impossible. Enough can resolve this in the same way its resolved today: use mail "servers" with high uptime, as simple hosts that host the inbox objects and appending actions on them, to allow network references to be given to those hosts.

# File system #

The file system serves a few purposes:

## System files ##

System files in Enough are replaced by ordinary objects who are serialized to disk transparently.

## Persisting user data ##

In Enough, [everything persists](OrthogonalPersistence.md).

## Organizing/searching user data ##

In Enough, object databases hold the user data, and allow for far more powerful organization than a hierarchy of strings. Objects can refer to other objects directly, are typed, and can be associated with metadata that is indexed for fast searches.

# Save/Load #

Save is a user interface action that asks the system to persist the document, or whatever is being edited, now. Save has a few problems:
  * Saving multiple times typically requires writing a lot more than the amount of data that actually changed between saves, as the entire document is re-written.
  * It requires moving the disk head to a specific location that stores the specific document.
  * It often writes in-place, which may have catastrophic results in case of a crash (Not only may the save itself fail, but it may destroy the existing copy).

These problems have led to the current design of exposing an explicit "Save" action to the user, which also requires the user to select a "name" for the file.

This has a significant drawback: User data is **Lost by default**.
In Enough, save is unnecessary. Only the very latest user data can be lost in a crash (inherent flaw), which loses at most a short moment of work.

## Saving multiple times ##

In Enough, the platform divides information into "computables" and "source data". "source data" must be kept, whereas computables can be recomputed (or requested again) at will.

The modifications to the world generated by user actions are "source data", while the world itself, or anything within it, is a "computable".

These modifications can be persisted all the time, and thus avoiding rewriting the same redundant data multiple times.

## Disk head optimizations ##

Unlike existing file systems which have to move the head to a specific document in order to write the changes to it, Enough can organize the disk differently. It can place "source modification logs" in various locations on the disk, allowing to write the source modifications as they arrive to the disk position nearest the head.
This may make the crash recovery process more expensive, as it would have to scan all the relevant regions in the disk for modifications made, but it would make normal operation much quicker.
This makes constantly saving important inputs cheap, even with existing disk hardware.

## In-place writes ##

Enough saves source modifications, which are relative, and does not overwrite previous modifications. This means that a crash can only lose "newer" writes.
This may mean that a single corrupted modification can start a chain reaction that loses all of the computed world that follows. This means that we may want to redundantly store the modifications, and that we may want to store "snapshots" (a computation of the entire world) that can be used as sources, and are redundant to all of the sources before them.

## Result ##

Enough can thus recover from crashes without losing almost any user data, without the need for explicitly saving. Due to revision control, the user can also go back to any previous revision of a document, so there's no need to worry about "save" overriding his previous revision.