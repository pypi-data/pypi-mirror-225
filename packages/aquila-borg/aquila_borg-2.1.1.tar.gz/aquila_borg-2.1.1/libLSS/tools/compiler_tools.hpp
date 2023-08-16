#pragma once

#define DISABLE_WARN_DIV_BY_ZERO \
_Pragma("GCC diagnostic push") \
_Pragma("GCC diagnostic ignored \"-Wdiv-by-zero\"")

#define ENABLE_WARN_DIV_BY_ZERO \
_Pragma("GCC diagnostic pop")

