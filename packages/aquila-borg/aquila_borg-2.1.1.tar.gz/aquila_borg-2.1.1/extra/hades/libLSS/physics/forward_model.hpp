/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forward_model.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_FORWARD_MODEL_HPP
#define __LIBLSS_BORG_FORWARD_MODEL_HPP

#include <map>
#include <boost/any.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/memusage.hpp"
#include "libLSS/tools/hdf5_type.hpp"
#include "libLSS/physics/model_io.hpp"

namespace LibLSS {

  typedef std::map<std::string, boost::any> ModelDictionnary;

  struct BORGForwardModelTypes {
    typedef FFTW_Manager_3d<double> DFT_Manager;
    typedef boost::multi_array<double, 2> PhaseArray;
    typedef boost::multi_array_ref<double, 2> PhaseArrayRef;
    typedef ModelIO<3>::ArrayRef ArrayRef;
    typedef ModelIO<3>::CArrayRef CArrayRef;
  };

  class outOfBoundParam : virtual public ErrorBase {
  public:
    explicit outOfBoundParam(std::string const &p) : ErrorBase(p) {}
  };

  /**
   * This defines the interface for a forward physical model in BORG.  
   */
  class BORGForwardModel : public BORGForwardModelTypes {
  public:
    std::shared_ptr<DFT_Manager> lo_mgr;
    std::shared_ptr<DFT_Manager> out_mgr;

    MPI_Communication *communicator() { return comm; }

    BORGForwardModel(BORGForwardModel &&other) = default;

    explicit BORGForwardModel(MPI_Communication *comm, const BoxModel &box)
        : comm(comm), L0(box.L0), L1(box.L1), L2(box.L2), N0(box.N0),
          N1(box.N1), N2(box.N2), xmin0(box.xmin0), xmin1(box.xmin1),
          xmin2(box.xmin2), forwardModelHold(false), box_input(box),
          box_output(box) {
      setup(false);
    }

    explicit BORGForwardModel(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &box_out)
        : comm(comm), L0(box.L0), L1(box.L1), L2(box.L2), N0(box.N0),
          N1(box.N1), N2(box.N2), xmin0(box.xmin0), xmin1(box.xmin1),
          xmin2(box.xmin2), forwardModelHold(false), box_input(box),
          box_output(box_out) {
      setup(true);
    }

    virtual ~BORGForwardModel() {
      if (analysis_plan) {
        lo_mgr->destroy_plan(analysis_plan);
        lo_mgr->destroy_plan(synthesis_plan);
      }
    }

    void setName(std::string const &name_) { modelName = name_; }

    void holdParticles() { forwardModelHold = true; }

    // Default is the standard historical behaviour
    virtual PreferredIO getPreferredInput() const { return PREFERRED_FOURIER; }
    virtual PreferredIO getPreferredOutput() const { return PREFERRED_REAL; }

    // This executes the forward model but rely on auxiliary functions to pass down the result. So it holds
    // internal information and need a release call.
    virtual void forwardModelSimple(CArrayRef &delta_init) {
      forwardModel_v2(ModelInput<3>(lo_mgr, box_input, delta_init, true));
    }

    virtual void forwardModel(
        CArrayRef &delta_init, ArrayRef &delta_output, bool adjointNext) {
      // Default implementation uses the v2 interface
      // Warning. adjointNext do not exist anymore in the v2, it is superseded by setAdjointRequired.
      fwrap(delta_init) = fwrap(delta_init) * get_box_model().volume();
      forwardModel_v2(ModelInput<3>(lo_mgr, box_input, delta_init));
      getDensityFinal(ModelOutput<3>(lo_mgr, box_output, delta_output));
    }

    virtual void forwardModel(
        CArrayRef &delta_init, ArrayRef &delta_output, ArrayRef &vx,
        ArrayRef &vy, ArrayRef &vz, bool adjointNext) {
      error_helper<ErrorNotImplemented>(
          "forwardModel is not supported velocity output");
    }
    virtual void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) {
      error_helper<ErrorNotImplemented>(
          "forwardModelRsdField not supported here.");
    }

    /**
     * @brief Run a forwardModel with APIv2. Only the input must be provided.
     * 
     * @param delta_init ModelInput object holding the input array.
     */
    virtual void forwardModel_v2(ModelInput<3> delta_init) {
      error_helper<ErrorNotImplemented>("forwardModel_v2 not supported here.");
    }

    /**
     * @brief Get the output of the forward model.
     * 
     * @param delta_output ModelOutput object holding the output array.
     */
    virtual void getDensityFinal(ModelOutput<3> delta_output) {
      error_helper<ErrorNotImplemented>(
          "forwardModel_v2 (getDensityFinal) not supported here.");
    }

    /**
     * @brief Runs the adjoint model on the provided input vector.
     * 
     * @param ag_delta_input Input vector adjoint model.
     */
    virtual void adjointModel_v2(ModelInputAdjoint<3> ag_delta_input) {
      error_helper<ErrorNotImplemented>("adjointModel_v2 not supported here.");
    }

    /**
     * @brief Changes the behavior of adjointModel_v2 to accumulate all the vectors prior to computing the result.
     *
     * This changes the behavior of the adjoint forward model to accept to
     * accumulate new adjoint vectors before computing the final result through
     * `getAdjointModelOutput`.
     *
     * @param do_accumulate switch on the accumulate behaviour
     */
    virtual void accumulateAdjoint(bool do_accumulate) {
      error_helper<ErrorNotImplemented>("accumulateAdjoint not supported here.");
    }

    /**
     * @brief Retrieve the output vector after the adjoint model has been run.
     * 
     * @param ag_delta_output 
     */
    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) {
      error_helper<ErrorNotImplemented>(
          "adjointModel_v2 (getAdjointModelOutput) not supported here.");
    }

    /**
     * @brief Apply the jacobian
     * 
     * @param gradient_delta 
     */
    [[deprecated("Replaced by adjointModel_v2, with better API")]]
    virtual void adjointModel(ArrayRef &gradient_delta) {
      adjointModel_v2(ModelInputAdjoint<3>(lo_mgr, box_input, gradient_delta));
      getAdjointModelOutput(
          ModelOutputAdjoint<3>(lo_mgr, box_output, gradient_delta));
    }

    virtual void releaseParticles() {}

    void setCosmoParams(const CosmologicalParameters &p_cosmo_params);

    // FIXME: Add a setModelParams API point with model name
    //

    /**
     * @brief set model parameters call for all models subtended by this one.
     *
     * @params params a dictionnary of parameters
     */
    virtual void setModelParams(ModelDictionnary const &params);


    // FIXME: Add a getModelParam without name.

    /**
     * @brief Query a single parameter from a specific sub-model.
     */
    virtual boost::any
    getModelParam(std::string const &name, std::string const &parameterName) {
      return boost::any();
    }

    void setObserver(const ArrayType1d::ArrayType &v) { this->vobs = v; }

    /**
     * @brief Indicate whether an adjoint model is required.
     * The caller indicates it wants to be able to run adjointGradient.
     * This may involve allocating a lot more memory during forward
     * evaluation.
     * 
     * @param on 
     */
    virtual void setAdjointRequired(bool on) {}

    /**
     * @brief Clear the internal buffers for adjoint gradient.
     * 
     */
    virtual void clearAdjointGradient() {}

    void save(CosmoTool::H5_CommonFileGroup &fg) {}

    void restore(CosmoTool::H5_CommonFileGroup &fg) {}

    BoxModel get_box_model() const {
      BoxModel box;

      box.L0 = L0;
      box.L1 = L1;
      box.L2 = L2;
      box.N0 = N0;
      box.N1 = N1;
      box.N2 = N2;
      box.xmin0 = xmin0;
      box.xmin1 = xmin1;
      box.xmin2 = xmin2;
      return box;
    }

    BoxModel get_box_model_output() const { return box_output; }

    virtual bool densityInvalidated() const { return true; }

  private:
    BORGForwardModel(const BORGForwardModel &) {}
    BORGForwardModel &operator=(const BORGForwardModel &) { return *this; }

    void setup(bool distinct_io);

  protected:
    void setupDefault();

    MPI_Communication *comm;
    double L0, L1, L2;
    double volume, volNorm;
    long N0, N1, N2, startN0, localN0, N2_HC, N2real;
    double xmin0, xmin1, xmin2;
    DFT_Manager::plan_type synthesis_plan, analysis_plan;
    bool forwardModelHold;
    BoxModel box_input, box_output;

    std::unique_ptr<DFT_Manager::U_ArrayFourier> tmp_complex_field;
    std::unique_ptr<DFT_Manager::U_ArrayReal> tmp_real_field;

    typedef DFT_Manager::U_ArrayReal U_Array;
    typedef DFT_Manager::U_ArrayFourier U_CArray;

    typedef std::unique_ptr<U_Array> U_Array_p;
    typedef std::unique_ptr<U_CArray> U_CArray_p;

    typedef U_Array::array_type Array;
    typedef U_CArray::array_type CArray;

    CosmologicalParameters cosmo_params;
    ModelDictionnary params;
    ArrayType1d::ArrayType vobs;
    std::string modelName;

    virtual void updateCosmo() {}

    void ensureInputEqualOutput() {
      if (box_input == box_output)
        return;
      error_helper<ErrorBadState>(
          "Input box must be the same as the output box.");
    }
  };

  /**
   * This define a gravity model which uses particles to trace matter flows. 
   */
  class ParticleBasedForwardModel : public BORGForwardModel {
  public:
    using BORGForwardModel::BORGForwardModel;

    typedef boost::multi_array<double, 2>::const_array_view<2>::type
        PhaseSubArray;
    typedef boost::multi_array<double, 2>::array_view<2>::type PhaseSubArrayRW;
    typedef boost::multi_array<size_t, 1>::const_array_view<1>::type IdSubArray;
    typedef std::function<void(
        double, size_t, IdSubArray, PhaseSubArray, PhaseSubArray)>
        StepNotifier;

    StepNotifier currentNotifier;

    virtual IdSubArray getLagrangianIdentifiers() const {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      error_helper<ErrorNotImplemented>(
          "getLagrangianIdentifiers is not implemented for this model.");
      return boost::multi_array_ref<size_t, 1>(
          0, boost::extents[0])[i_gen[range()]];
    }

    virtual size_t getNumberOfParticles() const = 0;

    /**
     * @brief Get the Particle Positions object
     * 
     * @return PhaseSubArray 
     */
    virtual PhaseSubArray getParticlePositions() = 0;

    /**
     * @brief Get the Particle Velocities object
     * 
     * @return PhaseSubArray 
     */
    virtual PhaseSubArray getParticleVelocities() = 0;

    /**
     * @brief Get the Velocity Multiplier 
     * 
     * @return double 
     */
    virtual double getVelocityMultiplier() { return 1.0; }

    /**
     * @brief Get the Supersampling Rate 
     * 
     * @return unsigned int 
     */
    virtual unsigned int getSupersamplingRate() const = 0;

    /**
     * @brief 
     * 
     * This computes the adjoint gradient on the particle positions, velocities
     * Not all models may support this. The default implementation triggers an error.
     *
     * @param grad_pos 
     * @param grad_vel 
     */
    virtual void
    adjointModelParticles(PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel) {
      error_helper<ErrorNotImplemented>(
          "adjointModelParticles is not implemented in this model.");
    }

    virtual void setStepNotifier(StepNotifier notifier) {
      currentNotifier = notifier;
    }
  };

  /**
   * This is a type alias to specify how to store the BORG gravity model
   * in the MarkovState dictionnary.
   */
  typedef SharedObjectStateElement<BORGForwardModel> BorgModelElement;

  template <typename Model>
  void borgSaveParticles(
      CosmoTool::H5_CommonFileGroup &g, Model &m, bool savepos, bool savevel,
      int step = -1) {
    typedef boost::multi_array<double, 2> VectorArray;
    typedef UninitializedArray<VectorArray> U_VectorArray;
    using range = boost::multi_array_types::index_range;
    size_t numPart = m.getNumberOfParticles();
    U_VectorArray pos_vel(boost::extents[numPart][3]);

    if (savepos) {
      m.copyParticlePositions(pos_vel.get_array(), step);
      CosmoTool::hdf5_write_array(g, "u_pos", pos_vel.get_array());
    }

    if (savevel) {
      m.copyParticleVelocities(pos_vel.get_array(), step);
      CosmoTool::hdf5_write_array(g, "u_vel", pos_vel.get_array());
    }

    auto ids = m.getLagrangianIdentifiers();
    typename decltype(ids)::index_gen i_gen;

    boost::multi_array<size_t, 1> final_ids(boost::extents[numPart]);
    LibLSS::copy_array(final_ids, ids[i_gen[range(0, numPart)]]);

    CosmoTool::hdf5_write_array(g, "u_lagrangian_id", final_ids);
  }

}; // namespace LibLSS

#endif
