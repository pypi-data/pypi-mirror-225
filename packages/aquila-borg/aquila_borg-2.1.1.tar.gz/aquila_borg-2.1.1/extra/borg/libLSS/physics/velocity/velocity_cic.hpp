/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/velocity/velocity_cic.hpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_VELOCITY_CIC
#  define __LIBLSS_PHYSICS_VELOCITY_CIC

#  include <boost/multi_array.hpp>

#  include "libLSS/physics/velocity/velocity.hpp"
#  include "libLSS/physics/classic_cic.hpp"

namespace LibLSS {

  namespace VelocityModel {

    class CICModel : public ParticleBasedModel {
    public:
      typedef ClassicCloudInCell<double> CIC;

    protected:
      LibLSS::FFTW_Manager<double, 3> mgr;

    public:
      CICModel(BoxModel box_out_, particleForwardModel_t model_)
          : ParticleBasedModel(box_out_, model_),
            mgr(box_out_.N0, box_out_.N1, box_out_.N2, model_->communicator()) {
      }

      LibLSS::FFTW_Manager<double, 3> const &getMgr() const { return mgr; }

      virtual void queryLocalExtents(std::array<ssize_t, 6> &e) {
        e[0] = mgr.startN0;
        e[1] = mgr.startN0 + mgr.localN0;
        e[2] = 0;
        e[3] = mgr.N1;
        e[4] = 0;
        e[5] = mgr.N2;
      }

      void getVelocityField(arrayVelocityField_t VelocityField);
      virtual void computeAdjointModel(
          arrayVelocityField_view_t AGVelocityField);

    }; // class CICModel
  }    // namespace VelocityModel
};     // namespace LibLSS

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
