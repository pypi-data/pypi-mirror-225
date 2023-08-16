/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/hdf5_scalar.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HDF5_SCALAR_HPP
#define __LIBLSS_HDF5_SCALAR_HPP

#include <boost/format.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS {
    
    template<typename T>
    void hdf5_save_scalar(H5_CommonFileGroup& fg, const std::string& name, const T& scalar) {
        hsize_t d = 1;
        using CosmoTool::get_hdf5_data_type;
        H5::DataSpace dataspace(1, &d);
        H5::DataSet dataset = fg.createDataSet(name, get_hdf5_data_type<T>::type(), dataspace);
        
        dataset.write(&scalar, get_hdf5_data_type<T>::type());
    }

    namespace details {
        namespace {
            void scalar_error(const std::string& name) {
                error_helper<ErrorIO>(boost::format("Scalar '%s' has wrong dimensions in file") % name);
            }
        }
    }

    
    template<typename T>
    T hdf5_load_scalar(H5_CommonFileGroup& fg, const std::string& name) {
        using CosmoTool::get_hdf5_data_type;
        H5::DataSet dataset = fg.openDataSet(name);
        H5::DataSpace dataspace = dataset.getSpace();
        hsize_t d;
        
        if (dataspace.getSimpleExtentNdims() != 1)
            details::scalar_error(name);

        dataspace.getSimpleExtentDims(&d);
        if (d != 1)
            details::scalar_error(name);
        
        T data;
        dataset.read(&data, get_hdf5_data_type<T>::type());
        return data;
    }
    
}

#endif
