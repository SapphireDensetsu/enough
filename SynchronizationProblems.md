# Traditional concurrency #
[Multithreading on Wikipedia](http://en.wikipedia.org/wiki/Multithreading)

Many applications require or gain by dividing work into concurrent parts. Unfortunately, this entails a heavy cost of coordinating these parts (usually processes or threads) to work together. The coordination of concurrent (or synchronization of asynchronic) processes is hard because the abstract part of our mind is much better at analyzing serial situations. It is very hard to imagine more even two processes working at once, with all the possible combinations of states for each one.

Traditional synchronization primitives include:
  * Mutex
  * Semaphore
  * Barrier


# Problems #
The traditional methods for synchronizing are mutexes and semaphores. These are low-level synchronization primitives because they do not "know about" the specific task that is being coordinated. Rather, they are at the level of protecting "critical sections" of code, or locking a resource at a particular point. It is a complicated (if not impossible) task to validate that the low-level primitives that are used in a system really cover all the asynchronous possibilities correctly.

After a concurrent system is implemented, it is also very hard to test and debug it. To perform full tests on such a system means to reach all combinations of states between all concurrent processes. This is very hard and usually practically impossible. To debug a concurrency bug means to re-create the asynchronous state of the system, which is also very hard. It may be interesting to see statistics of bugs in multithreaded applications. It will be no surprise to find that these applications harbor many "unfixable" known bugs.

# Common bugs #
Usually, the source of the problem is identified in some forgotten situation that requires locking, or some other synchronization mistake. The truth is that unless the design and implementation are intensively verified (by repeated review), these mistakes will always occur. The real reason behind these problems is that it's the programmer's responsibility to avoid them.

The solution (as described in many BuzzWords, especially [Promises](Promises.md) and [LiveProgramming](LiveProgramming.md)) is to remove the responsibility of low-level synchronization from the programmer. Instead of saying "lock before running this code", the programmer should be able to say "do this concurrently" and the system will take care of the rest.

Here are some examples of common asynchronous programming bugs, and the **fundamental** reasons behind them.

### Race conditions, deadlocks, and the rest ###
Race conditions are very common bugs in multithreaded applications. Any mistake in synchronization, usually in usage of locking mechanisms, can lead to several equally possible behaviours, that depend on timing and scheduling order. Deadlocks and starvations occur for similar reasons. Any non-determined behaviour is very hard to debug. The reason for these bugs is that the programmer has to remember the dependencies between threads and enumerate all the possible interactions between them (see DependencySystem and [Promises](Promises.md)). To make it even worse, it is extremely hard to analyze the implementation (see LiveProgramming).

### Example: deadlocks with thread pools ###
A real example of a deadlock bug involves using a thread pool (see [Thread pool on Wikipedia](http://en.wikipedia.org/wiki/Thread_pool)). In this particular case, there is only one ("singleton") thread pool. The main program module requests some threads from a thread pool that contains N threads. These threads in turn also need to create threads, so they also use the pool. Sometimes, the main module creates more than (or exactly) the number threads (N) that the pool contains. In that case, if a thread also needs to create a thread it will deadlock with the main module. The thread pool does not contain any more threads, and each of the running threads is _waiting for the thread pool_.

#### Where is the problem? ####
One could say that the problem lies in the fact that the thread pool is a singleton. If there would be many thread pools, at least one for the main module and one for all the threads that need to create threads, the problem will be solved. However, **the real problem** is that the programmer needs to think in terms of threads in the first place. A modern system should offer the programmer high-level constructs that will allow him to say "run this concurrently". See [Promises](Promises.md) and HighLevelProgramming.