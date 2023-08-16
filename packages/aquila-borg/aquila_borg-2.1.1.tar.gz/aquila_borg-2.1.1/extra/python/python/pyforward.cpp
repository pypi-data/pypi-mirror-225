/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyforward.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include <memory>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <CosmoTool/cosmopower.hpp>
#include <pybind11/numpy.h>

#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"

#include "pyborg.hpp"

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "pyforward.hpp"
#include "pyfuse.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/physics/chain_forward_model.hpp"

#include "py_mpi.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

using namespace LibLSS;
typedef boost::multi_array_types::index_range i_range;

template <typename T, typename U>
static inline void transfer_in(
    std::shared_ptr<BORGForwardModel::DFT_Manager> &mgr, T &tmp_in, U &in,
    bool cplx) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  size_t s0 = mgr->startN0;
  Python::PyToFuseArray<typename T::element, 3, false> p_in(in);
  auto vv =
      tmp_in[boost::indices[i_range(s0, s0 + mgr->localN0)][i_range(0, mgr->N1)]
                           [i_range(0, cplx ? mgr->N2_HC : mgr->N2)]];

  fwrap(vv) = fwrap(p_in);
}

template <typename T, typename U>
static inline void transfer_out(
    std::shared_ptr<BORGForwardModel::DFT_Manager> &mgr, T &tmp_out, U &out,
    bool cplx) {
  size_t s0 = mgr->startN0;
  Python::PyToFuseArray<typename T::element, 3, true> p_out(out);

  fwrap(p_out) =
      fwrap(tmp_out[boost::indices[i_range(s0, s0 + mgr->localN0)][i_range(
          0, mgr->N1)][i_range(0, cplx ? mgr->N2_HC : mgr->N2)]]);
}

class BaseForwardModel : public BORGForwardModel {
public:
  BaseForwardModel(BaseForwardModel &&other) = default;

  BaseForwardModel(BoxModel const &in_box, BoxModel const &out_box)
      : BORGForwardModel(MPI_Communication::instance(), in_box, out_box) {}
};

/**
 * @brief Class to reverse wrap python object to make them available in C++
 * 
 */
class PyBaseForwardModel : public BaseForwardModel {
public:
  using BaseForwardModel::BaseForwardModel;

  PyBaseForwardModel(BaseForwardModel &&other)
      : BaseForwardModel(std::move(other)) {}

  PreferredIO getPreferredInput() const override {
    py::gil_scoped_acquire acquire;
    PYBIND11_OVERLOAD_PURE(PreferredIO, BaseForwardModel, getPreferredInput);
  }

  PreferredIO getPreferredOutput() const override {
    py::gil_scoped_acquire acquire;
    PYBIND11_OVERLOAD_PURE(PreferredIO, BaseForwardModel, getPreferredOutput);
  }

  void accumulateAdjoint(bool on) override {
    py::gil_scoped_acquire acquire;
    PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, accumulateAdjoint, on);
  }

  void setModelParams(ModelDictionnary const &params) override {
    {
      py::gil_scoped_acquire acquire;
      py::dict pyParams;

      for (auto const &k : params) {
        if (k.second.type() == typeid(double)) {
          pyParams[k.first.c_str()] = boost::any_cast<double>(k.second);
        } else if (k.second.type() == typeid(LibLSS::multi_array<double, 1>)) {
          auto values =
              boost::any_cast<LibLSS::multi_array<double, 1>>(k.second);
          py::array_t<double> tmp({values.shape()[0]}, {1}, values.data());
          pyParams[k.first.c_str()] = tmp;
        } else if (
            k.second.type() ==
            typeid(std::shared_ptr<LibLSS::CosmologicalParameters>)) {
          CosmologicalParameters cosmo =
              *boost::any_cast<std::shared_ptr<LibLSS::CosmologicalParameters>>(
                  k.second);
          pyParams[k.first.c_str()] = cosmo;
        } else {
          error_helper<ErrorParams>(
              "Unknown type to be converted to Python in setModelParams");
        }
      }

      auto pythonFunction = py::get_overload(
          static_cast<BaseForwardModel const *>(this), "setModelParams");
      if (pythonFunction) {
        pythonFunction(pyParams);
      }
    }
    BaseForwardModel::setModelParams(params);
  }

  boost::any
  getModelParam(std::string const &name, std::string const &keyname) override {
    {
      py::gil_scoped_acquire acquire;
      py::dict pyParams;

      auto pythonFunction = py::get_overload(
          static_cast<BaseForwardModel const *>(this), "getModelParam");
      if (pythonFunction) {
        py::object ret = pythonFunction(name, keyname);
        return Python::python_to_any(ret);
      }
    }
    return BaseForwardModel::getModelParam(name, keyname);
  }

  void forwardModel_v2(ModelInput<3> input) override {
    switch (getPreferredInput()) {
    case PREFERRED_REAL: {
      input.setRequestedIO(PREFERRED_REAL);
      auto &x = input.getRealConst();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, input.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, forwardModel_v2_impl, h);
      }
      break;
    }
    case PREFERRED_FOURIER: {
      input.setRequestedIO(PREFERRED_FOURIER);
      auto &x = input.getFourierConst();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, input.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, forwardModel_v2_impl, h);
      }
      break;
    }
    default:
      error_helper<ErrorNotImplemented>("IO type not implemented.");
      break;
    }
  }

  void getDensityFinal(ModelOutput<3> output) override {
    switch (getPreferredOutput()) {
    case PREFERRED_REAL: {
      output.setRequestedIO(PREFERRED_REAL);
      auto &x = output.getRealOutput();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, output.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, getDensityFinal_impl, h);
      }
      break;
    }
    case PREFERRED_FOURIER: {
      output.setRequestedIO(PREFERRED_FOURIER);
      auto &x = output.getFourierOutput();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, output.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, getDensityFinal_impl, h);
      }
      break;
    }
    default:
      error_helper<ErrorNotImplemented>("IO type not implemented.");
      break;
    }
  }

  void adjointModel_v2(ModelInputAdjoint<3> input) override {
    switch (getPreferredOutput()) {
    case PREFERRED_REAL: {
      input.setRequestedIO(PREFERRED_REAL);
      auto &x = input.getRealConst();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, input.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, adjointModel_v2_impl, h);
      }
      break;
    }
    case PREFERRED_FOURIER: {
      input.setRequestedIO(PREFERRED_FOURIER);
      auto &x = input.getFourierConst();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, input.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, adjointModel_v2_impl, h);
      }
      break;
    }
    default:
      error_helper<ErrorNotImplemented>("IO type not implemented.");
      break;
    }
  }

  void getAdjointModelOutput(ModelOutputAdjoint<3> output) override {
    switch (getPreferredInput()) {
    case PREFERRED_REAL: {
      output.setRequestedIO(PREFERRED_REAL);
      auto &x = output.getRealOutput();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, output.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, getAdjointModel_impl, h);
      }
      break;
    }
    case PREFERRED_FOURIER: {
      output.setRequestedIO(PREFERRED_FOURIER);
      auto &x = output.getFourierOutput();
      {
        py::gil_scoped_acquire acquire;
        py::object h = Python::makeNumpy(x, output.hold_original);

        PYBIND11_OVERLOAD_PURE(void, BaseForwardModel, getAdjointModel_impl, h);
      }
      break;
    }
    default:
      error_helper<ErrorNotImplemented>("IO type not implemented.");
      break;
    }
  }
};

static void do_forward_v2(BORGForwardModel *fwd_model, py::array input) {
  ModelInput<3> model_input;

  if (input.dtype().is(py::dtype::of<double>())) {
    auto in = input.unchecked<double, 3>();

    check_array_real(in, fwd_model->lo_mgr);

    auto tmp_in_p = fwd_model->lo_mgr->allocate_ptr_array();
    auto &tmp_in = tmp_in_p->get_array();

    transfer_in(fwd_model->lo_mgr, tmp_in, in, false);

    model_input = std::move(ModelInput<3>(
        fwd_model->lo_mgr, fwd_model->get_box_model(), tmp_in,
        std::move(tmp_in_p)));
  } else if (input.dtype().is(py::dtype::of<std::complex<double>>())) {
    auto in = input.unchecked<std::complex<double>, 3>();

    check_array_complex(in, fwd_model->lo_mgr);

    auto tmp_in_c_p = fwd_model->lo_mgr->allocate_ptr_complex_array();
    auto &tmp_in_c = tmp_in_c_p->get_array();

    transfer_in(fwd_model->lo_mgr, tmp_in_c, in, true);

    model_input = std::move(ModelInput<3>(
        fwd_model->lo_mgr, fwd_model->get_box_model(), tmp_in_c,
        std::move(tmp_in_c_p)));
  } else {
    throw std::runtime_error(
        "PyBORGForward only support double and complex double.");
  }

  {
    py::gil_scoped_release release;

    fwd_model->forwardModel_v2(std::move(model_input));
  }
  // If the forward model has put a hold on input, it will not be destroyed till the hold is released.
}

static void do_adjoint_v2(BORGForwardModel *fwd_model, py::object o_input) {
  ModelInputAdjoint<3> model_input;

  if (o_input.is_none()) {
    py::gil_scoped_release release;
    // We just a push an empty AG vector.
    fwd_model->adjointModel_v2(std::move(model_input));
    return;
  }

  py::array input = o_input;

  if (input.dtype().is(py::dtype::of<double>())) {
    auto in = input.unchecked<double, 3>();

    check_array_real(in, fwd_model->out_mgr);

    auto tmp_in_p = fwd_model->lo_mgr->allocate_ptr_array();
    auto &tmp_in = tmp_in_p->get_array();

    transfer_in(fwd_model->lo_mgr, tmp_in, in, false);

    model_input = std::move(ModelInputAdjoint<3>(
        fwd_model->out_mgr, fwd_model->get_box_model_output(), tmp_in,
        std::move(tmp_in_p)));
  } else if (input.dtype().is(py::dtype::of<std::complex<double>>())) {
    auto in = input.unchecked<std::complex<double>, 3>();

    check_array_complex(in, fwd_model->out_mgr);

    auto tmp_in_c_p = fwd_model->out_mgr->allocate_ptr_complex_array();
    auto &tmp_in_c = tmp_in_c_p->get_array();

    transfer_in(fwd_model->out_mgr, tmp_in_c, in, true);

    model_input = std::move(ModelInputAdjoint<3>(
        fwd_model->lo_mgr, fwd_model->get_box_model(), tmp_in_c,
        std::move(tmp_in_c_p)));
  } else {
    throw std::runtime_error(
        "PyBORGForward only support double and complex double.");
  }

  {
    py::gil_scoped_release release;

    fwd_model->adjointModel_v2(std::move(model_input));
  }
  // If the forward model has put a hold on input, it will not be destroyed till the hold is released.
}

static void
do_get_adjoint_model(BORGForwardModel *fwd_model, py::array output) {
  decltype(fwd_model->lo_mgr->allocate_ptr_array()) tmp_in_p;
  std::function<void()> do_post_transfer;
  std::shared_ptr<void> buf_holder;
  ModelOutputAdjoint<3> model_output;

  if (output.dtype().is(py::dtype::of<double>())) {
    auto out = output.mutable_unchecked<double, 3>();

    check_array_real(out, fwd_model->out_mgr);

    auto tmp_out_p = fwd_model->lo_mgr->allocate_ptr_array();
    auto &tmp_out = tmp_out_p->get_array();

    buf_holder = std::move(tmp_out_p);
    model_output = std::move(ModelOutputAdjoint<3>(
        fwd_model->lo_mgr, fwd_model->get_box_model(), tmp_out, buf_holder));

    do_post_transfer = [&]() {
      auto out = output.mutable_unchecked<double, 3>();
      transfer_out(fwd_model->lo_mgr, tmp_out, out, false);
    };

  } else if (output.dtype().is(py::dtype::of<std::complex<double>>())) {
    auto out = output.mutable_unchecked<std::complex<double>, 3>();

    check_array_complex(out, fwd_model->lo_mgr);

    auto tmp_out_p = fwd_model->lo_mgr->allocate_ptr_complex_array();
    auto &tmp_out = tmp_out_p->get_array();

    buf_holder = std::move(tmp_out_p);
    model_output = std::move(ModelOutputAdjoint<3>(
        fwd_model->lo_mgr, fwd_model->get_box_model(), tmp_out, buf_holder));

    do_post_transfer = [&]() {
      auto out = output.mutable_unchecked<std::complex<double>, 3>();
      transfer_out(fwd_model->lo_mgr, tmp_out, out, true);
    };

  } else {
    throw std::runtime_error(
        "PyBORGForward only support double and complex double.");
  }

  {
    py::gil_scoped_release release;

    fwd_model->getAdjointModelOutput(std::move(model_output));

    do_post_transfer();
  }
}

static void
do_get_density_final(BORGForwardModel *fwd_model, py::array output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  decltype(fwd_model->lo_mgr->allocate_ptr_array()) tmp_in_p;
  std::function<void()> do_post_transfer;
  std::shared_ptr<void> buf_holder;
  ModelOutput<3> model_output;

  if (output.dtype().is(py::dtype::of<double>())) {
    auto out = output.mutable_unchecked<double, 3>();

    check_array_real(out, fwd_model->out_mgr);

    auto tmp_out_p = fwd_model->out_mgr->allocate_ptr_array();
    auto &tmp_out = tmp_out_p->get_array();

    buf_holder = std::move(tmp_out_p);
    model_output = std::move(ModelOutput<3>(
        fwd_model->out_mgr, fwd_model->get_box_model_output(), tmp_out,
        buf_holder));

    do_post_transfer = [&]() {
      auto out = output.mutable_unchecked<double, 3>();
      transfer_out(fwd_model->out_mgr, tmp_out, out, false);
    };

  } else if (output.dtype().is(py::dtype::of<std::complex<double>>())) {
    auto out = output.mutable_unchecked<std::complex<double>, 3>();

    check_array_complex(out, fwd_model->out_mgr);

    auto tmp_out_p = fwd_model->out_mgr->allocate_ptr_complex_array();
    auto &tmp_out = tmp_out_p->get_array();

    buf_holder = std::move(tmp_out_p);
    model_output = std::move(ModelOutput<3>(
        fwd_model->out_mgr, fwd_model->get_box_model_output(), tmp_out,
        buf_holder));

    do_post_transfer = [&]() {
      auto out = output.mutable_unchecked<std::complex<double>, 3>();
      transfer_out(fwd_model->out_mgr, tmp_out, out, true);
    };

  } else {
    throw std::runtime_error(
        "PyBORGForward only support double and complex double.");
  }

  {
    py::gil_scoped_release release;

    fwd_model->getDensityFinal(std::move(model_output));

    do_post_transfer();
  }
}

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.forward.hpp"
#include "pyborg_doc/aquila_borg.forward.BaseForwardModel.hpp"
#include "pyborg_doc/aquila_borg.forward.BORGForwardModel.hpp"
#include "pyborg_doc/aquila_borg.forward.ChainForwardModel.hpp"
#include "pyborg_doc/aquila_borg.forward.BoxModel.hpp"

void LibLSS::Python::pyForwardBase(py::module this_module) {
  this_module.doc() = DOC(aquila_borg, forward);

  py::enum_<PreferredIO>(
      this_module, "PreferredIO", DOC(aquila_borg, forward, PreferredIO))
      .value(
          "PREFERRED_REAL", PREFERRED_REAL,
          "Indicate that real space representation is requested for IO")
      .value(
          "PREFERRED_FOURIER", PREFERRED_FOURIER,
          "Indicate that fourier space representation is requested for IO")
      .value(
          "PREFERRED_NONE", PREFERRED_NONE,
          "None are preferred. It is not supported in python.")
      .export_values();

  py::class_<BoxModel>(this_module, "BoxModel")
      .def(
          py::init([](double L, int N) {
            BoxModel *boxmodel = new BoxModel;
            boxmodel->L0 = boxmodel->L1 = boxmodel->L2 = L;
            boxmodel->N0 = boxmodel->N1 = boxmodel->N2 = N;
            boxmodel->xmin0 = boxmodel->xmin1 = boxmodel->xmin2 = 0;
            return boxmodel;
          }),
          "L"_a = 100.0, "N"_a = 128,
          DOC(aquila_borg, forward, BoxModel, __init__))
      .def_property(
          "xmin",
          [](BoxModel *boxmodel) {
            return py::make_tuple(
                boxmodel->xmin0, boxmodel->xmin1, boxmodel->xmin2);
          },
          [](BoxModel *boxmodel, py::tuple t) {
            boxmodel->xmin0 = t[0].cast<double>();
            boxmodel->xmin1 = t[1].cast<double>();
            boxmodel->xmin2 = t[2].cast<double>();
          },
          DOC(aquila_borg, forward, BoxModel, xmin))
      .def_property(
          "L",
          [](BoxModel *boxmodel) {
            return py::make_tuple(boxmodel->L0, boxmodel->L1, boxmodel->L2);
          },
          [](BoxModel *boxmodel, py::tuple t) {
            boxmodel->L0 = t[0].cast<double>();
            boxmodel->L1 = t[1].cast<double>();
            boxmodel->L2 = t[2].cast<double>();
          },
          DOC(aquila_borg, forward, BoxModel, L))
      .def_property_readonly(
          "volume",
          [](BoxModel *boxmodel) {
            return boxmodel->L0 * boxmodel->L1 * boxmodel->L2;
          },
          DOC(aquila_borg, forward, BoxModel, volume))
      .def_property_readonly(
          "Ntot",
          [](BoxModel *boxmodel) {
            return boxmodel->N0 * boxmodel->N1 * boxmodel->N2;
          },
          DOC(aquila_borg, forward, BoxModel, Ntot))
      .def(
          "copy",
          [](BoxModel *boxmodel) {
            BoxModel *newboxmodel = new BoxModel;
            *newboxmodel = *boxmodel;
            return newboxmodel;
          },
          DOC(aquila_borg, forward, BoxModel, copy))
      .def_property(
          "N",
          [](BoxModel *boxmodel) {
            return py::make_tuple(boxmodel->N0, boxmodel->N1, boxmodel->N2);
          },
          [](BoxModel *boxmodel, py::tuple t) {
            boxmodel->N0 = t[0].cast<long>();
            boxmodel->N1 = t[1].cast<long>();
            boxmodel->N2 = t[2].cast<long>();
          },
          DOC(aquila_borg, forward, BoxModel, N))
      .def("__repr__", [](BoxModel *boxmodel) {
        return boost::str(
            boost::format(
                "<BoxModel: xc=[%g,%g,%g], L=[%g,%g,%g], N=[%d,%d,%d]") %
            boxmodel->xmin0 % boxmodel->xmin1 % boxmodel->xmin2 % boxmodel->L0 %
            boxmodel->L1 % boxmodel->L2 % boxmodel->N0 % boxmodel->N1 %
            boxmodel->N2);
      });

  py::class_<BORGForwardModel, std::shared_ptr<BORGForwardModel>>(
      this_module, "BORGForwardModel",
      DOC(aquila_borg, forward, BORGForwardModel))
      .def(
          "getPreferredOutput", &BORGForwardModel::getPreferredOutput,
          DOC(aquila_borg, forward, BORGForwardModel, getPreferredOutput))
      .def(
          "getPreferredInput", &BORGForwardModel::getPreferredInput,
          DOC(aquila_borg, forward, BORGForwardModel, getPreferredOutput))
      .def(
          "setCosmoParams",
          [](BORGForwardModel *fwd_model, CosmologicalParameters *cpar) {
            Console::instance().print<LOG_DEBUG>(
                "setting cosmological parameters");
            fwd_model->setCosmoParams(*cpar);
          },
          "cosmo_params"_a,
          DOC(aquila_borg, forward, BORGForwardModel, setCosmoParams))

      .def(
          "getModelParam",
          [](BORGForwardModel *fwd_model, std::string const &model,
             std::string const &keyname) {
            boost::any ret = fwd_model->getModelParam(model, keyname);
            return any_to_python(ret);
          },
          "model"_a, "keyname"_a,
          DOC(aquila_borg, forward, BORGForwardModel, getModelParam))
      .def(
          "setName", &BORGForwardModel::setName, "name"_a,
          DOC(aquila_borg, forward, BORGForwardModel, setName))
      .def(
          "setModelParams",
          [](BORGForwardModel *fwd_model, py::dict d) {
            ModelDictionnary params;
            for (auto const &kv : d) {
              std::string name = py::cast<std::string>(kv.first);
              if (py::isinstance<py::array>(kv.second)) {
                auto a_typed = kv.second.cast<py::array_t<double>>();
                if (a_typed.ndim() != 1)
                  throw std::runtime_error("Only 1-d arrays are supported.");
                LibLSS::multi_array<double, 1> local_values(
                    boost::extents[a_typed.shape()[0]]);
                auto a_direct = a_typed.unchecked<1>();
                for (int i = 0; i < local_values.num_elements(); i++)
                  local_values[i] = a_direct(i);
                params.insert({name, local_values});
              } else if (py::isinstance<py::float_>(kv.second)) {
                double value = kv.second.cast<double>();
                params.insert({name, value});
              } else if (py::isinstance<py::int_>(kv.second)) {
                int value = kv.second.cast<int>();
                params.insert({name, value});
              } else if (py::isinstance<LikelihoodInfo>(kv.second)) {
                std::shared_ptr<LikelihoodInfo> info =
                    kv.second.cast<std::shared_ptr<LikelihoodInfo>>();
                params.insert({name, info});
              } else if (py::isinstance<CosmologicalParameters>(kv.second)) {
                CosmologicalParameters cosmo = kv.second.cast<CosmologicalParameters>();
                params.insert({name, cosmo});
              }
            }
            fwd_model->setModelParams(params);
          },
          "params"_a,
          DOC(aquila_borg, forward, BORGForwardModel, setModelParams))
      .def(
          "getBoxModel",
          [](BORGForwardModel *fwd_model) {
            BoxModel *bm = new BoxModel();
            *bm = fwd_model->get_box_model();
            return bm;
            ;
          },
          "Return the box on which is defined the input of the model is "
          "defined.")
      .def(
          "getOutputBoxModel",
          [](BORGForwardModel *fwd_model) {
            BoxModel *bm = new BoxModel();
            *bm = fwd_model->get_box_model_output();
            return bm;
            ;
          },
          DOC(aquila_borg, forward, BORGForwardModel, getOutputBoxModel))
      .def(
          "getMPISlice",
          [](BORGForwardModel *fwd_model) {
            return py::make_tuple(
                fwd_model->lo_mgr->startN0, fwd_model->lo_mgr->localN0,
                fwd_model->lo_mgr->N1, fwd_model->lo_mgr->N2);
          },
          DOC(aquila_borg, forward, BORGForwardModel, getMPISlice))
      .def(
          "getCommunicator",
          [](BORGForwardModel *model) {
            return makePythonMPI(model->communicator());
          },
          DOC(aquila_borg, forward, BORGForwardModel, getCommunicator))
      .def(
          "getOutputMPISlice",
          [](BORGForwardModel *fwd_model) {
            return py::make_tuple(
                fwd_model->out_mgr->startN0, fwd_model->out_mgr->localN0,
                fwd_model->out_mgr->N1, fwd_model->out_mgr->N2);
          },
          "Return a tuple indicating what is the expected output MPI slicing "
          "(startN0,localN0,N1,N2)  (Warning! unstable API)")
      .def("holdParticles", &BORGForwardModel::holdParticles)
      .def(
          "setAdjointRequired", &BORGForwardModel::setAdjointRequired,
          DOC(aquila_borg, forward, BORGForwardModel, setAdjointRequired))
      .def(
          "forwardModel_v2", do_forward_v2,
          DOC(aquila_borg, forward, BORGForwardModel, forwardModel_v2))
      .def(
          "getDensityFinal", do_get_density_final,
          "Obtain the density field produced by the forward model (part 2 of "
          "the evaluation, v2 API).")
      .def(
          "accumulateAdjoint", &BORGForwardModel::accumulateAdjoint,
          "do_accumulate"_a,
          DOC(aquila_borg, forward, BORGForwardModel, accumulateAdjoint))
      .def(
          "adjointModel_v2", do_adjoint_v2,
          py::arg("adjoint_gradient").none(true),
          DOC(aquila_borg, forward, BORGForwardModel, adjointModel_v2))
      .def(
          "clearAdjointGradient", &BORGForwardModel::clearAdjointGradient,
          DOC(aquila_borg, forward, BORGForwardModel, clearAdjointGradient))
      .def("getAdjointModel", do_get_adjoint_model)
      .def(
          "forwardModel", [](BORGForwardModel *fwd_model,
                             py::array_t<std::complex<double>> in_delta,
                             py::array_t<double> out_delta) {
            auto in = in_delta.unchecked<3>();
            auto out = out_delta.mutable_unchecked<3>();

            if (in.shape(0) != fwd_model->lo_mgr->localN0 ||
                in.shape(1) != fwd_model->lo_mgr->N1 ||
                in.shape(2) != fwd_model->lo_mgr->N2_HC)
              throw std::range_error(boost::str(
                  boost::format("Input array has invalid dimensions, expecting "
                                "%dx%dx%d") %
                  fwd_model->lo_mgr->localN0 % fwd_model->lo_mgr->N1 %
                  fwd_model->lo_mgr->N2_HC));

            if (out.shape(0) != fwd_model->lo_mgr->localN0 ||
                out.shape(1) != fwd_model->lo_mgr->N1 ||
                out.shape(2) != fwd_model->lo_mgr->N2)
              throw std::range_error(boost::str(
                  boost::format(
                      "Output array has invalid dimensions, expecting "
                      "%dx%dx%d") %
                  fwd_model->lo_mgr->localN0 % fwd_model->lo_mgr->N1 %
                  fwd_model->lo_mgr->N2));

            py::gil_scoped_release release;

            auto tmp_in_p = fwd_model->lo_mgr->allocate_complex_array();
            auto &tmp_in = tmp_in_p.get_array();
            auto tmp_out_p = fwd_model->lo_mgr->allocate_array();
            auto &tmp_out = tmp_out_p.get_array();
            size_t s0 = fwd_model->lo_mgr->startN0;
            size_t const localN0 = fwd_model->lo_mgr->localN0,
                         N1 = fwd_model->lo_mgr->N1,
                         N2_HC = fwd_model->lo_mgr->N2_HC;

#pragma omp parallel for schedule(static) collapse(3)
            for (size_t i = 0; i < localN0; i++) {
              for (size_t j = 0; j < N1; j++) {
                for (size_t k = 0; k < N2_HC; k++) {
                  tmp_in[i + s0][j][k] = in(i, j, k);
                }
              }
            }

            fwd_model->forwardModel(tmp_in, tmp_out, false);

#pragma omp parallel for schedule(static) collapse(3)
            for (size_t i = 0; i < localN0; i++) {
              for (size_t j = 0; j < N1; j++) {
                for (size_t k = 0; k < N2_HC; k++) {
                  out(i, j, k) = tmp_out[i + s0][j][k];
                }
              }
            }
          });

  py::class_<
      ParticleBasedForwardModel, BORGForwardModel,
      std::shared_ptr<ParticleBasedForwardModel>>(
      this_module, "ParticleBasedForwardModel",
      DOC(aquila_borg, forward, ParticleBasedForwardModel))
      .def(
          "getNumberOfParticles",
          &ParticleBasedForwardModel::getNumberOfParticles,
          DOC(aquila_borg, forward, ParticleBasedForwardModel,
              getNumberOfParticles))
      .def(
          "getParticlePositions",
          [](ParticleBasedForwardModel *fwd, py::array_t<double> particles) {
            PyToFuseArray<double, 2, true> out_p(
                particles.mutable_unchecked<2>());
            LibLSS::copy_array(out_p, fwd->getParticlePositions());
          },
          "positions"_a,
          DOC(aquila_borg, forward, ParticleBasedForwardModel,
              getParticlePositions))
      .def(
          "setStepNotifier",
          [](ParticleBasedForwardModel *fwd, py::object callback) {
            fwd->setStepNotifier([callback](
                                     double t, size_t i,
                                     ParticleBasedForwardModel::IdSubArray,
                                     ParticleBasedForwardModel::PhaseSubArray,
                                     ParticleBasedForwardModel::PhaseSubArray) {
              py::gil_scoped_acquire acquire;
              callback(t, i);
            });
          },
          DOC(aquila_borg, forward, ParticleBasedForwardModel, setStepNotifier))
      .def(
          "getParticleVelocities",
          [](ParticleBasedForwardModel *fwd, py::array_t<double> particles) {
            PyToFuseArray<double, 2, true> out_p(
                particles.mutable_unchecked<2>());
            LibLSS::copy_array(out_p, fwd->getParticleVelocities());
          },
          "velocities"_a,
          DOC(aquila_borg, forward, ParticleBasedForwardModel,
              getParticleVelocities));

  py::class_<
      BaseForwardModel, BORGForwardModel, PyBaseForwardModel,
      std::shared_ptr<BaseForwardModel>>(
      this_module, "BaseForwardModel",
      DOC(aquila_borg, forward, BaseForwardModel))
      .def(
          py::init<>([](BoxModel *b1, BoxModel *b2) {
            return new BaseForwardModel(*b1, *b2);
          }),
          "box_input"_a, "box_output"_a,
          "Construct the C++ side of the forward model with provided input and "
          "output boxes.");

  py::class_<
      ChainForwardModel, BORGForwardModel, std::shared_ptr<ChainForwardModel>>(
      this_module, "ChainForwardModel",
      DOC(aquila_borg, forward, ChainForwardModel))
      .def(
          py::init([](BoxModel *box) {
            return std::make_unique<ChainForwardModel>(
                MPI_Communication::instance(), *box);
          }),
          "box_model"_a, DOC(aquila_borg, forward, ChainForwardModel, __init__))
      .def(
          "addModel",
          [](ChainForwardModel *fwd_model, py::object fwd_python) {
            std::shared_ptr<BORGForwardModel> c =
                fwd_python.cast<std::shared_ptr<BORGForwardModel>>();
            fwd_python.inc_ref();
            // Make a new shared_object which, once ChainForwardModel does not need the model anymore will release
            // the reference count on the original object.
            fwd_model->addModel(std::shared_ptr<BORGForwardModel>(
                c.get(), [c, fwd_python](void *) mutable {
                  fwd_python.dec_ref();
                  c.reset();
                }));
          },
          "forward"_a, DOC(aquila_borg, forward, ChainForwardModel, addModel));
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
