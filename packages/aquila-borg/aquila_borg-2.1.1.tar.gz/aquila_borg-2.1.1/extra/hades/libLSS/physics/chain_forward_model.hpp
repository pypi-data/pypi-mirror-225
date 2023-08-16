/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/chain_forward_model.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2019 Doogesh Kodi Ramanah <ramanah@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_CHAIN_FORWARD_MODEL_HPP
#  define __LIBLSS_CHAIN_FORWARD_MODEL_HPP

#  include <boost/multi_array.hpp>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include <list>
#  include <map>
#  include <boost/variant.hpp>

namespace LibLSS {

  class ChainForwardModel : public BORGForwardModel {
  public:
    ModelOutput<3> final_output;
    ModelOutputAdjoint<3> ag_final_output;
    typedef std::shared_ptr<DFT_Manager::U_ArrayReal> S_U_ArrayReal;
    typedef std::shared_ptr<DFT_Manager::U_ArrayFourier> S_U_ArrayFourier;
    S_U_ArrayReal final_real, ag_final_real;
    S_U_ArrayFourier final_fourier, ag_final_fourier;
    boost::variant<S_U_ArrayReal, S_U_ArrayFourier> previous, next;
    bool accumulate;
    ModelInputAdjoint<3> accumulateAg;

    ChainForwardModel(MPI_Communication *comm, const BoxModel &box);

    ChainForwardModel(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox);

    virtual ~ChainForwardModel();

    bool densityInvalidated() const override;

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

    void
    addModel(std::shared_ptr<BORGForwardModel> model, std::string const &name);

    std::shared_ptr<BORGForwardModel> queryModel(std::string const &name);

    void setAdjointRequired(bool required) override;

    void clearAdjointGradient() override;

    void setModelParams(ModelDictionnary const &params) override;

    boost::any getModelParam(
        std::string const &model_name, std::string const &parameter) override;

    void accumulateAdjoint(bool do_accumulate) override;

  protected:
    std::list<std::shared_ptr<BORGForwardModel>> model_list;
    std::list<std::shared_ptr<BORGForwardModel>> model_list_adjoint;
    std::map<std::string, std::shared_ptr<BORGForwardModel>> named_models;

    void updateCosmo() override;

    void trigger_ag();
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
