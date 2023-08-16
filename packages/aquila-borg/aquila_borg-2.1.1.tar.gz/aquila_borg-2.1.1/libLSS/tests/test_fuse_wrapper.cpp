/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_fuse_wrapper.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/timer/timer.hpp>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/static_init.hpp"

double fun() {
  static int i = 0;
  i++;
  return i;
}

using namespace boost::timer;

int main() {
  LibLSS::StaticInit::execute();
  using boost::extents;
  using boost::multi_array;
  using LibLSS::_p1;
  using LibLSS::_p2;
  using LibLSS::b_fused_idx;
  using LibLSS::b_va_fused;
  using LibLSS::fwrap;

  size_t N = 256;
  multi_array<double, 3> A(extents[N][N][N]);
  multi_array<double, 3> B(extents[N][N][N]);

  auto fA = fwrap(A);
  auto fC = fwrap(fA.fautowrap(fun));
  auto fD = LibLSS::b_fused<double>(A, 2.0 * M_PI * _p1);

  // Initialize A with some linear space.
  fA = b_fused_idx<double, 3>([N](int i, int j, int k) -> double {
    return double(i) / N + double(j) / N + double(k) / N;
  });

  std::cout << "Reference: " << LibLSS::reduce_sum<double>(A) << std::endl;

  {
    double r = 0;
    for (int i = 0; i < N; i++)
      for (int j = 0; j < N; j++)
        for (int k = 0; k < N; k++)
          r += A[i][j][k];
    std::cout << "Manual: " << r << std::endl;
  }

  {
    cpu_timer timer;
    double r = 0;
    for (int i = 0; i < 10; i++)
      r += ((fA * 2. + 5.) / 7).sum();
    std::cout << "10 composite multiply, sum and reduce:" << timer.format()
              << " " << r << std::endl;
  }
  // Create a lazy expression.
  auto fB = std::cos(fA * (2 * M_PI)); //std::cos(fA*2*M_PI);
  // WORKS PARTIALLY: shapeness must be better computed
  auto fB2 = std::cos((2 * M_PI) * fA); //std::cos(fA*2*M_PI);

  std::cout << fwrap(fD).sum() << std::endl;

  // This does a full collapse of the expression, including the squaring

  {
    cpu_timer timer;
    std::cout << (LibLSS::ipow<2>(fB)).sum() / LibLSS::ipow<3>(N) << std::endl;
    std::cout << "Composite multiply, cos, square and reduce:" << timer.format()
              << std::endl;
    std::cout << (LibLSS::ipow<2>(fB2)).sum() / LibLSS::ipow<3>(N) << std::endl;
  }

  {
    cpu_timer timer;
    std::cout << std::abs(fB).sum() / LibLSS::ipow<3>(N) << std::endl;
    std::cout << "Composite multiply, cos, abs and reduce:" << timer.format()
              << std::endl;
  }

  //std::cout << fB->shape()[0] << std::endl;

  // Assign the cos part
  auto fE = fwrap(B);
  {
    cpu_timer timer;
    fE = fB;
    std::cout << "Composite multiply, cos and assign:" << timer.format()
              << std::endl;
  }

  {
    cpu_timer timer;
    std::cout << (fE * fE).sum() << std::endl;
    std::cout << "Composite square and reduce:" << timer.format() << std::endl;
  }

  std::cout << std::pow(std::abs(fE), 2.5).sum()
            << std::endl; ////std::pow(std::abs(fE), 2.5).sum() << std::endl;
  std::cout << (std::abs(fE)).min()
            << std::endl; ////std::pow(std::abs(fE), 2.5).sum() << std::endl;
  std::cout << (std::abs(fE)).max()
            << std::endl; ////std::pow(std::abs(fE), 2.5).sum() << std::endl;
  double r = std::numeric_limits<double>::infinity();
  for (size_t i = 0; i < N; i++)
    for (size_t j = 0; j < N; j++)
      for (size_t k = 0; k < N; k++)
        r = std::min(r, std::abs((*fE)[i][j][k]));

  std::cout << r << std::endl;

  fwrap(B) = fwrap(A);


  fwrap(B) = -fwrap(A);

  std::cout << fwrap(B).sum() << " " << fwrap(A).sum() << std::endl;

  std::cout << fwrap(B).no_parallel().sum() << std::endl;

  multi_array<std::complex<double>, 3> c_B(extents[N][N][N]);
   auto f_c_B = fwrap(c_B);
double x = std::real(f_c_B).sum();
   std::cout << x << std::endl;


  auto c_a = LibLSS::make_complex(fwrap(A), fwrap(B));

  //double sB;
  //auto scalar_A = fwrap(1.0);
  //auto scalar_B = fwrap(sB);

  //scalar_B = scalar_A + 2;

  return 0; //fA.sum();
}
