/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_uninit.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/static_init.hpp"

using std::cout;
using std::endl;
using namespace LibLSS;

#pragma GCC push_options
#pragma GCC optimize ("O0")
template<typename T>
void f(T& a)
{
    a[0][0] = 1;
}
#pragma GCC pop_options        

#pragma GCC push_options
#pragma GCC optimize ("O0")
template<typename T>
void g(T& a)
{
    a[0] = 1;
}
#pragma GCC pop_options        


int main()
{
    typedef boost::multi_array_ref<double, 2> Array;
    StaticInit::execute();
    
    int iteration = 1000;
    {
        ConsoleContext<LOG_STD> ctx("multi_array uninit ");
    
        for (int j = 0; j < iteration; j++) {
            UninitializedArray<Array> a0(boost::extents[128][128*128]);
            Array& a = a0.get_array();
            for (int i = 0; i < a.shape()[0]; i++) {
                for (int j = 0; j < a.shape()[1]; j++) {
                    a[i][j] = i;
                }
            }
            
            f(a);
        }
    }

    {
        boost::multi_array<double, 2> a(boost::extents[128][128*128]);
        ConsoleContext<LOG_STD> ctx("multi_array prealloc");
        
        for (int j = 0; j < iteration; j++) {
            for (int i = 0; i < a.shape()[0]; i++) {
                for (int j = 0; j < a.shape()[1]; j++) {
                    a[i][j] = i;
                }
            }
            
            f(a);
        }
    }
    
    
    {
        ConsoleContext<LOG_STD> ctx("multi_array init");
        
        for (int j = 0; j < iteration; j++) {
            boost::multi_array<double, 2> a(boost::extents[128][128*128]);
            for (int i = 0; i < a.shape()[0]; i++) {
                for (int j = 0; j < a.shape()[1]; j++) {
                    a[i][j] = i;
                }
            }
            f(a);
        }

    }

    {
        ConsoleContext<LOG_STD> ctx("native uninit");        
        
        for (int j = 0; j < iteration; j++) {
            double *a = new double[128*128*128];
            for (int i = 0; i < 128; i++) {
                for (int j = 0; j < 128*128; j++) {
                    a[i*128*128+j] = i;
                }
            }
            g(a);
            delete[] a;
        }

    }
    
    
    return 0;
}