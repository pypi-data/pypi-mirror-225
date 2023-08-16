#ifndef __LIBLSS_PHYSICS_VELOCITY_LINEAR
#  define __LIBLSS_PHYSICS_VELOCITY_LINEAR

#  include <boost/multi_array.hpp>

#  include "libLSS/physics/velocity/velocity.hpp"

namespace LibLSS {

  namespace VelocityModel {

    class LinearModel : public Base {
    public:
    
    protected:
      LibLSS::FFTW_Manager<double, 3> mgr;

    public:
      LinearModel(BoxModel box_out_, ARGS, mgr(box_out_.N0, box_out_.N1, box_out_.N2, model_->communicator()) {
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

      void getVelocityField(ARGS);
      virtual void pushAG(ARGS);

    }; // class LinearModel
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
