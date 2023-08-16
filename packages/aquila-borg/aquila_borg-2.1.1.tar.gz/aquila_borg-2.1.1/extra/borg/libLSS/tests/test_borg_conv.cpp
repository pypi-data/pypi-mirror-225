/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_borg_conv.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/physics/cosmo.hpp"
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include "libLSS/samplers/borg/borg_conv_likelihood.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"

using namespace LibLSS;
using namespace LibLSS::CNN;
using CosmoTool::square;
using boost::format;
using std::string;

#define LAYERS 5
//#define CONV 2
#define GRIDSIZE 64
#define DO_RSD false
#define LIGHTCONE false

#define MODEL_TO_TEST(obj) BorgLptModel<> *obj = new BorgLptModel<>(comm, box, DO_RSD, 1, 0.001, LIGHTCONE)

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberMPI<GSL_RandomNumber> RGenType;

static const bool TEST_BORG_REDSHIFT = true;

int main(int argc, char **argv)
{
    MPI_Communication *comm = setupMPI(argc, argv);
    StaticInit::execute();
#if !defined(ARES_MPI_FFTW) && defined(_OPENMP)
    fftw_plan_with_nthreads(smp_get_max_threads());
#endif

    Console& cons = Console::instance();
    cons.setVerboseLevel<LOG_DEBUG>();

    cons.outputToFile(boost::str(format("fwd_test_rank_%d.txt") % comm->rank()));
    {
    MarkovState state;
    RGenType randgen(comm, -1);
    BoxModel box;

    randgen.seed(2348098);

    state.newElement("random_generator", new RandomStateElement<RandomNumber>(&randgen));

    //state.newSyScalar<long>("C0", CONV);
    //state.newSyScalar<long>("C1", CONV);
    //state.newSyScalar<long>("C2", CONV);
    state.newSyScalar<long>("tot_num_conv", LAYERS);

    //boost::multi_array<double, 1> bias_params(boost::extents[LAYERS * CONV * CONV * CONV + LAYERS]);
    boost::multi_array<double, 1> bias_params(boost::extents[LAYERS * 4 + LAYERS]);
    fwrap(bias_params) = 0.;
    //bias_params[LAYERS * CONV * CONV * CONV] = 0.;
    for (int ind = 0; ind < LAYERS; ind++) {
        bias_params[4 * ind] = 1.;
    }
    LibLSS_test::setup_hades_test_run(comm, GRIDSIZE, 100, state, &bias_params);
    LibLSS_test::setup_box(state, box);
    state.newScalar<bool>("borg_do_rsd", TEST_BORG_REDSHIFT);

    BorgConvDensitySampler s(comm, 10, 0.1);

    MODEL_TO_TEST(model);

    BorgModelElement *model_element = new BorgModelElement();

    model_element->obj = model;

    state.newElement("BORG_model", model_element);

    s.init_markov(state);

    s.generateMockData(state, false);

    {
        H5::Group g;

        if (comm->rank() != 0) {
           string tmpname(str(format("tmp.h5_rank_%d")  % comm->rank()));
           H5::H5File f(tmpname, H5F_ACC_TRUNC);

           state.mpiSaveState(f, comm, false);
           unlink(tmpname.c_str());
        } else {
           H5::H5File f("dump.h5", H5F_ACC_TRUNC);

           state.mpiSaveState(f, comm, false);
        }

    }

    }
    StaticInit::finalize();
    doneMPI();

    return 0;
}
