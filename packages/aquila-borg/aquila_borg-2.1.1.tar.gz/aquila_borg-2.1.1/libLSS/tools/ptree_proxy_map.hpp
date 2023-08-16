/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/ptree_proxy_map.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PTREE_PROXY_MAP_HPP
#  define __LIBLSS_PTREE_PROXY_MAP_HPP

#  include "libLSS/tools/ptree_proxy.hpp"

namespace LibLSS {

  /**
   * @brief Class to holds a simple map that stores property fro PropertyProxy
   */
  class PropertyFromMap : public LibLSS::PropertyProxy {
  protected:
    std::map<std::string, PropertyType> properties;

    PropertyType
    real_get(std::string const &n, std::type_index v) const override {
      auto r = real_get_optional(n, v);
      if (!r)
        throw std::runtime_error("Missing entry");
      return *r;
    }

    PropertyType real_get(std::string const &n, PropertyType v) const override {
      auto i = properties.find(n);
      if (i == properties.end())
        return v;
      return i->second;
    }

    boost::optional<PropertyType>
    real_get_optional(std::string const &n, std::type_index v) const override {
      auto i = properties.find(n);
      if (i == properties.end())
        return boost::optional<PropertyType>();
      return boost::optional<PropertyType>(i->second);
    }

  public:
    /**
     * @brief Constructor
     */
    PropertyFromMap() : PropertyProxy() {}

    /**
     * @brief assign a value to some property
     * @params n name of the property
     * @params prop value of the property, must be one of the supported variant
     */
    void set(std::string const &n, PropertyType prop) { properties[n] = prop; }
  };

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: author(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
