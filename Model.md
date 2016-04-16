# Definitions #

Instance: Values can be "leaves" (in which case they hold Pythonic instances) or hold fields which are also instances.

Class: Each instance has a "class". Several instances can have the same class.

Field: A field is an instance.  Fields are "keys" to children in the instance hierarchy. The set of fields in an instance is determined by its class.

Public fields: Instance-fields of a class that are exposed in the class's "public\_fields" field.

Private fields: Non-public fields.

Path: Each instance's "identity" is a "path".  A path is a sequence of fields.

Universe: Universe is an instance. Its the "root" of the instance hierarchy. Its identity is the empty path.

Subpath: A subpath is a path that is not relative to the Universe ("root").

Links: All references are represented by a "links" map. A links map, maps all sub-paths in a class to other sub-paths in the same class. All Instance values are taken from the link sources.

Magic Function: A class whose fields have magical relationships. Values of fields in instances of Magic Functions may be derived from values of other fields in that magic function.

Magic Types: The types of objects which are "leaves".

Source Values: A set of objects that are a given an immutable and eternal value that is not the result of a computation.  All other values are computed.

## Revisioning ##

World: An immutable state of things.  "Mutations" on world actually mutate universe, not worlds, by creating derivative worlds.

  * In "source-control" terms, a "Universe" is like a "repository", and a "world" is a "revision".

# Implementation #

## Pull ##

Compute a value of an object (identified by path).
To do this, a recursive process that involves following links is ran until a "source value" or a field of a Magic Function is encountered. If a field of a Magic Function is encountered, the magic function is requested to compute it. It, in turn, is likely to recursively invoke a Pull operation on its source values.

### Following links ###

Links of the classes of each of the subpaths of the path (ordered by shortest to longest) are consulted to find a linked source of the value.  If the full path is not linked into, links are then searched in the same way for each of its subpaths (from longest to shortest).

# TODO #

  * Non-directional computing
  * Actions/Revisioning