/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_box.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_auto.hpp"
#include "libLSS/tools/static_init.hpp"
#include <array>
#include <julia.h>
#include <list>
#include <string>
#include <algorithm>
#include <vector>
#include <iterator>
#include <boost/algorithm/string/join.hpp>
#include "libLSS/julia/julia.hpp"
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>

using namespace LibLSS;
using boost::format;

using LibLSS::Julia::Object;

static constexpr size_t LIBLSS_MAX_JULIA_STACK = 256;

static void *opaque_stack[LIBLSS_MAX_JULIA_STACK];
static void *opaque_other_stack[3 * LIBLSS_MAX_JULIA_STACK];
static bool opaque_stack_busy[LIBLSS_MAX_JULIA_STACK];
static size_t currentOpaqueStackPosition = 0;

#define OPAQUE opaque_stack[opaquePosition]

namespace LibLSS {
  namespace Julia {

    template <typename T>
    jl_value_t *julia_types();

    template <typename T>
    std::string julia_type_name() {
      return jl_symbol_name(((jl_datatype_t *)julia_types<T>())->name->name);
    }

    void Object::protect() {
      Console::instance().c_assert(currentOpaqueStackPosition < LIBLSS_MAX_JULIA_STACK, "Julia stack not large enough, increase LIBLSS_MAX_JULIA_STACK");
      opaque_stack_busy[opaquePosition = currentOpaqueStackPosition++] = true;
      OPAQUE = 0;

#if (JULIA_VERSION_MAJOR==1) && (JULIA_VERSION_MINOR >= 4)
      opaque_other_stack[3 * opaquePosition] = (void *)JL_GC_ENCODE_PUSH(1);
      opaque_other_stack[3 * opaquePosition + 1] = jl_pgcstack;
      opaque_other_stack[3 * opaquePosition + 2] = &OPAQUE;
#else
      opaque_other_stack[3 * opaquePosition] = (void *)3;
      opaque_other_stack[3 * opaquePosition + 1] = jl_pgcstack;
      opaque_other_stack[3 * opaquePosition + 2] = &OPAQUE;
#endif
      jl_pgcstack = (jl_gcframe_t *)&opaque_other_stack[3 * opaquePosition];
    }

    Object::Object(Object const &o) {
      protect();
      OPAQUE = o.ptr();
    }

    Object::Object(Object &&o) {
      protect();
      OPAQUE = o.ptr();
    }

    void *Object::ptr() const { return OPAQUE; }

    Object::~Object() {
      opaque_stack_busy[opaquePosition] = false;
      if (currentOpaqueStackPosition == opaquePosition + 1) {
        // Ok complete full stack unwinding
        do {
          if (opaque_stack_busy[currentOpaqueStackPosition - 1])
            break;
          currentOpaqueStackPosition--;
          Console::instance().c_assert(jl_pgcstack == (jl_gcframe_t *)&opaque_other_stack[3 * currentOpaqueStackPosition], "Julia stack ordering is broken.");
          jl_pgcstack = jl_pgcstack->prev;
        } while (currentOpaqueStackPosition > 0);
      }
    }

    Object &Object::operator=(void *o) {
      OPAQUE = o;
      return *this;
    }

    Object &Object::operator=(Object const &o) {
      OPAQUE = o.ptr();
      return *this;
    }

    Object::Object() { protect(); }

    Object::Object(void *v) {
      protect();
      OPAQUE = v;
    }

    template <>
    void Object::box(Object o) {
      OPAQUE = o.ptr();
    }

#define IMPLEMENT_AUTO_TRANSLATE(type, jtype)                                  \
  template <>                                                                  \
  void Object::box<type>(type x) {                                             \
    OPAQUE = BOOST_PP_CAT(jl_box_, jtype)(x);                                  \
  }                                                                            \
  template <>                                                                  \
  type Object::unbox<type>() {                                                 \
    type x;                                                                    \
    if (OPAQUE == 0) {                                                         \
      throw JuliaBadUnbox();                                                   \
    }                                                                          \
    x = BOOST_PP_CAT(jl_unbox_, jtype)(                                        \
        reinterpret_cast<jl_value_t *>(OPAQUE));                               \
    return x;                                                                  \
  }                                                                            \
  template <>                                                                  \
  jl_value_t *julia_types<type>() {                                            \
    return (jl_value_t *)BOOST_PP_CAT(BOOST_PP_CAT(jl_, jtype), _type);        \
  }

#define ONE_AUTO_TRANSLATE(r, data, T)                                         \
  IMPLEMENT_AUTO_TRANSLATE(                                                    \
      BOOST_PP_TUPLE_ELEM(2, 0, T), BOOST_PP_TUPLE_ELEM(2, 1, T))

    BOOST_PP_SEQ_FOR_EACH(
        ONE_AUTO_TRANSLATE, X,
        ((bool, bool))((double, float64))((float, float32))((int8_t, int8))(
            (uint8_t, uint8))((int16_t, int16))((uint16_t, uint16))(
            (int32_t, int32))((uint32_t, uint32))((int64_t, int64))(
            (uint64_t, uint64))((void *, voidpointer)));

    template <typename T, size_t N>
    array<T, N> Object::unbox_array() {
      std::array<size_t, N> julia_extents;
      jl_value_t *jobj = reinterpret_cast<jl_value_t *>(OPAQUE);
      jl_datatype_t *el =
          reinterpret_cast<jl_datatype_t *>(jl_array_eltype(jobj));

      if (el != (jl_datatype_t *)julia_types<T>()) {
        error_helper<ErrorBadState>(
            "Incompatible array type, got " +
            std::string(jl_symbol_name(el->name->name)) + " and expected " +
            julia_type_name<T>());
      }

      for (size_t i = 0; i < N; i++)
        julia_extents[i] = jl_array_dim(jobj, i);

      return array<T, N>(
          reinterpret_cast<T *>(jl_array_data(jobj)), julia_extents);
    }

    template <typename T, size_t N>
    void Object::box_array(array<T, N> &a) {
      jl_value_t *array_type = 0;
      jl_value_t *dims = 0;
      jl_value_t *tmp_array = 0;
      jl_value_t *cppOrder = 0;
      JL_GC_PUSH4(&array_type, &dims, &tmp_array, &cppOrder); 

      std::string tuple_string = "(";

      for (ssize_t i = N - 1; i >= 0; i--)
        tuple_string += std::to_string(a.shape()[i]) + ",";
      tuple_string += ")";

      array_type = jl_apply_array_type(julia_types<T>(), N);

      cppOrder = jl_box_bool(true);

      dims = jl_eval_string(tuple_string.c_str());
      handle_julia_exception();
      tmp_array = (jl_value_t *)jl_ptr_to_array(array_type, a.data(), dims, 0);
      handle_julia_exception();
      OPAQUE = jl_call2( (jl_value_t*) Julia::details::julia_array_reorder, tmp_array, cppOrder);
      handle_julia_exception();

      JL_GC_POP();
    }

#define DECL_ARRAY_SINGLE(z, n, data)                                          \
  template array<data, n> Object::unbox_array<data, n>();                      \
  template void Object::box_array<data, n>(array<data, n> &);

#define DECL_ARRAY_MULTIPLE(r, data, elem)                                     \
  BOOST_PP_REPEAT(4, DECL_ARRAY_SINGLE, elem)

    BOOST_PP_SEQ_FOR_EACH(
        DECL_ARRAY_MULTIPLE, X,
        (bool)(double)(float)(int8_t)(uint8_t)(int16_t)(uint16_t)(int32_t)(
            uint32_t)(int64_t)(uint64_t));
#ifdef __APPLE__
    // Funny OSX types long long is 64 bits, long int is 64 bits too but different.
    IMPLEMENT_AUTO_TRANSLATE(unsigned long, uint64)
    DECL_ARRAY_MULTIPLE(X, X, unsigned long)
#endif

  } // namespace Julia

} // namespace LibLSS
