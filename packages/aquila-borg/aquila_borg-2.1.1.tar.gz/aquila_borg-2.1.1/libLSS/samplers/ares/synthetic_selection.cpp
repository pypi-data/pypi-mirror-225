/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/synthetic_selection.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/format.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"
#include "libLSS/samplers/ares/synthetic_selection.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"

using namespace LibLSS;
using boost::format;

using boost::extents;

typedef boost::multi_array_types::extent_range range;


void SyntheticSelectionUpdater::initialize(MarkovState& state)
{
    long N0, N1, N2;
    long localN0, startN0;
    long localNdata[6], Ndata[3];
    
    ConsoleContext<LOG_DEBUG> ctx("initialization of Selection updater");
    
    Ncat = static_cast<SLong&>(state["NCAT"]);
    
    N0 = static_cast<SLong&>(state["N0"]);
    localN0 = static_cast<SLong&>(state["localN0"]);
    startN0 = static_cast<SLong&>(state["startN0"]);
    N1 = static_cast<SLong&>(state["N1"]);
    N2 = static_cast<SLong&>(state["N2"]);
    state.getScalarArray<long,3>("Ndata", Ndata);
    state.getScalarArray<long,6>("localNdata", localNdata);

    Ntot = N0*N1*N2;
    localNtot = localN0*N1*N2;

    for (int c = 0; c < Ncat; c++) {
        SelArrayType *sel_window;
        state.newElement(format("galaxy_synthetic_sel_window_%d") % c, 
            sel_window = new SelArrayType(extents[range(localNdata[0],localNdata[1])][range(localNdata[2],localNdata[3])][range(localNdata[4],localNdata[5])]));

        sel_window->setRealDims(ArrayDimension(Ndata[0], Ndata[1], Ndata[2]));
    }
}

void SyntheticSelectionUpdater::restore(MarkovState& state)
{
    initialize(state);
}

void SyntheticSelectionUpdater::sample(MarkovState& state)
{
    ConsoleContext<LOG_VERBOSE> ctx("processing of 3d selection (including foregrounds)");
    
    for (int c = 0; c < Ncat; c++) {
        SelArrayType *original_selection_grid = state.get<SelArrayType>(format("galaxy_sel_window_%d") % c);
        SelArrayType *sel_grid = state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c);
        IArrayType1d *fgmap = state.get<IArrayType1d>(format("catalog_foreground_maps_%d") % c);
        ArrayType1d *fgvals = state.get<ArrayType1d>(format("catalog_foreground_coefficient_%d") % c);
        int NcatForegrounds = fgmap->array->num_elements();
        
        ctx.format("Copy initial selection for catalog %d", c);
        sel_grid->eigen() = original_selection_grid->eigen();
        
        for (int f = 0; f < NcatForegrounds; f++) {
            int c = (*fgmap->array)[f];
            double val = (*fgvals->array)[f];
            
            ctx.print(format("Applying foreground %d (value %lg) to selection of catalog %d") % f % val % c);
            
            ArrayType *fgField = state.get<ArrayType>(format("foreground_3d_%d") % (c)); 

            auto mergingFunction = [val](double s,double f) { return s*(1 - f * val); };

            // copy_array is parallelized, hopefully later vectorized  
            if (f == 0) {
                LibLSS::copy_array(*sel_grid->array, 
                  b_fused<double>(*original_selection_grid->array,
                                  *fgField->array, 
                                  mergingFunction
                                 )
                );
            } else {
                LibLSS::copy_array(*sel_grid->array, 
                  b_fused<double>(*sel_grid->array, 
                                  *fgField->array, 
                                  mergingFunction
                                 )
                );
            }
        }
    }
}
