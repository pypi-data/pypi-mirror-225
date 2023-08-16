#!/bin/bash
#+
#   ARES/HADES/BORG Package -- ./build.sh
#   Copyright (C) 2016-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2020 Florent Leclercq <florent.leclercq@polytechnique.org>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+

print_help()
{
  cat <<EOF
This is the build helper. The arguments are the following:

--cmake CMAKE_BINARY    instead of searching for cmake in the path,
  use the indicated binary

--without-openmp        build without openmp support (default with)
--with-mpi              build with MPI support (default without)
--c-compiler COMPILER   specify the C compiler to use (default to cc)
--cxx-compiler COMPILER specify the CXX compiler to use (default to c++)
--julia JULIA_BINARY    specify the full path of julia interpreter
--build-dir DIRECTORY   specify the build directory (default to "build/" )
--debug                 build for full debugging
--no-debug-log          remove all the debug output to increase speed on parallel
                        filesystem.
--perf                  add timing instructions and report in the log files

--extra-flags FLAGS     extra flags to pass to cmake
--download-deps         Predownload dependencies
--use-predownload       Use the predownloaded dependencies. They must be in
                        downloads/
--no-predownload        Do not use predownloaded dependencies in downloads/
--purge                 Force purging the build directory without asking
                        questions.
--native                Try to activate all optimizations supported by the
                        running CPU.
--python[=PATH]         Enable the building of the python extension. If PATH
                        is provided it must point to the executable of your
                        choice for (e.g \`/usr/bin/python3.9\`)
--with-julia            Build with Julia support (default false)
--hades-python          Enable hades-python (implies --python)
--skip-building-tests   Do not build all the tests
--install-system-python Install python package in the python system dir
--install-user-python   Install python package in the user directory [default]

Advanced usage:

--eclipse                Generate for eclipse use
--ninja                  Use ninja builder
--update-tags            Update the TAGS file
--use-system-boost[=PATH] Use the boost install available from the system. This
                          reduces your footprint but also increases the
                          possibilities of miscompilation and symbol errors.
--use-system-fftw[=PATH] Same but for FFTW3. We require the prefix path.
--use-system-gsl         Same but for GSL
--use-system-eigen=PATH  Same but for EIGEN. Here we require the prefix path of
                         the installation.
--use-system-hdf5[=PATH] Same but for HDF5. Require an HDF5 with C++ support.
                         The path indicate the prefix path of the installation of HDF5
                         (e.g. /usr/local or /usr). By default it will use
                         environment variables to guess it (HDF5_ROOT)

After the configuration, you can further tweak the configuration using ccmake
(if available on your system).
EOF
}


add_skip()
{
  if test "x${skip_url}" = x; then
    skip_url=$1
  else
    skip_url="${skip_url}|$1"
  fi
}

[[ x$ZSH_VERSION == x ]] || setopt local_options BASH_REMATCH
C_DEFAULT=$(echo -e "\033[0m")
C_WHITE=$(echo -e "\033[1m")
C_RED=$(echo -e "\033[91;1m")
C_ORANGE=$(echo -e "\033[33m")
C_BG_RED=$(echo -e "\033[41m")
C_BG_WHITE=$(echo -e "\033[107m")
C_BG_GREEN=$(echo -e "\033[42m")

errormsg() {
  # explained in
  # https://stackoverflow.com/questions/44440506/split-string-with-literal-n-in-a-for-loop
  str=$1
  while [[ $str ]]; do            # iterate as long as we have input
    if [[ $str = *'\n'* ]]; then  # if there's a '\n' sequence later...
      first=${str%%'\n'*}         #   put everything before it into 'first'
      rest=${str#*'\n'}           #   and put everything after it in 'rest'
    else                          # if there's no '\n' later...
      first=$str                  #   then put the whole rest of the string in 'first'
      rest=''                     #   and there is no 'rest'
    fi
    echo -e "${C_BG_RED}${first}${C_DEFAULT}"
    str=$rest
  done
}

noticemsg() {
  str=$1
  while [[ $str ]]; do            # iterate as long as we have input
    if [[ $str = *'\n'* ]]; then  # if there's a '\n' sequence later...
      first=${str%%'\n'*}         #   put everything before it into 'first'
      rest=${str#*'\n'}           #   and put everything after it in 'rest'
    else                          # if there's no '\n' later...
      first=$str                  #   then put the whole rest of the string in 'first'
      rest=''                     #   and there is no 'rest'
    fi
    echo -e "${C_WHITE}${C_BG_GREEN}${first}${C_DEFAULT}"
    str=$rest
  done
}

check_command() {
  cmd="$1"
  msg="$2"

  if ! command -v "${cmd}" > /dev/null 2>&1; then
    echo "${cmd} is not available. ${msg}";
    exit 1
  fi
  echo -e "-- ${C_WHITE}${C_BG_GREEN}Found:${C_DEFAULT} ${C_WHITE}${cmd}${C_DEFAULT}"
}

check_existence() {
  if test "$1" = "-q"; then
    quiet=1
    shift
  else
    quiet=0
  fi
  file="$1"
  error_message="$2"
  if ! test -e "${file}"; then
    echo "-- ${C_RED}${C_BG_WHITE}Not found:${C_DEFAULT} ${file}"
    echo "${error_message}"
    exit 1
  fi
  if test $quiet = 0; then
    echo -e "-- ${C_WHITE}${C_BG_GREEN}Found:${C_DEFAULT} ${file}"
  fi
}

echo "Ensure the current directory is ARES"
check_existence -q "src/ares3.cpp" "Please move current working directory to ares3 source directory."
check_existence -q "external/cosmotool/CMakeLists.txt" "Submodules were not cloned. Please run 'git submodule update --init --recursive' (WARNING! You might have to start from afresh.)."

srcdir=$(pwd)
build_dir=${srcdir}/build

build_type=Release
cmake=cmake
cmake_flags=()
c_compiler=$(which cc)
cxx_compiler=$(which c++)
USE_PREDOWNLOAD=1
julia_binary=
do_purge=0
cmake_generator=

while test $# -gt 0; do
  key="$1"
  case $key in
  --cmake)
      cmake="$2"
      shift
      ;;
  --extra-flags)
      cmake_flags+=($2)
      shift
      ;;
  --without-openmp)
      cmake_flags+=(-DENABLE_OPENMP:BOOL=OFF)
      ;;
  --with-mpi)
      cmake_flags+=(-DENABLE_MPI:BOOL=ON)
      ;;
  --c-compiler)
      c_compiler=$(which $2)
      shift
      ;;
  --cxx-compiler)
      cxx_compiler=$(which $2)
      shift
      ;;
  --julia)
      julia_binary="$2"
      shift
      ;;
  --build-dir)
      build_dir="$2"
      shift
      ;;
  --debug)
      build_type="Debug"
      ;;
  --no-debug-log)
      cmake_flags+=(-DDISABLE_DEBUG_OUTPUT:BOOL=ON)
      ;;
  --eclipse)
      cmake_generator=eclipse
      ;;
  --native)
      cmake_flags+=(-DUSE_NATIVE_ARCH:BOOL=ON)
      ;;
  --perf)
      cmake_flags+=(-DCONTEXT_TIMER:BOOL=ON)
      ;;
  --with-julia)
      cmake_flags+=(-DBUILD_JULIA:BOOL=ON)
      ;;
  --install-user-python)
      cmake_flags+=(-DINSTALL_PYTHON_LOCAL=ON)
      ;;
  --install-system-python)
      cmake_flags+=(-DINSTALL_PYTHON_LOCAL=OFF)
      ;;
  --python|--python=*)
      if [[ $1 =~ ^--python=(.+)$ ]]; then
        PYTHON_PATH=${BASH_REMATCH[1]}
        cmake_flags+=(-DPYTHON_EXECUTABLE=${PYTHON_PATH})
      fi
      cmake_flags+=(-DBUILD_PYTHON_EXTENSION:BOOL=ON)
      ;;
  --hades-python)
      cmake_flags+=(-DBUILD_PYTHON_EXTENSION:BOOL=ON -DBUILD_PYTHON_EMBEDDER:BOOL=ON)
      ;;
  --skip-building-tests)
      cmake_flags+=(-DBUILD_TESTING:BOOL=OFF)
      ;;
  --ninja)
      cmake_generator=ninja
      ;;
  --no-predownload)
      USE_PREDOWNLOAD=0
      ;;
  --use-predownload)
      USE_PREDOWNLOAD=1
      ;;
  --download-deps)

      #This step requires wget.
      if ! command -v wget > /dev/null 2>&1; then
        echo "The command wget is required to pre-download the dependencies. Please install it before retrying. Also it must be"
        echo "available from the PATH"
        exit 1
      fi

      lf=$'\n'
      grep -E "SET\\([a-zA-Z0-9_]+_URL" ${srcdir}/external/external_build.cmake |grep -e 'ftp://' | sed -e "s%^.*(\([a-zA-Z0-9_]*\)_URL[ ]*\"\(ftp.*\)\"[ ]*CACHE.*$%\1_URL \\$lf\2%g" > pre_list
      grep -E "SET\\([a-zA-Z0-9_]+_URL" ${srcdir}/external/external_build.cmake | grep -E 'https?://' |sed -e "s%^.*(\([a-zA-Z0-9_]*\)_URL[ ]*\"\(http.*\)\"[ ]*CACHE.*$%\1_URL \\$lf\2%g" >> pre_list

      test -e ${srcdir}/downloads || mkdir ${srcdir}/downloads;
      ( \
       cd ${srcdir}/downloads; \
       rm -f deps.txt; \
       echo $dlist
       while read url_name; do \
         read d; \
         prename=$(echo $url_name | sed -e 's%^\([a-zA-Z0-9]\+\)_URL%\L\1%g') ; \
         d_tmp=$(echo $d | cut -d/ -f2-); \
         if [[ $d_tmp =~ /.*/([^/]*(tar\.|zip)[^/]*).* ]]; then \
           out_d=${BASH_REMATCH[1]}; \
         else \
           echo "Error matching $d"; \
           exit 1; \
         fi; \
         out_d=${prename}_$out_d; \
         echo "Downloading $d for ${url_name} to ${out_d}"; \
         if ! test -e ${out_d}; then
           wget --no-check-certificate --quiet  -O $out_d $d || (echo "${C_RED}Failure to download $d to $out_d${C_DEFAULT}"; exit 1) || exit 1; \
         else
           echo "=> Already downloaded ${out_d}"; \
         fi; \
         echo ${url_name} >> deps.txt; \
         echo ${out_d} >> deps.txt; \
       done \
      ) < pre_list || echo "${C_RED}Error.${C_DEFAULT} "
      rm -f pre_list
      echo "Done. You can now upload the ${srcdir}/downloads/ directory to the remote computer in the source directory and use --use-predownload."
      exit 0
      ;;
  -h|--h|--he|--hel|--help)
      print_help
      exit 1
      ;;
  --use-system-fftw|--use-system-fftw=*)
      if [[ $1 =~ ^--use-system-fftw=(.+)$ ]]; then
        FFTW_PATH=${BASH_REMATCH[1]}
      else
        if [[ $FFTW_INC =~ ^(.+)/include$ ]]; then
          FFTW_PATH=${BASH_REMATCH[1]}
        fi
      fi
      cmake_flags+=(-DINTERNAL_FFTW:BOOL=OFF)
      if [ "x$FFTW_PATH" != x ]; then
        CMAKE_PREFIX_PATH="${FFTW_PATH};${CMAKE_PREFIX_PATH}"
      fi
      add_skip FFTW_URL
      ;;
  --use-system-hdf5|--use-system-hdf5=*)
      if [[ $1 =~ ^--use-system-hdf5=(.+)$ ]]; then
        HDF5_ROOT=${BASH_REMATCH[1]}
        cmake_flags+=(-DINTERNAL_HDF5:BOOL=OFF "-DHDF5_ROOT=${HDF5_ROOT}")
      else
        cmake_flags+=(-DINTERNAL_HDF5:BOOL=OFF)
      fi
      add_skip HDF5_URL
      ;;
  --use-system-boost|--use-system-boost=*)
      cmake_flags+=(-DINTERNAL_BOOST:BOOL=OFF)
      if [[ $1 =~ ^--use-system-boost=(.+)$ ]]; then
        boost_root=${BASH_REMATCH[1]}
        cmake_flags+=("-DBOOST_ROOT=${boost_root}")
      fi
      add_skip BOOST_URL
      ;;
  --use-system-eigen|--use-system-eigen=*)
      cmake_flags+=(-DINTERNAL_EIGEN:BOOL=OFF)
      if [[ $1 =~ ^--use-system-eigen=(.+)$ ]]; then
        EIGEN_PATH=${BASH_REMATCH[1]}
        cmake_flags+=(-DEIGEN_PATH:PATH=${EIGEN_PATH})
      fi
      add_skip EIGEN_URL
      ;;
  --use-system-gsl)
      cmake_flags+=(-DINTERNAL_GSL:BOOL=OFF)
      if ! command -v gsl-config > /dev/null 2>&1; then
        errormsg "Missing 'gsl-config' in the execution path.\n I cannot detect location of GSL"
        exit 1
      fi
      CMAKE_PREFIX_PATH="$(gsl-config --prefix);${CMAKE_PREFIX_PATH}"
      add_skip GSL_URL
      ;;
  --purge)
      do_purge=1
      ;;
  --update-tags)
      echo "Updating tags file."
      rm -f ctags
      for module in . extra/hades extra/borg extra/virbius extra/hmclet extra/dm_sheet; do
          if test -e ${module}; then
	      (cd ${module}; git ls-files '*.[ch]pp' | awk "{ print \"${module}/\" \$0;}") | xargs ctags -a 
	  fi
      done 

      echo "Done. Exiting."
      exit 0
      ;;
  *)
      echo "Unknown option. Abort."
      print_help
      exit 1
      ;;
  esac
  shift
done


if test ${USE_PREDOWNLOAD} = 1; then
  if ! test -d "${srcdir}/downloads"; then
    echo "--- ${C_RED}No deps predownloaded. Stop${C_DEFAULT} ---"
    exit 1
  fi
  cmd=$( (
    flags=()
    while read url_name; do
      if [[ "${url_name}" =~ ^(${skip_url})$ ]]; then
        read path;
        continue
      fi
      read path;
      path="${srcdir}/downloads/${path}";
      flags+=("-D${url_name}:URL=file://${path}");
    done;
    echo "cmake_flags+=(${flags[@]})"
  ) < ${srcdir}/downloads/deps.txt )
  eval ${cmd}
else
  echo "--- ${C_ORANGE}WARNING: Not using predownloaded deps.${C_DEFAULT} --- "
fi
export CMAKE_PREFIX_PATH
#CMAKE_PREFIX_PATH=$(printf %q "${CMAKE_PREFIX_PATH}")

cmake_flags+=(-DARES_PREFIX_PATH=${CMAKE_PREFIX_PATH} -DCMAKE_BUILD_TYPE=${build_type} -DCMAKE_C_COMPILER=${c_compiler} -DCMAKE_CXX_COMPILER=${cxx_compiler})
if test x"${julia_binary}" != x""; then
  cmake_flags+=(-DJULIA_EXECUTABLE=${julia_binary})
fi

if test x$cmake_generator = "xninja"; then
  cmake_flags+=("-GNinja")
elif test x$cmake_generator = "xeclipse"; then
  cmake_flags+=("-GEclipse CDT4 - Unix Makefiles")
fi

echo "Summary of CMAKE_FLAGS:"
for f in "${cmake_flags[@]}"; do
  printf "   %s\n" "$f"
done

if test -e ${build_dir}; then
  if test x${do_purge} == x1; then
    rm -f -r ${build_dir}
  else
    while true; do
      echo -n "${build_dir} already exists. Remove ? [y/n] "
      read RESULT
      if test "x${RESULT}" = "xn"; then
        echo "Abort"
        exit 1
      fi
      if test "x${RESULT}" = "xy"; then
        echo "Removing"
        rm -f -r ${build_dir}
        break
      fi
    done
 fi
fi

check_command "${cmake}" "Please install CMake or provide --cmake to build.sh"
#check_command autoconf "Autoconf is missing. Please install it."
#check_command automake "Automake is missing. Please install it."
check_command patch "Patch is missing. Please install it."
check_command pkg-config "Pkgconfig is missing. Please install it."


if ! mkdir -p ${build_dir}; then
  echo -e "${C_WHITE}--------------------------${C_DEFAULT}"
  echo -e "${C_BG_RED}Cannot create build directory.${C_DEFAULT}"
  echo -e "${C_WHITE}--------------------------${C_DEFAULT}"
  echo
  exit 1
fi

if ! ( \
  cd ${build_dir} && \
  ${cmake} "${cmake_flags[@]}" ${srcdir}; \
  exit $? \
); then
  echo -e "${C_WHITE}-------------------------------------------------${C_DEFAULT}"
  echo -e "${C_BG_RED}An error occured in CMake.${C_DEFAULT}"
  echo -e "${C_BG_RED}Please collect the messages above in your report.${C_DEFAULT}"
  echo -e "${C_WHITE}-------------------------------------------------${C_DEFAULT}"
  echo
  exit 1
fi

cat <<EOF
------------------------------------------------------------------

${C_BG_GREEN}Configuration done.${C_DEFAULT}
Move to ${build_dir} and type 'make' now.
Please check the configuration of your MPI C compiler. You may need
to set an environment variable to use the proper compiler.

Some example (for SH/BASH shells):
- OpenMPI:
    OMPI_CC=${c_compiler}
    OMPI_CXX=${cxx_compiler}
    export OMPI_CC OMPI_CXX

------------------------------------------------------------------

EOF
# ARES TAG: authors_num = 2
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2016-2018
# ARES TAG: name(1) = Florent Leclercq
# ARES TAG: email(1) = florent.leclercq@polytechnique.org
# ARES TAG: year(1) = 2020
