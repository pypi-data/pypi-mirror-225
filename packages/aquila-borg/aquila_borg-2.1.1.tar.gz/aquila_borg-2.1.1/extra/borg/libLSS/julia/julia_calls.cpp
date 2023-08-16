/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_calls.cpp
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
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>

using namespace LibLSS;

using LibLSS::Julia::Object;

namespace LibLSS {
  namespace Julia {

    std::string JuliaException::prepare(Object &j_obj) {
      Object pipe, data;

      std::string msg =
          jl_typeof_str(reinterpret_cast<jl_value_t *>(j_obj.ptr()));
      msg += ": ";
      pipe = evaluate("PipeBuffer()");
      jl_call2(
          jl_get_function(jl_base_module, "showerror"),
          (jl_value_t *)pipe.ptr(), (jl_value_t *)j_obj.ptr());

      data = jl_call1(
          jl_get_function(jl_base_module, "read"), (jl_value_t *)pipe.ptr());
      char *full_msg = (char *)jl_array_data(data.ptr());
      size_t msg_len = jl_array_dim(data.ptr(), 0);

      std::vector<std::string> splitted_error;
      std::string s_msg(full_msg, msg_len);
      boost::algorithm::split(splitted_error, s_msg, boost::is_any_of("\n"));

      Console::instance().print<LOG_ERROR>("Julia exception trace:");
      Console::instance().indent();

      for (auto &one_msg : splitted_error) {
        Console::instance().print<LOG_ERROR>(one_msg);
        msg += one_msg;
      }
      Console::instance().unindent();
      Console::instance().print<LOG_ERROR>("End of Julia exception");

      return msg;
    }

    void handle_julia_exception() {
      Object exc = jl_exception_occurred();
      if (exc.ptr() != 0) {
        jl_exception_clear();
        throw JuliaException(std::move(exc));
      }
    }

    Object evaluate(std::string const &code) {
      Object ret = jl_eval_string(code.c_str());
      handle_julia_exception();
      return ret;
    }

    bool isBadGradient(JuliaException &e) {
      return manual_invoke("libLSS._checkBadGradient", {e.getJuliaException()})
          .unbox<bool>();
    }

    void load_file(std::string const &name) {
      std::string cmd = "Base.include(Main, \"" + name + "\");";
      Console::instance().print<LOG_DEBUG>("Loading command " + cmd);
      (void)jl_eval_string(cmd.c_str());
      handle_julia_exception();
    }

    Object
    manual_invoke(std::string const &name, std::vector<Object> const &args) {
      Object func, ret, exc;

      func = jl_eval_string(name.c_str());
      handle_julia_exception();
      if (func.ptr() == 0) {
        throw JuliaNotFound(name);
      }

      {
        jl_value_t **j_args;
        JL_GC_PUSHARGS(j_args, args.size());
        for (size_t i = 0; i < args.size(); i++)
          j_args[i] = reinterpret_cast<jl_value_t *>(args[i].ptr());

        ret = jl_call((jl_function_t *)func.ptr(), j_args, args.size());
        JL_GC_POP();
      }

      exc = jl_exception_occurred();
      if (exc.ptr() != 0) {
        jl_exception_clear();
        throw JuliaException(std::move(exc));
      }

      return ret;
    }

    Object manual_invoke(
        Module *module, std::string const &name,
        std::vector<Object> const &args) {
      Object ret, func;

      func = jl_get_function((jl_module_t *)module, name.c_str());

      if (func.ptr() == 0) {
        throw JuliaNotFound(name);
      }

      {
        jl_value_t **j_args;
        JL_GC_PUSHARGS(j_args, args.size());

        for (size_t i = 0; i < args.size(); i++)
          j_args[i] = reinterpret_cast<jl_value_t *>(args[i].ptr());

        ret = jl_call((jl_function_t *)func.ptr(), j_args, args.size());

        JL_GC_POP();
      }

      jl_value_t *exc = jl_exception_occurred();
      if (exc != 0) {
        jl_exception_clear();
        throw JuliaException(Object(exc));
      }

      return ret;
    }

  } // namespace Julia
} // namespace LibLSS
