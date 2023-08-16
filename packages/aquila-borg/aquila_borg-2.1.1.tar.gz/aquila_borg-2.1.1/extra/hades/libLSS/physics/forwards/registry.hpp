/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/registry.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PHYSICS_FORWARDS_REGISTRY_HPP
#  define __LIBLSS_PHYSICS_FORWARDS_REGISTRY_HPP

#  include <map>
#  include <string>
#  include <memory>
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/ptree_proxy.hpp"
#  include "libLSS/tools/errors.hpp"

namespace LibLSS {

  typedef std::function<std::shared_ptr<BORGForwardModel>(
      MPI_Communication *comm, BoxModel const &box,
      PropertyProxy const &params)>
      ForwardModelFactory;

  /**
   * @brief Class that handles the automatic registration of forward model element.
   * 
   * The models can be later automatically constructed provided a name, a box and a dictionary.
   */
  class ForwardRegistry {
  private:
    std::map<std::string, ForwardModelFactory> forwardRegistry;
    ForwardRegistry();

  public:
    static ForwardRegistry &instance();

    /**
     * @brief Register a new element factory. This is internal, do not call it directly.
     * 
     * @param n 
     * @param factory 
     */
    void registerFactory(std::string const &n, ForwardModelFactory factory) {
      forwardRegistry[n] = factory;
    }

    /**
     * @brief List all registered models.
     * 
     * @return std::map<std::string, ForwardModelFactory> const 
     */
    auto const list() { return forwardRegistry; }

    /**
     * @brief Lookup a factory
     * 
     * @param n name
     * @return ForwardModelFactory a factory
     */
    ForwardModelFactory get(std::string const &n);
  };

  struct _RegisterForwardModel {
    _RegisterForwardModel(std::string n, ForwardModelFactory factory) {
      ForwardRegistry::instance().registerFactory(n, factory);
    }
  };

  ForwardModelFactory setup_forward_model(std::string const &n);

/**
 * @brief Declare an automatic registrator. This is required to get the dynamic linker includes the symbols.
 * 
 */
#  define LIBLSS_REGISTER_FORWARD_DECL(NAME)                                   \
    AUTO_REGISTRATOR_DECL(Forward_##NAME)

#  define LIBLSS_REGISTER_NAME(NAME) Forward_##NAME
#  define MANGLED_LIBLSS_REGISTER_NAME(NAME) _register_##NAME
#  define LIBLSS_REGISTER_NAMESTR(NAME) #  NAME

/**
 * @brief Implements an automatic registrator. A builder function must be provided as an argument.
 * 
 */
#  define LIBLSS_REGISTER_FORWARD_IMPL(NAME, BUILDER)                          \
    AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(NAME))                          \
    namespace {                                                                \
      _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(NAME)(                \
          LIBLSS_REGISTER_NAMESTR(NAME), BUILDER);                             \
    }

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
