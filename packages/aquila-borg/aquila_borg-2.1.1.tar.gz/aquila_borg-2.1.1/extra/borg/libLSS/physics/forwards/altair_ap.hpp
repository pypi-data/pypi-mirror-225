/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/altair_ap.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2020 Doogesh Kodi Ramanah <ramanah@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ALTAIR_AP_FORWARD_MODEL_HPP
#  define __LIBLSS_ALTAIR_AP_FORWARD_MODEL_HPP

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/fused_cond.hpp"
#  include "libLSS/tools/errors.hpp"
#  include <gsl/gsl_const_mksa.h>
#  include <Eigen/Dense>
#  include <cmath>
#  include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {

  namespace ALTAIR {
    using namespace Eigen;
    using boost::format;

    // For case of tricubic interpolation
    static constexpr int TRICUBIC = 2;
    static constexpr int TRIQUINTIC = 4;
    static constexpr int TRISEPTIC = 6;
    static constexpr int TRIHEPTIC = 8;

    constexpr static const int n_order = TRIQUINTIC;

    class AltairAPForward : public BORGForwardModel {
    protected:
      double rho_mean;
      double L_z[3];
      double corner_z[3];
      double delta_z[3];
      double delta_c[3];

      constexpr static const double H100 = 100.; // km/s/Mpc
      constexpr static const double M_IN_KM =
          1000.; // number of metres in one kilometer
      constexpr static const double cosmo_clight =
          GSL_CONST_MKSA_SPEED_OF_LIGHT; // speed of light in m/s
      static constexpr double epsilon = 1e-4;

      MatrixXd
          M_matrix, // (n_order**3,n_order**3) matrix of interpolation coefficients
          M_inverse; // inverse of M_matrix

      boost::multi_array<double, 4> grid_transform;
      boost::multi_array<double, 4> soft_factor;

      int x_inter[n_order];

      GhostPlanes<double, 2> ghosts; // 2d ghost planes
      ModelInput<3> hold_input;
      ModelInputAdjoint<3> hold_in_gradient;
      bool is_contrast;

    public:
      explicit AltairAPForward(
          MPI_Communication *comm, const BoxModel &box_c,
          const BoxModel &box_z, bool is_contrast = true);

      void prepareMatrix();

      void setModelParams(ModelDictionnary const &params) override; //FIXME
      CosmologicalParameters my_params;                             //FIXME
      bool COSMO_INIT;                                              //FIXME

      void updateCoordinateSystem();

      template <typename SArray>
      void interpolate_3d(SArray const &s_field, ArrayRef &z_field);

      void forwardModelSimple(CArrayRef &delta_init) override;

      void forwardModel_v2(ModelInput<3> delta_init) override;

      void getDensityFinal(ModelOutput<3> delta_output) override;

      void updateCosmo() override;

      void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) override;

      void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;

      void
      getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) override;

      void clearAdjointGradient() override;

      void releaseParticles() override;
    };

  } // namespace ALTAIR
} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(ALTAIR_AP);

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2020
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: year(1) = 2018-2020
