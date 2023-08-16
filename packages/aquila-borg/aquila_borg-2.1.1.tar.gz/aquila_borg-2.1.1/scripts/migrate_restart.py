#+
#   ARES/HADES/BORG Package -- ./scripts/migrate_restart.py
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
  
def detect_job(path):
  
  obj_list=[]
  group_list=[]
  
  def _handle_item(name, obj):
    if isinstance(obj, h5.Group):
      group_list.append(name)
    if not isinstance(obj, h5.Dataset):
      return

    obj_list.append(name)
      
  with h5.File("%s_0" % path, mode="r") as f:  
    f.visititems(_handle_item)

  return obj_list,group_list

def load_nonarray(path, outpath, objlist, group_list):
  arr = {}
  with h5.File(path, mode="r") as f, h5.File(outpath, mode="w") as of:
    for g in group_list:
      if g[:4] == 'info':
        newname = g[4:]
      elif g[:6] == 'markov':
        newname = g[6:]
      if len(newname)==0:
        continue
      if newname in of:
        continue
      print("Create group %s" % newname)
      of.create_group(newname)
    for oname in objlist:
      print("Loading %s..." % oname)
      if oname[:4] == 'info':
        newname = oname[4:]
      elif oname[:6] == 'markov':
        newname = oname[6:]
      else:
        print("Beuh ! " + oname)
        abort

      if oname == '/info/scalars/BORG_version':
        of[newname] = np.array([f[oname][0]], dtype='S')
      else:
        of[newname] = f[oname][:]
  
def migrate(path, newpath):

  ncpu = detect_ncpus(path)
  elem_list,group_list = detect_job(path)
  
  print("Loading spliced arrays")  
  for n in range(ncpu):
    load_nonarray("%s_%d" % (path,n), "%s_%d" % (newpath,n), elem_list, group_list)
  
  
if __name__=="__main__":
   migrate("./restart.h5", "./new/restart.h5")
