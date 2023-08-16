/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_JULIA_HPP
#define __LIBLSS_TOOLS_JULIA_HPP

#include <boost/multi_array.hpp>
#include "libLSS/tools/static_auto.hpp"
#include "libLSS/tools/errors.hpp"
#include <memory>
#include <vector>

AUTO_REGISTRATOR_DECL(JuliaInit);

namespace LibLSS {

  namespace Julia {

    template <typename T, size_t N>
    using array = boost::multi_array_ref<T, N>;

    struct Object;

    struct Object {
      size_t opaquePosition;

      template <typename T>
      void box(T v);

      template <typename Ret>
      Ret unbox();

      template <typename T, size_t N>
      array<T, N> unbox_array();

      template <typename T, size_t N>
      void box_array(array<T, N> &a);

      void *ptr() const;

      Object(Object const &o);
      Object(Object &&o);
      Object(void *o);
      Object();
      ~Object();
      Object &operator=(void *o);
      Object &operator=(Object const &o);

    private:
      void protect();
    };

    template <typename T>
    Object translate(T x) {
      Object o;
      o.box(x);
      return o;
    }

    struct Module;

    class JuliaNotFound : virtual public ErrorBase {
    private:
      std::string symbol;

    public:
      JuliaNotFound(const std::string &n)
          : ErrorBase("Not found symbol: " + n) {}
    };

    class JuliaBadUnbox : virtual public ErrorBase {
    public:
      JuliaBadUnbox() : ErrorBase("Attempt to unbox a null pointer") {}
    };

    class JuliaException : virtual public ErrorBase {
    private:
      Object j_obj;

      static std::string prepare(Object &o);

    public:
      Object getJuliaException() { return j_obj; }
      JuliaException(Object &&o) : ErrorBase(prepare(o)), j_obj(o) {}
    };

    bool isBadGradient(JuliaException &e);

    Object evaluate(std::string const &code);
    void load_file(std::string const &filename);
    void handle_julia_exception();

    Module *module(std::string const &name);

    Object manual_invoke(
        Module *module, std::string const &name,
        std::vector<Object> const &args);

    Object
    manual_invoke(std::string const &name, std::vector<Object> const &args);

    void global(std::string const &name, Object o);

    Object global(std::string const &name);

    namespace details {
      using std::vector;

      extern void *julia_array_reorder;

      template <typename T>
      void variadic_vector_emplace(vector<T> &) {}

      template <typename T, typename First, typename... Args>
      void
      variadic_vector_emplace(vector<T> &v, First &&first, Args &&... args) {
        v.emplace_back(std::forward<First>(first));
        variadic_vector_emplace(v, std::forward<Args>(args)...);
      }

      template <typename... Args>
      Object invoke(std::string const &name, Args &&... args) {
        vector<Object> vec;
        variadic_vector_emplace(vec, translate(args)...);
        return manual_invoke(name, vec);
      }

      template <typename... Args>
      Object invoke(Module *module, std::string const &name, Args &&... args) {
        vector<Object> vec;
        variadic_vector_emplace(vec, translate(args)...);
        return manual_invoke(module, name, vec);
      }

    } // namespace details

    using details::invoke;
  } // namespace Julia

} // namespace LibLSS

#endif
