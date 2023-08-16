/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/transfer.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/forwards/transfer.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"

using namespace LibLSS;

void ForwardTransfer::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_FOURIER);

  hold_input = std::move(delta_init);
}

void ForwardTransfer::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  delta_output.setRequestedIO(PREFERRED_FOURIER);
  auto w_delta_init = fwrap(hold_input.getFourierConst());
  auto w_delta_output = fwrap(delta_output.getFourierOutput());

  w_delta_output = w_delta_init * fwrap(*Tk);
}

void ForwardTransfer::setupInverseCIC(double smoother) {
  size_t N0 = lo_mgr->N0, N1 = lo_mgr->N1, N2 = lo_mgr->N2;
  size_t hN0 = N0 / 2;
  size_t hN1 = N1 / 2;
  size_t hN2 = N2 / 2;
  double const regul = std::sin(M_PI * smoother) / (M_PI * smoother);
  auto sinc = [regul, smoother](double x) {
    return (std::abs(x) < smoother) ? (std::sin(M_PI * x) / (M_PI * x)) : regul;
  };
  auto cic_Kernel =
      b_fused_idx<double, 3>([&](ssize_t i, ssize_t j, ssize_t k) {
        if (i > hN0)
          i -= N0;
        if (j > hN1)
          j -= N1;
        if (k > hN2)
          k -= N2;
        double r = 1.0;
        if (i != 0)
          r *= sinc(double(i) / N0);
        if (j != 0)
          r *= sinc(double(j) / N1);
        if (k != 0)
          r *= sinc(double(k) / N2);
        assert(r != 0);
        return 1.0 / (r * r);
      });

  Tk = std::move(lo_mgr->allocate_ptr_complex_array());

  fwrap(*Tk) = cic_Kernel;
}

void ForwardTransfer::setupSharpKcut(double cut, bool reversed) {
  size_t N0 = lo_mgr->N0, N1 = lo_mgr->N1, N2 = lo_mgr->N2;
  double const cut2 = cut * cut;
  size_t hN0 = N0 / 2;
  size_t hN1 = N1 / 2;
  size_t hN2 = N2 / 2;
  auto sharp_Kernel =
      b_fused_idx<double, 3>([&](ssize_t i, ssize_t j, ssize_t k) {
        if (i > hN0)
          i -= N0;
        if (j > hN1)
          j -= N1;
        if (k > hN2)
          k -= N2;
        double r = 0.0;
        if (i != 0)
          r += CosmoTool::square(2*M_PI/L0*double(i));
        if (j != 0)
          r += CosmoTool::square(2*M_PI/L1*double(j));
        if (k != 0)
          r += CosmoTool::square(2*M_PI/L2*double(k));
        return r < cut2 ? 1.0 : 0.0;
      });

  Tk = std::move(lo_mgr->allocate_ptr_complex_array());

  if (reversed)
    fwrap(*Tk) = 1.0 - fwrap(sharp_Kernel);
  else
    fwrap(*Tk) = sharp_Kernel;
}

void ForwardTransfer::setTransfer(
    std::shared_ptr<DFT_Manager::U_ArrayFourier> Tk_) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  Tk = Tk_;
}

void ForwardTransfer::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardTransfer::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  auto w_in_gradient = fwrap(hold_ag_input.getFourierConst());
  auto w_out_gradient = fwrap(out_gradient_delta.getFourierOutput());

  w_out_gradient = w_in_gradient * fwrap(*Tk);
}

static std::shared_ptr<BORGForwardModel> build_transfer(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  auto transfer_filename = params.get_optional<std::string>("transfer");
  auto transfer_cic = params.get_optional<bool>("use_invert_cic");
  auto transfer_sharp = params.get_optional<bool>("use_sharpk");

  // TODO: Setup transfer function
  auto model = std::make_shared<ForwardTransfer>(comm, box);

  if (transfer_filename) {
    auto Tk = model->lo_mgr->allocate_ptr_complex_array();
    H5::H5File f(*transfer_filename, H5F_ACC_RDONLY);
    try {
      CosmoTool::hdf5_read_array(f, "transfer", Tk->get_array(), false, true);
    } catch (CosmoTool::InvalidDimensions const &) {
      error_helper<ErrorParams>(
          "Provided transfer function does not have the correct shape.");
    }
    model->setTransfer(std::move(Tk));
  } else if (transfer_cic && *transfer_cic) {
    model->setupInverseCIC(params.get<double>("smoother"));
  } else if (transfer_sharp && *transfer_sharp) {
    model->setupSharpKcut(params.get<double>("k_max"));
  } else {
    error_helper<ErrorParams>("Transfer function non specified");
  }
  return model;
}

LIBLSS_REGISTER_FORWARD_IMPL(Transfer, build_transfer);

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
