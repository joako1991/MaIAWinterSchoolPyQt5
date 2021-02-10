# Tabs and buttons example
This example creates two tabs.
A tab is a page-like object, that allows to show a series of widgets
at the time, and hide the other ones. This allows grouping widgets by task, for
instance. If we are doing image processing, we can split in tabs to change the
color space, to do histogram related tasks, particle analysis, morphological
operators.

The way to create a tab is to previously create a single widget with all the
elements we want to include on it. All this elements will be organized in a
layout, and then we create a temporal QWidget to whom we will set the previously
created layout. This last widget is the one that we send to the addTab function.

Each tab is identified by an index (0,1,2,3,4,...) in the order in which
we added them, or we can insert them into an specific position directly
using the insertTab function. This index is useful to change from one tab
to another by code, and don't wait for the user to change from the desired tab.

If we have global layout, and we add the tab layout, and then we add  other
widgets that are not in the layout, those widgets will stay in their position,
regardless the tab we choose. For instance, we might want to have the exit
button all the time, regardless in which tab we are in.

# Application screenshot
![app screenshot](/PyQtExamples/TabsAndPushButton/images/TabsExample.png)