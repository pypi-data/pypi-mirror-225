#+
#   ARES/HADES/BORG Package -- ./scripts/ares_tools/visu/vtktools.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import numpy as np
from vtk.util.numpy_support import get_vtk_array_type, create_vtk_array, get_numpy_array_type

def numpy_scalar_to_vtk(np_array):
    """This function converts a numpy scalar array to a VTK array.
    
    Args:
      np_array (np.array): A numpy array
      
    Returns:
      vtk.vtkArray: An array of the closest possible type of numpy array. The array is deep
                    copied to avoid SEGV.
    
    """
    atype = get_vtk_array_type(np_array.dtype)    
    array = create_vtk_array(atype)
    array.SetNumberOfComponents(1)
    ntype = get_numpy_array_type(atype)
    adata = np.ravel(np_array).astype(ntype)
    array.SetVoidArray(adata, len(adata), 1)
    
    copy = array.NewInstance()
    copy.DeepCopy(array)
    return copy

def numpy_vector_to_vtk(np_array):
    """This function converts a numpy scalar array to a VTK array.
    
    Args:
      np_array (np.array): A numpy array
      
    Returns:
      vtk.vtkArray: An array of the closest possible type of numpy array. The array is deep
                    copied to avoid SEGV.
    
    """
    if np_array.shape[3] != 3:
      raise ValueError()
      
    atype = get_vtk_array_type(np_array.dtype)    
    array = create_vtk_array(atype)
    array.SetNumberOfComponents(3)
    ntype = get_numpy_array_type(atype)
    adata = np.ravel(np_array).astype(ntype)
    array.SetVoidArray(adata, len(adata), 1)
    
    copy = array.NewInstance()
    copy.DeepCopy(array)
    return copy


def smooth_array(a, L=[1.0,1.0,1.0], R=0.1):
    a_hat = np.fft.rfftn(a)
    ik = [np.fft.fftfreq(iN, d=iL/iN)*2*np.pi for iN,iL in zip(a.shape,L)]
    k2 = ik[0][:,None,None]**2 + ik[1][None,:,None]**2 + ik[2][None,None,:a.shape[2]/2+1]**2
    
    a_hat *= np.exp(-0.5*k2*R**2)
    return np.fft.irfftn(a_hat)

def displacement_array(a, L=[1.0,1.0,1.0], R=0.1):
    a_hat = np.fft.rfftn(a)
    ik = [np.fft.fftfreq(iN, d=iL/iN)*2*np.pi for iN,iL in zip(a.shape,L)]
    k2 = ik[0][:,None,None]**2 + ik[1][None,:,None]**2 + ik[2][None,None,:a.shape[2]/2+1]**2
    
    b = np.empty(a.shape + (3,), dtype=np.float32)
    
    b_hat = -a_hat * 1j*ik[0][:,None,None]/k2
    b_hat[0,0,0]=0
    b[...,0] = np.fft.irfftn(b_hat)

    b_hat = -a_hat * 1j*ik[1][None,:,None]/k2
    b_hat[0,0,0]=0
    b[...,1] = np.fft.irfftn(b_hat)

    b_hat = -a_hat * 1j*ik[2][None,None,:a.shape[2]/2+1]/k2
    b_hat[0,0,0]=0
    b[...,2] = np.fft.irfftn(b_hat)
    
    return b


def setupImageData3D(img_data, np_array, dims=[1.0,1.0,1.0], name="numpy array"):
    """This function setups a 3D image data object.
    
    """
    shape = np_array.shape
    
    dx = (d0/(N0-1) for d0,N0 in zip(dims,shape))
    img_data.SetOrigin(*(-d0/2 for d0 in dims)) # default values
    img_data.SetSpacing(*dx)
    img_data.SetDimensions(*shape) # number of points in each direction
    
    array = numpy_scalar_to_vtk(np_array)
    
    img_data.GetPointData().AddArray(array)
    array.SetName(name)
    
    return array
    

