#!/bin/bash
set -e -x

CC=cc
CXX=c++

export CC CXX

# Install a system package required by our library
#yum install -y atlas-devel
yum install -y cmake3 gsl-devel zlib-devel fftw3-devel libffi-devel hdf5 hdf5-devel

ln -fs /usr/bin/cmake3 /usr/bin/cmake


test -d /io/wheelhouse || mkdir /io/wheelhouse
test -d /io/wheelhouse/fix || mkdir /io/wheelhouse/fix

ALL_PYTHON="cp37-cp37m cp38-cp38 cp39-cp39 cp310-cp310"

# Compile wheels
for pkg in $ALL_PYTHON; do
    PYBIN=/opt/python/${pkg}/bin
#    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" install setuptools wheel Cython 
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel -vvv /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse/cosmotool*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/fix
done

# Install packages and test
#for pkg in $ALL_PYTHON; do
#    PYBIN=/opt/python/${pkg}/bin
#    "${PYBIN}/pip" install cosmotool --no-index -f /io/wheelhouse
#done
