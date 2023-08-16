/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyforward_all.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <memory>
#include <pybind11/stl.h>
#include "pyforward.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"
#include "pyborg.hpp"
#include "libLSS/physics/forwards/all_models.hpp"

/**
 * @brief This class adapts a Python dictionnary to a PropertyProxy usable by model factories
 * 
 */
class PyProperty : public LibLSS::PropertyProxy {
protected:
  typedef LibLSS::Python::py::dict dict;
  typedef LibLSS::Python::py::str str;

  dict opts;
  std::map<std::type_index, std::function<PropertyType(std::string const &)>>
      getters;

  template <typename T>
  PropertyType _caster(std::string const &n) const {
    return PropertyType(opts[str(n)].template cast<T>());
  }

  template <typename T>
  PropertyType
  _caster_with_default(std::string const &n, PropertyType v) const {
    auto py_n = str(n);
    if (!opts.contains(py_n))
      return v;
    return PropertyType(opts[py_n].cast<T>());
  }

  virtual PropertyType real_get(std::string const &n, std::type_index v) const {
    return getters.find(v)->second(n);
  }

  virtual PropertyType real_get(std::string const &n, PropertyType v) const {
    return boost::apply_visitor(
        [&](auto t) { return PropertyType(_caster_with_default<decltype(t)>(n, v)); }, v);
  };

  virtual boost::optional<PropertyType>
  real_get_optional(std::string const &n, std::type_index v) const {
    if (opts.contains(n))
      return boost::optional<PropertyType>(getters.find(v)->second(n));
    return boost::optional<PropertyType>();
  };

  template <typename U>
  inline void setup_getters(boost::variant<U>) {
    getters[typeid(U)] =
        std::bind(&PyProperty::_caster<U>, this, std::placeholders::_1);
  }

  template <typename U, typename V, typename... T>
  inline void setup_getters(boost::variant<U, V, T...>) {
    getters[typeid(U)] =
        std::bind(&PyProperty::_caster<U>, this, std::placeholders::_1);
    setup_getters(boost::variant<V, T...>());
  }

public:
  /**
   * @brief Construct a new Py Property object
   * 
   * @param opts_ Python dictionnary
   */
  PyProperty(dict &opts_) : opts(opts_) { setup_getters(PropertyType()); }
};

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.forward.models.hpp"

void LibLSS::Python::pyForwardAll(Python::py::module m) {
  using LibLSS::Python::py::dict;

  m.def("newModel", [](std::string const &name, BoxModel *box, py::dict opts) {
    auto factory = LibLSS::setup_forward_model(name);

    return factory(MPI_Communication::instance(), *box, PyProperty(opts));
  }, DOC(aquila_borg, forward, models, newModel));
  m.def("listModels", []() {
    auto all_models = ForwardRegistry::instance().list();
    std::vector<std::string> model_names;
    for (auto &m : all_models)
      model_names.push_back(m.first);
    return model_names;
  }, DOC(aquila_borg, forward, models, listModels));
}

// ARES TAG: num_authors = 1
// ARES TAG: author(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
