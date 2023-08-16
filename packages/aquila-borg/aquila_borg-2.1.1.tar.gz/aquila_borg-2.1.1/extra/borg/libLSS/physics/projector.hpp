/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/projector.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef __LIBLSS_PHYSICS_PROJECTOR_HPP
#define __LIBLSS_PHYSICS_PROJECTOR_HPP

#include <cmath>
#include "boost/multi_array.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/data/lyman_alpha.hpp"

namespace LibLSS {

  typedef boost::multi_array<size_t, 2> VoxelIdType;
  typedef boost::multi_array<double, 1> LosType;

  struct LOSContainer {
    VoxelIdType voxel_id{boost::extents[1][3]};
    LosType dlos{boost::extents[1]};
    LosType flux{boost::extents[1]};
    LosType z{boost::extents[1]};
    LOSContainer& operator=(LOSContainer const& other) {
      voxel_id.resize(boost::extents[other.voxel_id.shape()[0]][other.voxel_id.shape()[1]]);
      dlos.resize(boost::extents[other.dlos.shape()[0]]);
      flux.resize(boost::extents[other.flux.shape()[0]]);
      z.resize(boost::extents[other.z.shape()[0]]);
      voxel_id = other.voxel_id;
      dlos = other.dlos;
      flux = other.flux;
      z = other.z;
      return *this;
    }
  };

  static inline void
  get_vox_id(double *position, size_t *idx, double *min, double *dd) {
    for (int i = 0; i < 3; i++)
      idx[i] = std::floor((position[i] - min[i]) / dd[i]);
  }

  static inline void
  get_vox_id(double *position, double *idx, double *min, double *dd) {
    for (int i = 0; i < 3; i++)
      idx[i] = (position[i] - min[i]) / dd[i];
  }

  static inline void
  get_coord(double *position, size_t *idx, double *min, double *dd) {
    for (int i = 0; i < 3; i++)
      position[i] = idx[i] * dd[i] + min[i];
  }

  static inline void resize_container(LOSContainer &data, int idx) {
    data.dlos.resize(boost::extents[idx + 1]);
    data.flux.resize(boost::extents[idx + 1]);
    data.z.resize(boost::extents[idx + 1]);
    data.voxel_id.resize(boost::extents[idx + 1][3]);
  }

  static inline void store_container(
      LOSContainer &data, int idx, double pos, double dlos, size_t *voxel,
      CosmologicalParameters &cosmo_param) {
    Cosmology cosmo(cosmo_param);
    double a = cosmo.comph2a(pos);

    data.z[idx] = (1. - a) / a;
    data.dlos[idx] = dlos;
    for (int j = 0; j < 3; j++)
      data.voxel_id[idx][j] = voxel[j];
  }

  static inline void accept_voxel(
      LOSContainer &data, int idx, double pos, double dlos, size_t *voxel,
      CosmologicalParameters &cosmo_param) {
    resize_container(data, idx);
    store_container(data, idx, pos, dlos, voxel, cosmo_param);
  }

  static int ray_tracer(
      double *origin, double qso_distance, double *u, double *corner,
      double *dl, size_t *N, LOSContainer &data,
      CosmologicalParameters &cosmo_param) {

    ConsoleContext<LOG_DEBUG> ctx("ray_tracer");
    size_t len = (data.flux).shape()[0];
    data.z.resize(boost::extents[len]);
    data.voxel_id.resize(boost::extents[len][3]);

    Cosmology cosmo(cosmo_param);

    double u0[0], dist;
    size_t voxel[3];

    for (int i = 0; i < len; i++) {
      data.z[i] = (data.dlos[i] - 1.) / 1215.;
      dist = cosmo.com2comph(cosmo.a2com(cosmo.z2a(data.z[i])));
      for (int k = 0; k < 3; k++)
        u0[k] = u[k] * dist + origin[k];
      get_vox_id(u0, voxel, corner, dl);
      ctx.print(boost::format("voxel[2] = %d") % voxel[2]);
      if ((voxel[0] < N[0] - 1) and (voxel[0] > 0) and (voxel[1] < N[1] - 1) and
          (voxel[1] > 0) and (voxel[2] < N[2] - 1) and (voxel[2] > 0)) {
        for (int j = 0; j < 3; j++)
          data.voxel_id[i][j] = voxel[j];
      }
    }

    return 0;
  }

  static int ray_tracer_mock_data(
      double *origin, double qso_distance, double *u, double *corner,
      double *dl, size_t *N, LOSContainer &data,
      CosmologicalParameters &cosmo_param) {
    ConsoleContext<LOG_DEBUG> ctx("ray_tracer_mock_data");
    double qso_distance2 = qso_distance * qso_distance;
    double start_los = qso_distance - 250.;
    //250 Mpc/h is the length of lyman alpha forest (Lee 2014)

    double u0[3], ifu0[3];
    size_t iu0[3];

    for (int i = 0; i < 3; i++)
      u0[i] = u[i] * start_los;
    get_vox_id(u0, ifu0, corner, dl);

    for (int i = 0; i < 3; i++) {
      if (ifu0[i] <= 0 || ifu0[i] >= N[i])
        continue;

      iu0[i] = int(floor(ifu0[i]));
      u0[i] = ifu0[i] - iu0[i];

      if ((u0[i] < 0) || (u0[i] > 1))
        continue;
    }

    bool completed = 0;
    if ((iu0[0] >= N[0] - 1) or (iu0[0] <= 0) || (iu0[1] >= N[1] - 1) or
        (iu0[1] <= 0) || (iu0[2] >= N[2] - 1) or (iu0[2] <= 0)) {
      completed = 1;
    }

    double I = 0., dist2 = 0;
    int jumper;
    int container_idx = 0;
    double tmp_a, alpha_max, delta;

    while (completed == 0) {
      alpha_max = qso_distance - pow(dist2, 0.5);

      for (int i = 0; i < 3; i++) {

        if (u[i] == 0.)
          continue;

        if (u[i] < 0) {
          tmp_a = -u0[i] / u[i];
        } else {
          tmp_a = (1. - u0[i]) / u[i];
        }

        if (tmp_a < alpha_max) {
          alpha_max = tmp_a;
          jumper = i;
        }
      }

      for (int i = 0; i < 3; i++)
        u0[i] += u[i] * alpha_max;

      I += alpha_max;

      if (u[jumper] < 0) {

        ifu0[jumper] -= 1.;
        u0[jumper] = 1.;

      } else {

        ifu0[jumper] += 1.;
        u0[jumper] = 0.;
      }

      for (int i = 0; i < 3; i++)
        iu0[i] = int(floor(ifu0[i]));

      if ((iu0[0] >= N[0] - 1) || (iu0[0] <= 0) || (iu0[1] >= N[1] - 1) ||
          (iu0[1] <= 0) || (iu0[2] >= N[2] - 1) || (iu0[2] <= 0)) {

        completed = 1;

      } else {

        accept_voxel(data, container_idx, I, alpha_max, iu0, cosmo_param);
        container_idx += 1;

        dist2 = 0.;
        for (int i = 0; i < 3; i++) {
          dist2 += pow(iu0[i] * dl[i] + corner[i], 2);
        }

        if (dist2 > qso_distance2) {
          completed = 1;
        }
      }
    }

    return 0;
  }
} // namespace LibLSS
#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

