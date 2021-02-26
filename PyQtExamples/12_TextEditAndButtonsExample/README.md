# Text edit with push buttons example
The Text edit object from Qt allows to create text in several lines. It allows
also to change text parameters, like type of letter, size, and alignment, between
others. Then, entered text, can be retrieved, and for instance, be stored in
a text file.

The line edit allows to enter text also, but in only one line, which makes
it unconmformtable if we want to add long texts at once.

So we make a combination of both of them, in order to create a longer text by pieces.
The line edit serves to insert phrase by phrase, and we store them in a text edit
box. This application is similar to a chat application, in which we have a line
to insert our text, and a bigger box to show the history of the exchanged texts.

In this example show how to change the font family, the font **size**, and to enable
the *Italic* mode

We also include two buttons, one to insert each phrase, and one to erase all the
previously inserted texts.

# Application screenshot
![app screenshot](/PyQtExamples/12_TextEditAndButtonsExample/images/TextEditWithButtonsExample.png)