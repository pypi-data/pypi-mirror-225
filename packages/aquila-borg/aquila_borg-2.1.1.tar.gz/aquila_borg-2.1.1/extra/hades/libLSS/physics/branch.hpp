/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/branch.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2019 Doogesh Kodi Ramanah <ramanah@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_BRANCH_FORWARD_MODEL_HPP
#  define __LIBLSS_BRANCH_FORWARD_MODEL_HPP

#  include <boost/multi_array.hpp>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include <list>
#  include <boost/variant.hpp>

namespace LibLSS {

  class BranchForwardModel : public BORGForwardModel {
  public:
    ModelOutput<3> final_output;
    ModelOutputAdjoint<3> ag_final_output;
    typedef std::shared_ptr<DFT_Manager::U_ArrayReal> S_U_ArrayReal;
    typedef std::shared_ptr<DFT_Manager::U_ArrayFourier> S_U_ArrayFourier;
    S_U_ArrayReal final_real, ag_final_real;
    S_U_ArrayFourier final_fourier, ag_final_fourier;
    boost::variant<S_U_ArrayReal, S_U_ArrayFourier> previous, next;

    BranchForwardModel(MPI_Communication *comm, const BoxModel &box);

    BranchForwardModel(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox);

    ~BranchForwardModel() override;

    void forwardModelSimple(CArrayRef &delta_init) override;

    void forwardModel_v2(ModelInput<3> delta_init) override;

    void getDensityFinal(ModelOutput<3> output) override;

    void clear_chain();

    void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) override;

    // adjointModel auto release particles. Beware !

    void adjointModel_v2(ModelInputAdjoint<3> gradient_delta) override;
    void getAdjointModelOutput(ModelOutputAdjoint<3> ag_output) override;
    void releaseParticles() override;

    void addModel(std::shared_ptr<BORGForwardModel> model);

    void setAdjointRequired(bool required) override;
    void clearAdjointGradient() override; 

  protected:
    std::list<std::shared_ptr<BORGForwardModel>> model_list;

    void updateCosmo() override;
  };
}; // namespace LibLSS

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2020
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: year(1) = 2018-2019
