# Background #

Persistence is a term used to describe the copying of data from volatile memory (such as RAM) to non-volatile memory (such as the disk) in order for it to _persist_ in a case of a crash or power-down.

Orthogonal Persistence means that the operating system offers **only** non-volatile memory that always persists to the applications, and thus frees them from considerations of persistence as well as "bootup" and "shutdown" sequences.

# Traditional Systems #
Traditional systems require programs to persist their data explicitly.  Programs allocate and access non-persistent space (RAM) with a set of totally different tools than they allocate and access persistent space (Disk).

## Example ##
An application such as a word processor usually installs with files of different sorts:
  * The main executable
  * Additional libraries (DLL's or shared objects)
  * Application data - localization data, icons, help files (which are actually directories or archives including many files and multimedia content)
  * User-specific information (stored in the user's home directory or in a database such as the registry)
  * Built-in user data (supplied by the creator of the word processor):
    * Templates
    * Multimedia (clipart, images, sounds)
    * Example documents

There is a whole lot of code written just to handle these files:
The installer has to deal with putting each of these files in the correct location, and the uninstaller has to know which files were installed in order to delete them properly.
The application itself has to know where to look for these files on disk and maybe allow the user to control these locations.

## Consequences ##

  * All programs must explicitly designate which parts are persistent, and which aren't, and _use different primitives_ to manage and access the different parts.
  * Persistent data may not contain references to other objects because there is no way to guarantee where the data will be loaded in each instance the program runs. This highly limits the program design and requires explicit attention to the issue of persistence when designing the program.
  * The program is burdened with the task of choosing a file system location and filename in which to store the data.
  * The program is burdened with the task of choosing correct file permissions that avoid security problems.
  * All programs are burdened with the task of "booting up" and "shutting down", during which they must examine the file status and perform differing logic.
  * All programs must contain code to serialize/de-serialize their data (this is becoming simpler in high-level languages)
  * All programs must waste run-time in order to serialize/de-serialize the data, while translating it from run-time representation to file representation.

### Handling crashes ###

#### The "simple" case ####
When explicitly writing into files, _all_ programs must take into account that the computer may crash during the write, and when booting up, they must know to handle the case where some of the data is more up-to-date than the rest of the data.
Most programs don't do this and in fact are **vulnerable to data loss in crashes, even if the underlying file system is journaling and perfectly handling the writes in the correct order**.

#### The "Concurrent" case ####
When accessing multiple files concurrently, where those files have cross references to each other, the problem is even more difficult. It becomes very difficult to handle crashes in a correct way that does not lose data, and verifies that all of the cross references are actually in sync.

# Orthogonal Persistency #

Orthogonal persistence greatly simplifies the world of applications. They no longer have multiple sets of primitives with which to access memory - there is just one memory type - the persistent memory. If program "installations" consist of copying the program in a valid initial state, then no "bootup" code or "shutdown" code is ever necessary to write.

There are many ways to implement orthogonal persistence in the OS, some of which are more efficient than others.

## The Naive implementation ##

The naive implementation of orthogonal persistence (the one used by "Hibernate" in Windows and Linux) is to simply copy the non-persistent small fast memory (RAM) into the persistent large slow memory (Disk) periodically.

In order to guarantee that the "image" copied to disk is coherent and from a single point in time, this naive implementation requires halting the computer until the copying is complete.

This implementation model was actually used in early computers, which also gave a bad name to orthogonal persistence decades ago.

## A smarter implementation ##

Note: This sections simply explains the persistency models of KeyKOS and later the EROS operating systems.

### The outlook ###

Consider the only space exposed by the OS is the large slow space (Typically Disk).  It does not offer primitives to allocate/free RAM, but only ones to allocate/free Disk space.
The smaller RAM is not "exposed" to applications, but instead used to cache the slow large space.

### Checkpoints ###

Periodically, a _checkpoint_ occurs. A _checkpoint_ means that the current state of the computer is logically frozen so that all data will be copied from RAM to disk to ensure that the current time point persists.

### Disk layout ###

The large disk is divided into 2 principal spaces: The _Log Area_ and _Home Locations_.
The _Log Area_ is too divided into an _Active Log_ which also serves as a _Swap Area_ and a _Passive Log_.

### Memory layout ###

  * The large _Home Locations_ area is where the actual objects are stored.
  * The _Passive Log_ may either be empty, or contains some modifications to the _Home Locations_ (which are soon to be copied to the _Home Locations_ after which it becomes empty again).
  * The _Active Log_ contains modifications on top of those of the _Passive Log_. However, these modifications are not copied to the Passive Log or to the home locations until a _checkpoint_.
  * The RAM contains modification on top of those of the _Active Log_.

### The mechanism ###

A checkpoint truly freezes the computer for a very short while, during which all of the RAM is marked [copy-on-write](COW.md). This is short enough time that the freeze is completely unnoticable, but does guarantee that further writes to memory will modify the next checkpoint data, and not this one.
After that, data is copied from the frozen RAM to the Active Log.
When this copying is completed, the frozen RAM may be discarded (i.e: Unmarked as [copy-on-write](COW.md) and discarding copied pages), and the Active Log switches roles with the Passive Log.
In the background, the Passive Log is migrated to the Home Locations.
In any case of a crash, the Operating System bootup code can simply complete the copying of the current Passive Log to the Home Locations to get a coherent system state from a specific point in time.

#### A slight improvement ####

The above mechanism is the one used by the KeyKOS operating system. EROS enhanced this mechanism with a simple modification. Instead of a Log Area statically divided into 2 (Active and Passive), the Log Area is divided into an arbitrary number of "generations" dynamically and according to the storage needs. Multiple generations can exist concurrently, where all of the non-active generations together serve as the "Passive Log". This approach is an improvement both because it does not waste unused space in a Log Area, and because it allows to copy each page that changed in multiple past generations (a common scenario) to the home locations only once, instead of once-per-generation.

### The Problem ###

Orthogonal Persistency has one large problem: If the log area (or current generation) is too small to contain all of the changes made to memory, the operating system can run out of memory for applications, until a checkpoint is complete. This is similar to the problem of running out of virtual memory in traditional Operating Systems.

#### The Solution ####

Either force an early checkpoint if the active log is filling up too fast, or allow dynamic increase of the log area (much like the swap space is enlarged when Virtual Memory is running low in existing systems).

### Advantages ###

#### Greatly simplified programs ####
Applications don't have to deal with files. They simply create a new object in the same way all new objects are created and the operating system takes care of the rest.

  * No need for serialization
  * No need for bootup/shutdown code in programs

#### Improved Disk Efficiency ####
The above described orthogonal persistence implementation copies data from RAM to the disk, and later from the _log_ to the _home locations_ in bulk. This frees it from write order constraints, and allows the data to be written in the most efficient disk order. Since disks are very fast at writing packed sequential data, but very slow at moving their heads, this could greatly improve disk performance by minimizing disk head movement.

# Additional Information & References #
_Put some more references, find publications on Orthogonal Persistence_
[Orthogonal Persistence on WikiPedia](http://en.wikipedia.org/wiki/Orthogonal_persistence)