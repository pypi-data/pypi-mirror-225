/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tools/hermiticity_fixup.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2019 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <set>
#include <array>
#include <algorithm>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"

static constexpr bool ULTRA_VERBOSE = true;

using namespace LibLSS;

template <typename T, size_t Nd>
Hermiticity_fixer<T, Nd>::Hermiticity_fixer(Mgr_p mgr_)
    : comm(mgr_->getComm()), mgr(mgr_) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  std::set<ssize_t> wanted_planes, owned_planes;

  std::array<ssize_t, Nd - 1> dims;
  std::copy(mgr->N.begin() + 1, mgr->N.end(), dims.begin());
  dims[Nd - 2] = dims[Nd - 2] / 2 + 1;

  {
    size_t i_min = mgr->startN0;
    size_t i_max = mgr->startN0 + mgr->localN0;
    ctx.format("own: i_min=%d, i_max=%d", i_min, i_max);
    for (size_t i = i_min; i < i_max; i++) {
      owned_planes.insert(i);
    }
  }

  {
    size_t i_min = std::max(size_t(mgr->startN0), mgr->N[0] / 2 + 1);
    size_t i_max = mgr->startN0 + mgr->localN0;
    ctx.format("want: i_min=%d, i_max=%d", i_min, i_max);
    for (size_t i = i_min; i < i_max; i++) {
      size_t conj_plane = mgr->N[0] - i;
      if (!mgr->on_core(conj_plane)) {
        wanted_planes.insert(conj_plane);
      }
    }
  }

  ghosts.setup(comm, wanted_planes, owned_planes, dims, mgr->N[0]);
}

template <size_t Nd>
static ssize_t encode_index(
    std::array<ssize_t, Nd> const &index, std::array<size_t, Nd> const &N) {
  ssize_t ret = 0;

  for (size_t i = 0; i < Nd; i++)
    ret = ret * N[i] + index[i];
  return ret;
}

template <size_t Nd>
static void decode_index(
    ssize_t coded_index, std::array<ssize_t, Nd> &decoded,
    std::array<size_t, Nd> const &N) {
  for (size_t i = Nd; i > 0; i--) {
    size_t j = i - 1;
    ssize_t tmp = coded_index / N[j];
    ssize_t tmp2 = coded_index - tmp * N[j];
    decoded[j] = tmp2;
    coded_index = tmp;
  }
}

template <size_t Nd>
static void find_conjugate(
    std::array<ssize_t, Nd> &reversed_index,
    std::array<ssize_t, Nd> const &index, std::array<size_t, Nd> const &N) {
  for (size_t i = 0; i < Nd; i++) {
    if (index[i] == 0)
      reversed_index[i] = 0;
    else
      reversed_index[i] = N[i] - index[i];
  }
}

template <size_t Nd>
static bool
has_nyquist(std::array<ssize_t, Nd> &index, std::array<size_t, Nd> const &N) {
  for (size_t i = 0; i < Nd; i++) {
    if (index[i] == N[i] / 2 || index[i] == 0)
      return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
//  Forward hermiticity fixer

template <
    size_t rank, typename Mgr, typename Ghosts, typename CArray,
    size_t Dim = CArray::dimensionality>
static typename std::enable_if<Dim == 1, void>::type
fix_plane(Mgr &mgr, Ghosts &&ghosts, CArray &&a, size_t *N) {
  std::array<size_t, 1> current_N = {N[0]};
  size_t Ntot = N[0];
  size_t N0_HC = N[0] / 2;

#pragma omp parallel for
  for (size_t i = 1; i < N0_HC; i++) {
    size_t current, conj_current;
    current = i;
    conj_current = current_N[0] - i;
    a[conj_current] = std::conj(a[current]);
  }

  for (size_t i : {size_t(0), N0_HC}) {
    a[i].imag(0);
  }
}

template <bool full, size_t Nd, typename AccessDirect, typename AccessConj>
static void direct_fix(
    std::array<size_t, Nd> const &current_N, AccessDirect &&direct_access,
    AccessConj &&conj_access) {
  size_t Ntot =
      full ? array::product(current_N) / 2 : array::product(current_N);
#pragma omp parallel for
  for (size_t i = 0; i < Ntot; i++) {
    std::array<ssize_t, Nd> current, conj_current;
    decode_index(i, current, current_N);
    //if (!has_nyquist(current, current_N))
    {
      find_conjugate(conj_current, current, current_N);
      direct_access(current) = std::conj(conj_access(conj_current));
    }
  }
}

template <
    size_t rank, typename Mgr, typename Ghosts, typename CArray,
    size_t Dim = CArray::dimensionality>
static typename std::enable_if<Dim != 1, void>::type
fix_plane(Mgr &mgr, Ghosts &&ghosts, CArray &&a, size_t *N) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  std::array<size_t, Dim> current_N;
  size_t Ntot = array::product(current_N);
  size_t N0_HC = N[0] / 2;

  std::copy(N, N + Dim, current_N.begin());

  if (rank != 0) {
    auto accessor = [&a](auto &&x) -> auto & { return a(x); };
    direct_fix<true>(current_N, accessor, accessor);
  } else if (mgr.startN0 + mgr.localN0 > N0_HC) {
    size_t i_min = std::max(N0_HC, size_t(mgr.startN0));
    size_t i_max = mgr.startN0 + mgr.localN0;
    std::array<size_t, Dim - 1> sub_N;
    std::copy(current_N.begin() + 1, current_N.end(), sub_N.begin());

    ctx.format("i_min = %d, i_max = %d", i_min, i_max);

    for (size_t i0 = i_min; i0 < i_max; i0++) {
      size_t i0_conj = N[0] - i0;
      auto this_plane = a[i0];
      auto direct_access = [&this_plane](auto &&x) -> auto & {
        return this_plane(x);
      };

      if (mgr.on_core(i0_conj)) {
        auto conj_plane = a[i0_conj];
        auto conj_direct_access = [&conj_plane](auto &&x) -> auto & {
          return conj_plane(x);
        };
        direct_fix<false>(sub_N, direct_access, conj_direct_access);
      } else {
        ctx.format(" Fix plane %d using i0_conj=%d from remote", i0, i0_conj);
        auto conj_plane = ghosts(i0_conj);
        direct_fix<false>(
            sub_N, direct_access, [&conj_plane](auto &&x) -> auto & {
              return conj_plane(x);
            });
      }
    }
  }

  if (rank != 0 || mgr.on_core(0))
    fix_plane<rank + 1>(mgr, ghosts, a[0], N + 1);
  if (rank != 0 || mgr.on_core(N0_HC))
    fix_plane<rank + 1>(mgr, ghosts, a[N0_HC], N + 1);
}

template <typename T, size_t Nd>
void Hermiticity_fixer<T, Nd>::forward(CArrayRef &a) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Grab the planes that is required to build the Nyquist correction
  ghosts.synchronize(a);

  std::array<size_t, Nd> N = mgr->N;
  size_t N_HC = mgr->N_HC;

  auto idx = array::make_star_indices<Nd - 1>(boost::indices);
  auto idx_g = array::make_star_indices<Nd - 2>(boost::indices);
  fix_plane<0>(
      *mgr,
      [this, idx_g, N_HC](ssize_t plane) {
        return array::slice_array(ghosts.getPlane(plane), idx_g[0]);
      },
      array::slice_array(a, idx[0]), N.data());
  fix_plane<0>(
      *mgr,
      [this, idx_g, N_HC](ssize_t plane) {
        return array::slice_array(ghosts.getPlane(plane), idx_g[N_HC - 1]);
      },
      array::slice_array(a, idx[N_HC - 1]), N.data());

  ghosts.release();
}

// ---------------------------------------------------------------------------
// Adjoint gradient of hermiticity fixer

template <
    size_t rank, typename Mgr, typename CArray,
    size_t Dim = CArray::dimensionality>
static typename std::enable_if<Dim == 1, void>::type
adjoint_fix_plane(Mgr &mgr, CArray &&a, size_t *N) {
  std::array<size_t, 1> current_N = {N[0]};
  size_t Ntot = N[0];
  size_t N0_HC = N[0] / 2;

#pragma omp parallel for
  for (size_t i = 1; i < N0_HC; i++) {
    size_t current, conj_current;
    current = i;
    conj_current = current_N[0] - i;
    a[conj_current] = 0;
  }

  for (size_t i : {size_t(0), N0_HC}) {
    auto &a0 = a[i];
    a0.real(a0.real() * 0.5);
    a0.imag(0);
  }
}

template <bool full, size_t Nd, typename AccessDirect>
static void adjoint_direct_fix(
    std::array<size_t, Nd> const &current_N, AccessDirect &&direct_access) {
  size_t const Ntot =
      full ? array::product(current_N) / 2 : array::product(current_N);
#pragma omp parallel for
  for (size_t i = 0; i < Ntot; i++) {
    std::array<ssize_t, Nd> current, conj_current;
    decode_index(i, current, current_N);
    //if (!has_nyquist(current, current_N))
    {
      find_conjugate(conj_current, current, current_N);
      direct_access(conj_current) = 0;
    }
  }
}

template <
    size_t rank, typename Mgr, typename CArray,
    size_t Dim = CArray::dimensionality>
static typename std::enable_if<Dim != 1, void>::type
adjoint_fix_plane(Mgr &mgr, CArray &&a, size_t *N) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  std::array<size_t, Dim> current_N;
  size_t Ntot = array::product(current_N);
  size_t N0_HC = N[0] / 2;

  std::copy(N, N + Dim, current_N.begin());

  if (rank != 0) {
    auto accessor = [&a](auto &&x) -> auto & { return a(x); };
    adjoint_direct_fix<true>(current_N, accessor);
  } else if (mgr.startN0 + mgr.localN0 > N0_HC) {
    size_t i_min = std::max(N0_HC, size_t(mgr.startN0));
    size_t i_max = mgr.startN0 + mgr.localN0;
    std::array<size_t, Dim - 1> sub_N;
    std::copy(current_N.begin() + 1, current_N.end(), sub_N.begin());

    for (size_t i0 = i_min; i0 < i_max; i0++) {
      auto this_plane = a[i0];
      auto direct_access = [&this_plane](auto &&x) -> auto & {
        return this_plane(x);
      };

      adjoint_direct_fix<false>(sub_N, direct_access);
    }
  }

  if (rank != 0 || mgr.on_core(0))
    adjoint_fix_plane<rank + 1>(mgr, a[0], N + 1);
  if (rank != 0 || mgr.on_core(N0_HC))
    adjoint_fix_plane<rank + 1>(mgr, a[N0_HC], N + 1);
}

template <typename T, size_t Nd>
void Hermiticity_fixer<T, Nd>::adjoint(CArrayRef &a) {
  // Grab the planes that is required to build the Nyquist correction

  std::array<size_t, Nd> N = mgr->N;
  size_t N_HC = mgr->N_HC;

  fwrap(a) = fwrap(a) * 2.0;
//  if (mgr->on_core(0))
//    a[0][0][0] *= 0.5;

  auto idx = array::make_star_indices<Nd - 1>(boost::indices);
  adjoint_fix_plane<0>(*mgr, array::slice_array(a, idx[0]), N.data());
  adjoint_fix_plane<0>(*mgr, array::slice_array(a, idx[N_HC - 1]), N.data());
}

//template struct LibLSS::Hermiticity_fixer<double, 1>;
//template struct LibLSS::Hermiticity_fixer<double, 2>;
template struct LibLSS::Hermiticity_fixer<double, 3>;

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2019
