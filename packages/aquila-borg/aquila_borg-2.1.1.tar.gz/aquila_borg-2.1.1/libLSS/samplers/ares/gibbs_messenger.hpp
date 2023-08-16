/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/gibbs_messenger.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GIBBS_MESSENGER_HPP
#define __LIBLSS_GIBBS_MESSENGER_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

namespace LibLSS {

    namespace GibbsMessenger {

        namespace details {

            typedef FFTW_Manager_3d<double> FFTMgr;

            class MessengerSampler: public MarkovSampler {
            protected:
                long N0, N1, N2, Ntot, N_k;
                long localN0, startN0, localNtot;
                ArrayType *messenger_mask, *data_field;
                SDouble *messenger_tau;
                RandomGen *rng;
                bool constrainedGeneration;
                MPI_Communication *comm;
                FFTMgr *mgr;
            public:
                MessengerSampler(MPI_Communication *comm);
                virtual ~MessengerSampler();

                virtual void restore(MarkovState& state);
                virtual void initialize(MarkovState& state);
                virtual void sample(MarkovState& state);

                void setMockGeneration(bool b) { constrainedGeneration = !b; }

            };

            class MessengerSignalSampler: public MarkovSampler {
            protected:
                typedef boost::multi_array_ref< IArrayType::ArrayType::element, 1> FlatIntType;
                long fourierLocalSize;
                FCalls::plan_type analysis_plan, synthesis_plan;
                FCalls::complex_type *tmp_fourier, *tmp_fourier_m;
                FlatIntType *flat_key;
                double volNorm;
                long N0, N1, N2, Ntot, Ntot_k, N_k;
                long startN0, localN0, localNtot, localNtot_k;
                double L0, L1, L2, volume;
                ArrayType *tmp_m_field, *x_field, *s_field;
                bool constrainedGeneration;
                MPI_Communication *comm;
                FCalls::real_type *tmp_real_field;
                FFTMgr *mgr;
            public:
                MessengerSignalSampler(MPI_Communication* comm);
                virtual ~MessengerSignalSampler();

                virtual void restore(MarkovState& state);
                virtual void initialize(MarkovState& state);
                virtual void sample(MarkovState& state);

                void setMockGeneration(bool b) { constrainedGeneration = !b; }

            };

            class CatalogProjectorSampler: public MarkovSampler {
            protected:
                int Ncat;
                MPI_Communication *comm;
                bool mockGeneration;
            public:
                CatalogProjectorSampler(MPI_Communication *comm0): comm(comm0), mockGeneration(false) {}

                virtual void restore(MarkovState& state);
                virtual void initialize(MarkovState& state);
                virtual void sample(MarkovState& state);

                void setMockGeneration(bool b) { mockGeneration = b; }
            };
        }
    }

    using GibbsMessenger::details::MessengerSampler;
    using GibbsMessenger::details::MessengerSignalSampler;
    using GibbsMessenger::details::CatalogProjectorSampler;
}

#endif
