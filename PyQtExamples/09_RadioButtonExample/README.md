# Radio button example
This example contains 3 buttons grouped in a QGroupBox object.
A Radio button is a circular object that can be activated or deactivated, with
the user clicks. The objective of grouping them is that only one of them
can be activated at the time. For example, if the first radio button is activated,
and we click the 3rd button, the first one will be deactivated automatically.

The Grouping step can be avoided, depending on the requirements of the program.
More complex implementations will create several radio buttons, and only
one callback (all the radio buttons call the same callback). Then, inside
this function, we detect which radio button has been activated, and we act
accordingly.

On each toggle (from on to off, or from off to on), the corresponding callback
is called.

# Application screenshot
![app screenshot](/PyQtExamples/RadioButtonExample/images/RadioButtonExample.png)