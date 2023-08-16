/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_stl_container.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <vector>
#include <set>
#include "libLSS/tools/is_stl_container.hpp"

using namespace LibLSS;

int main()
{
  //std::cout << is_stl_container_like<std::vector<double>>::value << std::endl;
  std::cout << is_stl_container_like<std::set<double>>::value << std::endl;
  return 0;
}
