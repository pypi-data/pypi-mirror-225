#include <functional>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include <utility>

using namespace LibLSS;

namespace ph = std::placeholders;

template <typename T, std::size_t Dims, std::size_t... Is>
std::unique_ptr<FFTW_Manager<T, Dims>> makeMgr(
    MPI_Communication *comm, std::array<size_t, Dims> const &d,
    std::index_sequence<Is...>) {
  typedef FFTW_Manager<T, Dims> Mgr;
  return std::unique_ptr<Mgr>(new Mgr(d[Is]..., comm));
}

template <int Dims>
GridDensityLikelihoodBase<Dims>::GridDensityLikelihoodBase(
    MPI_Communication *comm_, GridSizes const &N_, GridLengths const &L_)
    : LikelihoodBase(), comm(comm_), N(N_), L(L_), volume(array::product(L_)) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  // FIXME: Is that the only preserved symmetry ?
  //        This one is enforced because average(s_field) == 0 at all time
  //        So the gradient of the likelihood may not create any mean or risk
  //        imbalance.
  // FIXME: This is only valid for 3D. It has to be generalized to N-d
  //special_cases.push_back(std::make_tuple(Index{0, 0, 0}, 0));
  special_cases.push_back(std::make_tuple(
      Index{ssize_t(N[0] / 2), ssize_t(N[1] / 2), ssize_t(N[2] / 2)}, 0));
  for (size_t i = 1; i < 7; i++) {
    auto j = Index{0, 0, 0};

    j[0] = (i & 1) * (N[0] / 2);
    j[1] = ((i & 2) >> 1) * (N[1] / 2);
    j[2] = ((i & 4) >> 2) * (N[2] / 2);
    special_cases.push_back(std::make_tuple(j, 0.5));
  }

  mgr = makeMgr<double, Dims>(comm_, N_, std::make_index_sequence<Dims>());
  auto tmp_real_field = mgr->allocate_array();
  auto tmp_complex_field = mgr->allocate_complex_array();
  analysis_plan = mgr->create_r2c_plan(
      tmp_real_field.get_array().data(), tmp_complex_field.get_array().data());
}

template <int Dims>
GridDensityLikelihoodBase<Dims>::~GridDensityLikelihoodBase() {}

template <>
void GridDensityLikelihoodBase<3>::computeFourierSpace_GradientPsi(
    ArrayRef &real_gradient, CArrayRef &grad_array, bool accumulate,
    double scaling) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  double normalizer =
      1 /
      volume; // Normalization is like synthesis here, we consider the transpose synthesis
  auto tmp_complex_field_p = mgr->allocate_complex_array();
  auto plane_set = std::array<size_t, 2>{0, N[2] / 2};
  using boost::multi_array_types::index_range;

  // BEWARE: real_gradient is destroyed!
  mgr->execute_r2c(
      analysis_plan, real_gradient.data(),
      tmp_complex_field_p.get_array().data());

  auto &c_field = tmp_complex_field_p.get_array();
  auto e = fwrap(c_field) * (2 * normalizer); // Factor 2 owed to hermiticity
  auto output = fwrap(grad_array);
  size_t startN0 = mgr->startN0;
  size_t endN0 = mgr->startN0 + mgr->localN0;

  // FIXME: Why do we do this already ?
  ctx.print(" Handle special cases");
  for (auto &h : special_cases) {
    ssize_t i0 = std::get<0>(h)[0];
    if (i0 >= startN0 && i0 < endN0)
      c_field(std::get<0>(h)) *= std::get<1>(h);
  }

  for (auto p : plane_set) {
    size_t i0_start = std::max(startN0, N[0] / 2 + 1);
    size_t i0_end = std::min(endN0, N[0]);
    ctx.print(
        "Fix plane " + std::to_string(p) + " " + std::to_string(i0_start) +
        " => " + std::to_string(i0_end));
    if (i0_start < i0_end)
      fwrap(c_field[boost::indices[index_range(i0_start, i0_end)][index_range()]
                                  [p]]) = 0;
    for (auto q : {size_t(0), N[0] / 2}) {
      ctx.print("Fix plane (2) " + std::to_string(q));
      if (mgr->on_core(q)) {
        fwrap(c_field[boost::indices[q][index_range(N[1] / 2 + 1, N[1])][p]]) =
            0;
      }
    }
  }

  if (mgr->on_core(0))
    c_field[0][0][0] = 0;

  if (accumulate)
    output = output + scaling * e;
  else
    output = e * scaling;
}

namespace LibLSS {
  template class GridDensityLikelihoodBase<3>;
}
