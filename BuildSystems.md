DependencySystem is an attempt to generalize this subject and solve the problems.

# Build systems #
Most software projects (except very small ones) require a _build system_ to build correctly. A build system's main feature is the ability to decide what is the correct build order, based on the dependency tree given. For example, if module A requires module B to compile correctly, the programmer will tell the build system about that. When building A, the build system will make sure that B is built (and if not, build it first).

The concept of dependency systems can be generalized beyond software building. A good example is booting Linux. When a Linux system boots, a long list of processes (usually daemons) need to be run. Some of these processes depend on others, and some don't. The usual method for booting Linux is basically a long script that executes the processes sequentially. Some special Linux distributions have come up with a nice way to speed up the boot procedure: they use a build tool (I think _make_) to control the running of processes. If two processes don't depend on each other, the build tool will execute them in parallel. (Although on single-cpu machines this doesn't seem to make any difference, it actually does because of the large amount of I/O performed by these processes.)

This example highlights the fact that a build system is much more than a build system: it is a dependency system.

## Side note: problems with Make ##
Before we go into the various applications of a general dependency systems, let's review the common build systems' faults. We will review _make_, keeping in mind the fact that most build systems have similar limitations:

  * Requires use of special syntax (with its own limitations)
  * Can't detect dependencies automatically
  * Hard to manage (a lot of makefiles)
  * Doesn't identify build changes correctly (e.g., doesn't take into account the switches we passed to the compiler when deciding whether the existing target is new or old)
  * Can't propogate information up or down a tree (e.g., if we want to disable logging in a whole subsystem we need to change the logging variable in all the makefiles of the subsystem)

People who use _make_ usually supplement the build system with scripts that will make it easier to use. This means that the build system fails to supply some very important features. And of course, other build systems exist. Because of these limitations, many people use build systems other than _make_.