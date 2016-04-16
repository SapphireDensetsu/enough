# The Problem #

Enough uses [DifferentialComputing](DifferentialComputing.md). This means that every result is actually the application of a difference (delta) to a previous result. This also works in the opposite direction - a previous result can be recomputed by applying the reverse difference on the newer result.

As described in [MemoryManagement](MemoryManagement.md), once we compute a result we have two options:

  1. Store the result until we need it next time, and possibly discard the old results from which it was derived.
  1. Discard the result, and save instead a cheaper (in terms of resources) older result that will be used as the basis for applying differences. When we need our result again, we will recompute it from the old, saved result.

# Formulation as a graph #
This problem can be formulated in the following manner.

A **node** in the graph is a computed result. Each node has its associated "cost" in resources of storing that result. For a node A, the cost will be notated A. The actual cost of "being" at a node is the amount of time spent at that node, times the cost associated with that node. Since we can store as many computation results as we want (in theory), we can "be" at any number of nodes simultaneously. We suffer the total cost of all the nodes.

An **edge** in the graph is a difference. Each edge has a time-cost associated with it, which represents the amount of time it takes to apply that difference. Thus, to move from node A to node B on an edge E implies wasting the amount of time that is associated with E. An edge can be traveresed in both directions (because deltas are reversible). We can only move across one edge at any given time (ignoring parallel computers).

The **graph** is the history of an object. Each independant object thus has its own seperate graph. The graph will probably really be acyclic.


Now we can re-state the problem using the new terms. At various points in time, we will need a computation result A. This means we will need to "be" at the node A at that time. We can say that the requirement to be at A is anticipated to occur according to some time-dependant probability. Thus, we can either:
  1. Move to and stay at the node A until the result is needed, suffering the cost A\*t, where t is the amount of time until A will never be needed again (or when we can anticipate that A will be needed only on rare occasions).
  1. Move to and stay at some other node B, such that B < A (cost of B < cost of A), suffering B\*t. When A will be needed, we will have to move from B to A which will waste the amount of time of the shortest edge path from B to A.