# Introduction #

Some general principles that should guide UI design.


# Details #

1. Properly use the screen real-estate

Avoid overlapping windows (Very stupid use of pixels) - it is always possible to better arrange the pixels than overlapping windows.

2. Display output as soon as possible

> 2a. Dependence

> If the output does not depend on some input, DO NOT wait for that input to display the output.  Example: A question such as "Should I save the password you just entered?" should not delay the login itself.

> 2b. Defaults
> > If the output does depend on some input, but the action that generates the output is not harmfully irreversible, and there is a sensible or likely default to use as a possible input, try to use that default and display output as soon as possible.
This may also increase the user's understanding of how the output depends on the input.

TODO: Explain more thoroughly.