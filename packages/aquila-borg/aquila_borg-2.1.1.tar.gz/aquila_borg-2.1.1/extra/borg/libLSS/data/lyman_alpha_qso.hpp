/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/data/lyman_alpha_qso.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DATA_LYMAN_ALPHA_HPP
#define __LIBLSS_DATA_LYMAN_ALPHA_HPP

#include <H5Cpp.h>
#include <boost/utility/base_from_member.hpp>
#include <boost/mpl/assert.hpp>
#include <boost/utility/enable_if.hpp>
#include <boost/multi_array.hpp>
#include <boost/function.hpp>
#include <healpix_cxx/pointing.h>
#include "libLSS/data/base.hpp"
#include "libLSS/tools/allocator_policy.hpp"
#include "libLSS/tools/checkmem.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/projector.hpp"

namespace LibLSS
{
    template<class GT,class AllocationPolicy = DefaultAllocationPolicy>
    class LymanAlphaSurvey: virtual LibLSS::Base_Data
    {
    public:
        typedef GT QSOType;
        typedef LOSContainer LOSType;
        typedef typename boost::multi_array<QSOType, 1> QSOArray;
        typedef typename boost::multi_array<LOSType, 1> ProjectionArray;
    protected:
        QSOArray QSO;
        ProjectionArray projection;
        long numQSO;
        long numLOS;
        
    public:
        LymanAlphaSurvey() : numQSO(0), numLOS(0) {}
        ~LymanAlphaSurvey() {}	
        		
        long NumberQSO() const { return numQSO; }
        long NumberLOS() const { return numLOS; }
        
        // Methods defined in the tcc file
        void addQSO(const QSOType& qso);
        void addLOS(LOSType& los);
        
        QSOArray& getQSO() { return QSO; }
        const QSOArray& getQSO() const { return QSO; }
        
        ProjectionArray& getProjection() {return projection; }
        const ProjectionArray& getProjection() const {return projection; }
        
        void optimize() {
           QSO.resize(boost::extents[numQSO]);
        }
        
        void saveMain(H5::H5Location& fg);
        void restoreMain(H5::H5Location& fg);

        void save(H5::H5Location& fg) { saveMain(fg); }
        void restore(H5::H5Location& fg) { restoreMain(fg); }

    };

};

#include "lyman_alpha_qso.tcc"

#endif
