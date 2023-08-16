/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/ptree_proxy.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PTREE_PROXY_HPP
#  define __LIBLSS_PTREE_PROXY_HPP

#  include <boost/variant.hpp>
#  include <string>
#  include "libLSS/tools/ptree_translators.hpp"
#  include <typeindex>
#  include <functional>

namespace LibLSS {

  class PropertyProxy {
  protected:
    typedef boost::variant<int, double, bool, std::string> PropertyType;

    virtual PropertyType
    real_get(std::string const &n, std::type_index v) const = 0;

    virtual PropertyType
    real_get(std::string const &n, PropertyType v) const = 0;

    virtual boost::optional<PropertyType>
    real_get_optional(std::string const &n, std::type_index v) const = 0;

  public:
    PropertyProxy() {}
    ~PropertyProxy() {}

    template <typename T>
    inline T get(std::string const &n) const {
      return boost::get<T>(real_get(n, typeid(T)));
    }

    template <typename T>
    inline T get(std::string const &n, T def_value) const {
      return boost::get<T>(real_get(n, PropertyType(def_value)));
    }

    template <typename T>
    inline boost::optional<T> get_optional(std::string const &n) const {
      auto ret = real_get_optional(n, typeid(T));
      if (!ret)
        return boost::optional<T>();
      else
        return boost::optional<T>(boost::get<T>(*ret));
    }
  };

  template <typename ptree>
  class PropertyProxyPtree : public PropertyProxy {
  protected:
    typedef ptree PropertyTree;

    PropertyTree tree;
    std::map<std::type_index, std::function<PropertyType(std::string const &)>>
        getters;
    std::map<
        std::type_index,
        std::function<boost::optional<PropertyType>(std::string const &)>>
        optional_getters;

    virtual boost::optional<PropertyType>
    real_get_optional(std::string const &n, std::type_index ti) const {
      return optional_getters.find(ti)->second(n);
    }

    virtual PropertyType
    real_get(std::string const &n, std::type_index ti) const {
      return getters.find(ti)->second(n);
    }

    virtual PropertyType real_get(std::string const &n, PropertyType v) const {
      return boost::apply_visitor(
          [this, &n, &v](auto v_hint) {
            auto o = this->tree.template get_optional<decltype(v_hint)>(n);
            if (o) return PropertyType(*o);
            return v;
          },
          v);
    }

    template <typename U>
    PropertyType implement_getter(std::string const &n) const {
      return this->tree.template get<U>(n);
    }

    template <typename U>
    boost::optional<PropertyType> implement_optional_getter(std::string const &n) const {
      auto ret = this->tree.template get_optional<U>(n);
      if (!ret)
        return boost::optional<PropertyType>();
      return boost::optional<PropertyType>(*ret);
    }

    template <typename U>
    inline void setup_getters(boost::variant<U>) {
      getters[typeid(U)] = std::bind(
          &PropertyProxyPtree<ptree>::implement_getter<U>, this,
          std::placeholders::_1);
      optional_getters[typeid(U)] = std::bind(
          &PropertyProxyPtree<ptree>::implement_optional_getter<U>, this,
          std::placeholders::_1);
    }

    template <typename U, typename V, typename... T>
    inline void setup_getters(boost::variant<U, V, T...>) {
      getters[typeid(U)] = std::bind(
          &PropertyProxyPtree<ptree>::implement_getter<U>, this,
          std::placeholders::_1);
      optional_getters[typeid(U)] = std::bind(
          &PropertyProxyPtree<ptree>::implement_optional_getter<U>, this,
          std::placeholders::_1);
      setup_getters(boost::variant<V, T...>());
    }

  public:
    PropertyProxyPtree(PropertyTree &tree_) : tree(tree_) {
      setup_getters(PropertyType());
    }

    PropertyProxyPtree(boost::optional<PropertyTree &> tree_) {
      if (tree_)
        tree = *tree_;
      setup_getters(PropertyType());
    }

    ~PropertyProxyPtree() {}
  };

  template <typename T>
  auto make_proxy_property_tree(T &tree_) {
    return PropertyProxyPtree<T>(tree_);
  }

  template <typename T>
  auto make_proxy_property_tree(boost::optional<T &> tree_) {
    return PropertyProxyPtree<T>(tree_);
  }

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
