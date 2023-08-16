#include <iostream>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_scalar.hpp"

namespace LibLSS {

  template <class QSOType, class AllocationPolicy>
  void LymanAlphaSurvey<QSOType, AllocationPolicy>::addQSO(const QSOType &qso) {
    if (numQSO == QSO.size()) {
      QSO.resize(boost::extents[numQSO + AllocationPolicy::getIncrement()]);
    }

    QSO[numQSO] = qso;

    numQSO++;
  }

  template <class QSOType, class AllocationPolicy>
  void LymanAlphaSurvey<QSOType, AllocationPolicy>::addLOS(LOSType &los) {
    if (numLOS == projection.size()) {
      projection.resize(
          boost::extents[numLOS + AllocationPolicy::getIncrement()]);
    }

    projection[numLOS] = los;
    numLOS++;
  }

  template <class QSOType, class AllocationPolicy>
  void
  LymanAlphaSurvey<QSOType, AllocationPolicy>::saveMain(H5::H5Location &fg) {
    optimize();

    H5::Group g0 = fg.createGroup("qso_array");
    CosmoTool::hdf5_write_array(g0, "QSO", QSO);

    for (int i = 0; i < numQSO; i++) {
      H5::Group g = g0.createGroup(str(boost::format("qso_%d") % i));
      CosmoTool::hdf5_write_array(g, "voxel_id", projection[i].voxel_id);
      CosmoTool::hdf5_write_array(g, "dlos", projection[i].dlos);
      CosmoTool::hdf5_write_array(g, "flux", projection[i].flux);
    }
  }

  template <class QSOType, class AllocationPolicy>
  void
  LymanAlphaSurvey<QSOType, AllocationPolicy>::restoreMain(H5::H5Location &fg) {
    H5::Group g0 = fg.openGroup("qso_array");
    CosmoTool::hdf5_read_array(g0, "QSO", QSO);

    numQSO = QSO.size();

    projection.resize(boost::extents[numQSO]);

    for (int i = 0; i < numQSO; i++) {
      int s = 0;
      H5::Group g = g0.openGroup(str(boost::format("qso_%d") % i));

      CosmoTool::hdf5_read_array(g, "voxel_id", projection[i].voxel_id);
      CosmoTool::hdf5_read_array(g, "dlos", projection[i].dlos);
      CosmoTool::hdf5_read_array(g, "flux", projection[i].flux);
    }
  }

}; // namespace LibLSS
