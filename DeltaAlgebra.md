# Introduction #
"Delta Algebra" is the name for a formalism of the concept of deltas used in PackageLibrary. The relation between this formalism and the practical deltas used in the Enough PackageLibrary is not well defined. This formalism was created mainly for amusement, but it may find future applications in (possibly automatic) formal verification of a system that uses the delta concept.

## Notation ##
  * Functions are in _italic_, e.g. _f_.
  * Sets are in **bold**, e.g. **V1**.
  * The empty set is {}.

# Foundations #
## Invertible functions group ##
### Basics ###
  * **V** is the set of all values.
  * **Common domain** of _f_ and _g_ is the intersection of their domains.
  * **F<sub>inv</sub>** is the set of invertible functions. These are functions satifying:
    * _f: **V1** -> **V2**_, where **V1** and **V2** are subsets of **V**.
    * _f_ is **invertible**: There exists _f<sup>-1</sup>_ such that _f<sup>-1</sup>_(_f_(x)) = x for every x in **V1**.
      * By definition, we have _f<sup>-1</sup>_: **V2** -> **V1**.
  * **Equality**:
    * Given the following:
      * _f_: **V1** -> **V2**, where **V1**, **V2** are subsets of **V**
      * _g_: **W1** -> **W2**, where **W1**, **W2** are subsets of **V**
      * _intersection_(**V1**, **W1**) != {}
      * **X1** is a subset of **V1** and also a subset of **W1** (a subdomain of both _f_ and _g_).
    * We define _f_ = _g_ _in **X1**_ iff for every x in **X1** _f_(x) = _g_(x).
    * If **V1** = **W1** ( = **X1**) then we say that _f_ = _g_ _totally_, or: _f_ and _g_ are totally equal, or: _f_ and _g_ are identical. In this case the two functions are indistinguishable and are one and the same.
      * Trivial result: _f_ = _g_ _totally_ iff  _f<sup>-1</sup>_ = _g<sup>-1</sup>_ _totally_.
    * The **Greatest subdomain of equality** is the largest set **X2** such that **X2** is a subdomain of both _f_ and _g_, and such that _f_ = _g_ in **X2**.
    * **Theorem e1**: If _f_ = _g_ _in **X1**_ then _Image_(_f_ on **X1**) = _Image_(_g_ on **X1**) =  **Y**, and **Y** is a subset of _intersection_(_Image_(_f_), _Image_(_g_)).
      * **Proof**: Since _f_ = _g_ _in **X1**_ we have for every x in **X1** a value y = _f_(x) = _g_(x). Call the set of all y's: **Y**. By definition every y in **Y** is in _Image_(_f_) and also in _Image_(_g_), so it is in their intersection.
    * **Theorem e2**: Using theorem e1's defintions. If **Y** = _intersection_(_Image_(_f_), _Image_(_g_)) then **X1** is the greatest subdomain of equality.
      * **Proof**: **TODO**.
    * **Theorem e3**: The restriction of _f_ to **X1** a subset of the common domain, named _f<sub>x1</sub>_ is totally equal to the restriction of _g_ to **X1**, named _g<sub>x1</sub>_.
      * **Proof**: _f<sub>x1</sub>_ and _g<sub>x1</sub>_ have the same domain, and the same image, and are therefore totally equal.
  * The **identity function** _id_: **V** -> **V** maps every value to itself. By definition _id_ = _id<sup>-1</sup>_.
    * **Theorem id1**: There is only one identity function in F<sub>inv</sub>.
      * **Proof**: If _f_: **V** -> **V** is an identity function, then _f_(x) = x for every x in **V** by definition. However, x = _id_(x) because we have already defined the identity function _id_. Therefore by definition _f_ = _id_ (totally) and they are the same function.
    * **Theorem id2**: For every _f_: _f_ _id_ = _id_ _f_ = _f_ in the domain of _f_.
      * **Proof**: _f_ _id_ means by definition _f_(_id_(x)) = _f_(x) = _id_(_f_(x)).
    * **Theorem id3**: _g_ _f_ = _h_ _f_ in the domain of _f_, if and only if: _g_ = _h_ in the image of _f_.
      * **Proof**:
        1. =>: The first equation means that for every x in the domain of _f_, _g_(_f_(x)) = _h_(_f_(x)). We can name y = _f_(x), then: _g_(y) = _h_(y) for all y in the image of _f_, which means that _g_ = _h_ in the image of _f_.
        1. <=: The second equation is: _g_ = _h_ in the image of _f_. For all x in the domain of _f_, there exists y = _f_(x). So for all x, we get _g_(_f_(x)) = _h_(_f_(x)).

### Group ###
The set of invertible functions F<sub>inv</sub> with **composition** and **inversion** form a **group**.
  * **Composition**: (_f_ o _g_)(x) = _f_(_g_(x)). In our notation: _f_ o _g_ = _fg_.
    * **Associativity**: _(fg)h_ = _f(gh)_ because _(fg)h_(x) = _f_(_g_( _h_(x) )) = _f_( _g_(_h_(x))) = _f(gh)_(x) for every x in the domain of _h_.
      * By induction, any finite composition of functions is associative, and we can always simply write: _f<sub>1</sub>f<sub>2</sub>f<sub>3</sub>f<sub>4</sub>...f<sub>n</sub>_ without parenthesis.
  * **Inversion**: by definition every function in the set of invertible function has an inverse. Therefore we may define the _inverse operation_ notated by <sup>-1</sup>.
    * **Theorem inv1**: _Symmetry of reverse_: If _f<sup>-1</sup>_ is the inverse of _f_, then _f_ is the inverse of _f<sup>-1</sup>_. (Trivial proof).
    * **Theorem inv2**: _Uniqueness of inverse_: For every _f_ there exists exactly one inverse.
      * **Proof**: If _g_ is another inverse of _f_, then _g_ _f_ = _id_ = _f<sup>-1</sup>_ _f_ => {theorem e3} => _f<sup>-1</sup>_ = _g_.

### Additional definitions ###
  * **A** is a set of functions, called the **atomic set**. Every function in **A** is called an **atomic function**.
  * A function _f_ is **applicable** to a value x if x is in the domain of _f_.
  * A **common applicable function** for a set of values **W** is a function that is applicable to all the values in **W** (**W** is a subset of the domain of _f_).
  * **Value class**: A **value class** is a set of values with at least one common applicable function (in other words, a value class is a set **W** of values where **W** is a subset of an intersection of _n_ domains of functions, where _n_ > 0).
  * **Conflict**: a pair of functions is said to _**conflict** in **X**_ (**X** is a subset of **V**) if and only if the functions are **not commutative** under composition, in **X**.
    * **Theorem (conflict 1)**: _An identity function never conflicts_.
      * **Proof**: Trivial - by definition, an identity function is always commutative under composition with any function.

## Metric space ##
After constructing the **group** with **F<sub>inv</sub>**, composition, and inversion, we define a metric on this group.

  * **Function path**: For two functions _f_, _g_ with an identical domain, a **function path** from _f_ to _g_ is a sequence of atomic functions, {_h<sub>n</sub>_} (called "the path", where each _h<sub>n</sub>_ belongs to _A_) such that _h<sub>n</sub>_ _h<sub>n-1</sub>_ ... _h<sub>1</sub>_  _f_ = _g_ totally.
    * If _f_ = _g_ totally then the empty sequence is a path ("empty path") from _f_ to _g_ and vice verse.
  * **Length** of a function path is the number of elements in the path (number of elements in {_h<sub>n</sub>_}, which is simply _n_). An empty path has length 0.
    * **Theorem path1**: For every path from _f_ to _g_ there exists a path of the same length from _g_ to _f_.
      * **Proof**: **TODO** using inversion.
  * **Function distance**: The distance _d_(_f_, _g_) is defined as the length of the shortest path from _f_ to _g_. Properties:
    * _d_(_f_, _g_) >= 0 (there is no path with negative length).
    * _d_(_f_, _g_) = 0 if and only if _f_ = _g_ in the domain of _f_.
      * **Proof**:
        * =>: if _d_(_f_, _g_) = 0 then the path from _f_ to _g_ is empty, therefore _f_ = _g_ in the domain of _f_.
        * <=: if _f_ = _g_ in the domain of _f_, then an empty path leads from _f_ to _g_, and the distance is 0.
    * _d_(_f_, _g_) = _d_(_g_, _f_). (Because of theorem path1).
    * _d_(_f_, _h_) <= _d_(_f_, _g_) + _d_(_g_, _h_).
      * **Proof**: If there is a path from _f_ to _g_ to _h_, then the path from _f_ to _h_ is at least as short - if we use the same path from _f_ to _h_ (through _g_). (Need to prove that it can be shorter?).

### Additional definitions on the metric space ###
  * **Connected values**: For a given set of functions, **F1** subset of **F<sub>inv</sub>**, two values x, y are **connected** if and only if there is a function _f_ in **F1** such that _f_(x) = y (by inversion we also have the opposite).
    * We then say that x and y are connected under **F1**.

## Invertible atomic function space ##
Given **A** a set of atomic functions, we may define a set _S<sub>A</sub>_ as follows:
  1. Every element of **A** is in _S<sub>A</sub>_.
  1. Every finite composition of atomic functions from **A** is also in _S<sub>A</sub>_.
  1. If _f_ is in _S<sub>A</sub>_, then _f<sup>-1</sup>_ is also in _S<sub>A</sub>_.

The resultant set _S<sub>A</sub>_ is an _invertible, atomic, function set_.
  * _Invertible_ because of property 3.
  * _Atomic_ because of properties 1, 2.

It is fundamental that only functions that can be composed from atomic functions can exist in _S<sub>A</sub>_.