#ifndef __LIBLSS_HMCLET_MASS_SAVER_HPP
#define __LIBLSS_HMCLET_MASS_SAVER_HPP

#include <CosmoTool/hdf5_array.hpp>

#include "libLSS/hmclet/hmclet.hpp"
#include "libLSS/hmclet/hmclet_qnhmc.hpp"

namespace LibLSS {

  namespace HMCLet {

    template <typename Mass_t>
    struct MassSaver {
      Mass_t &mass;

      MassSaver(Mass_t &mass_) : mass(mass_) {}

      void save(CosmoTool::H5_CommonFileGroup &fg) { mass.saveMass(fg); }

      void restore(CosmoTool::H5_CommonFileGroup &fg) { mass.loadMass(fg); }
    };

    template <typename Mass_t, typename BMass_t>
    struct QNMassSaver {
      Mass_t &mass;
      BMass_t &B;

      QNMassSaver(Mass_t &mass_, BMass_t& b_) : mass(mass_), B(b_) {}

      void save(CosmoTool::H5_CommonFileGroup &fg) { mass.saveMass(fg); B.save(fg); }

      void restore(CosmoTool::H5_CommonFileGroup &fg) { mass.loadMass(fg); B.load(fg); }
    };
    template <typename Mass_t>
    static void add_saver(
        MarkovState &state, std::string const &name,
        std::unique_ptr<SimpleSampler<Mass_t>> &sampler) {
      Console::instance().print<LOG_DEBUG>(
          "Creating a saver for the mass matrix in " + name);
      auto obj_elt = new ObjectStateElement<MassSaver<Mass_t>, true>();
      obj_elt->obj = new MassSaver<Mass_t>(sampler->getMass());
      state.newElement(name, obj_elt, true);
    }

    template <typename Mass_t>
    static void add_saver(
        MarkovState &state, std::string const &name,
        std::unique_ptr<QNHMCLet::Sampler<Mass_t,QNHMCLet::BDense>> &sampler) {
      Console::instance().print<LOG_DEBUG>(
          "Creating a saver for the QN mass matrix in " + name);
      auto obj_elt = new ObjectStateElement<QNMassSaver<Mass_t,QNHMCLet::BDense>, true>();
      obj_elt->obj = new QNMassSaver<Mass_t,QNHMCLet::BDense>(sampler->getMass(), sampler->getB());
      state.newElement(name, obj_elt, true);
    }


  } // namespace HMCLet

} // namespace LibLSS

#endif
