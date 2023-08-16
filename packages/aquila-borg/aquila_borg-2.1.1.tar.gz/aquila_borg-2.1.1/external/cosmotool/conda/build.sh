export CC=$(basename ${CC})
export CXX=$(basename ${CXX})

$PYTHON setup.py install
