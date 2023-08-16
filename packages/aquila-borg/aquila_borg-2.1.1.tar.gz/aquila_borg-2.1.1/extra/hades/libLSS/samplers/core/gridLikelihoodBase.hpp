/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/core/gridLikelihoodBase.hpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SAMPLERS_CORE_GRID_LIKELIHOOD_BASE_HPP
#  define __LIBLSS_SAMPLERS_CORE_GRID_LIKELIHOOD_BASE_HPP

#  include <array>
#  include <tuple>
#  include <vector>
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/mcmc/global_state.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/samplers/core/likelihood.hpp"

namespace LibLSS {

  template <int Dims>
  class GridDensityLikelihoodBase : virtual public LikelihoodBase {
  public:
    typedef std::array<size_t, Dims> GridSizes;
    typedef std::array<double, Dims> GridLengths;
    typedef std::array<ssize_t, Dims> Index;

    typedef boost::multi_array_ref<double, Dims> ArrayRef;
    typedef boost::multi_array_ref<std::complex<double>, Dims> CArrayRef;

    GridDensityLikelihoodBase(
        MPI_Communication *comm, GridSizes const &N, GridLengths const &L);
    virtual ~GridDensityLikelihoodBase();

    void commitAuxiliaryFields(MarkovState &state) override {}

    virtual void
    generateMockData(CArrayRef const &parameters, MarkovState &state) = 0;

    /*
     * This is the opposite of log likelihood, Fourier representation. The same
     * rules applies as for the real space variant. The modes must be
     * in unit of Volume as per the continuous Fourier transform.
     */
    virtual double
    logLikelihood(CArrayRef const &parameters, bool gradientIsNext = false) = 0;

    /*
     * This computes the opposite of the log likelihood. If gradientIsnext is
     * true the model has to prepare itself for a gradientLikelihood call.
     * Otherwise it can free temporary memory used to compute the forward model.
     * This variant takes the image in real space representation. The input is
     * preserved as indicated by the const.
     */
    virtual double
    logLikelihood(ArrayRef const &parameters, bool gradientIsNext = false) = 0;

    /*
     * This is the gradient of the logarithm of the opposite of the log
     * likelihood (Fourier representation variant).
     * The same rules applies as for the real space variant.
     */
    virtual void gradientLikelihood(
        CArrayRef const &parameters, CArrayRef &gradient_parameters,
        bool accumulate = false, double scaling = 1.0) = 0;

    /*
    * This is the gradient of the opposite of the log likelihood. It
    * returns the gradient in real space representation.
    * You must have called logLikelihood with gradientIsNext=true first.
    * If accumulate is set to true, the gradient will be summed with existing values.
    * 'scaling' indicates by how much the gradient must be scaled before accumulation.
    */
    virtual void gradientLikelihood(
        ArrayRef const &parameters, ArrayRef &gradient_parameters,
        bool accumulate = false, double scaling = 1.0) = 0;

  protected:
    typedef std::tuple<std::array<ssize_t, Dims>, double> SpecialType;
    typedef FFTW_Manager<double, Dims> Mgr;
    std::vector<SpecialType> special_cases;
    GridSizes N;
    GridLengths L;
    long Ncat;
    MPI_Communication *comm;
    double volume;
    std::shared_ptr<Mgr> mgr;
    typename Mgr::plan_type analysis_plan;

    void computeFourierSpace_GradientPsi(
        ArrayRef &real_gradient, CArrayRef &grad_array, bool accumulate,
        double scaling);

  public:
    std::shared_ptr<Mgr> getManager() { return mgr; }
  };

  class ForwardModelBasedLikelihood : public GridDensityLikelihoodBase<3> {
  public:
    ForwardModelBasedLikelihood(
        MPI_Communication *comm, GridSizes const &N, GridLengths const &L)
        : GridDensityLikelihoodBase<3>(comm, N, L) {}

    virtual std::shared_ptr<BORGForwardModel> getForwardModel() = 0;
  };

} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
