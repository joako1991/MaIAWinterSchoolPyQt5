# Open file example
This example shows how to open a file or a directory. When we say open, we mean that
the user can select a given directory, or file, and then we can retrieve
in code the path of the selection element. This way, we do not need to
hardcode paths of files in the code, and we can change the files we
open in a flexible way.

We use the object QFileDialog in order to explore the disk, and find our file
using the Graphical User Interface.

This example shows how we get paths of directories, or path for files.
We might use directories only, and not an specific file, when we want to process
several images at the same time, that are all located in the same folder. So,
the only information we need is the folder name, and then we search on it all the
image files.
When we want to open only one file, we use the open file part only.

# Application screenshot
![app screenshot](/PyQtExamples/08_OpenFilesExample/images/MainWIndow.png)
![app screenshot](/PyQtExamples/08_OpenFilesExample/images/DirectorySearch.png)
![app screenshot](/PyQtExamples/08_OpenFilesExample/images/FileSearch.png)