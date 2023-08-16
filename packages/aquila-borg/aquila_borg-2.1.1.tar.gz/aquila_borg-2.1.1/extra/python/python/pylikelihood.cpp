/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pylikelihood.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <memory>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <CosmoTool/cosmopower.hpp>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/console.hpp"

#include "pyborg.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "pyfuse.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include <typeindex>
#include "libLSS/mcmc/state_element.hpp"

#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"

#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/bias/noop.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/passthrough.hpp"
#include "libLSS/physics/likelihoods/gaussian.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"

#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

#include "py_mpi.hpp"

using namespace LibLSS;
namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MAKE_OPAQUE(LikelihoodInfo);

template <typename Bias, typename Likelihood>
static void create_generic_bind(
    py::module m, std::string const &name, std::string const &doc) {
  py::class_<
      GenericHMCLikelihood<Bias, Likelihood>, ForwardModelBasedLikelihood,
      std::shared_ptr<GenericHMCLikelihood<Bias, Likelihood>>>(
      m, name.c_str(), doc.c_str())
      .def(py::init([](LikelihoodInfo *info) {
        return new GenericHMCLikelihood<Bias, Likelihood>(*info);
      }))
      .def("numBiasParams", [](py::object o) { return Bias::numParams; });
}

struct basic_scalar_converter {
  virtual py::object
  load(StateElement *, py::handle _ = py::handle()) const = 0;
  virtual void store(StateElement *, py::object) const = 0;
};

template <typename T>
struct scalar_converter : basic_scalar_converter {
  static basic_scalar_converter *instance() {
    static scalar_converter<T> obj;
    return &obj;
  }
  py::object
  load(StateElement *e, py::handle hold = py::handle()) const override {
    return py::cast(dynamic_cast<ScalarStateElement<T> *>(e)->value);
  }
  void store(StateElement *e, py::object obj) const override {
    dynamic_cast<ScalarStateElement<T> *>(e)->value = py::cast<T>(obj);
  }
};

template <typename T>
struct array_converter : basic_scalar_converter {
  static basic_scalar_converter *instance() {
    static array_converter<T> obj;
    return &obj;
  }
  py::object
  load(StateElement *e, py::handle hold = py::handle()) const override {
    T *array = dynamic_cast<T *>(e);
    typedef typename T::ArrayType::element element;

    auto ref_array = array->array; // this is a shared_ptr with refcount
    std::array<ssize_t, T::ArrayType::dimensionality> shapes, strides;
    std::copy(
        ref_array->shape(), ref_array->shape() + shapes.size(), shapes.begin());
    for (int i = 0; i < strides.size(); i++)
      strides[i] = ref_array->strides()[i] * sizeof(element);
    return py::array_t<element>(shapes, strides, ref_array->data(), hold);
  }
  void store(StateElement *e, py::object obj) const override {
    throw std::runtime_error("Cannot store yet");
  }
};

#include "pylikelihood_wrap.hpp"

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.likelihood.hpp"

void LibLSS::Python::pyLikelihood(py::module m) {

  std::map<std::type_index, basic_scalar_converter *> converter;

  m.doc() = DOC(aquila_borg, likelihood);

  converter[typeid(ScalarStateElement<float>)] =
      scalar_converter<float>::instance();
  converter[typeid(ScalarStateElement<double>)] =
      scalar_converter<double>::instance();
  converter[typeid(ScalarStateElement<int>)] =
      scalar_converter<int>::instance();
  converter[typeid(ScalarStateElement<long>)] =
      scalar_converter<long>::instance();
  converter[typeid(ScalarStateElement<bool>)] =
      scalar_converter<bool>::instance();
  converter[typeid(ScalarStateElement<CosmologicalParameters>)] =
      scalar_converter<CosmologicalParameters>::instance();
  converter[typeid(ArrayType1d)] = array_converter<ArrayType1d>::instance();
  converter[typeid(ArrayType)] = array_converter<ArrayType>::instance();
  converter[typeid(CArrayType)] = array_converter<CArrayType>::instance();

  auto ares_to_python =
      [converter](std::type_index ti, StateElement *elt, py::handle h) {
        auto iter = converter.find(ti);
        if (iter == converter.end())
          throw std::runtime_error("Unknown stored type in global state.");
        return iter->second->load(elt, h);
      };

  auto python_to_ares =
      [converter](std::type_index ti, StateElement *elt, py::object obj) {
        auto iter = converter.find(ti);
        if (iter == converter.end())
          throw std::runtime_error("Unknown stored type in global state.");
        return iter->second->store(elt, obj);
      };

  py::class_<MarkovState>(
      m, "MarkovState", DOC(aquila_borg, likelihood, MarkovState))
      .def(
          py::init<>([](int seed) {
            MarkovState *s = new MarkovState();
            MPI_Communication *comm = MPI_Communication::instance();
            if (seed == 0)
              seed = 24032015;

            typedef RandomNumberMPI<GSL_RandomNumber> RGenType;
            auto randgen = std::make_shared<RGenType>(comm, -1);

            randgen->seed(seed);

            s->newElement(
                "random_generator",
                new RandomStateElement<RandomNumber>(randgen));
            return s;
          }),
          "seed"_a = 0)
      .def(
          "__getitem__",
          [ares_to_python](py::object o, std::string const &name) {
            MarkovState *state = py::cast<MarkovState *>(o);
            if (!state->exists(name))
              throw py::key_error(name);
            return ares_to_python(
                state->getStoredType(name), state->get<StateElement>(name), o);
          })
      .def(
          "__setitem__",
          [python_to_ares](
              MarkovState *state, std::string const &name, py::object obj) {
            if (!state->exists(name))
              throw py::key_error();
            return python_to_ares(
                state->getStoredType(name), state->get<StateElement>(name),
                obj);
          })
      .def(
          "newScalar",
          [](MarkovState *state, std::string const &name, py::object o,
             bool in_mcmc, char type_code) {
            if (py::isinstance<py::bool_>(o)) {
              state->newScalar<bool>(name, py::cast<bool>(o), in_mcmc);
            } else if (py::isinstance<py::float_>(o)) {
              state->newScalar<double>(name, py::cast<double>(o), in_mcmc);
            } else if (py::isinstance<py::int_>(o)) {
              if (type_code == 'L')
                state->newScalar<long>(name, py::cast<long>(o), in_mcmc);
              else if (type_code == ' ')
                state->newScalar<int>(name, py::cast<int>(o), in_mcmc);
              else
                error_helper<ErrorParams>("Unsupported type code for int");
            } else if (py::isinstance<CosmologicalParameters>(o)) {
              state->newScalar<CosmologicalParameters>(
                  name, py::cast<CosmologicalParameters>(o), in_mcmc);
            } else {
              error_helper<ErrorParams>("Unsupported scalar type");
            }
          },
          "name"_a, "object"_a, "in_mcmc"_a = false, "type_code"_a = ' ')
      .def(
          "newArray1d",
          [](MarkovState *state, std::string const &name, size_t N,
             bool in_mcmc) {
            if (state->exists(name))
              throw py::key_error();
            state->newElement(
                name, new ArrayType1d(boost::extents[N]), in_mcmc);
          },
          "name"_a, "N"_a, "in_mcmc"_a = false,
          DOC(aquila_borg, likelihood, MarkovState, newArray1d))
      .def(
          "newForwardModel",
          [](MarkovState *state, std::string const &name,
             std::shared_ptr<BORGForwardModel> model) {
            if (state->exists(name))
              throw py::key_error();
            state->newElement(
                name, new SharedObjectStateElement<BORGForwardModel>(model),
                false);
          },
          DOC(aquila_borg, likelihood, MarkovState, newForwardModel))
      .def(
          "newArray3d",
          [](MarkovState *state, std::string const &name, size_t N0, size_t N1,
             size_t N2, bool in_mcmc) {
            if (state->exists(name))
              throw py::key_error();
            state
                ->newElement(
                    name, new ArrayType(boost::extents[N0][N1][N2]), in_mcmc)
                ->setRealDims(ArrayDimension(N0, N1, N2));
          },
          "name"_a, "N0"_a, "N1"_a, "N2"_a, "in_mcmc"_a = false,
          DOC(aquila_borg, likelihood, MarkovState, newArray3d))
      .def(
          "newArray3d_slab",
          [](MarkovState *state, std::string const &name,
             std::array<size_t, 6> slab, std::array<size_t, 3> real_size,
             bool in_mcmc) {
            typedef boost::multi_array_types::extent_range e_range;

            if (state->exists(name))
              throw py::key_error();

            size_t startN0, localN0, startN1, localN1, startN2, localN2, N0, N1,
                N2;

            startN0 = slab[0];
            localN0 = slab[1];
            startN1 = slab[2];
            localN1 = slab[3];
            startN2 = slab[4];
            localN2 = slab[5];
            N0 = real_size[0];
            N1 = real_size[1];
            N2 = real_size[2];
            state
                ->newElement(
                    name,
                    new ArrayType(
                        boost::extents[e_range(startN0, startN0 + localN0)]
                                      [e_range(startN1, startN1 + localN1)]
                                      [e_range(startN2, startN2 + localN2)]),
                    in_mcmc)
                ->setRealDims(ArrayDimension(N0, N1, N2));
          },
          "name"_a, "slab"_a, "real_size"_a, "in_mcmc"_a = false,
          DOC(aquila_borg, likelihood, MarkovState, newArray3d_slab));

  py::class_<
      GridDensityLikelihoodBase<3>,
      std::shared_ptr<GridDensityLikelihoodBase<3>>>(
      m, "Likelihood3d", DOC(aquila_borg, likelihood, Likelihood3d))
      .def(
          "gradientLikelihood",
          [](GridDensityLikelihoodBase<3> *likelihood,
             py::array_t<
                 std::complex<double>,
                 py::array::c_style | py::array::forcecast>
                 s_hat) {
            auto impl_s_hat = s_hat.unchecked<3>();

            py::gil_scoped_release release;

            // Due to an incorrect API in likelihood we have to const away
            // the pointer, though we only require a const access.
            boost::multi_array_ref<std::complex<double>, 3> cpp_s_hat(
                const_cast<std::complex<double> *>(impl_s_hat.data(0, 0, 0)),
                boost::extents[impl_s_hat.shape(0)][impl_s_hat.shape(1)]
                              [impl_s_hat.shape(2)]);

            auto u_gradient =
                std::make_shared<LibLSS::U_Array<std::complex<double>, 3>>(
                    boost::extents[impl_s_hat.shape(0)][impl_s_hat.shape(1)]
                                  [impl_s_hat.shape(2)]);

            likelihood->gradientLikelihood(cpp_s_hat, *u_gradient);

            return Python::makeNumpy(u_gradient->get_array(), u_gradient);
          })
      .def(
          "logLikelihood",
          [](GridDensityLikelihoodBase<3> *likelihood,
             py::array_t<
                 std::complex<double>,
                 py::array::c_style | py::array::forcecast>
                 s_hat) {
            auto impl_s_hat = s_hat.unchecked<3>();

            py::gil_scoped_release release;

            auto mgr = likelihood->getManager();

            size_t startN0 = mgr->startN0;
            size_t localN0 = mgr->localN0;

            // Check the array has correct size
            if (impl_s_hat.shape(0) != mgr->localN0 ||
                impl_s_hat.shape(1) != mgr->N1 ||
                impl_s_hat.shape(2) != mgr->N2_HC) {
              throw std::invalid_argument("The array has incorrect shape");
            }

            typedef boost::multi_array_types::extent_range e_range;

            // Due to an incorrect API in likelihood we have to const away
            // the pointer, though we only require a const access.
            boost::multi_array_ref<std::complex<double>, 3> cpp_s_hat(
                const_cast<std::complex<double> *>(impl_s_hat.data(0, 0, 0)),
                boost::extents[e_range(startN0, startN0+localN0)][mgr->N1][mgr->N2_HC]);

            return likelihood->logLikelihood(cpp_s_hat);
          })
      .def(
          "generateMockData",
          [](GridDensityLikelihoodBase<3> *likelihood,
             py::array_t<
                 std::complex<double>,
                 py::array::c_style | py::array::forcecast>
                 s_hat,
             MarkovState *state) {
            auto impl_s_hat = s_hat.unchecked<3>();

            py::gil_scoped_release release;

            // Due to an incorrect API in likelihood we have to const away
            // the pointer, though we only require a const access.
            boost::multi_array_ref<std::complex<double>, 3> cpp_s_hat(
                const_cast<std::complex<double> *>(impl_s_hat.data(0, 0, 0)),
                boost::extents[impl_s_hat.shape(0)][impl_s_hat.shape(1)]
                              [impl_s_hat.shape(2)]);

            likelihood->generateMockData(cpp_s_hat, *state);
          })
      .def(
          "updateMetaParameters",
          [](GridDensityLikelihoodBase<3> *likelihood, MarkovState *state) {
            likelihood->updateMetaParameters(*state);
          })
      .def(
          "initializeLikelihood",
          [](GridDensityLikelihoodBase<3> *likelihood, MarkovState *state) {
            likelihood->initializeLikelihood(*state);
          })
      .def(
          "getCommunicator",
          [](GridDensityLikelihoodBase<3> *likelihood) -> py::object {
            if (!mpi4py_available)
              return py::none();

            return makePythonMPI(likelihood->getManager()->getComm());
          });

  py::class_<
      ForwardModelBasedLikelihood, GridDensityLikelihoodBase<3>,
      std::shared_ptr<ForwardModelBasedLikelihood>>(
      m, "ForwardModelLikelihood3d",
      DOC(aquila_borg, likelihood, ForwardModelLikelihood3d))
      .def(
          "getForwardModel", &ForwardModelBasedLikelihood::getForwardModel,
          DOC(aquila_borg, likelihood, ForwardModelLikelihood3d,
              getForwardModel));

  py::class_<
      BasePyLikelihood, ForwardModelBasedLikelihood, PyLikelihood,
      std::shared_ptr<BasePyLikelihood>>(
      m, "BaseLikelihood", DOC(aquila_borg, likelihood, BaseLikelihood))
      .def(py::init<>([](std::shared_ptr<BORGForwardModel> fwd,
                         py::array_t<size_t> N, py::array_t<double> L) {
        auto v = new PyLikelihood(fwd, N, L);
        return v;
      }));

  py::class_<LikelihoodInfo, std::shared_ptr<LikelihoodInfo>>(
      m, "LikelihoodInfo", DOC(aquila_borg, likelihood, LikelihoodInfo))
      .def(
          py::init<>([]() {
            LikelihoodInfo *info = new LikelihoodInfo();
            (*info)[Likelihood::MPI] = MPI_Communication::instance();
            return info;
          }),
          "Construct an empty LikelihoodInfo object")
      .def(
          "items",
          [](LikelihoodInfo *info) {
            std::vector<std::string> names;
            for (auto &x : *info) {
              names.push_back(x.first);
            }
            return names;
          },
          "Returns:\n  list(str): list of strings to give the name of each "
          "entry in the dictionnary")
      .def(
          "__getitem__",
          [](LikelihoodInfo *info, std::string const &name) {
            auto iter = info->find(name);
            if (iter == info->end()) {
              throw py::key_error(name);
            }

            return any_to_python(iter->second);
          })
      .def(
          "__setitem__",
          [](LikelihoodInfo *info, std::string const &name, py::object o) {
            (*info)[name] = python_to_any(o);
          });

  create_generic_bind<AdaptBias_Gauss<bias::Passthrough>, GaussianLikelihood>(
      m, "GaussianPassthrough",
      DOC(aquila_borg, likelihood, GaussianPassthrough));

  create_generic_bind<bias::Passthrough, VoxelPoissonLikelihood>(
      m, "PoissonPassthrough",
      DOC(aquila_borg, likelihood, PoissonPassthrough));

  create_generic_bind<AdaptBias_Gauss<bias::LinearBias>, GaussianLikelihood>(
      m, "GaussianLinear", DOC(aquila_borg, likelihood, GaussianLinear));

  create_generic_bind<bias::PowerLaw, VoxelPoissonLikelihood>(
      m, "PoissonPowerLaw", DOC(aquila_borg, likelihood, PoissonPowerLaw));
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
