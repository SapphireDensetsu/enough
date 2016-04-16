# Current Results #
**Coming soon** - a Subtext-like environment implemented in Python.

# (old) Goals #
## Near-future ##
  * Implement a programming environment akin to Subtext, in Python
  * Implement a similar program in Haskell (this is for us to learn Haskell)
  * Organize a shared code base, and start making a Python library

# Top-down #
I believe we should go for a top-down design of the system first. I think that going bottom-up (like Subtext) is too "open". Its unclear what the right way to go is.

Going top-down (from the desktop down) has much clearer requirements (an interface that minimizes the learning curve and working time to achieve certain use-case goals).

## Common computer features used ##
I believe we can start by specifying desktop requirements we want to provide. For this we can look at what most people use their computer for.

  1. Processing simple information (via Excel, calc, etc)
  1. Searching for and reading textual/graphic information (usually via web)
  1. Communicating with service vendors (i.e performing simple input/output tasks against vendor web sites)
  1. Conversing with others (either online via instant messaging, or offline via email) by exchanging static textual/graphic information
  1. Publishing textual/graphic information for anyone to see (blogs, web sites, comments on these)
  1. Editing shared textual/graphic information (i.e wikipedia)
  1. Editing non-shared rich textual/graphic data (usually via word processors)
  1. Formatting rich textual/graphic data (usually via word processors)
  1. Printing rich textual/graphic data
  1. Games
  1. Voice/Video conversations

## Requirements' analysis ##

### Processing simple information (via Excel, calc, etc) ###
This is to be supported by exposing an interface to access literal values (such as numbers, text, etc), and various "built-in" functions as desktop operators (such as simple arithmetic, trigonometry, etc). This can be done in a Subtextual way at the desktop level. Ofcourse this exposes us already to convinence issues about the data entry (the arithmetic is stored and used as a functional flow, but should be viewable and editable as an expression).

### Textual/graphic information ###
A recurring data object in today's world, is the rich textual/graphic information. This is usually HTML, but sometimes it is a collection of HTML, CSS, XML's, etc.
I believe that we should have a standard way to store textual/graphic information that consists of:
  * The unformatted information (equivalent to CSS'd html today). This would include information about the headings, and perhaps be similar to a TeX document. However, there could be multiple "templates" for unformatted information (actually different languages in which contexts' there are different heading types, etc).  For example, a "letter" template could have heading types: "Recipient", "Sender", etc. which are later formatted by a "letter" formatter to be printed whereever. A normal document would simply have "Heading 1", "Heading 2", etc.
  * The formatting rules (equivalent to the CSS or such today): Rules that explain which heading types are displayed where, and how. Note that you can attach multiple formatting rules to the same data, such that it is best displayed on the screen when being read, and yet printed in a different pre-conceived set of rules.

The unformatted information can also include references to images, links to other objects, etc.

### Editing non-shared rich textual/graphic data (usually via word processors) ###
These textual/graphic data described above can be edited via special editors that can edit the formatted representation (The formatter should probably be a combined formatter/editor) via any formatter (i.e: Word's normal vs. WYSIWYG view).

### Formatting rich textual/graphic data (usually via word processors) ###
The same formatters should be able to also editing the formatting information(?)

### Printing rich textual/graphic data ###
Normal formatters (that are used with the screen) may have special features for the windowing system that are unsuitable for printing (such as rezooming and shuffling things to allow better use of screen space).
Special print-friendly formatters can be used, which are very similar to the normal formatters, but output an image that can be connected as input to the printer spool.

### Publishing ###
Today, publishing addresses or information to the world consists of multiple systems:
  * Registering to a domain name registry if you want your address to be found by a simple name.
  * Implicitly registering your web pages to a search engine (by allowing it to spider you).
  * Email addresses typically register a name with an email provider.
  * IM systems typically register a name (or an email address) with an IM provider.
  * Other systems (i.e Skype) with the appropriate provider.

These should be united in a single central publishing system.
Attempts like these have already been made (Microsoft Passport), but these do not allow for all of the above services.

Registering your objects to a central searchable database is a necessity. Therefore, this database should probably be the only entity to which one registers.
It should be able to contain network references back to entities (web pages, an "instant messanger", a mail box).

This central database should not be searchable by something like a "unique name" alone, as this is prone to typos/phishing, trademark issues, etc.

A mail box would probably not be published on a personal computer, as that has downtime. You would probably publish a "buffering proxy" mailbox between the central database and the mailbox. Anecdote (move this to appropriate paper later): Only one mailbox should be put on the central database, for people trying to contact you by name alone, and this would be most prone to spam. Other references to your mailbox (on a business card, in "mailing lists" if those should still exist, etc) can be to dynamically created mailboxes which would help to identify the source of spam and localize it.

**note** (noam): maybe we should give out our mailbox as a "not passable" capability to our friends, which will have to request permission if they want to introduce us to someone new. wil can use a different facet for non-friends such as on our buisness card, and this too will be "not passable". that way if anyone who sends spam we can void his facet, therefore disabling his capability to mail us, and also we can trace exactly how he got our mail, by checking the facet he has used.

### Searching for and reading textual/graphic information (usually via web) ###
Search today is based on "web spiders" that walk the rich graphical/text objects and the links between them.  All such objects will addressable by a local database already, so we need to find a way to efficiently implement a "merged search" that searches all of the databases at the same time.  A merged database server (a.k.a Google equivalent) could sit somewhere and could actually be explicitly updated about changes to the local databases, instead of globally polling all of the databases for their entire contents all of the time.
Ofcourse, this means that only databases that want to be indexed are indexed, but this is already the way it is today (via robots control in web sites). However, today the default is to be indexed, and perhaps that should be addressed.

Everyone shall have a network reference to the central database by means of an initial reference, exchanging these references with each other or use of the domain name system, perhaps. In any case, this could become the only real central system (equivalent to today's domain name system).

### Communicating with service vendors (i.e performing simple input/output tasks against vendor web sites) ###

This can be replaced by the execution of simple code components on the vendors' hosts (that may be migrated to the user, ofcourse). These should probably contain rich textual/graphical information alongside processors that require the user to fill in appropriate inputs (just like any other program), allowing the "connection" of input from automated outputs, GUI widgets, or any other object.  They should probably not have any capability to any resource on the user's computer, unless connected to those explicitly by the user (for example to gui widgets to fill in the forms).

### Conversing with others (either online via instant messaging, or offline via email) by exchanging static textual/graphic information ###

It was already explained above how people should "find" each other (via the same central database). In fact, its not people finding each other, but entities such as an "instant messanger" that finds another instance of itself. Once found, it should be possible for them to communicate.
For conversing this is trivial (just drop a text/graphical object into a remote box you found).

### Publishing textual/graphic information for anyone to see (web sites, blogs, comments on these) ###
Web sites are trivial text/graphical objects that are referred by the central database.
Blogs may be lists of such, that also refer to comment trees (which are trees of such text/graphical objects).
The method by which one has authority to create comments according to arbitrary rules should be discussed.

#### Performance ####
(Noam): We shouldn't ruin the web's greatest acheivement which is how quickly you can surf. We might need to have different "protocol sets" for surfing the global world of objects, because for many websites authorization/authentication is not neccesary and would just waste our time. Same for video/voice and any highly performance sensitive application that requires minimum protocol overhead.

### Editing shared textual/graphic information (i.e wikipedia) ###
By having a full-access reference to the textual/graphic information (rather than a read-only one) from the central database, the data becomes editable.
Versioning is already built-in and versioned data cannot be edited in any case, even by fully authorized access to an object.

### Games ###
Games are too difficult to support in this early stage. Also, there are many users for whom a system that does not support games is very viable.

### Voice/Video conversations ###
Later.