/*+
    ARES/HADES/BORG Package -- ./libLSS/data/spectro_gals.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DATA_GALACTIC_HPP
#define __LIBLSS_DATA_GALACTIC_HPP

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
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS
{
    class NoSelection {
    public:
        int getNumRadial() const {return 1;}
        double getRadialSelection(double r, int n) const { return 1; }
        double get_sky_completeness(double x, double y, double z) const { return 1; }
    };

    HAS_MEM_FUNC(saveFunction, has_save_function);
    HAS_MEM_FUNC(loadFunction, has_load_function);

    /* These are two helper functions. Depending on the availability of the
     * member function void T::saveFunction(H5_CommonFileGroup&), the function
     * will be executed (or not if it does not exist). This ensures
     * that GalaxySurvey always try to save the maximum but still is
     * compatible with restricted selection functions.
     */
    namespace details {

        template<typename T>
        typename boost::enable_if< has_save_function<T, void (T::*)(H5_CommonFileGroup&)> >::type
           saveRadialCompleteness(H5_CommonFileGroup& fg, T& func)
        {
            func.saveFunction(fg);
        }

        template<typename T>
        typename boost::disable_if< has_load_function<T, void (T::*)(H5_CommonFileGroup&)> >::type
           saveRadialCompleteness(H5_CommonFileGroup& fg, T& func)

        {
        }

        template<typename T>
        typename boost::enable_if< has_load_function<T, void (T::*)(H5_CommonFileGroup&)> >::type
           loadRadialCompleteness(H5_CommonFileGroup& fg, T& func)
        {
            func.loadFunction(fg);
        }

        template<typename T>
        typename boost::disable_if< has_save_function<T, void (T::*)(H5_CommonFileGroup&)> >::type
           loadRadialCompleteness(H5_CommonFileGroup& fg, T& func)

        {
        }

        static double nullCorrection(double d) { return 0; }

    };

    typedef boost::function1<double, double> CorrectionFunction;

    template<typename SelFunction, class GT, class AllocationPolicy = DefaultAllocationPolicy>
    class GalaxySurvey: virtual LibLSS::Base_Data
    {
    public:
        typedef GT GalaxyType;
        typedef GT& RefGalaxyType;
        typedef const GT& ConstRefGalaxyType;
        typedef typename boost::multi_array<GalaxyType, 1> GalaxyArray;
    protected:
        GalaxyArray galaxies;
        long numGalaxies;
        SelFunction radialSelection;
        bool is_reference_survey;
        CorrectionFunction zcorrection;
    public:
        GalaxySurvey(bool ref_survey = false) : numGalaxies(0), is_reference_survey(ref_survey) {}
        ~GalaxySurvey() {}

        SelFunction& selection() { return radialSelection; }
        const SelFunction& selection() const { return radialSelection; }

        double getCompleteness(double phi, double theta) {
            vec3 v(pointing(0.5*M_PI - theta, phi));
            return radialSelection.get_sky_completeness(v.x, v.y, v.z);
        }

        void setSelectionFunction(SelFunction f) {
            radialSelection = f;
        }

        bool isReferenceSurvey() const { return is_reference_survey; }

        RefGalaxyType operator[](size_t i)  {
            return galaxies[i];
        }

        ConstRefGalaxyType operator[](size_t i) const {
            return galaxies[i];
        }

        void optimize() {
           galaxies.resize(boost::extents[numGalaxies]);
        }

        long surveySize() const { return numGalaxies; }

        // Methods defined in the tcc file
        void addGalaxy(const GalaxyType& g);

        // I/O support for galaxy surveys
        void saveMain(H5_CommonFileGroup& fg);
        void restoreMain(H5_CommonFileGroup& fg);

        void save(H5_CommonFileGroup& fg) {
            saveMain(fg);
            details::saveRadialCompleteness(fg, radialSelection);
        }

        void restore(H5_CommonFileGroup& fg) {
            restoreMain(fg);
            details::loadRadialCompleteness(fg, radialSelection);
        }

        void updateComovingDistance(const Cosmology& cosmo, const CorrectionFunction& zcorrection = details::nullCorrection);

        void useLuminosityAsWeight();
        void resetWeight();

        void setCorrections(const CorrectionFunction& zcorrection = details::nullCorrection) { this->zcorrection = zcorrection; }

        //
        GalaxyArray& getGalaxies() { return galaxies; }
        const GalaxyArray& getGalaxies() const { return galaxies; }
        GalaxyArray& allocateGalaxies(size_t numGals) { 
            numGalaxies = numGals;
            galaxies.resize(boost::extents[numGals]);
            return galaxies;
        }
    };

};

#include "spectro_gals.tcc"

#endif
