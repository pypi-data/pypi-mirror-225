/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pysamplers.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <typeindex>
#include <memory>
#include <boost/format.hpp>

#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "pyfuse.hpp"
#include "pyborg.hpp"
#include "py_mpi.hpp"

#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/samplers/generic/generic_sigma8_second.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/altair/altair_meta_sampler.hpp"

#include "libLSS/samplers/bias_model_params.hpp"
#include "libLSS/samplers/model_params.hpp"

using namespace LibLSS;

namespace py = pybind11;
using namespace py::literals;

PYBIND11_MAKE_OPAQUE(LikelihoodInfo);

class PythonGenericBiasSampler : public MarkovSampler {
protected:
  MPI_Communication *comm;
  std::shared_ptr<AbstractGenericHMCLikelihood> likelihood;

  void initialize(MarkovState &state) override;
  void restore(MarkovState &state) override;

public:
  PythonGenericBiasSampler(
      MPI_Communication *comm_,
      std::shared_ptr<AbstractGenericHMCLikelihood> likelihood_)
      : comm(comm_), likelihood(likelihood_) {}

  void sample(MarkovState &state) override;
};

class PyBaseSampler : public MarkovSampler {
  using MarkovSampler::MarkovSampler;
};

class PyWrapSampler : public PyBaseSampler {
public:
  void initialize(MarkovState &state) override {
    PYBIND11_OVERLOAD_PURE(void, PyBaseSampler, initialize, &state);
  }
  void restore(MarkovState &state) override {
    PYBIND11_OVERLOAD_PURE(void, PyBaseSampler, restore, &state);
  }

public:
  using PyBaseSampler::PyBaseSampler;

  void sample(MarkovState &state) override {
    PYBIND11_OVERLOAD_PURE(void, PyBaseSampler, sample, &state);
  }
};

void PythonGenericBiasSampler::initialize(MarkovState &state) {}
void PythonGenericBiasSampler::restore(MarkovState &state) {}

void PythonGenericBiasSampler::sample(MarkovState &state) {
  using boost::format;
  typedef ArrayType1d::ArrayType BiasParamArray;

  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  long Ncat = state.getScalar<long>("NCAT");
  auto &rgen = state.get<RandomGen>("random_generator")->get();

  for (int c = 0; c < Ncat; c++) {
    double &nmean =
        state.template getScalar<double>(format("galaxy_nmean_%d") % c);
    BiasParamArray &bias_params =
        *state.template get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;

    boost::multi_array<double, 1> current_biases = bias_params;

    if (!likelihood->nmeanIsBias()) {
      nmean = slice_sweep_double(
          comm, rgen,
          [&current_biases, c, this](double x) {
            return likelihood->logLikelihoodBias(c, x, current_biases);
          },
          nmean, 0.1);
    }
    for (int p = 0; p < likelihood->getNumberOfBiasParameters(); p++) {
      bias_params[p] = slice_sweep_double(
          comm, rgen,
          [&current_biases, c, this, nmean, p](double x) {
            current_biases[p] = x;
            return likelihood->logLikelihoodBias(c, nmean, current_biases);
          },
          bias_params[p], 0.1);
    }
  }
}

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.samplers.hpp"

void LibLSS::Python::pySamplers(py::module m) {
  m.doc() = DOC(aquila_borg, samplers);

  py::class_<MarkovSampler, std::shared_ptr<MarkovSampler>>(m, "MarkovSampler")
      .def("sample", &MarkovSampler::sample, py::call_guard<py::gil_scoped_release>());

  py::class_<
      PyBaseSampler, MarkovSampler, PyWrapSampler,
      std::shared_ptr<PyBaseSampler>>(
      m, "PyBaseSampler", DOC(aquila_borg, samplers, PyBaseSampler))
      .def(py::init<>());

  m.def(
      "slice_sampler",
      [](MarkovState *state, py::object callback, double previous_value,
         double step) {
        auto &rgen = state->get<RandomGen>("random_generator")->get();

        return slice_sweep(
            rgen,
            [&callback](double x) { return py::cast<double>(callback(x)); },
            previous_value, step);
      },
      "state"_a, "callback"_a, "previous_value"_a, "step"_a,
      DOC(aquila_borg, samplers, slice_sampler));

  m.def(
      "mpi_slice_sampler",
      [](MarkovState *state, py::object callback, double previous_value,
         double step, py::object mpi) {
        auto &rgen = state->get<RandomGen>("random_generator")->get();
        if (mpi.is_none()) {
          auto comm = MPI_Communication::instance();
          return slice_sweep(
              comm, rgen,
              [&callback](double x) { return py::cast<double>(callback(x)); },
              previous_value, step);
        } else {
          auto comm = Python::makeMPIFromPython(mpi);

          return slice_sweep(
              comm.get(), rgen,
              [&callback](double x) { return py::cast<double>(callback(x)); },
              previous_value, step);
        }
      },
      "state"_a, "callback"_a, "previous_value"_a, "step"_a,
      "mpi"_a = py::none(), DOC(aquila_borg, samplers, slice_sampler));

  py::class_<
      PythonGenericBiasSampler, MarkovSampler,
      std::shared_ptr<PythonGenericBiasSampler>>(
      m, "GenericBiasSampler", DOC(aquila_borg, samplers, GenericBiasSampler))
      .def(
          py::init([](std::shared_ptr<GridDensityLikelihoodBase<3>> model) {
            auto abstract_likelihood =
                std::dynamic_pointer_cast<AbstractGenericHMCLikelihood>(model);
            if (!abstract_likelihood) {
              throw std::invalid_argument(
                  "Likelihood must be of the generic class.");
            }
            return new PythonGenericBiasSampler(
                MPI_Communication::instance(), abstract_likelihood);
          }),
          "model"_a);

  py::class_<
      BiasModelParamsSampler, MarkovSampler,
      std::shared_ptr<BiasModelParamsSampler>>(
      m, "BiasModelParamsSampler",
      DOC(aquila_borg, samplers, BiasModelParamsSampler))
      .def(
          py::init([](std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood,
                      std::shared_ptr<BORGForwardModel> model, int numBias,
                      std::set<int> frozen, std::string const &prefix,
                      py::object limiter, py::object unlimiter) {
            auto sampler = new BiasModelParamsSampler(
                MPI_Communication::instance(), likelihood, model, numBias,
                prefix);
            sampler->freezeSet(frozen);
            sampler->setLimiterHooks(
                [limiter]() {
                  py::gil_scoped_acquire acquire;
                  if (!limiter.is_none())
                    limiter();
                },
                [unlimiter]() {
                  py::gil_scoped_acquire acquire;
                  if (!unlimiter.is_none())
                    unlimiter();
                });
            return sampler;
          }),
          "likelihood"_a, "model"_a, "numBias"_a, "frozen"_a = std::set<int>(),
          "prefix"_a = "", "limiter"_a = py::none(),
          "unlimiter"_a = py::none());

  py::class_<
      HMCDensitySampler, MarkovSampler, std::shared_ptr<HMCDensitySampler>>(
      m, "HMCDensitySampler", DOC(aquila_borg, samplers, HMCDensitySampler))
      .def(
          py::init([](std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood,
                      double k_max, std::string prefix) {
            return new HMCDensitySampler(
                MPI_Communication::instance(), likelihood, k_max, prefix);
          }),
          "likelihood"_a, "k_max"_a = 1000, "prefix"_a = "");

  py::class_<
      GenericSigma8SecondVariantSampler, MarkovSampler,
      std::shared_ptr<GenericSigma8SecondVariantSampler>>(
      m, "Sigma8Sampler", DOC(aquila_borg, samplers, Sigma8Sampler))
      .def(
          py::init([](std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood,
                      std::shared_ptr<LikelihoodInfo> info) {
            return new GenericSigma8SecondVariantSampler(
                MPI_Communication::instance(), likelihood, *info);
          }),
          "likelihood"_a, "likelihood_info"_a);

  py::class_<
      ModelParamsSampler, MarkovSampler, std::shared_ptr<ModelParamsSampler>>(
      m, "ModelParamsSampler", DOC(aquila_borg, samplers, ModelParamsSampler))
      .def(
          py::init([](std::string prefix,
                      std::vector<std::string> const &params,
                      std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood_,
                      std::shared_ptr<BORGForwardModel> model_,
                      ModelDictionnary init) {
            return new ModelParamsSampler(
                MPI_Communication::instance(), prefix, params, likelihood_,
                model_, init);
          }),
          "prefix"_a, "params"_a, "likelihood"_a, "model"_a, "init_values"_a);

  py::class_<
      AltairMetaSampler, MarkovSampler, std::shared_ptr<AltairMetaSampler>>(
      m, "AltairMetaSampler", DOC(aquila_borg, samplers, AltairMetaSampler))
      .def(
          py::init([](std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood,
                      std::shared_ptr<BORGForwardModel> model,
                      CosmologicalParameters bound_min,
                      CosmologicalParameters bound_max, double slice_factor, py::object limiter, py::object unlimiter) {
            auto sampler = new AltairMetaSampler(
                MPI_Communication::instance(), likelihood, model, bound_min,
                bound_max, slice_factor);
            sampler->setLimiter(
                [limiter]() {
                  py::gil_scoped_acquire acquire;
                  if (!limiter.is_none())
                    limiter();
                });
            sampler->setUnlimiter(
                [unlimiter]() {
                  py::gil_scoped_acquire acquire;
                  if (!unlimiter.is_none())
                    unlimiter();
                });
            return sampler;
          }),
          "likelihood"_a, "model"_a, "bound_min"_a, "bound_max"_a, "slice_factor"_a = 0.01, "limiter"_a = py::none(), "unlimiter"_a = py::none());
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
