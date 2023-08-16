#+
#   ARES/HADES/BORG Package -- ./scripts/ini_generator/gen_subcat_conf.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import sys
import os.path
import argparse

pp = argparse.ArgumentParser()
pp.add_argument('--output', type=str, required=True)
pp.add_argument('--configs', type=str, required=True)
pp.add_argument('--header', type=str, required=True)
args = pp.parse_args()
out_ini= args.output
all_config_files=args.configs.split(':')



subcat_id=0

PATTERN="""datafile=%(catalog)s
maskdata=%(mask)s
"""

def apply_cut_magnitude(CAT_config, j):
      CUT_PATTERN="""galaxy_bright_absolute_magnitude_cut=%(absmag_bright)15.15lf
galaxy_faint_absolute_magnitude_cut=%(absmag_faint)15.15lf
"""
      Nsubcat = CAT_config['num_subcat']
      DeltaMag = (CAT_config['absmag_max'] - CAT_config['absmag_min'])
      MagMin = CAT_config['absmag_min']
      absmag_bright = DeltaMag * j / Nsubcat + MagMin
      absmag_faint = DeltaMag * (j+1) / Nsubcat + MagMin
      f.write(CUT_PATTERN % {'absmag_bright':absmag_bright,'absmag_faint':absmag_faint})

def apply_cut_distance(CAT_config, j):
      CUT_PATTERN="""file_dmin=%(dmin)15.15lf
file_dmax=%(dmax)15.15lf
"""
      Nsubcat = CAT_config['num_subcat']
      DeltaMag = (CAT_config['d_max'] - CAT_config['d_min'])
      MagMin = CAT_config['d_min']
      dmin = DeltaMag * j / Nsubcat + MagMin
      dmax = DeltaMag * (j+1) / Nsubcat + MagMin
      f.write(CUT_PATTERN % {'dmin':dmin,'dmax':dmax})

def execfile(filename, globals=None, locals=None):
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(filename, "r") as fh:
        exec(fh.read()+"\n", globals, locals)

with open(out_ini, mode="wt") as f:

  with open(args.header, mode="rt") as fh:
    f.write(fh.read())
    f.write("\n")

  print("All configs = %r" % all_config_files)
  for config_file in all_config_files:
    path_config,_ = os.path.split(config_file)
    def file_subs(s):
      return os.path.join(path_config,s)

    config_locals={}
    config_globals={'FILE':file_subs}

    print("Analyze %s" % config_file)
    execfile(config_file, config_globals, config_locals)

    CAT_config = config_locals['CONFIG']
    del config_locals['CONFIG']
    
    CAT_config['catalog'] = os.path.join(path_config,CAT_config['catalog'])
    if CAT_config['cutter']=='magnitude':
      cut_function = apply_cut_magnitude
    elif CAT_config['cutter']=='distance':
      cut_function = apply_cut_distance
    else:
      print("Unknown cutter '%s'" % CAT_config['cutter'])
      sys.exit(1)

    Nsubcat = CAT_config['num_subcat']
    for j in range(Nsubcat):
      f.write("[catalog_%(subcat_id)d]\n" % {'subcat_id':subcat_id})
      for k,v in config_locals.items():
        if type(v)==str:
          f.write("%s=%s\n" % (k,v))
        elif type(v)==tuple:
          if len(v) > 0:
            f.write((("%s=" + "%r,"*len(v)) % ((k,) + v))[:-1] + "\n")
        else:
          f.write("%s=%r\n" % (k,v))
      cut_function(CAT_config, j)
      f.write(PATTERN % CAT_config)   
      if (j==CAT_config.get('ref_subcat',-1)):
        f.write("refbias=true\n")
      else:
        f.write("refbias=false\n")
      f.write("\n")
      
      subcat_id += 1
      
  f.write("[run]\nNCAT=%d\n\n" % subcat_id)
