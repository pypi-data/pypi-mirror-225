/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_fused_array.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/format.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_masked_assign.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/static_init.hpp"
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

template<typename A>
void printer(const A& a)
{
    for (int i = 0; i < a.num_elements(); i++)
        cout << a[i] << endl;
}

struct MulOp {
    int operator()(const int& a) const {
        return 2*a;
    }
};

template<typename T, typename T2, typename Operation>
void hand_coded(T& a, const T2& b, Operation op)
{
size_t e1 = a.shape()[0], e2 = a.shape()[1], e3 = a.shape()[2];
#pragma omp parallel for collapse(3)
  for (size_t i = 0; i < e1; i++) {
    for (size_t j = 0; j < e2; j++)
    for (size_t k = 0; k < e3; k++)
    {
      a[i][j][k] = op(b[i][j][k]);
    }
  }
}

template<typename T, typename T2>
void hand_constant(T& a, T2 value)
{
#pragma omp parallel for
  for (size_t i = 0; i < a.shape()[0]; i++) {
    for (size_t j = 0; j < a.shape()[1]; j++)
    for (size_t k = 0; k < a.shape()[2]; k++) {
      a[i][j][k] = value;
    }
  }
}

double op0(int a, int b, int c)
{
    return a + 10*b + 100*c;
}

int main(int argc, char **argv)
{
    setupMPI(argc, argv);
    StaticInit::execute();
    using boost::lambda::_1;
    using boost::lambda::_2;
    using boost::lambda::constant;
    namespace Larray = ::LibLSS::array;

    const std::size_t N = 128;
    typedef boost::multi_array<double,3> Array;
    Array::index_gen indices;
    typedef boost::multi_array<double,3> DArray;
    Array a(boost::extents[N][N][N]),
        b(boost::extents[N][N][N]),
        c(boost::extents[N][N][N]);
    DArray d(boost::extents[N][N][N]);

    for (size_t i = 0; i < a.num_elements(); i++) {
       a.data()[i] = i;
       b.data()[i] = i*i;
    }
#if 0
    {
        TimeContext ctx("Constant");
        for (int j = 0; j < 100; j++)
            copy_array(c, b_fused<int,3>(constant(2)));
    }

    {
        TimeContext ctx("Hand coded Constant");
        for (int j = 0; j < 100; j++)
            hand_constant(c, 2);
    }


    {
        TimeContext ctx("MulOp");
       for (int j = 0; j < 10000; j++)
            copy_array(c, b_fused<int>(b,MulOp()));
    }
    #endif
    {
        TimeContext ctx("Lambda");
        for (int j = 0; j < 1000; j++)
            copy_array(c, b_fused<int>(b,2*_p1));
    }
    {
        TimeContext ctx("Lambda va");
        for (int j = 0; j < 1000; j++)
            copy_array(c, b_va_fused<int>(2*_p1, b));
    }
    {
        TimeContext ctx("Lambda va on sliced array");
        auto slicer = indices[Array::index_range(1,N/2)][Array::index_range(1,N/2)][Array::index_range(1,N/2)];
        for (int j = 0; j < 1000; j++) {
            auto va = b_va_fused<int>(2*_1, b[slicer]);
            copy_array_rv(c[slicer], va);
        }
    }
    {
        TimeContext ctx("Float Lambda");
        for (int j = 0; j < 1000; j++)
            copy_array(d, b_va_fused<double>(2*_p1,b), true);
    }

    Larray::fill(b, 103);
    for (size_t i = 0; i < b.num_elements(); i++)
      if (b.data()[i] != 103) {
        cout << "At element " << i << " b = " << b.data()[i]  << endl;
        abort();
      }

    {
        TimeContext ctx("hand coded lambda");
        for (int j = 0; j < 1000; j++)
            hand_coded(c, b, 2*_p1);
    }
    Larray::copyArray3d(a, b);
    Larray::scaleArray3d(a, 2);
    for (size_t i = 0; i < a.num_elements(); i++)
      if (a.data()[i] != c.data()[i]) {
        cout << "At element " << i << " a = " << a.data()[i] << " c = " << c.data()[i]  << endl;
        abort();
      }

    {
        Array d(boost::extents[2][N][N]);
        copy_array_rv(d[0], b[0]);
        copy_array_rv(b[0], d[0]);
        copy_array(b, b_fused_idx<double, 3>(op0));
        for (size_t i = 0; i < N; i++)
            for (size_t j = 0; j < N; j++)
                for (size_t k = 0; k < N; k++)
                    if (size_t(b[i][j][k]) != (i+10*j+100*k)) {
                        cout << "Problem at (" << i << "," << j << "," << k << ")" << endl;
                        cout << "Value in b is " << b[i][j][k] << endl;
                        abort();
                    }

        copy_array_rv(
            d[indices[Array::index_range()][Array::index_range(1,3)][Array::index_range(1,3)]],
            b[indices[Array::index_range(1,3)][Array::index_range(1,3)][Array::index_range(1,3)]]
        );
        for (long i = 0; i < 2; i++) {
            for (long j = 1; j < 3; j++) {
                for (long k = 1; k < 3; k++) {
                    if (d[i][j][k] != (i+1) + 10*j + 100*k) {
                        cout << "Problem(2) at " << i << "," << j << "," << k << endl;
                        abort();
                    }
                }
            }

        }
    }


    {
      copy_array(b, b_fused_idx<int, 3>([N](int i, int j, int k)->double {
        return 4*i/N;
      }));
      copy_array_masked(a, b, b_va_fused<int>(2*_p1, b), b_va_fused<bool>(_p1 > 2, b));
      std::cout << reduce_sum<int>(a) << " " << reduce_sum<int>(b) << std::endl;

      double s= 0;
      for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
          for (int k = 0; k < N; k++)
            if (b[i][j][k] > 2)
              s += b[i][j][k];
            else
              s += 2*b[i][j][k];

      std::cout << s << std::endl;
    }

    {
      long s = 0;
      for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
          for (int k = 0; k < N; k++)
            if (b[i][j][k] > 2)  s += a[i][j][k];
      std::cout << s << " " << reduce_sum<int>(a, b_va_fused<bool>(_p1 > 2, b)) << std::endl;
    }


    return 0;
}
