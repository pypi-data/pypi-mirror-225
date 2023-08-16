@funcname:__init__
Create a new BoxModel object.

The constructors builds a cube by default.
However later modifications of the field L and N can give more generally
sized box.

Arguments:
  L (float): Physical size of the box
  N (int): Grid size of the box

@funcname:xmin
3-tuple with corner at (0,0,0) of the box in each direction

@funcname:volume
The total volume of the box

@funcname:Ntot
The total number of mesh elements

@funcname:copy
Make a new independent copy of the present box

@funcname:L
3-tuple of the side-length of the box

@funcname:N
3-tuple of the grid size of the box
