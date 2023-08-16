/*+
    ARES/HADES/BORG Package -- ./libLSS/data/linear_selection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DATA_LINEAR_SELECTION_HPP
#define __LIBLSS_DATA_LINEAR_SELECTION_HPP

#include <boost/format.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <H5Cpp.h>
#include <fstream>
#include <sstream>
#include <cmath>
#include <cfloat>
#include <healpix_cxx/pointing.h>
#include <healpix_cxx/healpix_map.h>
#include <healpix_cxx/healpix_map_fitsio.h>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS {

  class LinearInterpolatedSelection {
  protected:
    boost::multi_array<double, 1> selection;
    double dr, rmin, dmin, dmax;
    Healpix_Map<double> sky;

  public:
    LinearInterpolatedSelection() : sky(1, RING, SET_NSIDE), rmin(0), dr(1) {
      std::fill(
          selection.data(), selection.data() + selection.num_elements(), 1);
      this->dmin = 0;
      this->dmax = 0;
    }
    ~LinearInterpolatedSelection() {}

    void loadSky(const std::string &fname, double threshold = 0) {
      read_Healpix_map_from_fits(fname, sky);
      for (long i = 0; i < sky.Npix(); i++)
        if (sky[i] < threshold)
          sky[i] = 0;
    }

    void fillSky(double v) { sky.fill(v); }

    void clearSky() { sky.SetNside(1, RING); }

    void setMinMaxDistances(double dmin, double dmax) {
      this->dmin = dmin;
      this->dmax = dmax;
    }

    void loadRadial(const std::string &fname) {
      using namespace std;
      using boost::format;
      using boost::str;

      ifstream f(fname.c_str());
      string line;

      if (!f) {
        error_helper<ErrorIO>(
            str(format("Failed to open '%s' to load radial") % fname));
      }

      {
        int numPoints;

        while (getline(f, line))
          if (line[0] != '#')
            break;
        if (!f)
          error_helper<ErrorIO>("Error finding the first line");

        istringstream iss(line);

        iss >> rmin >> dr >> numPoints;
        selection.resize(boost::extents[numPoints]);
        Console::instance().print<LOG_INFO>(
            boost::format(
                "Found selection with %d points from %g Mpc/h to %g Mpc/h") %
            numPoints % rmin % (rmin + dr * numPoints));
        this->dmax = rmin + dr * numPoints * 2;
      }

      for (long i = 0; i < selection.shape()[0]; i++) {
        if (!getline(f, line))
          error_helper<ErrorIO>(str(format("Error reading line %d") % (i + 2)));
        if (line[0] == '#')
          continue;
        try {
          boost::algorithm::trim(line);
          selection[i] = boost::lexical_cast<double>(line);
        } catch (const std::exception &e) {
          error_helper<ErrorIO>(
              str(format("Bad value cast on line %d") % (i + 2)));
        }
      }
    }

    void setArray(const boost::multi_array<double, 1> &a, double rmax) {
      this->rmin = 0;
      this->dr = rmax / a.num_elements();
      selection.resize(boost::extents[a.num_elements()]);
      selection = a;
    }

    double getRadialSelection(double r, int n) const {

      double q = (r - rmin) / dr;
      double q0 = std::floor(q);
      int i = int(q0);
      double f = q - q0;

      //Console::instance().c_assert(r < rmax, "Box too large for radial selection table");
      if ((i + 1) >= selection.shape()[0] || i < 0)
        return 0;
      if (r < dmin || r > dmax)
        return 0;

      return (1 - f) * selection[i] + f * selection[i + 1];
    }

    int getNumRadial() const { return 1; }

    double get_sky_completeness(double x, double y, double z) const {
      double r = std::max(std::sqrt(x * x + y * y + z * z), DBL_EPSILON);
      return sky[sky.vec2pix(vec3(x / r, y / r, z / r))];
    }

    void saveFunction(H5_CommonFileGroup &fg) {
      CosmoTool::get_hdf5_data_type<double> ht;
      hsize_t Npix = sky.Npix();
      {
        H5::DataSpace dataspace(1, &Npix);
        H5::DataSet dataset =
            fg.createDataSet("completeness", ht.type(), dataspace);
        dataset.write(&sky[0], ht.type());
      }

      {
        hsize_t s = 1;
        H5::DataSpace dataspace(1, &s);
        H5::DataSet dataset = fg.createDataSet("dr", ht.type(), dataspace);
        dataset.write(&dr, ht.type());

        H5::DataSet dataset2 = fg.createDataSet("rmin", ht.type(), dataspace);
        dataset2.write(&rmin, ht.type());
      }

      CosmoTool::hdf5_write_array(fg, "radial_selection", selection);
    }

    void loadFunction(H5_CommonFileGroup &fg) {
      CosmoTool::get_hdf5_data_type<double> ht;
      hsize_t Npix;

      {
        H5::DataSet dataset = fg.openDataSet("completeness");
        H5::DataSpace dataspace = dataset.getSpace();

        if (dataspace.getSimpleExtentNdims() != 1) {
          error_helper<ErrorIO>("Invalid stored array");
        }

        dataspace.getSimpleExtentDims(&Npix);
        sky.SetNside(sky.npix2nside(Npix), RING);
        dataset.read(&sky[0], ht.type());
      }
      {
        H5::DataSet dataset = fg.openDataSet("rmin");
        H5::DataSpace dataspace = dataset.getSpace();
        hsize_t n;

        if (dataspace.getSimpleExtentNdims() != 1)
          error_helper<ErrorIO>("Invalid stored rmin");

        dataspace.getSimpleExtentDims(&n);
        if (n != 1)
          error_helper<ErrorIO>("Invalid stored rmin");

        dataset.read(&rmin, ht.type());
      }

      {
        H5::DataSet dataset = fg.openDataSet("dr");
        H5::DataSpace dataspace = dataset.getSpace();
        hsize_t n;

        if (dataspace.getSimpleExtentNdims() != 1)
          error_helper<ErrorIO>("Invalid stored dr");

        dataspace.getSimpleExtentDims(&n);
        if (n != 1)
          error_helper<ErrorIO>("Invalid stored dr");

        dataset.read(&dr, ht.type());
      }

      CosmoTool::hdf5_read_array(fg, "radial_selection", selection);
    }
  };

} // namespace LibLSS

#endif
