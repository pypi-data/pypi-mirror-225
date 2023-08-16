/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_tuple.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/tools/tuple_helper.hpp"


int main()
{
    auto t = std::make_tuple(0, 1, 2, 3);
    
    auto u0 = LibLSS::last_of_tuple<0>(t);
    auto u = LibLSS::last_of_tuple<1>(t);
    auto u2 = LibLSS::last_of_tuple<2>(t);
    auto u3 = LibLSS::last_of_tuple<3>(t);
    
    int a, b , c,d;
    std::tie(a,b,c,d) = u0;      
    std::cout << a << " " << b << " " << c << " " << d  << std::endl;
    std::tie(a,b,c) = u;      
    std::cout << a << " " << b << " " << c << std::endl;
    std::tie(b,c) = u2;      
    std::cout << b << " " << c << std::endl;
    std::tie(c) = u3;      
    std::cout << c << std::endl;
    return 0;
}
