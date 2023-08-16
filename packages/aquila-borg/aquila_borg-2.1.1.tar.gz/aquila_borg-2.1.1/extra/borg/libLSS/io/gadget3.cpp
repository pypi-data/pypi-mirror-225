/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/io/gadget3.cpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/io/gadget3.hpp"
#include <cstring>

using namespace std;
using namespace LibLSS;
using namespace LibLSS::IO;

///-------------------------------------------------------------------------------------
/** @fn get_bytes_per_blockelement
 *  This function tells the size of one data entry in each of the blocks
 *  defined for the output file. If one wants to add a new output-block, this
 *  function should be augmented accordingly.
 * @param blocknr
 */
static int get_bytes_per_blockelement(enum iofields blocknr) {
  int bytes_per_blockelement = 0;
  switch (blocknr) {
  case IO_POS:
  case IO_VEL:
  case IO_ACCEL:
    bytes_per_blockelement = 3 * sizeof(float);
    break;
  case IO_ID:
    bytes_per_blockelement = sizeof(particleID_t);
    break;
  case IO_MASS:
  case IO_U:
  case IO_RHO:
  case IO_HSML:
  case IO_POT:
  case IO_DTENTR:
  case IO_TSTP:
    bytes_per_blockelement = sizeof(float);
    break;
  }
  return bytes_per_blockelement;
} //get_bytes_per_blockelement
///-------------------------------------------------------------------------------------
/** @fn get_values_per_blockelement
 * This function informs about the number of elements stored per particle for
 *  the given block of the output file. If one wants to add a new
 *  output-block, this function should be augmented accordingly.
 * @param blocknr
 */
static int get_values_per_blockelement(enum iofields blocknr) {
  int values = 0;
  switch (blocknr) {
  case IO_POS:
  case IO_VEL:
  case IO_ACCEL:
    values = 3;
    break;
  case IO_ID:
  case IO_MASS:
  case IO_U:
  case IO_RHO:
  case IO_HSML:
  case IO_POT:
  case IO_DTENTR:
  case IO_TSTP:
    values = 1;
    break;
  }
  return values;
} //get_values_per_blockelement
///-------------------------------------------------------------------------------------
/** @fn get_dataset_name
 *  This function returns a descriptive character string that describes the
 *  name of the block when the HDF5 file format is used.  If one wants to add
 *  a new output-block, this function should be augmented accordingly.
 * @param blocknr
 * @param buf
 */
static void get_dataset_name(enum iofields blocknr, char *buf) {
  strcpy(buf, "default");

  switch (blocknr) {
  case IO_POS:
    strcpy(buf, "Coordinates");
    break;
  case IO_VEL:
    strcpy(buf, "Velocities");
    break;
  case IO_ID:
    strcpy(buf, "ParticleIDs");
    break;
  case IO_MASS:
    strcpy(buf, "Masses");
    break;
  case IO_U:
    strcpy(buf, "InternalEnergy");
    break;
  case IO_RHO:
    strcpy(buf, "Density");
    break;
  case IO_HSML:
    strcpy(buf, "SmoothingLength");
    break;
  case IO_POT:
    strcpy(buf, "Potential");
    break;
  case IO_ACCEL:
    strcpy(buf, "Acceleration");
    break;
  case IO_DTENTR:
    strcpy(buf, "RateOfChangeOfEntropy");
    break;
  case IO_TSTP:
    strcpy(buf, "TimeStep");
    break;
  }
} //get_dataset_name
///-------------------------------------------------------------------------------------
/** @fn read_header_attributes_in_hdf5
 *  This function reads the header information in case the HDF5 file format is
 *  used.
 * @param hdf5_file
 * @param header
 */
void read_header_attributes_in_hdf5(hid_t hdf5_file, header_t *header) {
  hid_t hdf5_headergrp, hdf5_attribute;

  hdf5_headergrp = H5Gopen(hdf5_file, "/Header", H5P_DEFAULT);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "NumPart_ThisFile");
  H5Aread(hdf5_attribute, H5T_NATIVE_UINT, header->npart);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "MassTable");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, header->mass);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Time");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->time);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Redshift");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->redshift);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_Sfr");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_sfr);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_Feedback");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_feedback);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "NumPart_Total");
  H5Aread(hdf5_attribute, H5T_NATIVE_UINT, header->npartTotal);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_Cooling");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_cooling);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "NumFilesPerSnapshot");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->num_files);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "BoxSize");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->BoxSize);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Omega0");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->Omega0);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "OmegaLambda");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->OmegaLambda);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "HubbleParam");
  H5Aread(hdf5_attribute, H5T_NATIVE_DOUBLE, &header->HubbleParam);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_StellarAge");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_stellarage);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_Metals");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_metals);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "NumPart_Total_HighWord");
  H5Aread(hdf5_attribute, H5T_NATIVE_UINT, header->npartTotalHighWord);
  H5Aclose(hdf5_attribute);

  hdf5_attribute = H5Aopen_name(hdf5_headergrp, "Flag_Entropy_ICs");
  H5Aread(hdf5_attribute, H5T_NATIVE_INT, &header->flag_entropy_instead_u);
  H5Aclose(hdf5_attribute);

  H5Gclose(hdf5_headergrp);
} //read_header_attributes_in_hdf5
///-------------------------------------------------------------------------------------
/** @fn write_header_attributes_in_hdf5
 *  This function writes the header information in case HDF5 is selected as
 *  file format.
 * @param hdf5_file
 * @param header
 */
void write_header_attributes_in_hdf5(hid_t hdf5_file, header_t header) {
  hsize_t adim[1] = {6};
  hid_t hdf5_headergrp, hdf5_dataspace, hdf5_attribute;

  hdf5_headergrp =
      H5Gcreate2(hdf5_file, "/Header", 0, H5P_DEFAULT, H5P_DEFAULT);

  hdf5_dataspace = H5Screate(H5S_SIMPLE);
  H5Sset_extent_simple(hdf5_dataspace, 1, adim, NULL);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "NumPart_ThisFile", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_UINT, header.npart);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SIMPLE);
  H5Sset_extent_simple(hdf5_dataspace, 1, adim, NULL);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "MassTable", H5T_NATIVE_DOUBLE, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, header.mass);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Time", H5T_NATIVE_DOUBLE, hdf5_dataspace, H5P_DEFAULT,
      H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.time);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Redshift", H5T_NATIVE_DOUBLE, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.redshift);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_Sfr", H5T_NATIVE_INT, hdf5_dataspace, H5P_DEFAULT,
      H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.flag_sfr);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_Feedback", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.flag_feedback);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SIMPLE);
  H5Sset_extent_simple(hdf5_dataspace, 1, adim, NULL);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "NumPart_Total", H5T_NATIVE_UINT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_UINT, header.npartTotal);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_Cooling", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.flag_cooling);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "NumFilesPerSnapshot", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.num_files);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Omega0", H5T_NATIVE_DOUBLE, hdf5_dataspace, H5P_DEFAULT,
      H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.Omega0);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "OmegaLambda", H5T_NATIVE_DOUBLE, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.OmegaLambda);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "HubbleParam", H5T_NATIVE_DOUBLE, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.HubbleParam);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "BoxSize", H5T_NATIVE_DOUBLE, hdf5_dataspace, H5P_DEFAULT,
      H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_DOUBLE, &header.BoxSize);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_StellarAge", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.flag_stellarage);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SCALAR);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_Metals", H5T_NATIVE_INT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_INT, &header.flag_metals);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SIMPLE);
  H5Sset_extent_simple(hdf5_dataspace, 1, adim, NULL);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "NumPart_Total_HighWord", H5T_NATIVE_UINT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_UINT, header.npartTotalHighWord);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  hdf5_dataspace = H5Screate(H5S_SIMPLE);
  H5Sset_extent_simple(hdf5_dataspace, 1, adim, NULL);
  hdf5_attribute = H5Acreate2(
      hdf5_headergrp, "Flag_Entropy_ICs", H5T_NATIVE_UINT, hdf5_dataspace,
      H5P_DEFAULT, H5P_DEFAULT);
  H5Awrite(hdf5_attribute, H5T_NATIVE_UINT, &header.flag_entropy_instead_u);
  H5Aclose(hdf5_attribute);
  H5Sclose(hdf5_dataspace);

  H5Gclose(hdf5_headergrp);
} //write_header_attributes_in_hdf5
///-------------------------------------------------------------------------------------
/** @fn write_hdf5_block
 *  This function writes a block in a Gadget fileformat 3 snapshot file
 * @param blocknr
 * @param hdf5_grp
 * @param Ids
 * @param positions
 * @param velocities
 * @param header
 * @param pc
 */
static void write_hdf5_block(
    enum iofields blocknr, hid_t hdf5_grp[6], arrayID_t Ids,
    arrayPosition_t positions, arrayPosition_t velocities, header_t header,
    particleID_t pc) {
  int rank, type, bytes_per_blockelement;
  particleID_t pc_new;
  unsigned int n;
  char h5buf[100];
  void *TestBuffer;
  hid_t hdf5_dataspace_in_file, hdf5_dataspace_in_memory, hdf5_dataset;
  hsize_t dims[2], offset[2];

  for (type = 0, pc_new = pc; type < 6; type++) {
    if (header.npart[type] <= 0)
      continue;
    get_dataset_name(blocknr, h5buf);
    bytes_per_blockelement = get_bytes_per_blockelement(blocknr);

    dims[0] = header.npart[type]; // write all particles in file
    dims[1] = get_values_per_blockelement(blocknr);
    if (dims[1] == 1)
      rank = 1;
    else
      rank = 2;
    hdf5_dataspace_in_file = H5Screate_simple(rank, dims, NULL);

    if ((TestBuffer = malloc(bytes_per_blockelement * header.npart[type])) !=
        NULL) // try to allocate a buffer to write the hdf5 block all at once
    {
      free(TestBuffer);
      dims[0] = header.npart[type]; // write all particles in memory
      offset[1] = 0;
      hdf5_dataspace_in_memory = H5Screate_simple(rank, dims, NULL);

      offset[0] = 0;
      H5Sselect_hyperslab(
          hdf5_dataspace_in_file, H5S_SELECT_SET, offset, NULL, dims, NULL);

      // malloc an array
      float *FloatBuffer;
      particleID_t *ParticleIDtypeBuffer;
      switch (blocknr) {
      case IO_ID:
        ParticleIDtypeBuffer =
            (particleID_t *)malloc(bytes_per_blockelement * header.npart[type]);
        break;
      default:
        FloatBuffer =
            (float *)malloc(bytes_per_blockelement * header.npart[type]);
        break;
      }

      // fill buffer array and write it to hdf5
      switch (blocknr) {
      case IO_POS:
        for (n = 0; n < header.npart[type]; n++) {
          // cast to float
          FloatBuffer[3 * n + 0] = float(positions[pc_new][0]);
          FloatBuffer[3 * n + 1] = float(positions[pc_new][1]);
          FloatBuffer[3 * n + 2] = float(positions[pc_new][2]);

          pc_new++;
        }
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_FLOAT, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        H5Dwrite(
            hdf5_dataset, H5T_NATIVE_FLOAT, hdf5_dataspace_in_memory,
            hdf5_dataspace_in_file, H5P_DEFAULT, FloatBuffer);
        break;
      case IO_VEL:
        for (n = 0; n < header.npart[type]; n++) {
          // cast to float
          FloatBuffer[3 * n + 0] = float(velocities[pc_new][0]);
          FloatBuffer[3 * n + 1] = float(velocities[pc_new][1]);
          FloatBuffer[3 * n + 2] = float(velocities[pc_new][2]);

          pc_new++;
        }
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_FLOAT, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        H5Dwrite(
            hdf5_dataset, H5T_NATIVE_FLOAT, hdf5_dataspace_in_memory,
            hdf5_dataspace_in_file, H5P_DEFAULT, FloatBuffer);
        break;
      case IO_ID:
        for (n = 0; n < header.npart[type]; n++) {
          ParticleIDtypeBuffer[n] = particleID_t(Ids[pc_new]);
          pc_new++;
        }
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_UINT64, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        H5Dwrite(
            hdf5_dataset, H5T_NATIVE_UINT64, hdf5_dataspace_in_memory,
            hdf5_dataspace_in_file, H5P_DEFAULT, ParticleIDtypeBuffer);
        break;
      case IO_MASS:
      case IO_U:
      case IO_RHO:
      case IO_HSML:
      case IO_POT:
      case IO_ACCEL:
      case IO_DTENTR:
      case IO_TSTP:
        break;
      }

      // free memory
      switch (blocknr) {
      case IO_ID:
        free(ParticleIDtypeBuffer);
        break;
      default:
        free(FloatBuffer);
        break;
      }
    } else // we write the hdf5 block particle per particle
    {
      dims[0] = 1; // write particles one by one in memory
      offset[1] = 0;
      hdf5_dataspace_in_memory = H5Screate_simple(rank, dims, NULL);

      switch (blocknr) {
      case IO_POS:
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_FLOAT, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        break;
      case IO_VEL:
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_FLOAT, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        break;
      case IO_ID:
        hdf5_dataset = H5Dcreate2(
            hdf5_grp[type], h5buf, H5T_NATIVE_UINT64, hdf5_dataspace_in_file,
            H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        break;
      case IO_MASS:
      case IO_U:
      case IO_RHO:
      case IO_HSML:
      case IO_POT:
      case IO_ACCEL:
      case IO_DTENTR:
      case IO_TSTP:
        break;
      }

      for (n = 0; n < header.npart[type]; n++) {
        offset[0] = n;
        H5Sselect_hyperslab(
            hdf5_dataspace_in_file, H5S_SELECT_SET, offset, NULL, dims, NULL);

        float Vector[3];
        switch (blocknr) {
        case IO_POS:
          // cast to float
          Vector[0] = float(positions[pc_new][0]);
          Vector[1] = float(positions[pc_new][1]);
          Vector[2] = float(positions[pc_new][2]);
          H5Dwrite(
              hdf5_dataset, H5T_NATIVE_FLOAT, hdf5_dataspace_in_memory,
              hdf5_dataspace_in_file, H5P_DEFAULT, &Vector);
          break;
        case IO_VEL:
          // cast to float
          Vector[0] = float(velocities[pc_new][0]);
          Vector[1] = float(velocities[pc_new][1]);
          Vector[2] = float(velocities[pc_new][2]);
          H5Dwrite(
              hdf5_dataset, H5T_NATIVE_FLOAT, hdf5_dataspace_in_memory,
              hdf5_dataspace_in_file, H5P_DEFAULT, &Vector);
          break;
        case IO_ID:
          H5Dwrite(
              hdf5_dataset, H5T_NATIVE_UINT64, hdf5_dataspace_in_memory,
              hdf5_dataspace_in_file, H5P_DEFAULT, &Ids[pc_new]);
          break;
        case IO_MASS:
        case IO_U:
        case IO_RHO:
        case IO_HSML:
        case IO_POT:
        case IO_ACCEL:
        case IO_DTENTR:
        case IO_TSTP:
          break;
        }

        pc_new++;
      }
    }
    H5Sclose(hdf5_dataspace_in_memory);
    H5Sclose(hdf5_dataspace_in_file);
    H5Dclose(hdf5_dataset);
  }
} //write_hdf5_block

namespace LibLSS {
  namespace IO {

    void readGadget(
        H5::H5File hdf5_file, arrayID_t &Ids, arrayPosition_t &Pos,
        arrayVelocity_t &Vel, CosmologicalParameters &cosmo, size_t &Np,
        double &L0, double &L1, double &L2) {
      // read header
      header_t header1;
      read_header_attributes_in_hdf5(hdf5_file.getId(), &header1);

      cosmo.omega_m = header1.Omega0;
      cosmo.omega_q = header1.OmegaLambda;
      cosmo.h = header1.HubbleParam;
      Np = (size_t)header1.npart[1];
      L0 = L1 = L2 = header1.BoxSize;

      // read positio
      CosmoTool::hdf5_read_array(hdf5_file, "PartType1/Coordinates", Pos);

      // read velocities
      CosmoTool::hdf5_read_array(hdf5_file, "PartType1/Velocities", Vel);

      // read Ids
      CosmoTool::hdf5_read_array(hdf5_file, "PartType1/ParticleIDs", Ids);
    } //readGadget

    void saveGadget(
        H5::H5File hdf5_file, arrayID_t Ids, arrayPosition_t Pos,
        arrayVelocity_t Vel, CosmologicalParameters cosmo, const size_t Np,
        const double L0, const double L1, const double L2) {
      hid_t hdf5_grp[6];
      char h5buf[100];
      particleID_t pc = 0;
      int type;

      header_t header1;
      header1.npart[0] = header1.npart[2] = header1.npart[3] =
          header1.npart[4] = header1.npart[5] = 0;
      header1.npart[1] = (unsigned int)Np;
      header1.npartTotal[0] = header1.npartTotal[2] = header1.npartTotal[3] =
          header1.npartTotal[4] = header1.npartTotal[5] = 0;
      header1.npartTotal[1] = (unsigned int)Np;
      header1
          .mass[0] = header1
                         .mass[2] = header1
                                        .mass[3] = header1
                                                       .mass[4] = header1
                                                                      .mass[5] =
          1.; // Shouldn't be zero, otherwise interpreted as "variable particle mass" by Gadget
      header1.mass[1] = cosmo.omega_m * 3 * P_Hubble * P_Hubble /
                        (8 * M_PI * P_G) * pow(L0, 3) /
                        Np; // First Friedmann equation in cosmic time
      header1.time;
      header1.redshift;
      header1.flag_sfr = 0;
      header1.flag_feedback = 0;
      header1.flag_cooling = 0;
      header1.num_files = 1;
      if (fabs(L1 - L0) > 1e-3 || fabs(L2 - L0) > 1e-3)
        error_helper<ErrorParams>(
            "L1 must be equal to L0, got L0=%g, L1=%g, L2=%g");
      header1.BoxSize = L0;
      header1.Omega0 = cosmo.omega_m;
      header1.OmegaLambda = cosmo.omega_q;
      header1.HubbleParam = cosmo.h;
      header1.flag_stellarage = 0;
      header1.flag_metals = 0;
      header1.npartTotalHighWord[0] = header1.npartTotalHighWord[1] =
          header1.npartTotalHighWord[2] = header1.npartTotalHighWord[3] =
              header1.npartTotalHighWord[4] = header1.npartTotalHighWord[5] = 0;
      header1.flag_entropy_instead_u = 0;
      header1.flag_doubleprecision = 0;
      header1.flag_ic_info = 0;
      header1.lpt_scalingfactor = 0.;

      // create groups
      for (type = 0; type < 6; type++) {
        if (header1.npart[type] > 0) {
          sprintf(h5buf, "/PartType%d", type);
          hdf5_grp[type] =
              H5Gcreate2(hdf5_file.getId(), h5buf, 0, H5P_DEFAULT, H5P_DEFAULT);
        }
      }

      // write header
      write_header_attributes_in_hdf5(hdf5_file.getId(), header1);

      // write positions
      write_hdf5_block(IO_POS, hdf5_grp, Ids, Pos, Vel, header1, pc);

      // write velocities
      write_hdf5_block(IO_VEL, hdf5_grp, Ids, Pos, Vel, header1, pc);

      // write Ids
      write_hdf5_block(IO_ID, hdf5_grp, Ids, Pos, Vel, header1, pc);

      // close groups
      for (type = 5; type >= 0; type--)
        if (header1.npart[type] > 0)
          H5Gclose(hdf5_grp[type]);
    } //saveGadget

  } // namespace IO
} // namespace LibLSS

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
