# List of initial tasks #
  * Work on the Python fork that will allow privates.
  * Add digital signature verification support for C-module imports.
  * Review Python library modules and classify each module as: Data (such as xml module) or Authority (ie. I/O or system calls, such as os or socket). We also need to specify if a module has mixed portions (for example, if a data module also does some direct IO from it's C code).
  * Create forks of all the mixed modules by removing the I/O parts and seperating it into a different module - we might do this in some other way, but this is the general idea.
  * There is a lot more to do, see below.

# Detailed explanation (by Peaker) #

Object-capability security is the opposite of "ambient authority" security. Ambient authority means that authority exists in the "background" and you "ask" for authority and permissions checks may or may not grant it. For example, any system with an "open" call that takes a filename into a global namespace has "ambient authority".

Object-capability systems must not have ambient authority.

First, start with some realizations:
Python Modules can be divided into **two kinds:**

  1. Pure immutable code/data modules (modules that define a class of mutable instances are themselves immutable. Its the instances that are mutable).
  1. Modules that use C code to access "Ambient authority" of the underlying system (access syscalls that let you access authority in global namespaces).

We want to get rid of ambient authority in Python, so we just need to
get rid of 2.
While the python modulespace is a global namespace, its a global
namespace into immutable objects which present no authority. In
practice, this is false because modules in Python have mutable dicts.

In order to implement things like a "Read-only proxy" for a file
(needed for capability-security), we need support for "real privates",
or we could do:

l33t\_hax0r = read\_only\_accessor._full\_access\_file_

Which is a big no-no.

Therefore, I propose this plan:
  1. Make normal modules (consider "xml" as an example) immutable (recursively. It must not contain anything mutable).
  1. Remove all "authority" from modules. ("os" goes bye bye! "zipfile" loses its open-wrappers, etc). This may prove to be the hard/tedious part (need to review all library modules for authority).
  1. Add private support to Python, by adding a C class that exposes only a subset of attributes/methods of any arbitrary object (thanks Rhamp for the idea).  This still means you have to use the C class everywhere and you unnecessarily expose authority, and can be further improved later.
  1. Create a main() wrapper that converts silly Unix conventions (like filenames) into authority-objects that represent directories, files, etc.  These objects can be passed around instead of an "almighty" "os" module.

This might allow Python to be used to run untrusted code without fear,
and be the first proper OCap language that uses mainstream concepts...