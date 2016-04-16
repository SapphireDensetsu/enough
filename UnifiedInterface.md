# Introduction #
As explained by LiveProgramming, the developer's and user's interface to develop and interact with the program are unified into one interface.
This unification has several major implications:
  * It allows users to become programmers without the fuss of having to learn a complicated syntax and development techniques, and in effect empowers the user to become as powerful in manipulating the program as the developer is.
  * It unburdens developers from a lot of the GUI work, especially "customization" features
  * It unburdens developers from adding scripting and features into their programs that merely attempt to give simple programming powers to the users.

# Users become programmers #
Today, programs are treated as black boxes with a rigid interface by users. They cannot look inside to see how they work, and they can definitely not modify these programs. With Open Source programs, the users can legally see and modify the programs, but for that they are required to learn complicated programming languages, conventions and libraries.
With LiveProgramming, a program still **can** be treated as an input/output black box, but now the users can dig into the program with the same graphical interface that they use the program.
They can also look at how any of the programs they use work to learn how they work. If a user wants to know how MP3 decoding works, he can simply "zoom in" on the implementation of the "MP3 decoder" and view the algorithms.

# Unburdening developers from GUI work #
Today, programmers must specify their programs' inputs in multiple forms:
  * In the source code, as inputs for the logic
  * In GUI forms, that have code to pass this input to the logic code
Instead, the GUI to receive the input for the logic can be deduced automatically from the logic itself, and the input types requested by that logic.
Arrangement of the inputs required can be optionally specified by the programmer initially, but they can be modified or respecified by willing users. This means that customization is always "built-in" as the user can change any part of the GUI, and even replace user-inputs with outputs from other components, allowing for much more power.

# Unburdening developers from scripting features #
Today, in order for programs to allow their users to do any of the following:
  * Replace a manual input with any automated input
  * Replace any file or device input or output with any other file or device input or output
  * Pass the inputs or outputs through any extra processing
  * Many more potential desires of the users

Developers must manually add interfaces to scripting languages, and specific features that let the user respecify inputs/outputs.
This is very difficult and has to be done repeatedly for every program in development. In practice, this is rarely done, so most programs are unscriptable and cannot be used in unforeseen ways.
With a Unified Interface, programs never specify their inputs and outputs directly, but are always attached to those inputs and outputs by the user. Whether the inputs are attached to an automated generator, an extra processing function or the sound device is completely the user's choice.  This does not require any extra work on the behalf of the developer which merely has to specify the input type and its processing.

Therefore, the user has complete control over the inputs and outputs of the program without the program's developer having to do a thing.

# Examples #

## The "playlist" ##
Today, every media player contains a "playlist" feature, which is basically a list of inputs that should be played one by one through the main media player.
With a Unified Interface, this feature is completely redundant, as the user can already use the generic GUI environment in order to pass multiple inputs through the media player input.

## Media "rippers" ##
Today, many media ripper programs (such as a CD-to-wav, or MP3-to-wav) as well as media capture programs exist. These programs are basically identical copies of the ordinary media players, except instead of writing their output to the sound or video device, they write it to a file.  Some programs use a special "output plugin" in the normal media player instead, but they still have to provide this plugin interface for this to be possible.
In a Unified Interface, the output of every component is already under the complete control of the user, so these programs and plugins are unnecessary, as the user simply connects the media's output to a storage object, instead of the audio device.

# Summary #
LiveProgramming brings a Unified Interface to developers and users. This Unified Interface unburdens programmers from specifying much of the user interface, all the while making a huge increase in power of the users.