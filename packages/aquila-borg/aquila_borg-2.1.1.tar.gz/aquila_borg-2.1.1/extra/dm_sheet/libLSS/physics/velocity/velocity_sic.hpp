/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/velocity/velocity_sic.hpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PHYSICS_VELOCITY_SIC
#  define __LIBLSS_PHYSICS_VELOCITY_SIC

#  include <boost/multi_array.hpp>

#  include "libLSS/physics/velocity/velocity.hpp"
#  include "libLSS/physics/dm_sheet/dm_sheet.hpp"

namespace LibLSS {

  void computeSICVelocityField(
      DM_Sheet::arrayID_t const &identifiers,
      DM_Sheet::arrayPosition_t const &pos,
      DM_Sheet::arrayVelocity_t const &vels, double L, int N, int Ng,
      boost::multi_array_ref<double, 3> &DensityField,
      VelocityModel::ParticleBasedModel::arrayVelocityField_t &VelocityField);

  namespace VelocityModel {

    /**
     * @brief Simplex-In-Cell velocity field model from BORGForwardModel
     * 
     */
    class SICModel : public ParticleBasedModel {
    protected:
      LibLSS::FFTW_Manager<double, 3> mgr;

    public:
      /**
       * @brief Construct a new SICModel object
       * 
       * @param box_out_ 
       * @param model_ 
       */
      SICModel(BoxModel box_out_, particleForwardModel_t model_)
          : ParticleBasedModel(box_out_, model_),
            mgr(box_out_.N0, box_out_.N1, box_out_.N2, model_->communicator()) {
      }

      /**
       * @brief Get the Mgr object
       * 
       * @return LibLSS::FFTW_Manager<double, 3> const& 
       */
      LibLSS::FFTW_Manager<double, 3> const &getMgr() const { return mgr; }

      void queryLocalExtents(std::array<ssize_t, 6> &e) override {
        e[0] = mgr.startN0;
        e[1] = mgr.startN0 + mgr.localN0;
        e[2] = 0;
        e[3] = mgr.N1;
        e[4] = 0;
        e[5] = mgr.N2;
      }

      void getVelocityField(arrayVelocityField_t VelocityField) override;
      void
      computeAdjointModel(arrayVelocityField_view_t AGVelocityField) override;
    };
  } // namespace VelocityModel
};  // namespace LibLSS

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
