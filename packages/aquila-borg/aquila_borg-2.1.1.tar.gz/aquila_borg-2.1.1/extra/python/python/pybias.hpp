/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pybias.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PYTHON_BIAS_HPP
#  define __LIBLSS_PYTHON_BIAS_HPP

#  include <pybind11/pybind11.h>
#  include <pybind11/numpy.h>
#  include <boost/format.hpp>
#  include "libLSS/physics/forward_model.hpp"
#  include "pyfuse.hpp"

namespace LibLSS {
  namespace Python {
    namespace py = pybind11;

    class BaseBiasModel {
    public:
      BaseBiasModel() {}
      virtual void compute(
          BORGForwardModel *m, double nmean, py::array_t<double> bias_params,
          py::array_t<double> density, py::array_t<double> biased_density) = 0;
    };

    template <typename Bias_t, bool protect = false>
    class BiasModel;

    template <typename Bias_t>
    class BiasModel<Bias_t, false> : public BaseBiasModel {
    public:
      std::unique_ptr<Bias_t> bias;

      virtual void compute(
          BORGForwardModel *m, double nmean, py::array_t<double> bias_params,
          py::array_t<double> density, py::array_t<double> biased_density) {
        if (!bias)
          bias = std::make_unique<Bias_t>();

        if (bias_params.ndim() != 1 ||
            bias_params.shape()[0] != Bias_t::numParams)
          throw std::range_error(boost::str(
              boost::format("Bias array has invalid dimensions. Expecting %d") %
              Bias_t::numParams));

        if (density.ndim() != 3 || density.shape(0) != m->lo_mgr->localN0 ||
            density.shape(1) != m->lo_mgr->N1 ||
            density.shape(2) != m->lo_mgr->N2)
          throw std::range_error(boost::str(
              boost::format("Input array has invalid dimensions, expecting "
                            "%dx%dx%d") %
              m->lo_mgr->localN0 % m->lo_mgr->N1 % m->lo_mgr->N2));
        if (biased_density.ndim() != 3 ||
            biased_density.shape(0) != m->lo_mgr->localN0 ||
            biased_density.shape(1) != m->lo_mgr->N1 ||
            biased_density.shape(2) != m->lo_mgr->N2)
          throw std::range_error(boost::str(
              boost::format("Output array has invalid dimensions, expecting "
                            "%dx%dx%d") %
              m->lo_mgr->localN0 % m->lo_mgr->N1 % m->lo_mgr->N2));

        py::gil_scoped_release release;
        PyToFuseArray<double, 1, false> bias_params_a(
            bias_params.unchecked<1>());
        PyToFuseArray<double, 3, false> in(density.unchecked<3>());
        PyToFuseArray<double, 3, true> out(
            biased_density.mutable_unchecked<3>());

        bias->prepare(*m, in, nmean, bias_params_a, true);

        LibLSS::copy_array(out, std::get<0>(bias->compute_density(in)));
        bias->cleanup();
      }
    };

    template <typename Bias_t>
    class BiasModel<Bias_t, true> : public BaseBiasModel {
    public:
      std::unique_ptr<Bias_t> bias;

      virtual void compute(
          BORGForwardModel *m, double nmean, py::array_t<double> bias_params,
          py::array_t<double> density, py::array_t<double> biased_density) {
        if (!bias)
          bias = std::make_unique<Bias_t>();

        if (bias_params.ndim() != 1 ||
            bias_params.shape()[0] != Bias_t::numParams)
          throw std::range_error(boost::str(
              boost::format("Bias array has invalid dimensions. Expecting %d") %
              Bias_t::numParams));

        if (density.ndim() != 3 || density.shape(0) != m->lo_mgr->localN0 ||
            density.shape(1) != m->lo_mgr->N1 ||
            density.shape(2) != m->lo_mgr->N2)
          throw std::range_error(boost::str(
              boost::format("Input array has invalid dimensions, expecting "
                            "%dx%dx%d") %
              m->lo_mgr->localN0 % m->lo_mgr->N1 % m->lo_mgr->N2));
        if (biased_density.ndim() != 3 ||
            biased_density.shape(0) != m->lo_mgr->localN0 ||
            biased_density.shape(1) != m->lo_mgr->N1 ||
            biased_density.shape(2) != m->lo_mgr->N2)
          throw std::range_error(boost::str(
              boost::format("Output array has invalid dimensions, expecting "
                            "%dx%dx%d") %
              m->lo_mgr->localN0 % m->lo_mgr->N1 % m->lo_mgr->N2));

        {
          py::gil_scoped_release release;
          PyToFuseArray<double, 1, false> bias_params_a(
              bias_params.unchecked<1>());
          PyToFuseArray<double, 3, false> in(density.unchecked<3>());
          PyToFuseArray<double, 3, true> out(
              biased_density.mutable_unchecked<3>());
          LibLSS::U_Array<double, 3> tmp_density(m->out_mgr->extents_real_strict());
          fwrap(tmp_density.get_array()[m->out_mgr->strict_range()]) = in;

          bias->prepare(*m, tmp_density.get_array(), nmean, bias_params_a, true);

          LibLSS::copy_array(out, std::get<0>(bias->compute_density(tmp_density.get_array())));
          bias->cleanup();
        }
      }
    };

  } // namespace Python
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
