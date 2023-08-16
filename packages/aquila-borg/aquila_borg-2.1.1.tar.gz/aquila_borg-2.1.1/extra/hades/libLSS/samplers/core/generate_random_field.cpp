#include "libLSS/samplers/core/generate_random_field.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

using namespace LibLSS;

void LibLSS::generateRandomField(MPI_Communication *comm, MarkovState &state) {
  auto &s_hat = *state.get<CArrayType>("s_hat_field")->array;
  auto &s = *state.get<ArrayType>("s_field")->array;
  auto &rgen = state.get<RandomGen>("random_generator")->get();
  std::array<long, 3> N;
  std::array<double, 3> L;

  state.getScalarArray<long, 3>("N", N);
  state.getScalarArray<double, 3>("L", L);

  FFTW_Manager<double, 3> mgr(N[0], N[1], N[2], comm);
  double volume = array::product(L);
  double volNorm = volume / array::product(N);
  double invN3 = 1.0 / array::product(N);
  double sqrt_invN3 = std::sqrt(invN3);

  //  auto s_hat_p = base_mgr->allocate_complex_array();
  //  auto &s_hat = s_hat_p.get_array();
  auto s_hat_w = fwrap(s_hat);
  auto s_w = fwrap(s);
  auto tmp_real_field_p = mgr.allocate_array();
  auto &tmp_real_field = tmp_real_field_p.get_array();
  auto tmp_complex_field_p = mgr.allocate_complex_array();
  auto &tmp_complex_field = tmp_complex_field_p.get_array();

  auto synthesis_plan =
      mgr.create_c2r_plan(tmp_complex_field.data(), tmp_real_field.data());
  auto analysis_plan =
      mgr.create_r2c_plan(tmp_real_field.data(), tmp_complex_field.data());

  fwrap(tmp_real_field) = rgen.gaussian(fwrap(b_fused_idx<double, 3>(
      [](size_t, size_t, size_t) -> double { return 1; },
      mgr.extents_real_strict())));

  mgr.execute_r2c(
      analysis_plan, tmp_real_field.data(), tmp_complex_field.data());

  // Convolve with sqrt(P(k))
  s_hat_w = fwrap(tmp_complex_field) *
            b_fused_idx<double, 3>(
                [sqrt_invN3](size_t i, size_t j, size_t k) -> double {
                  return sqrt_invN3;
                });
  {
    // Get back s_field now
    fwrap(tmp_complex_field) = s_hat_w * (1 / volume);
    mgr.execute_c2r(
        synthesis_plan, tmp_complex_field.data(), tmp_real_field.data());
  }
  fwrap(s[mgr.strict_range()]) = fwrap(tmp_real_field[mgr.strict_range()]);
}
