#+
#   ARES/HADES/BORG Package -- ./build_tools/gen_splash.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import sys
import re

prev_line=None
with open(sys.argv[1], mode="r") as f_in, open(sys.argv[2], mode="w") as f_out:
  for line in f_in:
    if prev_line is not None:
      f_out.write('"' + prev_line + '",\n')
    line = re.sub(r'\\', r'\\\\', line)
    line = re.sub(r'"', r'\"', line)
    prev_line = line[:-1]
  f_out.write('"' + prev_line + '"\n')
