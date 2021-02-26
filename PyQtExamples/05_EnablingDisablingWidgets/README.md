# Enabling / Disabling widgets example
Sometimes, we want to forbids the user to push a button, or use certain widget.
In order to do so, we have to DISABLE the given widget. Then, depending the
conditions of the program, we can allow him again to use that widget. So, we
need to ENABLE the widget. This example exemplifies how to do so.

We have a push button that each time we press it, it can enable or disable a
given widget. In this case, we used a QRadioButton as example widget, but
ANY OBJECT of qt can be enabled or disabled, using the same function. Even
the ones we create. If they inherit from a any Qt object, we can access to the
enabling / disabling function, which has always the same name: setEnabled.


# Application screenshot
![app screenshot](/PyQtExamples/05_EnablingDisablingWidgets/images/EnablingDisabling.png)