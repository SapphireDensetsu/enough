# Introduction #

Traditionally, there were two main approaches to memory management:
  * Manual memory management of a heap, and (semi-)automatic management of the stack.
  * Automatic memory management of both heap and stack.

## Manual Memory Management ##

In "lower-level" languages (e.g C, C++, Assembly, etc) memory is managed manually.

Memory is typically divided into a "stack" and a "heap".

The stack is used for allocations that use a LIFO-order.  LIFO allocations are much easier to manage, as you can just move a pointer forwards to allocate and backwards to free. Thus, each thread was allocated a stack, in which it could allocate data. The calls themselves (return addresses, local variables and arguments) were also allocated on this same stack, so all stack allocations had to be freed with a return from the allocating function.

The heap is used for random-ordered allocations.  The heap could allocate any sized object at any time (resource constraints applied, of course), and can free any allocated object at any time.  Freed objects theoretically allowed the space to be reused immediately, but objects could typically not be moved, so memory fragmentation often prevented use of freed space.

Traditionally, memory was also allocated on disk, in the form of files, but this is not important for this discussion.

## Automatic Memory Management ##

In "higher-level" languages (e.g Python, Lisp, Ruby, etc) memory is managed "automatically".  No "stack" or "heap" are exposed, and objects are allocated explicitly, but deallocated automatically. In some languages (Scheme), objects are said to exist "forever".  The objects do not exist forever, of course, but are simply deallocated when it is impossible to detect - when no references to them remain.

Some higher-level languages attempt to analyze the program in order to convert as many allocations as possible to stack allocations internally. Some just use random-ordered allocation for all objects.  Reference counting is sometimes used as an incomplete method of discovering that an object is no longer referred, but for completeness algorithms to track all references must also be used.
Some languages use multiple indirections so objects can be moved around to defragment memory, in which case a simple increasing pointer can be used for O(1) allocations.

# Computations #

The purpose of memory in higher-level languages, and in Enough, is to hold objects.
In Enough, unlike former languages (except some functional languages), some objects are "constants" and forcefully stored in memory, and some objects are computational results, and stored in memory as a "cache".  Any portion of the cache can be purged at any time, and recomputed at will.
The constants in Enough consist of the "Current World Version", and a list of "Actions" that are the state-transitions from the past and can be used to revert to the past.
A constant inside a computed value can also be recomputed and is in the cache.

When running out of fast memory (RAM), any cheap-recomputable object can be thrown away to make room.  If no cheap recomputable objects remain, normal swapping can be used.

When running out of real memory, or arbitrarily, actions can be purged from the constant action list. Typically, very old actions will be purged, but very large ones may also be purged for resource purposes (in which case, a version gap is created for some objects, which means that those versions of the objects and any dependent computations will become un-computable).  When constants are explicitly purged, they become inaccessible and can be freed.  All references to these constants are known as computational-relations and can be purged from the cache as well.

Note that the constants (Current Version and Action List) are stored in "Memory", but that does not mean RAM, which means much larger constraints are in effect.

# Recomputation costs #

Every item in the cache can be recomputed.  Recomputation costs CPU time and potentially other resources.  When each object is computed into the cache, measurements of the costs can be stored, and used as a good estimate for the costs of recomputing that object in the future.  Objects that are cheaper to recompute can be more cheaply purged from the cache. See ComputationVsStorage.

# RAM as a cache #

In Enough, RAM is just a cache to disk (See [OrthogonalPersistence](OrthogonalPersistence.md)). RAM can be thrown away to disk at any time and restored back into memory when accessed.  When RAM is used to store recomputable memory (a portion of the cache), Enough can compare the costs of writing and reading the object to disk, to the costs of recomputing it later, when it is necessary. This allows to eliminate a lot of swapping for memory that is quicker to recompute.  It also allows more aggressive RAM freeing, if a lot of the RAM stores easily recomputable objects.

# TODO #

Example of purging and recomputing?
How is the low-level RAM management done?