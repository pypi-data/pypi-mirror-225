/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_messenger3.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/ares/gibbs_messenger.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/samplers/ares/powerspectrum_a_sampler.hpp"

using namespace LibLSS;

typedef GSL_RandomNumber RGenType;


int main(int argc, char **argv)
{
    StaticInit::execute();
    MPI_Communication *mpi_world = setupMPI(argc, argv);
    Console::instance().setVerboseLevel<LOG_DEBUG>();
    MarkovState state;
    SLong *N0, *N1, *N2, *N2_HC, *NUM_MODES, *localN0, *startN0, *fourierLocalSize;
    SDouble *L0, *L1, *L2, *K_MIN, *K_MAX;
    RGenType randgen;
    ArrayType1d *ps;
    IArrayType *k_keys;

    state.newElement("random_generator", new RandomGen(&randgen));

    state.newElement("fourierLocalSize", fourierLocalSize = new SLong());
    state.newElement("localN0", localN0 = new SLong());
    state.newElement("startN0", startN0 = new SLong());
    state.newElement("N0", N0 = new SLong());
    state.newElement("N1", N1 = new SLong());
    state.newElement("N2", N2 = new SLong());
    state.newElement("N2_HC", N2_HC = new SLong());

    state.newSyScalar("messenger_signal_blocked", false);
    state.newSyScalar("power_sampler_a_blocked", false);
    state.newSyScalar("power_sampler_b_blocked", false);

    state.newElement("NUM_MODES", NUM_MODES = new SLong());
    state.newElement("K_MIN", K_MIN = new SDouble());
    state.newElement("K_MAX", K_MAX = new SDouble());


    NUM_MODES->value = 100;
    K_MIN->value = 0;
    K_MAX->value = 2.;

    state.newElement("L0", L0 = new SDouble());
    state.newElement("L1", L1 = new SDouble());
    state.newElement("L2", L2 = new SDouble());

    localN0->value = 64;
    startN0->value = 0;
    N0->value = 64;
    N1->value = 64;
    N2->value = 64;
    N2_HC->value = 33;
    fourierLocalSize->value = 64*64*33;

    L0->value = 200;
    L1->value = 200;
    L2->value = 200;

    MessengerSampler s(mpi_world);
    MessengerSignalSampler s2(mpi_world);
    PowerSpectrumSampler_a p(mpi_world);

    // Initialize (data,s)->t sampler
    s.init_markov(state);
    s2.init_markov(state);
    p.init_markov(state);

    ArrayType1d::ArrayType& k_val = *state.get<ArrayType1d>("k_modes")->array;
    int Nk  = NUM_MODES->value;

    s2.setMockGeneration(true);

    // Fill up powerspectrum
    ps = state.get<ArrayType1d>("powerspectrum");
    for (int k = 1; k < Nk; k++) {
        (*ps->array)[k] = pow(k_val[k], -2);
    }

    // Build some mock field
    ArrayType *field = state.get<ArrayType>("data_field");

    field->eigen().fill(0);

    // Setup messenger parameters
    ArrayType *mmask = state.get<ArrayType>("messenger_mask");
    mmask->eigen().fill(-1);

    (*mmask->array)[16][16][16] = 0;

    state.get<SDouble>("messenger_tau")->value = 1.; // Remove any sign of data. I should add a mechanism to generate unconstrained realizations


    // First round is unconstrained
    s2.sample(state);
    s2.setMockGeneration(false);
    field->eigen() = state.get<ArrayType>("s_field")->eigen();

    s.sample(state);
    s2.sample(state);
    p.sample(state);
    s.sample(state);
    s2.sample(state);
    p.sample(state);
    s.sample(state);
    s2.sample(state);
    p.sample(state);

    {
        H5::H5File f("dump.h5", H5F_ACC_TRUNC);
        state.saveState(f);
    }


    StaticInit::finalize();

    doneMPI();

    return 0;
}
