@class
This is the Console class. It allows doing pretty printing of the message from
the borg system. It dispatches the message to the appropriate log files and the
adequate level asked by the user. The Console object cannot be constructed from 
Python. To get a Console object use `aquila_borg.console`.


@@ -------------------------------------------------
@funcname:outputToFile

Args:
    filename (str): the filename to output the full log to

@@ -------------------------------------------------
@funcname:print_std
Prints a message to the console

Args:
    message (str): the message to be printed at the Standard level

