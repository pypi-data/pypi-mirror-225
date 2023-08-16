#!/bin/bash
set -e -x

# Install a system package required by our library
#yum install -y atlas-devel
yum install -y  zlib-devel

ln -fs /usr/local/bin/cmake /usr/bin/cmake


ALL_PYTHON="cp36-cp36m" # cp37-cp37m cp38-cp38" 

# Compile wheels
for pkg in $ALL_PYTHON; do
    PYBIN=/opt/python/${pkg}/bin
#    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel -vvv /io/ -w wheelhouse/
done

rm -f wheelhouse/numpy*

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

# Install packages and test
for pkg in $ALL_PYTHON; do
    PYBIN=/opt/python/${pkg}/bin
    "${PYBIN}/pip" install pyborg --no-index -f /io/wheelhouse
done
