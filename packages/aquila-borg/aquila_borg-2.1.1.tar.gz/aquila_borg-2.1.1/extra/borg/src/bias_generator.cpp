/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/bias_generator.cpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <map>
#include <string>
#include "bias_generator.hpp"
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include <H5Cpp.h>
#include <sys/types.h>
#include <string>
#include "libLSS/mcmc/global_state.hpp"
#include "healpix_cxx/healpix_map.h"

#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"

using namespace LibLSS;
using boost::format;

template <typename Bias>
void generate_biased_density(
    MPI_Communication *mpi_world, MarkovState &state, BORGForwardModel &model,
    ArrayType &out_density, H5::H5File &f, size_t Ncat) {
  Bias bias;
  auto box = model.get_box_model();

  ArrayType biased_density(
      model.lo_mgr->extents_real_strict(), model.lo_mgr->allocator_real);
  biased_density.setRealDims(ArrayDimension(box.N0, box.N1, box.N2));
  for (size_t cat = 0; cat < Ncat; cat++) {
    auto &bias_params =
        *state.get<ArrayType1d>("galaxy_bias_" + to_string(cat))->array;
    double nmean = state.getScalar<double>("galaxy_nmean_" + to_string(cat));

    if (bias_params.shape()[0] < Bias::numParams) {
      error_helper<ErrorParams>("Insufficient number of bias parameters for catalog " + LibLSS::to_string(cat));
    }

    bias.prepare(model, *out_density.array, nmean, bias_params, cat == 0);

    LibLSS::copy_array(
        *biased_density.array,
        std::get<0>(bias.compute_density(*out_density.array)));

    biased_density.unsafeSetName("biased_density_" + to_string(cat));
    biased_density.saveTo(f, mpi_world, false);

    bias.cleanup();
  }
}

void build_sel_window(int cat, MarkovState& state, boost::multi_array_ref<double, 3>& output_sel )
{
  auto& fgcoefs =
     *state.get<ArrayType1d>(
       format("catalog_foreground_coefficient_%d") % cat
     )->array;
  auto w_s = fwrap(output_sel);

  w_s = *state.get<ArrayType>(format("galaxy_sel_window_%d") % cat)->array;

  for (int fg = 0; fg < fgcoefs.shape()[0]; fg++) {
      w_s = w_s * (1 - fgcoefs[fg]*fwrap(*state.get<ArrayType>(format("foreground_3d_%d") % fg)->array));
  }
}

template <typename Bias>
void generate_systematic_map(
  MPI_Communication* comm, MarkovState& state, LikelihoodInfo& info, BORGForwardModel &model,
  ArrayType &out_density, H5::H5File& f, size_t Ncat, long Nside, size_t rayshoot)
{
  Bias bias;
  auto box = model.get_box_model();
  size_t startN0 = model.lo_mgr->startN0;
  size_t endN0 = startN0 + model.lo_mgr->localN0;
  size_t N1 = model.lo_mgr->N1;
  size_t N2 = model.lo_mgr->N2;
  size_t N0 = model.lo_mgr->N0;

  U_Array<double, 3> biased_density(model.lo_mgr->extents_real_strict());
  U_Array<double, 3> sel_window(model.lo_mgr->extents_real_strict());

  size_t N[3] = { N0, N1, N2 };
  double L[3] = { state.getScalar<double>("L0"), state.getScalar<double>("L1"), state.getScalar<double>("L2") };
  double delta[3] = {L[0]/N[0], L[1]/N[1], L[2]/N[2]};
  double corner[3] = { state.getScalar<double>("corner0"), state.getScalar<double>("corner1"), state.getScalar<double>("corner2") };

  auto& rgen = state.get<RandomGen>("random_generator")->get();

  for (size_t cat = 0; cat < Ncat; cat++) {
    auto &data =
        *state.get<ArrayType>("galaxy_data_" + to_string(cat))->array;
    auto &bias_params =
        *state.get<ArrayType1d>("galaxy_bias_" + to_string(cat))->array;
    double nmean =
        state.getScalar<double>("galaxy_nmean_" + to_string(cat));

    build_sel_window(cat, state, sel_window.get_array());

    bias.prepare(model, *out_density.array, nmean, bias_params, cat == 0);
    fwrap(biased_density.get_array()) = std::get<0>(bias.compute_density(*out_density.array)) * fwrap(sel_window.get_array());
    bias.cleanup();

    Healpix_Map<double> summary0(Nside, RING, SET_NSIDE);
    Healpix_Map<double> summary1(Nside, RING, SET_NSIDE);
    Healpix_Map<double> summary2(Nside, RING, SET_NSIDE);

    summary0.fill(0);
    summary1.fill(0);
    summary2.fill(0);

#pragma omp parallel for schedule(dynamic)
    for (size_t pix = 0; pix < summary0.Npix(); pix++) {
      vec3 vref = summary0.pix2vec(pix);
      double uref[3] = {vref.x,vref.y,vref.z};
      double rad = summary0.max_pixrad();
      double cos_rad = std::cos(rad);
      double v0[3], v1[3];
      std::set<std::array<ssize_t,3>> pixset;
      if (uref[0] == 0. && uref[2] == 0.) {
        v0[0] = 0;
        v0[1] = 1;
        v0[2] = 0;
      } else {
        v0[0] = uref[2];
        v0[1] = 0.;
        v0[2] = -uref[1];
      }
      v1[0] = uref[1] * v0[2] - uref[2] * v0[1];
      v1[1] = uref[2] * v0[0] - uref[0] * v0[2];
      v1[2] = uref[0] * v0[1] - uref[1] * v0[0];
      for (size_t ray = 0; ray < rayshoot; ray++) {
        // Find a vector close to uref that is still inside the pixel
        double u[3];
        while (true) {
          double alpha = rgen.uniform() * (1 - cos_rad) + cos_rad;
          double beta = std::sqrt(1-alpha*alpha);
          double phi = rgen.uniform() * 2 * M_PI;
          double cos_phi = std::cos(phi) * beta;
          double sin_phi = std::sin(phi) * beta;
          u[0] = uref[0]*alpha + v0[0] * cos_phi + v1[0] * sin_phi;
          u[1] = uref[1]*alpha + v0[1] * cos_phi + v1[1] * sin_phi;
          u[2] = uref[2]*alpha + v0[2] * cos_phi + v1[2] * sin_phi;

          // Now check that it is in pixel
          if (summary0.vec2pix(vec3(u[0], u[1], u[2])) != pix)
            continue;
          break;
        }

        double scale = 0;
        ssize_t ijk[3];
        double u0[3] = {0,0,0};
        int jumper = 0;

        ijk[0] = std::floor((- corner[0])/delta[0]);
        ijk[1] = std::floor((- corner[1])/delta[1]);
        ijk[2] = std::floor((- corner[2])/delta[2]);

        while (true) {

          if (ijk[0] >= N0 || ijk[0] < 0 || ijk[1] >= N1 || ijk[1] < 0 || ijk[2] >= N2 || ijk[2] < 0)
            break;

          if (sel_window.get_array()[ijk[0]][ijk[1]][ijk[2]] > 0) {
            pixset.insert({ijk[0],ijk[1],ijk[2]});
          }

          // find jump
          jumper = -1;
          double alpha_max = std::numeric_limits<double>::infinity();
          for (int q = 0; q < 3; q++) {
            double tmp_a;

            if (u[q] == 0.)
              continue;

            if (u[q] < 0.)
              tmp_a = -u0[q]/u[q];
            else
              tmp_a = (1-u0[q])/u[q];

            if (tmp_a < alpha_max) {
              alpha_max = tmp_a;
              jumper = q;
            }
          }

          for (int q = 0; q < 3; q++) u0[q] += u[q]*alpha_max;

          if (u[jumper] < 0) {
            ijk[jumper]--; // Decrease voxel
            u0[jumper] = 1; // Set it at intersection
          } else {
            ijk[jumper]++; // Increase voxel
            u0[jumper] = 0; // Set it at intersection
          }
        }
      }

      double s0 = 0, s1 = 0, s2 = 0;

      for (auto const& ijk: pixset) {

         double D = data[ijk[0]][ijk[1]][ijk[2]];
         s0 += D;
         s1 += biased_density.get_array()[ijk[0]][ijk[1]][ijk[2]];
         s2 += D*(D+1);
      }

      summary0[pix] = s0;
      summary1[pix] = s1;
      summary2[pix] = s2;
    }

    CosmoTool::hdf5_write_array(f, str(format("systematic_summaries_%d_0") % cat),  boost::multi_array_ref<double,1>(&summary0[0], boost::extents[summary0.Npix()]));
    CosmoTool::hdf5_write_array(f, str(format("systematic_summaries_%d_1") % cat),  boost::multi_array_ref<double,1>(&summary1[0], boost::extents[summary1.Npix()]));
    CosmoTool::hdf5_write_array(f, str(format("systematic_summaries_%d_2") % cat),  boost::multi_array_ref<double,1>(&summary2[0], boost::extents[summary2.Npix()]));
  }
}

BiasInfo_t
LibLSS::setup_biased_density_generator(std::string const &likelihood_name) {
  typedef BiasInfo_t mt;
  SystematicMapper_t nullMapper;

  std::map<std::string, BiasInfo_t> lh_map{
      {"GAUSSIAN_BROKEN_POWERLAW_BIAS",
       mt(&generate_biased_density<AdaptBias_Gauss<bias::BrokenPowerLaw>>, nullMapper)},
      {"GAUSSIAN_MO_WHITE_BIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::DoubleBrokenPowerLaw>>, nullMapper)},
      {"GAUSSIAN_POWERLAW_BIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::PowerLaw>>, nullMapper)},
      {"GAUSSIAN_EFT_THRESH_BIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::EFTBiasThresh>>, nullMapper)},
      {"GAUSSIAN_EFT_DEFAULT_BIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::EFTBiasDefault>>, nullMapper)},
      {"GENERIC_POISSON_BROKEN_POWERLAW_BIAS",
       mt(generate_biased_density<bias::BrokenPowerLaw>, nullMapper)},
      {"GENERIC_POISSON_BROKEN_POWERLAW_SIGMOID_BIAS",
       mt(generate_biased_density<bias::BrokenPowerLawSigmoid>, nullMapper)},
      {"GENERIC_GAUSSIAN_LINEAR_BIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::LinearBias>>, nullMapper)},
      {"GENERIC_GAUSSIAN_MANY_POWER_1^1",
       mt(generate_biased_density<
           AdaptBias_Gauss<bias::ManyPower<bias::ManyPowerLevels<double, 1>>>>, nullMapper)},
      {"GENERIC_GAUSSIAN_MANY_POWER_1^2",
       mt(generate_biased_density<AdaptBias_Gauss<
           bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>>, nullMapper)},
      {"GENERIC_GAUSSIAN_MANY_POWER_1^4",
       mt(generate_biased_density<AdaptBias_Gauss<
           bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>>>>, nullMapper)},
      {"GENERIC_POISSON_MANY_POWER_1^1",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 1>>>, nullMapper)},
      {"GENERIC_POISSON_MANY_POWER_1^2",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>, nullMapper)},
      {"GENERIC_POISSON_MANY_POWER_1^4",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>>>, nullMapper)},
      {"ROBUST_POISSON_MANY_POWER_1^1",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 1>>>, &generate_systematic_map<bias::ManyPower<bias::ManyPowerLevels<double, 1>>>)},
      {"ROBUST_POISSON_MANY_POWER_1^2",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>, &generate_systematic_map<bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>)},
      {"ROBUST_POISSON_MANY_POWER_2^2",
       mt(generate_biased_density<
           bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>>, &generate_systematic_map<bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>>)},
  };

  return lh_map[likelihood_name];
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
