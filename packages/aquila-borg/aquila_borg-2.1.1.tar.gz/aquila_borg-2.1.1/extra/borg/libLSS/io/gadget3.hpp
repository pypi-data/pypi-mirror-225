/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/io/gadget3.hpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_GADGET3_HPP
#  define __LIBLSS_BORG_GADGET3_HPP

#  include <boost/multi_array.hpp>
#  include "CosmoTool/hdf5_array.hpp"
#  include "libLSS/tools/hdf5_scalar.hpp"
#  include "libLSS/physics/cosmo.hpp"

namespace LibLSS {
  namespace IO {
    typedef size_t particleID_t;
    typedef boost::multi_array<particleID_t, 1> arrayID_t;
    typedef boost::multi_array<double, 2> arrayPosition_t;
    typedef boost::multi_array<double, 2> arrayVelocity_t;
    
    constexpr static double P_UnitLength_in_cm=3.085678e24; // 1.0 Mpc in cm
    constexpr static double P_UnitMass_in_g=1.989e43; // 1.0e10 solar masses in g
    constexpr static double P_UnitVelocity_in_cm_per_s=1e5; // 1 km/sec in cm/sec
    constexpr static double P_UnitTime_in_s=P_UnitLength_in_cm / P_UnitVelocity_in_cm_per_s;
    constexpr static double P_GRAVITY=6.67384e-8;
    constexpr static double P_G=P_GRAVITY / (P_UnitLength_in_cm*P_UnitLength_in_cm*P_UnitLength_in_cm) * P_UnitMass_in_g * (P_UnitTime_in_s*P_UnitTime_in_s);
    constexpr static double P_Hubble=100.; // so that HubbleParam is in units of 100 km/sec/Mpc
    
    enum iofields /*!< this enumeration lists the defined output blocks in snapshot files. Not all of them need to be present. */
    { IO_POS,
      IO_VEL,
      IO_ID,
      IO_MASS,
      IO_U,
      IO_RHO,
      IO_HSML,
      IO_POT,
      IO_ACCEL,
      IO_DTENTR,
      IO_TSTP,
    };

    struct __header_G3 {
      unsigned int
          npart[6]; /*!< number of particles of each type in this file */
      double mass
          [6]; /*!< mass of particles of each type. If 0, then the masses are explicitly stored in the mass-block of the snapshot file, otherwise they are omitted */
      double time;     /*!< time of snapshot file */
      double redshift; /*!< redshift of snapshot file */
      int flag_sfr; /*!< flags whether the simulation was including star formation */
      int flag_feedback; /*!< flags whether feedback was included (obsolete) */
      unsigned int npartTotal
          [6]; /*!< total number of particles of each type in this snapshot. This can be different from npart if one is dealing with a multi-file snapshot. */
      int flag_cooling; /*!< flags whether cooling was included  */
      int num_files;    /*!< number of files in multi-file snapshot */
      double
          BoxSize; /*!< box-size of simulation in case periodic boundaries were used */
      double Omega0;      /*!< matter density in units of critical density */
      double OmegaLambda; /*!< cosmological constant parameter */
      double HubbleParam; /*!< Hubble parameter in units of 100 km/sec/Mpc */
      int flag_stellarage; /*!< flags whether the file contains formation times of star particles */
      int flag_metals; /*!< flags whether the file contains metallicity values for gas and star particles */
      unsigned int npartTotalHighWord
          [6]; /*!< High word of the total number of particles of each type */
      int flag_entropy_instead_u; /*!< flags that IC-file contains entropy instead of u */
      // Specific to Gadget-3:
      int flag_doubleprecision; /*!< flags that snapshot contains double-precision instead of single precision */
      int flag_ic_info; /*!< flag to inform whether IC files are generated with ordinary Zeldovich approximation, or whether they contain 2nd order
    lagrangian perturbation theory initial conditions. For snapshots files, the value informs whether the simulation was evolved from Zeldoch or 2lpt ICs. Encoding is as follows:
                                                FLAG_ZELDOVICH_ICS     (1)   -IC file based on Zeldovich
                                                FLAG_SECOND_ORDER_ICS  (2)   -Special IC-file containing 2lpt masses
                                                FLAG_EVOLVED_ZELDOVICH (3)   -snapshot evolved from Zeldovich ICs
                                                FLAG_EVOLVED_2LPT      (4)   -snapshot evolved from 2lpt ICs
                                                FLAG_NORMALICS_2LPT    (5)   -standard gadget file format with 2lpt ICs
                                                All other values, including 0 are interpreted as "don't know" for backwards compatibility.*/
      float
          lpt_scalingfactor; /*!< scaling factor for 2lpt initial conditions */
      char fill[18];         /*!< fills to 256 Bytes */
      char names[15][2];
    };
    typedef struct __header_G3 header_t;

    void readGadget(
        H5::H5File hdf5_file, arrayID_t &Ids, arrayPosition_t &Pos,
        arrayVelocity_t &Vel, CosmologicalParameters &cosmo, size_t &Np,
        double &L0, double &L1, double &L2);
    void saveGadget(
        H5::H5File hdf5_file, arrayID_t Ids, arrayPosition_t Pos,
        arrayVelocity_t Vel, CosmologicalParameters cosmo, const size_t Np,
        const double L0, const double L1, const double L2);

  } // namespace IO
} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
