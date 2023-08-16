/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/hdf5_buffered_write.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HDF5_BUFFERED_WRITE_HPP
#  define __LIBLSS_HDF5_BUFFERED_WRITE_HPP

#  include <H5Cpp.h>
#  include <functional>
#  include <CosmoTool/hdf5_array.hpp>
#  include "libLSS/tools/hdf5_type.hpp"
#  include "libLSS/tools/array_tools.hpp"
#  include "libLSS/tools/fusewrapper.hpp"

namespace LibLSS {
  typedef std::function<void(size_t)> ProgressFunction;

  namespace hdf5_buffer_detail {
    template<typename B, typename D>
    typename std::enable_if<B::dimensionality != 1,void>::type buffer_it(B& b, D& d, std::vector<hsize_t>& memdims_local, std::vector<hsize_t>& offsets_local) {
       typedef boost::multi_array_types::index_range i_range;
       auto inds1 = array::make_star_indices<B::dimensionality-1>(boost::indices[i_range(0, memdims_local[0])]);
       auto inds2 = array::make_star_indices<B::dimensionality-1>(boost::indices[i_range(offsets_local[0], offsets_local[0]+memdims_local[0])]);
       fwrap(b[inds1]) = fwrap(d[inds2]);

//      for (int a = 0; a < memdims_local[0]; a++)
//        fwrap(b[a]) = fwrap(d[a+offsets_local[0]]);
    }

    template<typename B, typename D>
    typename std::enable_if<B::dimensionality == 1,void>::type buffer_it(B& b, D& d, std::vector<hsize_t>& memdims_local, std::vector<hsize_t>& offsets_local) {
      size_t N0 = memdims_local[0];
#pragma omp parallel for
      for (int a = 0; a < N0; a++)
        b[a] = d[a+offsets_local[0]];
    }
  }

  template <typename ArrayType, typename hdf5_data_type>
  void hdf5_write_buffered_array(
      H5_CommonFileGroup &fg, const std::string &data_set_name,
      const ArrayType &data, const hdf5_data_type &datatype,
      const std::vector<hsize_t> &dimensions, bool doCreate = true,
      bool useBases = false, ProgressFunction progress = ProgressFunction()) {
    LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
    typedef typename ArrayType::element element;
    size_t const NUM_ROWS = 1024*1000*100;
    std::vector<hsize_t> memdims(
        data.shape(), data.shape() + data.num_dimensions());
    std::vector<hsize_t> offsets(
        data.index_bases(), data.index_bases() + data.num_dimensions());
    H5::DataSpace dataspace(dimensions.size(), dimensions.data());
    H5::DataSpace memspace(memdims.size(), memdims.data());
    std::vector<hsize_t> offsets_zero;
    hsize_t one_block, block_size;

    H5::DataSet dataset;
    if (doCreate)
      dataset = fg.createDataSet(data_set_name, datatype, dataspace);
    else
      dataset = fg.openDataSet(data_set_name);

    offsets_zero.resize(data.num_dimensions());
    offsets_zero = offsets;
    offsets_zero[0] = 0;

    // Compute equivalent of a few MB of memory
    one_block = array::product(memdims.begin() + 1, memdims.end());
    block_size = one_block * NUM_ROWS;
    std::unique_ptr<element[]> p_buffer(new element[block_size]);

    boost::multi_array_ref<element, ArrayType::dimensionality> buffer(
        p_buffer.get(),
        array::make_extent<ArrayType::dimensionality - 1>(
            offsets_zero.data() + 1, &memdims[1], boost::extents[NUM_ROWS]));

    std::vector<hsize_t> offsets_local = offsets;
    std::vector<hsize_t> memdims_local = memdims;
    size_t block = 0;

    while (block < memdims[0]) {
      if (progress)
        progress(block);
      memdims_local[0] = std::min(NUM_ROWS, size_t(memdims[0] - block));
      H5::DataSpace memspace_local(memdims_local.size(), memdims_local.data());

      hdf5_buffer_detail::buffer_it(buffer, data, memdims_local, offsets_local);

      dataspace.selectHyperslab(
          H5S_SELECT_SET, memdims_local.data(), offsets_local.data());
      dataset.write(p_buffer.get(), datatype, memspace_local, dataspace);

      block += memdims_local[0];
      offsets_local[0] += memdims_local[0];
    }
  }

  template <typename ArrayType, typename hdf5_data_type>
  void hdf5_write_buffered_array(
      H5_CommonFileGroup &fg, const std::string &data_set_name,
      const ArrayType &data, const hdf5_data_type &datatype,
      bool doCreate = true, bool useBases = false,
      ProgressFunction progress = ProgressFunction()) {
    std::vector<hsize_t> dimensions(
        data.shape(), data.shape() + data.num_dimensions());
    hdf5_write_buffered_array(
        fg, data_set_name, data, datatype, dimensions, doCreate, useBases,
        progress);
  }

  template <typename ArrayType>
  void hdf5_write_buffered_array(
      H5_CommonFileGroup &fg, const std::string &data_set_name,
      const ArrayType &data, bool doCreate = true, bool useBases = false,
      ProgressFunction progress = ProgressFunction()) {
    CosmoTool::get_hdf5_data_type<typename ArrayType::element> hdf_data_type;
    hdf5_write_buffered_array(
        fg, data_set_name, data, hdf_data_type.type(), doCreate, useBases,
        progress);
  }

}; // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
