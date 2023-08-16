/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/upgrade.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/forwards/upgrade.hpp"

using namespace LibLSS;

static BoxModel mul_box(BoxModel inbox, unsigned int m) {
  inbox.N0 *= m;
  inbox.N1 *= m;
  inbox.N2 *= m;
  return inbox;
}

ForwardUpgrade::ForwardUpgrade(
    MPI_Communication *comm, BoxModel const &box, unsigned int multiply)
    : BORGForwardModel(comm, box, mul_box(box, multiply)) {

  //ghosts.setup();
}

void ForwardUpgrade::forwardModel_v2(ModelInput<3> delta_init) {
  delta_init.setRequestedIO(PREFERRED_FOURIER);

  hold_input = std::move(delta_init);
}

namespace {
  namespace details {
    template <size_t Dim, size_t r, typename A>
    auto _basic_range(
        size_t id, std::array<ssize_t, Dim> const &source_N,
        std::array<ssize_t, Dim> const &target_N, A a) {
      typedef boost::multi_array_types::index_range range;
      if (r == 0) {
        if ((id & 1) != 0) {
          return a[range(target_N[0] - source_N[0] / 2 + 1, target_N[0])];
        } else {
          return a[range(0, source_N[0] / 2)];
        }
      } else {
        if ((id & (1UL << r)) != 0) {
          return a[range(target_N[r] - source_N[r] / 2 + 1, target_N[r])];
        } else {
          return a[range(0, source_N[r] / 2)];
        }
      }
    }

    template <size_t Dim, size_t r, typename A>
    auto _basic_slice(
        size_t id, size_t nyquist_dir, std::array<ssize_t, Dim> const &source_N,
        std::array<ssize_t, Dim> const &target_N, A a) {
      typedef boost::multi_array_types::index_range range;
      if (nyquist_dir == r) {
        if ((id & (1UL << r)) == 0) {
          return a[range(source_N[r] / 2, source_N[r] / 2 + 1)];
        } else {
          return a[range(
              target_N[r] - source_N[r] / 2,
              target_N[r] - source_N[r] / 2 + 1)];
        }
      } else {
        if ((id & (1UL << r)) == 0) {
          return a[range(0, source_N[r] / 2 + 1)];
        } else {
          return a[range(target_N[r] - source_N[r] / 2, target_N[r])];
        }
      }
    }

    template <size_t Dim, size_t r>
    struct _gen_range {

      static auto
      gen(size_t id, std::array<ssize_t, Dim> const &source_N,
          std::array<ssize_t, Dim> const &target_N) {
        return _basic_range<Dim, r>(
            id, source_N, target_N,
            _gen_range<Dim, r - 1>::gen(id, source_N, target_N));
      }
      static auto slice(
          size_t id, size_t nyquist_dir,
          std::array<ssize_t, Dim> const &source_N,
          std::array<ssize_t, Dim> const &target_N) {
        return _basic_slice<Dim, r>(
            id, nyquist_dir, source_N, target_N,
            _gen_range<Dim, r - 1>::slice(id, nyquist_dir, source_N, target_N));
      }
    };

    template <size_t Dim>
    struct _gen_range<Dim, 0UL> {
      static auto
      gen(size_t id, std::array<ssize_t, Dim> const &source_N,
          std::array<ssize_t, Dim> const &target_N) {
        return _basic_range<Dim, 0>(id, source_N, target_N, boost::indices);
      }
      static auto slice(
          size_t id, size_t nyquist_dir,
          std::array<ssize_t, Dim> const &source_N,
          std::array<ssize_t, Dim> const &target_N) {
        return _basic_slice<Dim, 0>(
            id, nyquist_dir, source_N, target_N, boost::indices);
      }
    };

    template <size_t Dim>
    auto gen_range(
        size_t id, std::array<ssize_t, Dim> const &source_N,
        std::array<ssize_t, Dim> const &target_N) {
      return _gen_range<Dim, Dim - 1>::gen(id, source_N, target_N);
    }

    template <size_t Dim>
    auto gen_slice(
        size_t id, size_t nyquist_dir, std::array<ssize_t, Dim> const &source_N,
        std::array<ssize_t, Dim> const &target_N) {
      return _gen_range<Dim, Dim - 1>::slice(
          id, nyquist_dir, source_N, target_N);
    }
  } // namespace details

  using details::gen_range;
  using details::gen_slice;

} // namespace

template <size_t Dim, typename OutArray, typename InputArray>
static void upgrade(
    NBoxModel<Dim> const &in_box, NBoxModel<Dim> const &out_box,
    OutArray &output, InputArray const &input) {
  constexpr size_t Pairs = 1UL << (Dim - 1);

  std::array<ssize_t, Dim> in_Ns, out_Ns;
  in_box.fill(in_Ns);
  out_box.fill(out_Ns);

  fwrap(output) = 0;

  for (size_t i = 0; i < Pairs; i++) {
    auto r0 = gen_range(i, in_Ns, in_Ns);
    auto r1 = gen_range(i, in_Ns, out_Ns);

    fwrap(output[r1]) = fwrap(input[r0]);

    for (unsigned nyquist = 0; nyquist < Dim; nyquist++) {
      auto s0 = gen_slice(i, nyquist, in_Ns, out_Ns);
      auto s1 = gen_slice(i, nyquist, in_Ns, in_Ns);

      fwrap(output[s0]) = fwrap(input[s1]);
    }
  }

  for (size_t i = 0; i < Pairs; i++) {

    for (unsigned nyquist = 0; nyquist < Dim; nyquist++) {
      {
        auto s0 = gen_slice(i, nyquist, in_Ns, out_Ns);

        fwrap(output[s0]) = 0.5 * fwrap(output[s0]);
      }
    }
  }
}

template <size_t Dim, typename OutArray, typename InputArray>
static void adjoint_upgrade(
    NBoxModel<Dim> const &in_box, NBoxModel<Dim> const &out_box,
    OutArray &output, InputArray const &input) {
  constexpr size_t Pairs = 1UL << (Dim - 1);

  std::array<ssize_t, Dim> in_Ns, out_Ns;
  in_box.fill(in_Ns);
  out_box.fill(out_Ns);

  fwrap(output) = 0;

  for (size_t i = 0; i < Pairs; i++) {

    for (unsigned nyquist = 0; nyquist < Dim; nyquist++) {
      {
        auto s0 = gen_slice(i, nyquist, in_Ns, in_Ns);
        auto s1 = gen_slice(i, nyquist, in_Ns, out_Ns);
//        double const fac = (nyquist==(Dim-1) ? 2 : 1);
 
        fwrap(output[s0]) = fwrap(output[s0]) + fwrap(input[s1]);
      }
    }
  }

  for (unsigned nyquist = 0; nyquist < Dim; nyquist++)
    {
      auto s0 = gen_slice(1UL << nyquist, nyquist, in_Ns, in_Ns);

      fwrap(output[s0]) = 0.5 * fwrap(output[s0]);
    }

  for (size_t i = 0; i < Pairs; i++) {
    auto r0 = gen_range(i, in_Ns, in_Ns);
    auto r1 = gen_range(i, in_Ns, out_Ns);

    fwrap(output[r0]) = fwrap(input[r1]);
  }
}

void ForwardUpgrade::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  delta_output.setRequestedIO(PREFERRED_FOURIER);

  auto &in_delta = hold_input.getFourierConst();
  //  ghosts.synchronize(in_delta);

  upgrade(
      get_box_model(), get_box_model_output(), delta_output.getFourierOutput(),
      in_delta);
}

void ForwardUpgrade::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {

  in_gradient_delta.setRequestedIO(PREFERRED_FOURIER);

  hold_adjoint = std::move(in_gradient_delta);
}

void ForwardUpgrade::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {

  out_gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  adjoint_upgrade(
      get_box_model(), get_box_model_output(),
      out_gradient_delta.getFourierOutput(), hold_adjoint.getFourierConst());
}

static std::shared_ptr<BORGForwardModel> build_upgrade(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {

  int multiplier = params.get<int>("multiplier");
  if (multiplier <= 1) {
    error_helper<ErrorParams>("Invalid multiplier, it is required to be > 1");
  }

  // TODO: Setup transfer function
  auto model = std::make_shared<ForwardUpgrade>(comm, box, multiplier);
  return model;
}

LIBLSS_REGISTER_FORWARD_IMPL(Upgrade, build_upgrade);
