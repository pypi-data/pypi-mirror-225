/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/sum.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2019 Doogesh Kodi Ramanah <ramanah@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_SUM_FORWARD_MODEL_HPP
#  define __LIBLSS_SUM_FORWARD_MODEL_HPP

#  include <boost/multi_array.hpp>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include <list>
#  include <boost/variant.hpp>

namespace LibLSS {

  class SumForwardModel : public BORGForwardModel {
  public:
    SumForwardModel(MPI_Communication *comm, const BoxModel &box);

    SumForwardModel(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox);

    ~SumForwardModel() override;

    void forwardModel_v2(ModelInput<3> delta_init) override;

    void getDensityFinal(ModelOutput<3> output) override;

    void clear_chain();

    // adjointModel auto release particles. Beware !

    void adjointModel_v2(ModelInputAdjoint<3> gradient_delta) override;
    void getAdjointModelOutput(ModelOutputAdjoint<3> ag_output) override;
    void releaseParticles() override;

    void addModel(std::shared_ptr<BORGForwardModel> model);

    void setAdjointRequired(bool required) override;
    void clearAdjointGradient() override; 

    void setModelParams(ModelDictionnary const& params) override;

    boost::any getModelParam(std::string const& name, std::string const& param) override;

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
