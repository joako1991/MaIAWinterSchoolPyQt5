# SpinBox example
This example shows how to use an SpinBox.
A SpinBox is a little widget in which a number can be set. The change of its
value can be done by just typing the number, or using the keyboard arrows,
or the GUi arrows in the box. If we choose the arrows, the increase / decreasing
step of the SpinBox is used (for instance, we can make that each step is
of three units, so if we start from 10, the next value will be 13, then 16, 19, 22, etc).

It is an useful tool when we need to insert values and validate the input. For
example, if only positive values can be set, we can put the spin box minimum
value to 0. This way, even if the user tries to set a negative value, he couldn't.

As any other widget, we have signals that inform us when the user changes its
value, so we can execute instructions each time a new value is inserted.

In this example, we show two SpinBoxes: One for integers (QSpinBox) and one for
decimal numbers (QDoubleWidget). Depending on your requirements, you can use
one of the other one, but the basis is the same for both of them.

# Application screenshot
![app screenshot](/PyQtExamples/SpinBoxExample/images/SpinBoxExample.png)