/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_array.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/config.hpp>
#ifdef BOOST_NO_CXX11_AUTO_DECLARATIONS
#error This test needs C++11 features to compile.
#else

#include <boost/multi_array.hpp>
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/fused_array.hpp"
#include <boost/lambda/lambda.hpp>
#include <boost/bind/bind.hpp>

using boost::placeholders::_1;

using namespace LibLSS;


static
void aSwapper(boost::multi_array<double,1>& a, long i, long j)
{
    std::swap(a[i], a[j]);
}

int main(int argc, char **argv)
{
    using boost::extents;
    
    setupMPI(argc, argv);
    LibLSS::StaticInit::execute();
    
    boost::multi_array<double,1> a(extents[10]);
    boost::multi_array<long,1> idx(extents[10]);
    
    copy_array(a, b_fused_idx<double, 1>(10.0-boost::lambda::_1));
    copy_array(idx, b_fused_idx<long, 1>(9-boost::lambda::_1));

    for (int i = 0; i < 100; i++) {
      int j = drand48()*a.shape()[0];
      int k = drand48()*a.shape()[0];
      std::swap(a[j],a[k]);
      std::swap(idx[j],idx[k]);
    }

    std::cout << "Before sorting" << std::endl;
    for (auto r : a) {    
        std::cout << r << std::endl;
    }

    
    array::reorder(idx, boost::bind(aSwapper, boost::ref(a), boost::placeholders::_1, boost::placeholders::_2));
    
    std::cout << "After sorting" << std::endl;
    for (auto r : a) {    
        std::cout << r << std::endl;
    }

    doneMPI();
    
    return 0;
}
#endif
