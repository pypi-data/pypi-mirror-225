/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/testFramework.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TESTS_TESTFRAMEWORK_HPP
#define __LIBLSS_TESTS_TESTFRAMEWORK_HPP

#include <H5Cpp.h>
#include <boost/format.hpp>
#include <CosmoTool/hdf5_array.hpp>

namespace LibLSS_tests {
  extern std::string reference_path;

  namespace {
    namespace prefix {
      namespace details {
        std::string prefix_type(float a) { return "f"; }
        std::string prefix_type(double a) { return "f"; }
        std::string prefix_type(int a) { return "i"; }
        std::string prefix_type(std::complex<float> a) { return "c"; }
        std::string prefix_type(std::complex<double> a) { return "c"; }
      } // namespace details

      template <typename T>
      std::string get() {
        return details::prefix_type(T());
      }
    } // namespace prefix
  }   // namespace

  template <typename T>
  void loadReferenceInput(size_t N, boost::multi_array_ref<T, 3> &data) {
    H5::H5File f(reference_path, H5F_ACC_RDONLY);

    CosmoTool::hdf5_read_array(
        f, boost::str(boost::format("%s_size_%d") % prefix::get<T>() % N), data,
        false, true);
  }
} // namespace LibLSS_tests

#endif
