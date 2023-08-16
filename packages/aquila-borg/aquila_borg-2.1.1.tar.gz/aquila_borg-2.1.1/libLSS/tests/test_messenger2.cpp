/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_messenger2.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/ares/gibbs_messenger.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

using namespace LibLSS;

typedef GSL_RandomNumber RGenType;


int main(int argc, char **argv)
{
    StaticInit::execute();
    MPI_Communication *mpi_world = setupMPI(argc, argv);
    Console::instance().setVerboseLevel<LOG_DEBUG>();
    MarkovState state;
    SLong *N0, *N1, *N2;
    SDouble *L0, *L1, *L2;
    RGenType randgen;
    ArrayType1d *ps;
    IArrayType *k_keys;

    state.newElement("random_generator", new RandomStateElement<RandomNumber>(&randgen));

    state.newElement("N0", N0 = new SLong());
    state.newElement("N1", N1 = new SLong());
    state.newElement("N2", N2 = new SLong());

    state.newElement("L0", L0 = new SDouble());
    state.newElement("L1", L1 = new SDouble());
    state.newElement("L2", L2 = new SDouble());

    state.newSyScalar<bool>("messenger_signal_blocked", false);

    state.newSyScalar<long>("NUM_MODES", 100);

    double dk = 2*M_PI/200. * 16 * 2 /100.;
    boost::array<int, 3> N;
    boost::array<double, 3> L;
    N[0] = N[1] = N[2] = 32;
    L[0] = L[1] = L[2] = 200.;
    state.newElement("powerspectrum", ps = new ArrayType1d(boost::extents[100]), true);
    state.newElement("k_keys", k_keys = new IArrayType(boost::extents[32][32][17]));

    for (int ix = 0; ix < 32; ix++) {
        for (int iy = 0; iy < 32; iy++) {
            for (int iz = 0; iz < 17; iz++) {
                boost::array<int, 3> ik;
                ik[0] = ix;
                ik[1] = iy;
                ik[2] = iz;

                (*k_keys->array)[ix][iy][iz] = power_key(N, ik, L, 0, dk, 100);
            }
        }
    }

    ps->eigen().fill(0.00001);

    N0->value = 32;
    N1->value = 32;
    N2->value = 32;

    L0->value = 200;
    L1->value = 200;
    L2->value = 200;

    MessengerSampler s(mpi_world);
    MessengerSignalSampler s2(mpi_world);

    // Initialize (data,s)->t sampler
    s.init_markov(state);
    s2.init_markov(state);

    // Build some mock field
    ArrayType *field = state.get<ArrayType>("data_field");

    field->eigen().fill(0);
    (*field->array)[16][16][16] = 1;

    // Setup messenger parameters
    ArrayType *mmask = state.get<ArrayType>("messenger_mask");
    mmask->eigen().fill(0);

    state.get<SDouble>("messenger_tau")->value = 1;


    s.sample(state);
    s2.sample(state);

    {
        H5::H5File f("dump.h5", H5F_ACC_TRUNC);
        state.saveState(f);
    }


    StaticInit::finalize();

    doneMPI();

    return 0;
}
