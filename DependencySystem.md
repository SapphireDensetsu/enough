# Background #
Read about [Build systems](BuildSystems.md) and their problems first.

# Dependency Systems #
We haven't survyed the build system market and maybe some of them are quite good. Our point is that dependecies are much more common that just in software building. Some examples follow.

## Engineering ##
A common headache in software (or any other) engineering originates from dependencies. They begin in the _requirements_. The users or customers (a role often played by the designers themselves) define the basic _user requirements_. Sometimes these requirements are quite complex. Often, some requirements were instituted because of other requirements, even at this early stage. The next step is what we call _system requirements_. These are usually defined by the designers of the system when they begin their work. Obviously, many system requirements **depend** on one or more user requirements. Some system requirements depend on other system requirements. Some may depend on implicit requirements (the company's reputation is an implicit requirement!). During the system development process, some new requirements may come up - these too depend on something, usually something that was overlooked previously. Also, some requirements are cancelled later in the project's lifetime.

The eventual outcome of a requirement is some feature of the system being created. Thus, requirements _depend_ on features.

**Requirements are usually a dependency tree**, or a graph in a worse case. If this tree is not documented and managed, mistakes will happen. Someone might cancel a requirement without remembering to cancel all requirements that depend on it, leading to unneccesary work. A much worse scenario is the opposite - cancelling a requirement that is still caused by another existing one.

In critical systems the managers hopefully have enough sense to foresee this problem. To solve it, a software "requirements management system" is used (and it must be properly enforced). Such a system may supply features that are specific to requirements management such as easy documentation, collaboration, etc.

For every engineered project, further down the road comes quality assurance, and here too there are dependencies. A test is performed to validate some feature which was developed to fulfill some system requirement that was conceived because of a user requirement (in the average case this example does in fact reflect reality!). Documentation of this project depends on other things as well. This tedious description of engineering dependencies must come to and end and _here it is_.

The points are:
  * Dependencies can pop up everywhere. Sometimes they have a critical significance, and sometimes they can just be used to improve something, but they exist outside building software.
  * In many cases, it is important to **integrate dependency management**. In the above engineering project example, a true requirements management system should be usable at all stages of the project, from initial project definition to final release tests.

## Dependency Systems and Live Programming ##
In [Live Programming](LiveProgramming.md), we always work with objects that the system recognizes. Therefore, it is possible for the system to know about dependencies between these objects. **The two concepts merge naturally**. Using a Live Programming system we don't have to re-implement dependency management for every new application: it is part of the system's powerful understanding of what you are doing.

First of all, in LiveProgramming, there is no need to "build" a program. The program is built incrementally as it is being edited.

#### Visualising the new way to engineer ####
For the situation of requirements and testing described above, our vision is the following. The customers describe the initial system requirements using the UnifiedInterface, instead of writing a textual document. This can (and should) still be represented in natural language. Instead of typing letters on a page (which the computer will never understand), each requirement will be an object. Of course we can still generate a document from these requirements (and even graphs). It will be easy and intuitive to link related requirements and to specify dependencies between them, by a UnifiedInterface for representing dependency relationships between objects. The system designers will receive these initial requirement and expand on them with system requirements. Any new requirement will need to be assigned a "parent" to specify its origin (what does it depend on). Similarly, features will be defined and tests for each requirement and feature will be specified.

The system will supply several generic graph and dependency algorithms such as "find leaves" to easily manage this graph. For example, it will be easy to search for all tests for a given feature, or to automatically warn about a requirement that has no tests specified.

Connecting between different but related projects will not be such a headache because everything is in the same "world". Networking will be transparent with [Capabilities](Capabilities.md), [NetworkReferences](NetworkReferences.md), AdaptiveProfiling, and therefore there is no issue of a central server on which to place the project (we can still specify some way to centralize the data).

Project tasks ("change requests" or "todos") will similarly be managed by connecting related items. It will be easy to implement and modify various management tools - such as viewing overall progress, and creating a project schedule ("gantt"). No disconnected, specialized applications will be used. Instead, everything will be connected and a task in the gantt will be a task in the source control (or related to one) and will still depend on some requirements.



_expand this section!_