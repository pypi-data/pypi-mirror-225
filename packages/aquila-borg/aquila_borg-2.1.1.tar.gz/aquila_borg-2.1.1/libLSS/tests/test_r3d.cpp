#include <cstdio>
#include <iostream>
#include <healpix_cxx/healpix_base.h>

extern "C" {
#include "r3d.h"
}

int main(int argc, char **argv)
{
  Healpix_Base hpx(8, RING, SET_NSIDE);
  std::vector<vec3> out;
  int step = 1;

  out.resize(4*step);

  for (int pix = 0; pix < hpx.Npix(); pix++) {
    r3d_poly p[4];
    r3d_rvec3 v[4];
    double L = 1.0;

    hpx.boundaries(pix, step, out);

    v[0].x = 0;
    v[0].x = 0;
    v[0].z = 0;
//    v[1].x = out[q].x * L;
//    v[1].y = out[q].y * L;
//    v[1].z = out[q].z * L;
//    v[1].x = out[q].x * L;
//    v[1].y = out[q].y * L;
//    v[1].z = out[q].z * L;

//    r3d_init_tet(&poly[p], verts);
  }
  return 0;
}
