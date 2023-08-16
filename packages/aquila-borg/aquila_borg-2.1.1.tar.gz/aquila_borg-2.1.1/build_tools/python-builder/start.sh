#!/bin/bash

d=$(pwd)
if test x"$(basename $d)" = xbuilder; then
  d=${d}/../
fi
if ! [ -e ${d}/setup.py ] ; then
  echo "Unknown directory. Please move to the root of cosmotool source tree."
  exit 1
fi

#podman run -ti  --rm -e PLAT=manylinux2014_x86_64 -v ${d}:/io:Z pip-builder /io/builder/build-wheels.sh
podman run -ti  --rm -e PLAT=manylinux2010_x86_64 -v ${d}:/io:Z pip-builder /io/builder/build-wheels.sh
