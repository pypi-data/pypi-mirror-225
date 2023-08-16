/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/velocity/velocity.hpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_VELOCITY
#  define __LIBLSS_PHYSICS_VELOCITY

#  include <boost/multi_array.hpp>

#  include "libLSS/physics/forward_model.hpp"

namespace LibLSS {

  namespace VelocityModel {

    class Base {
    public:
      typedef LibLSS::multi_array_ref<double, 4> arrayVelocityField_t;
      typedef LibLSS::const_multi_array_ref<double, 4> arrayVelocityField_const_t;
      typedef arrayVelocityField_t::const_array_view<4>::type
          arrayVelocityField_view_t;
      typedef LibLSS::multi_array_ref<double, 2> arrayPosition_t;
      typedef LibLSS::multi_array_ref<double, 2> arrayVelocity_t;
      typedef LibLSS::const_multi_array_ref<double, 2> arrayVelocity_const_t;

      typedef std::shared_ptr<LibLSS::BORGForwardModel> forwardModel_t;

    protected:
      forwardModel_t model;
      BoxModel outputBox;

    public:
      virtual forwardModel_t getForwardModel() { return model; }
      virtual forwardModel_t const getForwardModel() const { return model; }

      BoxModel getOutputBox() { return outputBox; }

      Base(BoxModel box_out_) : outputBox(box_out_) {}

      virtual void queryLocalExtents(std::array<ssize_t, 6> &e) = 0;

      virtual void getVelocityField(arrayVelocityField_t VelocityField) = 0;
      virtual void computeAdjointModel(
          arrayVelocityField_view_t AGVelocityField) = 0;

      virtual void computeAdjointModel_array(
          arrayVelocityField_const_t const &AGVelocityField) {
        typedef boost::multi_array_types::index_range i_range;
        computeAdjointModel(
            AGVelocityField[boost::indices[i_range()][i_range()][i_range()]
                                          [i_range()]]);
      }

    }; // class Base

    class ParticleBasedModel : public Base {
    public:
      typedef std::shared_ptr<LibLSS::ParticleBasedForwardModel>
          particleForwardModel_t;
      typedef std::shared_ptr<LibLSS::ParticleBasedForwardModel const>
          particleForwardModel_const_t;

    protected:
      particleForwardModel_t p_model;

    public:
      ParticleBasedModel(BoxModel box_out_, particleForwardModel_t model_)
          : Base(box_out_), p_model(model_) {
        model = model_;
      }

      virtual particleForwardModel_t getParticleModel() { return p_model; }
      virtual particleForwardModel_const_t getParticleModel() const {
        return p_model;
      }
    }; // class ParticleBasedModel
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
