/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/static_auto.hpp"
#include <julia.h>
#include <list>
#include <string>
#include <algorithm>
#include <vector>
#include <iterator>
#include <boost/algorithm/string/join.hpp>
#include "libLSS/julia/julia.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include "libLSS/samplers/core/types_samplers.hpp"
#include "src/common/preparation_types.hpp"
#include "libLSS/tools/string_tools.hpp"
#include <boost/algorithm/string.hpp>

using namespace LibLSS;

using boost::format;
using boost::str;
using LibLSS::Julia::Object;

//extern "C" void jl_exit_on_sigint(int);
//
void *LibLSS::Julia::details::julia_array_reorder = 0;

namespace {

  void julia_console_print(int level, char const *msg) {
    Console &cons = Console::instance();
    std::vector<std::string> results;
    std::string s(msg);
    boost::split(results, s, [](char c) { return c == '\n'; });
    switch (level) {
    case 0:
      cons.print<LOG_STD>(msg);
      break;
    case 1:
      cons.print<LOG_ERROR>(msg);
      break;
    case 2:
      cons.print<LOG_WARNING>(msg);
      break;
    case 3:
      cons.print<LOG_INFO>(msg);
      break;
    case 4:
      cons.print<LOG_INFO_SINGLE>(msg);
      break;
    case 5:
      cons.print<LOG_VERBOSE>(msg);
      break;
    case 6:
      cons.print<LOG_DEBUG>(msg);
      break;
    default:
      cons.print<LOG_ERROR>(
          "Unknown log level for message '" + std::string(msg) + "'");
    }
  }

  void *julia_console_progress_start(int level, char const *msg, int max) {
    return 0;
  }

  void julia_console_progress_step(void *p) {}

  void julia_console_progress_end(void *p) {}

  double rand_uniform(MarkovState *state) {
    return state->get<RandomGen>("random_generator")->get().uniform();
  }

  double rand_gaussian(MarkovState *state) {
    return state->get<RandomGen>("random_generator")->get().gaussian();
  }

  LibLSS_prepare::GalaxySurveyType::GalaxyType *
  get_galaxy_descriptor(MarkovState *state, int id, int *sz) {
    using LibLSS_prepare::GalaxyElement;

    try {
      std::string cname = "galaxy_catalog_" + to_string(id);
      if (state->exists(cname)) {
        auto &survey = state->get<GalaxyElement>(cname)->get().getGalaxies();

        *sz = survey.size();
        return survey.data();
      } else {
        std::string cname = "halo_catalog_" + to_string(id);
        auto &survey = state->get<GalaxyElement>(cname)->get().getGalaxies();

        *sz = survey.size();
        return survey.data();
      }
    } catch (LibLSS::ErrorBase &e) {
      jl_error(e.what());
    }
  }

#define AUTO_STATE_EDIT_QUERY(type)                                            \
  void BOOST_PP_CAT(state_edit_, type)(                                        \
      MarkovState * state, char const *entry, type const *value, int sync) {   \
    try {                                                                      \
      if (sync != 0)                                                           \
        state->getSyncScalar<type>(entry) = *value;                            \
      else                                                                     \
        state->getScalar<type>(entry) = *value;                                \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  void BOOST_PP_CAT(state_query_, type)(                                       \
      MarkovState * state, char const *entry, type *v, int sync) {             \
    try {                                                                      \
      if (sync != 0)                                                           \
        *v = state->getSyncScalar<type>(entry);                                \
      else                                                                     \
        *v = state->getScalar<type>(entry);                                    \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  void BOOST_PP_CAT(state_new_, type)(                                         \
      MarkovState * state, char const *entry, type const *value, int sync,     \
      int mcmc_save) {                                                         \
    try {                                                                      \
      if (sync != 0)                                                           \
        state->newSyScalar<type>(entry, *value, mcmc_save != 0);               \
      else                                                                     \
        state->newScalar<type>(entry, *value, mcmc_save != 0);                 \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_new_1d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t N, int mcmc_save) {       \
    ArrayStateElement<type, 1> *elt;                                           \
    state->newElement(                                                         \
        entry, elt = new ArrayStateElement<type, 1>(boost::extents[N]),        \
        mcmc_save != 0);                                                       \
    return elt->array->data();                                                 \
  }                                                                            \
  void BOOST_PP_CAT(state_1d_array_autosize_, type)(                           \
      MarkovState * state, char const *entry, int b) {                         \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 1>>(entry);                  \
      a->setAutoResize(b == 1);                                                \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_get_1d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t *N) {                     \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 1>>(entry)->array;           \
      *N = a->size();                                                          \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
      return 0;                                                                \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_resize_1d_array_, type)(                            \
      MarkovState * state, char const *entry, size_t N) {                      \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 1>>(entry)->array;           \
      a->resize(boost::extents[N]);                                            \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      return 0;                                                                \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_new_2d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t N0, size_t N1,            \
      int mcmc_save) {                                                         \
    ArrayStateElement<type, 2> *elt;                                           \
    state->newElement(                                                         \
        entry, elt = new ArrayStateElement<type, 2>(boost::extents[N0][N1]),   \
        mcmc_save != 0);                                                       \
    return elt->array->data();                                                 \
  }                                                                            \
  type *BOOST_PP_CAT(state_get_2d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t *N) {                     \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 2>>(entry)->array;           \
      N[1] = a->shape()[0];                                                    \
      N[0] = a->shape()[1];                                                    \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
      return 0;                                                                \
    }                                                                          \
  }                                                                            \
  void BOOST_PP_CAT(state_2d_array_autosize_, type)(                           \
      MarkovState * state, char const *entry, int b) {                         \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 2>>(entry);                  \
      a->setAutoResize(b == 1);                                                \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_resize_2d_array_, type)(                            \
      MarkovState * state, char const *entry, size_t N0, size_t N1) {          \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 2>>(entry)->array;           \
      a->resize(boost::extents[N0][N1]);                                       \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      return 0;                                                                \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_new_3d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t N0, size_t N1, size_t N2, \
      int mcmc_save) {                                                         \
    ArrayStateElement<type, 3, FFTW_Allocator<type>, true> *elt;               \
    state->newElement(                                                         \
        entry,                                                                 \
        elt = new ArrayStateElement<type, 3, FFTW_Allocator<type>, true>(      \
            boost::extents[N0][N1][N2]),                                       \
        mcmc_save != 0);                                                       \
    return elt->array->data();                                                 \
  }                                                                            \
  type *BOOST_PP_CAT(state_get_3d_array_, type)(                               \
      MarkovState * state, char const *entry, size_t *N) {                     \
    try {                                                                      \
      auto a =                                                                 \
          state                                                                \
              ->get<ArrayStateElement<type, 3, FFTW_Allocator<type>, true>>(   \
                  entry)                                                       \
              ->array;                                                         \
      N[2] = a->shape()[0];                                                    \
      N[1] = a->shape()[1];                                                    \
      N[0] = a->shape()[2];                                                    \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
      return 0;                                                                \
    }                                                                          \
  }                                                                            \
  void BOOST_PP_CAT(state_3d_array_autosize_, type)(                           \
      MarkovState * state, char const *entry, int b) {                         \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 3>>(entry);                  \
      a->setAutoResize(b == 1);                                                \
    } catch (LibLSS::ErrorBase & e) {                                          \
      jl_error(e.what());                                                      \
    }                                                                          \
  }                                                                            \
  type *BOOST_PP_CAT(state_resize_3d_array_, type)(                            \
      MarkovState * state, char const *entry, size_t N0, size_t N1,            \
      size_t N2) {                                                             \
    try {                                                                      \
      auto a = state->get<ArrayStateElement<type, 3>>(entry)->array;           \
      a->resize(boost::extents[N0][N1][N2]);                                   \
      return a->data();                                                        \
    } catch (LibLSS::ErrorBase & e) {                                          \
      return 0;                                                                \
    }                                                                          \
  }

  AUTO_STATE_EDIT_QUERY(int);
  AUTO_STATE_EDIT_QUERY(long);
  AUTO_STATE_EDIT_QUERY(double);

  const std::string julia_module_code =
#if !defined(DOXYGEN_SHOULD_SKIP_THIS)
#include "libLSS/julia/julia_module.hpp"
#else
	  ""
#endif
      ;

  void initializeJulia() {
    auto &cons = Console::instance();

    cons.print<LOG_INFO>("Initialize Julia core");

    std::string thread_count = str(format("%d") % smp_get_max_threads());
    setenv("JULIA_NUM_THREADS", thread_count.c_str(), 1);
    setenv("JULIA_HOME", JULIA_HOME, 1);
    jl_init_with_image(JULIA_BINDIR, jl_get_default_sysimg_path());

    jl_value_t *exc;
    jl_value_t **args;
    jl_function_t *func;

    JL_GC_PUSH2(&exc, &func);
    // Load the special static module to make the wrapping easier.
    (void)jl_eval_string(julia_module_code.c_str());

    exc = jl_exception_occurred();
    if (exc != 0) {
      cons.print<LOG_ERROR>("Fatal error in the initialization of Julia core");
      jl_call2(
          jl_get_function(jl_base_module, "showerror"), jl_stderr_obj(), exc);
      JL_GC_POP();
      jl_exception_clear();
      throw Julia::JuliaException(Object(exc));
    }

    cons.print<LOG_VERBOSE>("Invoking _setup_module");
    // Now setup some hooks between julia and ARES Core.
    {
      jl_value_t *func_entries;
      JL_GC_PUSH1(&func_entries);
      constexpr size_t maxNumArgs = 52;
      std::string array_creation =
          str(format("Array{Ptr{Nothing}}(undef,(%d,))") % maxNumArgs);

      func_entries = jl_eval_string(array_creation.c_str());
      exc = jl_exception_occurred();
      if (exc != 0) {
        cons.print<LOG_ERROR>(
            "Fatal error in the initialization of Julia core");
        jl_call2(
            jl_get_function(jl_base_module, "showerror"), jl_stderr_obj(), exc);
        JL_GC_POP();
        jl_exception_clear();
        throw Julia::JuliaException(Object(exc));
      }
      void **func_entries_p = (void **)jl_array_data(func_entries);

      size_t current_arg = 0;
      func_entries_p[current_arg++] =
          reinterpret_cast<void *>(&julia_console_print);

#define PUSH_FUNC(func)                                                        \
  func_entries_p[current_arg++] = reinterpret_cast<void *>(func)
#define PUSH_STATE_EDIT_QUERY(type)                                            \
  PUSH_FUNC(BOOST_PP_CAT(&state_new_, type));                                  \
  PUSH_FUNC(BOOST_PP_CAT(&state_edit_, type));                                 \
  PUSH_FUNC(BOOST_PP_CAT(&state_query_, type));                                \
  PUSH_FUNC(BOOST_PP_CAT(&state_new_1d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_get_1d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_resize_1d_array_, type));                      \
  PUSH_FUNC(BOOST_PP_CAT(&state_1d_array_autosize_, type));                    \
  PUSH_FUNC(BOOST_PP_CAT(&state_new_2d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_get_2d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_resize_2d_array_, type));                      \
  PUSH_FUNC(BOOST_PP_CAT(&state_2d_array_autosize_, type));                    \
  PUSH_FUNC(BOOST_PP_CAT(&state_new_3d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_get_3d_array_, type));                         \
  PUSH_FUNC(BOOST_PP_CAT(&state_resize_3d_array_, type));                      \
  PUSH_FUNC(BOOST_PP_CAT(&state_3d_array_autosize_, type));

      PUSH_STATE_EDIT_QUERY(int);
      PUSH_STATE_EDIT_QUERY(long);
      PUSH_STATE_EDIT_QUERY(double);

      PUSH_FUNC(&rand_uniform);
      PUSH_FUNC(&rand_gaussian);

      PUSH_FUNC(&get_galaxy_descriptor);
      PUSH_FUNC(&julia_console_progress_start);
      PUSH_FUNC(&julia_console_progress_step);
      PUSH_FUNC(&julia_console_progress_end);

      func = (jl_function_t *)jl_eval_string("libLSS._setup_module");
      exc = jl_exception_occurred();
      if (exc != 0) {
        cons.print<LOG_ERROR>(
            "Fatal error in the initialization of Julia core");
        jl_call2(
            jl_get_function(jl_base_module, "showerror"), jl_stderr_obj(), exc);
        JL_GC_POP();
        jl_exception_clear();
        throw Julia::JuliaException(Object(exc));
      }

      cons.c_assert(func != 0, "Julia could not resolve our setup function");
      cons.c_assert(
          current_arg == maxNumArgs, "Invalid allocation for arguments");
      cons.print<LOG_VERBOSE>("Run _setup_module");
      jl_call1(func, (jl_value_t *)func_entries);
      cons.print<LOG_VERBOSE>("Done _setup");

      Julia::details::julia_array_reorder = jl_get_global(
          (jl_module_t *)jl_get_global(jl_main_module, jl_symbol("libLSS")),
          jl_symbol("_array_reorder"));
      cons.c_assert(
          Julia::details::julia_array_reorder != 0,
          "Array reordering symbol not found");

      JL_GC_POP();
    }
    JL_GC_POP();

    //    jl_exit_on_sigint(1);
  }

  void finalizeJulia() {
    Console::instance().print<LOG_INFO>("Cleaning julia core.");
    jl_atexit_hook(0);
  }

  RegisterStaticInit reg(initializeJulia, finalizeJulia, 10);
} // namespace

AUTO_REGISTRATOR_IMPL(JuliaInit);

Object Julia::global(std::string const &n) {
  return Object(jl_get_global(jl_main_module, jl_symbol(n.c_str())));
}

void Julia::global(std::string const &n, Object o) {
  jl_set_global(jl_main_module, jl_symbol(n.c_str()), (jl_value_t *)o.ptr());
}
