/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/haar.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/haar.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"

using namespace LibLSS;

void ForwardHaar::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  delta_init.needDestroyInput();

  hold_input = std::move(delta_init);
}

template <typename ArrayIn, typename ArrayOut>
void ihaar_1d(ArrayIn &&in, ArrayOut &&out) {
  int N = in.shape()[0];
  int k = 1;

  while (2 * k <= N) {
    for (int i = 0; i < k; i++) {
      double a = in[i], b = in[i + k];
      out[2 * i] = (a + b) * M_SQRT1_2;
      out[2 * i + 1] = (a - b) * M_SQRT1_2;
    }

    // The last one does not need anything
    k = k * 2;
    if (k < N)
      for (int i = 0; i < (2 * k); i++)
        in[i] = out[i];
  }
}

template <typename ArrayIn, typename ArrayOut>
void haar_1d(ArrayIn &&in, ArrayOut &&out) {
  int N = in.shape()[0];
  int k = N;

  while (k > 1) {
    k = k / 2;
    for (int i = 0; i < k; i++) {
      double a = in[2 * i], b = in[2 * i + 1];
      out[i] = (a + b) * M_SQRT1_2;
      out[i + k] = (a - b) * M_SQRT1_2;
    }

    // The last one does not need anything
    if (k > 1)
      for (int i = 0; i < (2 * k); i++)
        in[i] = out[i];
  }
}

template <typename ArrayIn, typename ArrayOut>
void haar_3d(ArrayIn &&in, ArrayOut &&out) {
  typedef decltype(out) Array;
  typedef boost::multi_array_types::index_range range;
  using boost::indices;
  size_t N0 = in.shape()[0], N1 = in.shape()[1], N2 = in.shape()[2];

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N1; j++) {
    for (int k = 0; k < N2; k++) {
      auto sub_idx = indices[range()][j][k];
      haar_1d(in[sub_idx], out[sub_idx]);
    }
  }

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N0; j++) {
    for (int k = 0; k < N2; k++) {
      auto sub_idx = indices[j][range()][k];
      // THIS IS NOT A TYPO! out and in are reversed here.
      haar_1d(out[sub_idx], in[sub_idx]);
    }
  }

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N0; j++) {
    for (int k = 0; k < N1; k++) {
      auto sub_idx = indices[j][k][range()];
      haar_1d(in[sub_idx], out[sub_idx]);
    }
  }
}

template <typename ArrayIn, typename ArrayOut>
void ihaar_3d(ArrayIn &&in, ArrayOut &&out) {
  typedef decltype(out) Array;
  typedef boost::multi_array_types::index_range range;
  using boost::indices;
  size_t N0 = in.shape()[0], N1 = in.shape()[1], N2 = in.shape()[2];

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N0; j++) {
    for (int k = 0; k < N1; k++) {
      auto sub_idx = indices[j][k][range()];
      ihaar_1d(in[sub_idx], out[sub_idx]);
    }
  }

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N0; j++) {
    for (int k = 0; k < N2; k++) {
      auto sub_idx = indices[j][range()][k];
      // THIS IS NOT A TYPO! out and in are reversed here.
      ihaar_1d(out[sub_idx], in[sub_idx]);
    }
  }

#pragma omp parallel for schedule(static) collapse(2)
  for (int j = 0; j < N1; j++) {
    for (int k = 0; k < N2; k++) {
      auto sub_idx = indices[range()][j][k];
      ihaar_1d(in[sub_idx], out[sub_idx]);
    }
  }
}

void ForwardHaar::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_REAL);

  size_t N2 = lo_mgr->N2;
  typedef boost::multi_array_types::index_range range;

  auto sub_array = boost::indices[range()][range()][range(0, N2)];
  auto &out = delta_output.getRealOutput();
  auto &in = hold_input.getReal();

  if (do_inverse)
    ihaar_3d(in[sub_array], out[sub_array]);
  else
    haar_3d(in[sub_array], out[sub_array]);
}

void ForwardHaar::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  in_gradient_delta.needDestroyInput();
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardHaar::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);

  size_t N2 = lo_mgr->N2;
  typedef boost::multi_array_types::index_range range;

  auto sub_array = boost::indices[range()][range()][range(0, N2)];
  auto &in = hold_ag_input.getReal();
  auto &out = out_gradient_delta.getRealOutput();

  // Haar transpose is its inverse.
  if (do_inverse)
    haar_3d(in[sub_array], out[sub_array]);
  else
    ihaar_3d(in[sub_array], out[sub_array]);
}

static std::shared_ptr<BORGForwardModel> build_haar(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  bool use_inverse = params.get("inverse", false);

  return std::make_shared<ForwardHaar>(comm, box, use_inverse);
}

LIBLSS_REGISTER_FORWARD_IMPL(Haar, build_haar);

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
