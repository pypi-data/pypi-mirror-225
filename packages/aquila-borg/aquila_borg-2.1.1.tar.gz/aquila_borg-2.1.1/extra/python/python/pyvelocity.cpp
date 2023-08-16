/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyvelocity.cpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <memory>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <CosmoTool/cosmopower.hpp>
#include <pybind11/numpy.h>

#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"

#include "pyborg.hpp"

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "pyforward.hpp"
#include "pyfuse.hpp"
#include "pyvelocity.hpp"
#include "libLSS/physics/chain_forward_model.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

using namespace LibLSS;

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.forward.velocity.hpp"
#include "pyborg_doc/aquila_borg.forward.velocity.VelocityBase.hpp"

void LibLSS::Python::pyVelocity(py::module m) {
  m.doc() = DOC(aquila_borg, forward, velocity);

  py::class_<VelocityModel::Base, std::shared_ptr<VelocityModel::Base>>(
      m, "VelocityBase", DOC(aquila_borg, forward, velocity, VelocityBase))
      .def(
          "getOutputBox",
          [](VelocityModel::Base *vmodel) {
            BoxModel *box = new BoxModel;

            *box = vmodel->getOutputBox();
            return box;
          },
          DOC(aquila_borg, forward, velocity, VelocityBase, getOutputBox))
      .def(
          "computeAdjointModel",
          [](VelocityModel::Base *vmodel,
             py::array_t<double, py::array::c_style | py::array::forcecast>
                 ag) {
            auto input_ag = ag.unchecked<4>();
            std::array<ssize_t, 6> local_ext;
            typedef boost::multi_array_types::extent_range range;

            vmodel->queryLocalExtents(local_ext);
            // We have to copy the numpy because of no guarantee of
            VelocityModel::Base::arrayVelocityField_const_t cpp_ag(
                input_ag.data(0, 0, 0, 0),
                boost::extents[3][range(local_ext[0], local_ext[1])]
                              [range(local_ext[2], local_ext[3])]
                              [range(local_ext[4], local_ext[5])]);

            vmodel->computeAdjointModel_array(cpp_ag);
          },
          "ag"_a,
          DOC(aquila_borg, forward, velocity, VelocityBase, computeAdjointModel))
      .def(
          "getVelocityField",
          [](VelocityModel::Base *vmodel) {
            typedef boost::multi_array_types::extent_range range;
            py::array_t<double> velocity;
            std::array<ssize_t, 6> local_ext;

            vmodel->queryLocalExtents(local_ext);
            size_t lengths[3] = {
                size_t(local_ext[1] - local_ext[0]),
                size_t(local_ext[3] - local_ext[2]),
                size_t(local_ext[5] - local_ext[4])};

            velocity.resize({size_t(3), lengths[2], lengths[1], lengths[0]});

            //boost::multi_array_ref<double, 4> arrayVelocityField_t;
            auto out = velocity.mutable_unchecked<4>();

            VelocityModel::Base::arrayVelocityField_t vel_out(
                out.mutable_data(0, 0, 0, 0),
                boost::extents[3][range(local_ext[0], local_ext[1])]
                              [range(local_ext[2], local_ext[3])]
                              [range(local_ext[4], local_ext[5])]);

            {
              py::gil_scoped_release release;

              vmodel->getVelocityField(vel_out);
            }
            return velocity;
          },
          DOC(aquila_borg, forward, velocity, VelocityBase, getVelocityField));

  py::class_<
      VelocityModel::ParticleBasedModel, VelocityModel::Base,
      std::shared_ptr<VelocityModel::ParticleBasedModel>>(
      m, "ParticleBasedModel",
      DOC(aquila_borg, forward, velocity, ParticleBasedModel));

  py::class_<
      VelocityModel::CICModel, VelocityModel::ParticleBasedModel,
      std::shared_ptr<VelocityModel::CICModel>>(
      m, "CICModel", DOC(aquila_borg, forward, velocity, CICModel))
      .def(py::init([](BoxModel *box, std::shared_ptr<BORGForwardModel> model) {
        auto pmodel =
            std::dynamic_pointer_cast<ParticleBasedForwardModel>(model);
        if (!pmodel) {
          throw std::invalid_argument("Provided model is not particle based");
        }
        return VelocityModel::CICModel(*box, pmodel);
      }));

  py::class_<
      VelocityModel::SICModel, VelocityModel::ParticleBasedModel,
      std::shared_ptr<VelocityModel::SICModel>>(
      m, "SICModel", DOC(aquila_borg, forward, velocity, SICModel))
      .def(
          py::init([](BoxModel *box, std::shared_ptr<BORGForwardModel> model) {
            auto pmodel =
                std::dynamic_pointer_cast<ParticleBasedForwardModel>(model);
            if (!pmodel) {
              throw std::invalid_argument(
                  "Provided model is not particle based");
            }
            return VelocityModel::SICModel(*box, pmodel);
          }),
          "box_model"_a, "base_forward_model"_a,
          DOC(aquila_borg, forward, velocity, SICModel, __init__));

  m.def(
      "computeSICVelocityfield",
      [](py::array_t<size_t, py::array::c_style> identifiers,
         py::array_t<double, py::array::c_style> positions,
         py::array_t<double, py::array::c_style> velocities, double L, size_t N,
         size_t Ng) {
        py::array_t<double> velocity, density;
        velocity.resize({size_t(3), Ng, Ng, Ng});
        density.resize({Ng, Ng, Ng});
        auto velocity_impl = velocity.mutable_unchecked<4>();
        auto density_impl = density.mutable_unchecked<3>();
        boost::multi_array_ref<double, 3> den_out(
            density_impl.mutable_data(0, 0, 0), boost::extents[Ng][Ng][Ng]);
        VelocityModel::Base::arrayVelocityField_t vel_out(
            velocity_impl.mutable_data(0, 0, 0, 0),
            boost::extents[3][Ng][Ng][Ng]);

        int Np = identifiers.shape(0);
        if (positions.shape(0) != Np || velocities.shape(0) != Np) {
          throw std::invalid_argument(
              "Invalid size of the array of positions or "
              "velocities. Must conform to identifiers.");
        }
        if (positions.shape(1) != 3 || velocities.shape(1) != 3) {
          throw std::invalid_argument(
              "Position and velocity arrays must have a shape Nx3");
        }

        auto identifiers_impl = identifiers.mutable_unchecked<1>();
        auto positions_impl = positions.mutable_unchecked<2>();
        auto velocities_impl = velocities.mutable_unchecked<2>();

        DM_Sheet::arrayID_t ids(
            identifiers_impl.mutable_data(0), boost::extents[Np]);
        DM_Sheet::arrayPosition_t pos(
            positions_impl.mutable_data(0, 0), boost::extents[Np][3]);
        DM_Sheet::arrayPosition_t vels(
            velocities_impl.mutable_data(0, 0), boost::extents[Np][3]);

        {
          py::gil_scoped_release release;

          computeSICVelocityField(ids, pos, vels, L, N, Ng, den_out, vel_out);
        }
        py::tuple ret(2);
        ret[0] = density;
        ret[1] = velocity;
        return ret;
      },
      "ids"_a, "positions"_a, "velocities"_a, "L"_a, "N"_a, "Ng"_a);
}

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
