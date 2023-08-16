/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/julia_slice.hpp
    Copyright (C) 2014-2020 2018-2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __JULIA_META_SLICE_HPP
#  define __JULIA_META_SLICE_HPP

#  include <vector>
#  include "libLSS/samplers/core/markov.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"
#  include "libLSS/hmclet/mass_burnin.hpp"
#  include "libLSS/hmclet/dense_mass.hpp"
#  include "libLSS/samplers/julia/julia_likelihood.hpp"

namespace LibLSS {

  class JuliaMetaSlice : public MarkovSampler {
  protected:
    GhostPlanes<double, 2> ghosts;
    std::string module_name;
    size_t N0, N1, N2, N2real, localN0, startN0, Ncatalog;
    MPI_Communication *comm;

    typedef HMCLet::MassMatrixWithBurnin<HMCLet::DenseMassMatrix> mass_t;

    std::vector<std::shared_ptr<mass_t>> covariances;

    std::shared_ptr<JuliaDensityLikelihood> likelihood;
    size_t burnin, memorySize;

  public:
    JuliaMetaSlice(
        MPI_Communication *comm, const std::string &likelihood_module,
        std::shared_ptr<JuliaDensityLikelihood> likelihood_, size_t burnin_,
        size_t memorySize_);
    ~JuliaMetaSlice();

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2018-2019
