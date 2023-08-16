/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pylikelihood_wrap.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

// We implement here the thin wrap to be able to call likelihood defined in python.
// The overloading call has to happen explicitly.
// This is the base class first.
class BasePyLikelihood : public ForwardModelBasedLikelihood {
private:
  template <typename G, typename T>
  static inline G _to_grid(py::array_t<T> a) {
    G g;

    auto real_a = a.template unchecked<1>();
    if (real_a.shape(0) != g.size()) {
      throw std::runtime_error("Invalid number of dimensions");
    }
    for (int i = 0; i < g.size(); i++) {
      g[i] = real_a.data(0)[i];
    }
    return g;
  }

public:
  // We delete all default constructors to avoid avoid any mistakes.
  BasePyLikelihood(BasePyLikelihood &&other) = delete;
  BasePyLikelihood(BasePyLikelihood const &other) = delete;
  BasePyLikelihood() = delete;

  // Setup a general constructor to create the appropriate internal structure
  // for a cube with mesh size N and side length L.
  BasePyLikelihood(py::array_t<size_t> N, py::array_t<double> L)
      : ForwardModelBasedLikelihood(
            MPI_Communication::instance(), _to_grid<GridSizes>(N),
            _to_grid<GridLengths>(L)) {}
};

// This is the thin wrapper class.
class PyLikelihood : public BasePyLikelihood {
public:
  std::shared_ptr<BORGForwardModel> base_fwd;

  // Make a constructor that set aside the forward model inside the
  // likelihood object for later use.
  PyLikelihood(
      std::shared_ptr<BORGForwardModel> fwd, py::array_t<size_t> N,
      py::array_t<double> L)
      : BasePyLikelihood(N, L), base_fwd(fwd) {}

  std::shared_ptr<BORGForwardModel> getForwardModel() override {
    return base_fwd;
  }

  // All the following functions are wrappers that follow the same
  // basic schema.

  void gradientLikelihood(
      ArrayRef const &parameters, ArrayRef &gradient_parameters,
      bool accumulate = false, double scaling = 1.0) override {
    py::gil_scoped_acquire acquire;

    py::object py_params = Python::makeNumpy(parameters);

    py::function overload = py::get_overload(
        static_cast<const BasePyLikelihood *>(this), "gradientLikelihoodReal");
    if (overload) {
      py::array_t<double> o = overload(py_params);

      Python::PyToFuseArray<double, 3, false> boosted_o(o.unchecked<3>());
      if (accumulate)
        fwrap(gradient_parameters) =
            fwrap(gradient_parameters) + fwrap(boosted_o) * scaling;
      else
        fwrap(gradient_parameters) = fwrap(boosted_o) * scaling;
      return;
    }
    py::pybind11_fail("Tried to call a pure virtual function "
                      "BasePyLikelihood::gradientLikelihoodReal");
  }

  void gradientLikelihood(
      CArrayRef const &parameters, CArrayRef &gradient_parameters,
      bool accumulate = false, double scaling = 1.0) override {
    py::gil_scoped_acquire acquire;
    py::object py_params = Python::makeNumpy(parameters);

    py::function overload = py::get_overload(
        static_cast<const BasePyLikelihood *>(this),
        "gradientLikelihoodComplex");
    if (overload) {
      py::array_t<std::complex<double>> o = overload(py_params);

      Python::PyToFuseArray<std::complex<double>, 3, false> boosted_o(
          o.unchecked<3>());
      typedef boost::multi_array_types::index_range i_range;

      size_t s0 = mgr->startN0;
      auto local_grad = gradient_parameters[boost::indices[i_range(
          s0, s0 + mgr->localN0)][i_range(0, mgr->N1)][i_range(0, mgr->N2_HC)]];

      if (accumulate)
        fwrap(local_grad) = fwrap(local_grad) + fwrap(boosted_o) * scaling;
      else
        fwrap(local_grad) = fwrap(boosted_o) * scaling;
      return;
    }
    py::pybind11_fail("Tried to call a pure virtual function "
                      "BasePyLikelihood::gradientLikelihoodComplex");
  }

  double logLikelihood(
      ArrayRef const &parameters, bool gradientIsNext = false) override {
    py::gil_scoped_acquire acquire;
    py::object py_params = Python::makeNumpy(parameters);

    PYBIND11_OVERLOAD_PURE(
        double, BasePyLikelihood, logLikelihoodReal, py_params, gradientIsNext);
  }

  double logLikelihood(
      CArrayRef const &parameters, bool gradientIsNext = false) override {
    py::gil_scoped_acquire acquire;
    py::object py_params = Python::makeNumpy(parameters);

    PYBIND11_OVERLOAD_PURE(
        double, BasePyLikelihood, logLikelihoodComplex, py_params,
        gradientIsNext);
  }

  void initializeLikelihood(MarkovState &state) override {
    PYBIND11_OVERLOAD_PURE(
        void, BasePyLikelihood, initializeLikelihood, &state);
  }

  void updateMetaParameters(MarkovState &state) override {
    PYBIND11_OVERLOAD_PURE(
        void, BasePyLikelihood, updateMetaParameters, &state);
  }

  void setupDefaultParameters(MarkovState &state, int catalog) override {
    PYBIND11_OVERLOAD_PURE(
        void, BasePyLikelihood, setupDefaultParameters, &state);
  }

  void updateCosmology(CosmologicalParameters const &params) override {
    PYBIND11_OVERLOAD_PURE(void, BasePyLikelihood, updateCosmology, &params);
  }

  void commitAuxiliaryFields(MarkovState &state) override {
    PYBIND11_OVERLOAD(void, BasePyLikelihood, commitAuxiliaryFields, state);
  }

  void
  generateMockData(CArrayRef const &parameters, MarkovState &state) override {
    py::gil_scoped_acquire acquire;
    {
      py::object py_params = Python::makeNumpy(parameters);

      PYBIND11_OVERLOAD_PURE(
          void, BasePyLikelihood, generateMockData, py_params, &state);
    }
  }
};
