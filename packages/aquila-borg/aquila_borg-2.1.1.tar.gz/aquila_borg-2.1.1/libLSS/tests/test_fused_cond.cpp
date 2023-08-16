/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_fused_cond.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/format.hpp>
//#include "libLSS/mpi/generic_mpi.hpp"
//#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/tools/fused_cond.hpp"
#include "libLSS/tools/array_tools.hpp"
#include <boost/chrono.hpp>

using namespace std;
using namespace LibLSS;


class TimeContext {
protected:
    std::string code;
    boost::chrono::system_clock::time_point start_context;
public:
    TimeContext(const std::string& code_name) {
        start_context = boost::chrono::system_clock::now();
        code = code_name;
    }

    ~TimeContext() {
        boost::chrono::duration<double> ctx_time = boost::chrono::system_clock::now() - start_context;
        cout << boost::format("Done %s  in %s")  % code % ctx_time << endl;;
    }
};


int main()
{
  static constexpr int N = 8192;
  boost::multi_array<bool, 1> amask(boost::extents[N]);
  boost::multi_array<double, 1> A(boost::extents[N]);
  boost::multi_array<double, 1> B(boost::extents[N]);
  boost::multi_array<double, 1> C(boost::extents[N]);
  
  auto mask = b_fused_idx<bool, 1>([](int i)->bool { return (i%2)==0; }, boost::extents[N]);
  auto a0 =  b_fused_idx<double, 1>(
      [](int i)->int { return -2*i; },
      boost::extents[N]
    );
  auto b0 =  b_fused_idx<double, 1>(
      [](int i)->int { return 3*i; },
      boost::extents[N]
    );

  LibLSS::copy_array(A, a0);
  LibLSS::copy_array(B, b0);
  LibLSS::copy_array(amask, mask);


  auto c = b_cond_fused<double>(
    amask,
    A,
    B
  );


  {
     TimeContext t("Automatic");
     for (int j = 0; j < 1000000; j++)
     LibLSS::copy_array(C, c);
  }
  {
     TimeContext t("Hand written");
     for (int j = 0; j < 1000000; j++)
#pragma omp parallel for
     for (int i = 0; i < N; i++)
     {
       if (amask[i])
         C[i] = A[i];
       else
         C[i] = B[i];
     }
  }

  auto e = b_cond_fused<double>(mask, 
    a0, b0
  );
  {
     TimeContext t("Inline");
     for (int j = 0; j < 1000000; j++)
     LibLSS::copy_array(C, e);
  }
  
  auto f = b_cond_fused<double>(
    b_fused_idx<bool, 1>(
      [](int i)->bool { return (i%2)==0; }, boost::extents[N]
    ),
    b_fused_idx<double, 1>(
      [](int i)->int { return -2*i; },
      boost::extents[N]
    ), 
    b_fused_idx<double, 1>(
      [](int i)->int { return 3*i; },
      boost::extents[N]
    )
  );
  
  {
     TimeContext t("Inline 2");
     for (int j = 0; j < 1000000; j++)
       LibLSS::copy_array(C, f);
  }
/*
  for (int i = 0; i < 16; i++)
    std::cout  << C[i] << std::endl;

  for (int i = 0; i < 16; i++)
    std::cout  << e[i] << std::endl;
 */

  std::cout << reduce_sum<double>(e) << std::endl; 

  return 0;
}
