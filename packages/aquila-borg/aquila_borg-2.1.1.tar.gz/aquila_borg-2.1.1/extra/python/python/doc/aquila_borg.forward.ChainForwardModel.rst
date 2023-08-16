@class
This is a forward model to chain several others. It is based on
:class:`aquila_borg.forward.BORGForwardModel`

The chain is mandatorily linear. In principle several chains could be combined
together with another auxiliary forward model.

@@ ------------------------------------------------------
@funcname:__init__
Construct a new chain forward model, starting with the input box model
corresponding to the first argument

@@ ------------------------------------------------------
@funcname:addModel
Add a new model to the chain

Args:
    forward (aquila_borg.forward.BORGForwardModel): a model to add