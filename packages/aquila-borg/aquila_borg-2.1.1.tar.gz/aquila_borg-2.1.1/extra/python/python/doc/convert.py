#+
#   ARES/HADES/BORG Package -- ./extra/python/python/doc/convert.py
#   Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+

# This tool transforms the doc rst in python/doc to a bunch
# of hpp header file. They are used to generate the adequate docstring
# for each module/class/function bound with pybind11 from C++ to Python
#
# The text must follow the Google convention for docstrings, formatted with
# RestructuredText markers. In addition to those markers this tool recognize
# the following formatting:
#
# A class/module doc is marked with a line starting by "@class"
# A comment line is a line starting with "@@"
# A function/member "F" is documented by writing the line "@funcname:F" followed
# by its documentation
#

import sys
import os

TAG_FUNCNAME = "@funcname:"
TAG_CLASSNAME = "@class:"
TAG_CLASS = "@class"
TAG_COMMENT = "@@"


def convert_doc(target_dir, fname):

    _, fname_base = os.path.split(fname)
    fname_header, ext = os.path.splitext(fname_base)
    base_prefix = prefix = fname_header.replace(".", "_")
    fname_header = os.path.join(target_dir, fname_header + ".hpp")
    funcname = None
    block_started = False
    funcs = {}

    with open(fname, mode="rt") as ff, open(fname_header, mode="wt") as gg:

        def finish_block():
            if block_started:
                gg.write(")str\";\n\n")

        def begin_block(funcname):
            nonlocal block_started
            gg.write(f"static const char * __pydocstring_{funcname} = R\"str(")
            block_started = True

        for l in ff:
            if l.startswith(TAG_COMMENT):
                continue
            if l.startswith(TAG_FUNCNAME):
                finish_block()
                l.strip()
                funcname = l[len(TAG_FUNCNAME):]
                funcname = prefix + "_" + funcname
                if funcname in funcs:
                    print(f"{funcname} is already defined")
                    sys.exit(1)
                begin_block(funcname)
                funcs[funcname] = True
                continue

            # Order matter here
            if l.startswith(TAG_CLASSNAME):
                prefix = base_prefix + "_" + l[len(TAG_CLASSNAME):].strip()
                finish_block()
                begin_block(prefix)
                continue

            if l.startswith(TAG_CLASS):
                prefix = base_prefix
                finish_block()
                begin_block(prefix)
                continue
            if block_started:
                gg.write(l)

        finish_block()


if __name__ == "__main__":
    target_dir = sys.argv[1]
    for a in sys.argv[2:]:
        convert_doc(target_dir, a)

# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2020
