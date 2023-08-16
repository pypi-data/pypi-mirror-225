/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_messenger.cpp
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
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/hdf5_error.hpp"

using namespace LibLSS;

typedef GSL_RandomNumber RGenType;

int main(int argc, char **argv)
{
    MPI_Communication *comm = setupMPI(argc, argv); 
    StaticInit::execute();
    Console::instance().setVerboseLevel<LOG_DEBUG>();
    MarkovState state;
    SLong *N0, *N1, *N2;
    SDouble *L0, *L1, *L2;
    RGenType randgen;

    state.newElement("random_generator", new RandomStateElement<RandomNumber>(&randgen));

    state.newElement("N0", N0 = new SLong());
    state.newElement("N1", N1 = new SLong());
    state.newElement("N2", N2 = new SLong());

    state.newElement("L0", L0 = new SDouble());
    state.newElement("L1", L1 = new SDouble());
    state.newElement("L2", L2 = new SDouble());

    state.newElement("s_field", new ArrayType(boost::extents[32][32][32]), true);

    N0->value = 32;
    N1->value = 32;
    N2->value = 32;

    state.newSyScalar<long>("localN0", N0->value);
    state.newSyScalar<long>("startN0", 0);
    state.newSyScalar<long>("NUM_MODES", 100);
    
    MessengerSampler s(comm);
    
    // Initialize (data,s)->t sampler
    s.init_markov(state);
    
    // Build some mock field
    ArrayType *field = state.get<ArrayType>("data_field");
    
    field->eigen().fill(0);
    (*field->array)[16][16][16] = 1;

    // Build some s field
    ArrayType *s_field = state.get<ArrayType>("s_field");
    
    s_field->eigen().fill(0);
    (*s_field->array)[16][16][16] = 1;

    
    // Setup messenger parameters
    ArrayType *mmask = state.get<ArrayType>("messenger_mask");
    mmask->eigen().fill(0);
    
    state.get<SDouble>("messenger_tau")->value = 0.0;
    
    
    s.sample(state);
    
    {
        H5::H5File f("dump.h5", H5F_ACC_TRUNC);
        state.saveState(f);
        auto f2 = std::make_shared<H5::H5File>("dump_snap.h5", H5F_ACC_TRUNC);
        state.mpiSaveState(f2, comm, true /* We do not do reassembly but there is only one node */, true);
    }
    
    
    StaticInit::finalize();
    
    return 0;
}
