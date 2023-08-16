/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/cpu/feature_check_gnuc.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>

namespace LibLSS {
  static inline bool check_compatibility(std::string &features) {
    __builtin_cpu_init();
    features = "";
#ifdef __MMX__
    if (!__builtin_cpu_supports("mmx"))
      return false;
    features += "MMX ";
#else
    if (__builtin_cpu_supports("mmx"))
      features += "[!MMX] ";
#endif
#ifdef __AVX__
    if (!__builtin_cpu_supports("avx"))
      return false;
    features += "AVX ";
#else
    if (__builtin_cpu_supports("avx"))
      features += "[!AVX] ";
#endif
#ifdef __AVX2__
    if (!__builtin_cpu_supports("avx2"))
      return false;
    features += "AVX2 ";
#else
    if (__builtin_cpu_supports("avx2"))
	    features += "[!AVX2] ";
#endif
#ifdef __AVX512F__
    if (!__builtin_cpu_supports("avx512f"))
      return false;
    features += "AVX512F ";
#else
    if (__builtin_cpu_supports("avx512f"))
       features += "[!AVX512F] ";
#endif
#ifdef __SSE__
    if (!__builtin_cpu_supports("sse"))
      return false;
    features += "SSE ";
#else
    if (__builtin_cpu_supports("sse"))
      features += "[!SSE] ";
#endif
#ifdef __SSE2__
    if (!__builtin_cpu_supports("sse2"))
      return false;
    features += "SSE2 ";
#else
    if (__builtin_cpu_supports("sse2"))
      features += "[!SSE2] ";
#endif
#ifdef __SSE3__
    if (!__builtin_cpu_supports("sse3"))
      return false;
    features += "SSE3 ";
#else
    if (__builtin_cpu_supports("sse3"))
      features += "[!SSE3] ";
#endif
#ifdef __SSE4_1__
    if (!__builtin_cpu_supports("sse4.1"))
      return false;
    features += "SSE4.1 ";
#else
    if (__builtin_cpu_supports("sse4.1"))
      features += "[!SSE4.1] ";
#endif
#ifdef __SSE4_2__
    if (!__builtin_cpu_supports("sse4.2"))
      return false;
    features += "SSE4.2 ";
#else
    if (__builtin_cpu_supports("sse4.2"))
      features += "[!SSE4.2] ";
#endif
    return true;
  }
} // namespace LibLSS
