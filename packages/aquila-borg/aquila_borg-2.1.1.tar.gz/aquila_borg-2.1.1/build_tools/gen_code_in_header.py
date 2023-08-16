#+
#   ARES/HADES/BORG Package -- ./build_tools/gen_code_in_header.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import sys
import re

code=""
with open(sys.argv[1], mode="r") as f_in, open(sys.argv[2], mode="w") as f_out:
  for line in f_in:
    line = re.sub(r'\\', r'\\\\', line)
    line = re.sub(r'"', r'\"', line)
    line = line[:-1]
    code += line + "\\n"
  f_out.write('"%s"' % (code,))
