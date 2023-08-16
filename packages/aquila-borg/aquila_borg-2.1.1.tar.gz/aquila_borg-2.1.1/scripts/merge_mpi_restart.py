#+
#   ARES/HADES/BORG Package -- ./scripts/merge_mpi_restart.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import os
import h5py as h5
import errno
from ares_tools import rebuild_spliced_h5

def detect_ncpus(path):
  ncpu = 0
  try:
    while True:
      with open("%s_%d" % (path,ncpu), mode= "rb") as f:
        ncpu += 1
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise e
      
  return ncpu
  
def detect_job_to_merge(path):
  
  array_list=[]
  other_list=[]
  group_list=[]
  
  def _handle_item(name, obj):
    if isinstance(obj, h5.Group):
      group_list.append(name)
    if not isinstance(obj, h5.Dataset):
      return

    if len(obj.shape) >= 3:
      array_list.append(name)
    else:
      other_list.append(name)
      
  with h5.File("%s_0" % path, mode="r") as f:  
    f.visititems(_handle_item)

  return array_list,other_list,group_list

def load_nonarray(path, objlist):
  arr = {}
  with h5.File("%s_0" % path, mode="r") as f:  
    for oname in objlist:
      print("Loading %s..." % oname)
      if oname == '/scalars/BORG_version':
        arr[oname] = np.array([f[oname][0]], dtype='S')
      else:
        arr[oname] = f[oname][:]
      
  return arr
  
def load_merged(path):

  ncpu = detect_ncpus(path)
  array_list,nonarray_list,group_list = detect_job_to_merge(path)
  
  array_elts = ['.'.join(e.split('/')) for e in array_list]

  print("Loading spliced arrays")  
  arr = load_nonarray(path, nonarray_list)
  arr2 = rebuild_spliced_h5(path, array_elts, ncpu, verbose=True)
  for k in arr2.keys():
    arr['/'.join(k.split('.'))] = arr2[k]
  
  return arr,group_list
  
  
def save_merged(outpath, omap):
  omap,group_list = omap
  with h5.File(outpath, mode="w") as f:
    for g in group_list:
      if not g in f:
        f.create_group(g)

    for o in omap.keys():
      print("Saving object '%s'" % o)
      f.create_dataset(o, data=omap[o])
      
      


if __name__=="__main__":
  merged_obj = load_merged("./restart.h5")
  
  save_merged("./merged_restart.h5", merged_obj)
