#FROM quay.io/pypa/manylinux2014_x86_64
FROM quay.io/pypa/manylinux2010_x86_64
ARG CMAKE=3.17.3

RUN yum install -y git && \
   ( \
      git clone git://github.com/ninja-build/ninja.git && \
      cd ninja && \
      /opt/python/cp36-cp36m/bin/python3 ./configure.py --bootstrap && \
      ./ninja && cp ninja /usr/bin \
   ) && rm -fr ninja && yum clean all

RUN \ 
  yum install -y wget openssl-devel &&  \
  wget https://github.com/Kitware/CMake/releases/download/v${CMAKE}/cmake-${CMAKE}.tar.gz && \
  tar zxvf cmake-${CMAKE}.tar.gz  && \
  ( \
     cd cmake-${CMAKE} &&  ./bootstrap && make -j4 && make install \
  ) && rm -fr cmake-${CMAKE}* && \
  yum clean all
