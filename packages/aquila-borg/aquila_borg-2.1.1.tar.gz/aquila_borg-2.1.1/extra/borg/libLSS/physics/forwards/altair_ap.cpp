/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/altair_ap.cpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2020 Doogesh Kodi Ramanah <ramanah@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/forwards/altair_ap.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/fused_cond.hpp"
#include "libLSS/tools/errors.hpp"
#include <gsl/gsl_const_mksa.h>
#include <Eigen/Dense>
#include <cmath>
#include "libLSS/tools/mpi/ghost_planes.hpp"
#include "libLSS/tools/auto_interpolator.hpp"

using namespace LibLSS;
using namespace LibLSS::ALTAIR;

AltairAPForward::AltairAPForward(
    MPI_Communication *comm, const BoxModel &box_c, const BoxModel &box_z,
    bool is_contrast_)
    : BORGForwardModel(comm, box_c, box_z),
      M_matrix(n_order * n_order * n_order, n_order * n_order * n_order),
      M_inverse(n_order * n_order * n_order, n_order * n_order * n_order),
      grid_transform(out_mgr->extents_real_strict()[4]),
      is_contrast(is_contrast_) {
  ConsoleContext<LOG_VERBOSE> ctx("Altair AP initialization");

  ctx.format(
      "Redshift box [%g,%g] [%g,%g] [%g,%g]", box_z.xmin0,
      (box_z.xmin0 + box_z.L0), box_z.xmin1, (box_z.xmin1 + box_z.L1),
      box_z.xmin2, (box_z.xmin2 + box_z.L2));
  ctx.format(
      "Comoving box [%g,%g] [%g,%g] [%g,%g]", xmin0, (xmin0 + L0), xmin1,
      (xmin1 + L1), xmin2, (xmin2 + L2));

  setupDefault();

  // ASSERTION: box_c.N* == box.N* // For the time being, redshift box corresponds to comoving one
  L_z[0] = box_z.L0;
  L_z[1] = box_z.L1;
  L_z[2] = box_z.L2;
  corner_z[0] = box_z.xmin0;
  corner_z[1] = box_z.xmin1;
  corner_z[2] = box_z.xmin2;

  delta_z[0] = L_z[0] / out_mgr->N0;
  delta_z[1] = L_z[1] / out_mgr->N1;
  delta_z[2] = L_z[2] / out_mgr->N2;

  delta_c[0] = box_c.L0 / lo_mgr->N0;
  delta_c[1] = box_c.L1 / lo_mgr->N1;
  delta_c[2] = box_c.L2 / lo_mgr->N2;

  prepareMatrix();   // Compute M_matrix only once
  COSMO_INIT = true; //FIXME
}

void AltairAPForward::prepareMatrix() {
  // Declare variables required for tricubic interpolation
  // For case of trilinear interpolation
  switch (n_order) {
  case 2:
    x_inter[0] = 0;
    x_inter[1] = 1;
    break;
  case 4:
    x_inter[0] = -1;
    x_inter[1] = 0;
    x_inter[2] = 1;
    x_inter[3] = 2;
    break;
  case 6:
    x_inter[0] = -2;
    x_inter[1] = -1;
    x_inter[2] = 0;
    x_inter[3] = 1;
    x_inter[4] = 2;
    x_inter[5] = 3;
    break;
  case 8:
    x_inter[0] = -3;
    x_inter[1] = -2;
    x_inter[2] = -1;
    x_inter[3] = 0;
    x_inter[4] = 1;
    x_inter[5] = 2;
    x_inter[6] = 3;
    x_inter[7] = 4;
    break;
  default:
    error_helper<ErrorNotImplemented>("Interpolation order not implemented");
    break;
  }
  // Construct the M_matrix [(64x64) for tricubic interpolation] that encodes the interpolation coefficients
  for (int alpha = 0; alpha < n_order; alpha++) {
    for (int beta = 0; beta < n_order; beta++) {
      for (int gamma = 0; gamma < n_order; gamma++) {
        for (int i = 0; i < n_order; i++) {
          for (int j = 0; j < n_order; j++) {
            for (int k = 0; k < n_order; k++) {

              M_matrix(
                  n_order * n_order * alpha + n_order * beta + gamma,
                  n_order * n_order * i + n_order * j + k) =
                  std::pow(x_inter[alpha], i) * std::pow(x_inter[beta], j) *
                  std::pow(x_inter[gamma], k);
            }
          }
        }
      }
    }
  }
  // Compute the inverse of M_matrix
  M_inverse = M_matrix.inverse();
}

void AltairAPForward::updateCoordinateSystem() {
  ConsoleContext<LOG_VERBOSE> ctx("Altair AP: updating coordinate system");
  Console &cons = Console::instance();
  Cosmology cosmo(my_params);

  double Qfactor = (H100 * M_IN_KM) / cosmo_clight; // Q has units h100/Mpc
  // Note that internal units are all Mpc/h100, so the external redshift has to be put on similar scales
  // This leaves only the physical effect due to distortion

  // Owned planes
  std::vector<size_t> owned_planes(lo_mgr->localN0);

  for (size_t i = 0; i < lo_mgr->localN0; i++)
    owned_planes[i] = lo_mgr->startN0 + i;

  size_t startN0 = out_mgr->startN0;
  size_t endN0 = startN0 + out_mgr->localN0;
  size_t out_N1 = out_mgr->N1;
  size_t out_N2 = out_mgr->N2;

  double far_z = 0;

  for (int a = 0; a <= 1; a++) {
    for (int b = 0; b <= 1; b++) {
      for (int c = 0; c <= 1; c++) {
        double z_x = corner_z[0] + a * out_mgr->N0 * delta_z[0];
        double z_y = corner_z[1] + b * out_N1 * delta_z[1];
        double z_z = corner_z[2] + c * out_N2 * delta_z[2];

        double z_r = std::sqrt(
            z_x * z_x + z_y * z_y + z_z * z_z); // z_r has units Mpc/h100
        far_z = std::max(far_z, z_r);
      }
    }
  }
  far_z *= Qfactor*1.1; // add 10% safety margin.
  ctx.format("far_z=%g", far_z);

  auto fast_r_c =
      build_auto_interpolator(
          [&](double z) { return cosmo.com2comph(cosmo.a2com(cosmo.z2a(z))); },
          0.0, far_z, 1e-2, 0.0, 0.0)
          .setThrowOnOverflow();

  auto fast_E_z =
      build_auto_interpolator(
          [&](double z) {
            return cosmo.Hubble(cosmo.z2a(z)) / (my_params.h * H100);
          },
          0.0, far_z, 1e-2, 0.0, 0.0)
          .setThrowOnOverflow();

#pragma omp parallel for collapse(3)
  for (size_t n0 = startN0; n0 < endN0; n0++) {
    for (size_t n1 = 0; n1 < out_N1; n1++) {
      for (size_t n2 = 0; n2 < out_N2; n2++) {
        double z_x = double(n0) * delta_z[0] + corner_z[0],
               z_y = double(n1) * delta_z[1] + corner_z[1],
               z_z = double(n2) * delta_z[2] + corner_z[2];

        double z_r = std::sqrt(
            z_x * z_x + z_y * z_y + z_z * z_z); // z_r has units Mpc/h100

        double r_c;
        try {
          r_c = fast_r_c(
            z_r *
            Qfactor); // z_r*Q_factor = adimensional;r_c has units Mpc/h100
} catch(LibLSS::ErrorParams& e) {
  ctx.format("Problem at z_r*Qfactor=%g", z_r*Qfactor);
  throw;
}

        //double r_c = z_r; // NO EXPANSION!!! -> Remove distortion due to cosmology

        double c_x = z_x / z_r * r_c, c_y = z_y / z_r * r_c,
               c_z = z_z / z_r * r_c;

        if (r_c == 0) {
          c_x = 0;
          c_y = 0;
          c_z = 0;
        }

        // Compute E(z)
        double E_z = fast_E_z(Qfactor * z_r); // E_z is dimensionless //FIXME
        //(cosmo_params.h * H100); // E_z is dimensionless

        //double E_z = 1/(1+2*Qfactor*z_r); // NO EXPANSION!!! -> Remove distortion due to cosmology
        double del_z_del_x = E_z;
        double Jc = del_z_del_x - (z_r / r_c);

        // Compute all 9 components of (3x3) matrix J for each voxel
        double J_00 = ((Jc * c_x * c_x) / (r_c * r_c)) + (z_r / r_c);
        double J_01 = ((Jc * c_x * c_y) / (r_c * r_c));
        double J_02 = ((Jc * c_x * c_z) / (r_c * r_c));
        double J_10 = J_01; // Symmetric about leading diagonal
        double J_11 = ((Jc * c_y * c_y) / (r_c * r_c)) + (z_r / r_c);
        double J_12 = ((Jc * c_y * c_z) / (r_c * r_c));
        double J_20 = J_02;
        double J_21 = J_12;
        double J_22 = ((Jc * c_z * c_z) / (r_c * r_c)) + (z_r / r_c);
        // Compute determinant of (3x3) matrix J -> Jacobian(voxel)
        double Jacobian = J_00 * (J_11 * J_22 - J_12 * J_21) -
                          J_01 * (J_10 * J_22 - J_12 * J_20) +
                          J_02 * (J_10 * J_21 - J_11 * J_20);

        grid_transform[n0][n1][n2][0] = (c_x - xmin0) / delta_c[0];
        grid_transform[n0][n1][n2][1] = (c_y - xmin1) / delta_c[1];
        grid_transform[n0][n1][n2][2] = (c_z - xmin2) / delta_c[2];
        grid_transform[n0][n1][n2][3] = 1.0 / Jacobian;

        if (r_c == 0) {
          grid_transform[n0][n1][n2][3] = 1.;
        }

#ifndef NDEBUG
        if (grid_transform[n0][n1][n2][3] < 0) {
          ctx.format(
              "Jacobian = %g, Jc = %g, r_c = %g, z_r = %g, "
              "del_z_del_x = %g, E_z = %g, Qfactor = %g",
              grid_transform[n0][n1][n2][3], Jc, r_c, z_r, del_z_del_x, E_z,
              Qfactor);
          cons.c_assert((grid_transform[n0][n1][n2][3] > 0), "Jacobian < 0");
        }
#endif
        // The following assertions ensure we do not go outside of box
        // We use error_helper to report to the caller that cosmology/box setup is wrong
        // but do not crash the code in case we are working in python.
        auto g = grid_transform[n0][n1][n2];
        if (g[0] < 0)
          error_helper<ErrorParams>("Underflow lower bound 0");
        if (g[0] >= lo_mgr->N0)
          error_helper<ErrorParams>("Overflow lower bound 0");
        if (g[1] < 0)
          error_helper<ErrorParams>("Underflow lower bound 1");
        if (g[1] >= lo_mgr->N1)
          error_helper<ErrorParams>("Overflow lower bound 1");
        if (g[2] < 0)
          error_helper<ErrorParams>("Underflow lower bound 2");
        if (g[2] >= lo_mgr->N1)
          error_helper<ErrorParams>("Overflow lower bound 2");
      }
    }
  }

  // Setup ghost plane
  std::set<size_t> required_planes;

  for (size_t n0 = startN0; n0 < endN0; n0++) {
    for (size_t n1 = 0; n1 < out_N1; n1++) {
      for (size_t n2 = 0; n2 < out_N2; n2++) {
        size_t base = std::floor(grid_transform[n0][n1][n2][0]);
        for (size_t j = 0; j < n_order; j++) {
          size_t k = (base + x_inter[j] + N0) % N0;
          if (!lo_mgr->on_core(k)) {
            required_planes.insert(k);
          }
        }
      }
    }
  }

  ghosts.setup(
      comm, required_planes, owned_planes,
      std::array<size_t, 2>{size_t(lo_mgr->N1), size_t(lo_mgr->N2real)},
      lo_mgr->N0);
}

// Function for tricubic interpolation here. Input: s_field --> Output: z_field
template <typename SArray>
void AltairAPForward::interpolate_3d(SArray const &s_field, ArrayRef &z_field) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  double shift;

  fwrap(*tmp_real_field) = s_field;

  ghosts.synchronize(*tmp_real_field);

  if (is_contrast)
    shift = 1;
  else
    shift = 0;

// Coordinate transformation (redshift -> comoving), followed by trilinear interpolation
#pragma omp parallel
  {
    size_t endN0 = out_mgr->startN0 + out_mgr->localN0;
    size_t startN0 = out_mgr->startN0;
    size_t out_N1 = out_mgr->N1;
    size_t out_N2 = out_mgr->N2;

    VectorXd interp_coeff(n_order * n_order * n_order);
    VectorXd rho(
        n_order * n_order *
        n_order); // vector that encodes values of (n_order**3) voxels that will contribute to interpolated value
#pragma omp for collapse(                                                      \
    3) //private(rho, interp_coeff) // private ensures that different arrays are used on different threads to avoid leakage
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < out_N1; n1++) {
        for (size_t n2 = 0; n2 < out_N2; n2++) {

          auto t = grid_transform[n0][n1][n2];
          double out = 0;

          int ix = (int)std::floor(t[0]); // input x-coordinate
          int iy = (int)std::floor(t[1]); // input y-coordinate
          int iz = (int)std::floor(t[2]); // input z-coordinate

          double rx = t[0] - ix;
          double ry = t[1] - iy;
          double rz = t[2] - iz;

          // Construct rho to evaluate store the value of s_field at all vertices of interest -> vector of dimension 64 for tricubic scheme
          // We use periodic BC here -> Add N0/N1/N2 to prevent negative values

          for (size_t alpha = 0; alpha < n_order; alpha++) {
            size_t r_alpha = (ix + x_inter[alpha] + N0) % N0;
            if (lo_mgr->on_core(r_alpha)) {
              for (size_t beta = 0; beta < n_order; beta++) {
                size_t r_beta = (iy + x_inter[beta] + N1) % N1;
                for (size_t gamma = 0; gamma < n_order; gamma++) {
                  size_t r_gamma = (iz + x_inter[gamma] + N2) % N2;
                  rho(n_order * n_order * alpha + n_order * beta + gamma) =
                      s_field[r_alpha][r_beta][r_gamma];
                }
              }
            } else {
              auto selected_plane = ghosts.getPlane(r_alpha);
              for (size_t beta = 0; beta < n_order; beta++) {
                size_t r_beta = (iy + x_inter[beta] + N1) % N1;
                for (size_t gamma = 0; gamma < n_order; gamma++) {
                  size_t r_gamma = (iz + x_inter[gamma] + N2) % N2;
                  rho(n_order * n_order * alpha + n_order * beta + gamma) =
                      selected_plane[r_beta][r_gamma];
                }
              }
            }
          }

          // Include an assertion below on all values of rho to ensure no negative values
#ifndef NDEBUG
          for (int i_assert = 0; i_assert < (n_order * n_order * n_order);
               i_assert++) {
            Console::instance().c_assert(
                rho(i_assert) >= (-1 + epsilon), "rho[i_assert] not positive");
          }
#endif

          // Construct interp_coeff via matricial operation -> vector of dimension 64 for tricubic scheme
          interp_coeff.noalias() =
              M_inverse *
              rho; // Apparently, the matricial operation is as simplistic as this

          // Core of generic nth order interpolation
          boost::array<double, n_order> ax, ay, az;
          for (unsigned int i_tilde = 0; i_tilde < n_order; i_tilde++) {
            ax[i_tilde] = std::pow(rx, i_tilde);
            ay[i_tilde] = std::pow(ry, i_tilde);
            az[i_tilde] = std::pow(rz, i_tilde);
          }

          for (unsigned int i_tilde = 0; i_tilde < n_order; i_tilde++) {
            for (unsigned int j_tilde = 0; j_tilde < n_order; j_tilde++) {
              for (unsigned int k_tilde = 0; k_tilde < n_order; k_tilde++) {
                out += interp_coeff(
                           n_order * n_order * i_tilde + n_order * j_tilde +
                           k_tilde) *
                       ax[i_tilde] * ay[j_tilde] * az[k_tilde];
              }
            }
          }

          // z_field may become < -1 owed to numerical inaccuracies
          z_field[n0][n1][n2] = t[3] * (shift + out) - shift;
        }
      }
    }
  }
}

void AltairAPForward::forwardModelSimple(CArrayRef &delta_init) {
  error_helper<ErrorNotImplemented>(
      "No forwardModelSimple in ALTAIR forward model");
}

void AltairAPForward::clearAdjointGradient() { hold_in_gradient.clear(); }

void AltairAPForward::forwardModel_v2(ModelInput<3> delta_init) {
  ConsoleContext<LOG_DEBUG> ctx("forward Altair AP");

  delta_init.setRequestedIO(PREFERRED_REAL);

  hold_input = std::move(delta_init);
}

void AltairAPForward::getDensityFinal(ModelOutput<3> delta_output) {

  // Need the real space density field -> s_field
  delta_output.setRequestedIO(PREFERRED_REAL);

  double G = 1; // Growth TBI

  auto const &s_field = hold_input.getRealConst();

  // Only bother of real values (no padding)
  // First part of the forward model, rescaling
  auto fdelta = fwrap(s_field);
  auto zero_array = b_fused_idx<double, 3>(
      [](int, int, int) -> double { return -1 + epsilon; });
  // Threshold the density at zero
  auto cond = *(fdelta > (-1 + epsilon));
  auto density = b_cond_fused<double>(cond, *fdelta, zero_array);

  // The function below does the trilinear interpolation and outputs z_field
  // Output of forward model -> galaxy density field in redshift space.
  interpolate_3d(density, delta_output.getRealOutput());
}

//FIXME
void AltairAPForward::setModelParams(ModelDictionnary const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  if (params.find("altair_cosmo") != params.end()) {
    ctx.print("Got new cosmology");
    my_params = boost::any_cast<CosmologicalParameters>(
        params.find("altair_cosmo")->second);
    updateCoordinateSystem();
  }
}

void AltairAPForward::updateCosmo() {
  ConsoleContext<LOG_DEBUG> ctx("Altair AP cosmo update");

  if (COSMO_INIT) { //FIXME
    my_params = cosmo_params;
    updateCoordinateSystem();
    COSMO_INIT = false;
  }
}

void AltairAPForward::forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) {
  error_helper<ErrorNotImplemented>("No RSD support in Log forward model");
}

void AltairAPForward::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  ConsoleContext<LOG_DEBUG> ctx("adjoint Altair AP");

  // Build strict range views (we do not want to see the
  // FFTW padding), ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);

  hold_in_gradient = std::move(in_gradient_delta);
}

void AltairAPForward::getAdjointModelOutput(
    ModelOutputAdjoint<3> ag_delta_output) {

  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  ag_delta_output.setRequestedIO(PREFERRED_REAL);

  auto &in_gradient = hold_in_gradient.getRealConst();

  auto in_gradient_view = in_gradient[out_mgr->strict_range()];

  auto out_gradient_view =
      ag_delta_output.getRealOutput()[lo_mgr->strict_range()];

  ghosts.clear_ghosts();

  fwrap(out_gradient_view) = 0;

  // Careful with MPI:
  // With strict range -> view where the first axis is no longer between [startN0, startN0+localNo] but between [0, localN0]
  //fwrap(in_gradient[lo_mgr->strict_range()]) = gradient_delta[lo_mgr->strict_range()];
  //fwrap(out_gradient_view) = 0;
  size_t endN0 = out_mgr->startN0 + out_mgr->localN0;
  size_t startN0 = out_mgr->startN0;
  size_t out_N1 = out_mgr->N1;
  size_t out_N2 = out_mgr->N2;

// Gradient of trilinear interpolation -> Loop over voxel of incoming gradient
#pragma omp parallel for collapse(3)
  for (size_t n0 = startN0; n0 < endN0; n0++) {
    for (size_t n1 = 0; n1 < out_N1; n1++) {
      for (size_t n2 = 0; n2 < out_N2; n2++) {

        // For adjoint gradient purposes
        VectorXd interp_coeff_adj(n_order * n_order * n_order);
        VectorXd rho_adj(n_order * n_order * n_order);

        auto input_gradient = in_gradient[n0][n1][n2];
        auto t = grid_transform[n0][n1][n2];

        // Compute adjoint (tangent) gradient
        int ix = (int)std::floor(t[0]); // input x-coordinate
        int iy = (int)std::floor(t[1]); // input y-coordinate
        int iz = (int)std::floor(t[2]); // input z-coordinate

        double rx = t[0] - ix;
        double ry = t[1] - iy;
        double rz = t[2] - iz;

        // Generalize gradient of trilinear interpolation below to tricubic version
        for (size_t alpha = 0; alpha < n_order; alpha++) {
          for (size_t beta = 0; beta < n_order; beta++) {
            for (size_t gamma = 0; gamma < n_order; gamma++) {
              rho_adj(n_order * n_order * alpha + n_order * beta + gamma) =
                  input_gradient * std::pow(rx, alpha) * std::pow(ry, beta) *
                  std::pow(rz, gamma);
            }
          }
        }

        interp_coeff_adj = (rho_adj.transpose() * M_inverse)
                               .transpose(); // Same M_inverse as computed above

        auto compute_value = [&interp_coeff_adj](size_t i, size_t j, size_t k) {
          return interp_coeff_adj(n_order * n_order * i + n_order * j + k);
        };

        double volume_expansion = t[3];

        auto accumulate = [this, iy, iz, &compute_value,
                           volume_expansion](size_t i_tilde, auto &&out) {
          for (size_t j_tilde = 0; j_tilde < n_order; j_tilde++) {
            size_t index_j = (iy + x_inter[j_tilde] + N1) % N1;
            for (size_t k_tilde = 0; k_tilde < n_order; k_tilde++) {
              size_t index_k = (iz + x_inter[k_tilde] + N2) % N2;
              out[index_j][index_k] +=
                  volume_expansion * compute_value(i_tilde, j_tilde, k_tilde);
            }
          }
        };

        auto &ag_real_out = ag_delta_output.getRealOutput();
        // Gradient of tricubic interpolation (Do not forget Jacobian factor)
        for (size_t i_tilde = 0; i_tilde < n_order; i_tilde++) {
          size_t index_i = (ix + x_inter[i_tilde] + N0) % N0;

          if (lo_mgr->on_core(index_i)) {
            accumulate(i_tilde, ag_real_out[index_i]);
          } else {
            accumulate(i_tilde, ghosts.ag_getPlane(index_i));
          }
        }
      }
    }
  }

  ghosts.synchronize_ag(ag_delta_output.getRealOutput());
}

void AltairAPForward::releaseParticles() {}

static std::shared_ptr<BORGForwardModel> build_altair_ap(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  bool is_contrast;
  BoxModel box_z;

  box_z.xmin0 = params.get<double>("corner0_z");
  box_z.xmin1 = params.get<double>("corner1_z");
  box_z.xmin2 = params.get<double>("corner2_z");
  box_z.L0 = params.get<double>("L0_z");
  box_z.L1 = params.get<double>("L1_z");
  box_z.L2 = params.get<double>("L2_z");
  box_z.N0 = params.get<double>("N0_z");
  box_z.N1 = params.get<double>("N1_z");
  box_z.N2 = params.get<double>("N2_z");
  is_contrast = params.get<bool>("is_contrast", false);

  return std::make_shared<AltairAPForward>(comm, box, box_z, is_contrast);
}

LIBLSS_REGISTER_FORWARD_IMPL(ALTAIR_AP, build_altair_ap);

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2020
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: year(1) = 2018-2020
