/*+
    ARES/HADES/BORG Package -- ./libLSS/mcmc/state_sync.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_STATE_ELEMENT_SYNC_HPP
#define __LIBLSS_STATE_ELEMENT_SYNC_HPP

#include <functional>
#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"

namespace LibLSS {

    class StateElement;
    
    /**
     * Helper class to synchronize many StateElement variable at the same time with MPI.
     * @deprecated
     */
    class MPI_SyncBundle {
    protected:
        typedef std::list<StateElement *> List;
        
        List list;
    public:
	/// Constructor
        MPI_SyncBundle() {}
        ~MPI_SyncBundle() {}
        
	/**
	 * Add a specified element to the bundle.
	 * @param e the element to be added
	 */
        MPI_SyncBundle& operator+=(StateElement *e) {
            list.push_back(e);
            return *this;
        }

	/**
	 * Execute the provided synchronization function on all elements
	 * of the bundle.
	 * @param f the Functor to be executed.
	 */
        template<typename Function>
        void syncData(Function f) {
            ConsoleContext<LOG_DEBUG> ctx("sync bundle");
            for (List::iterator i = list.begin(); i != list.end(); ++i)
                (*i)->syncData(f);
        }
        
	/**
	 * Execute a broadcast operation on the bundle.
	 * @param comm the MPI communicator.
	 * @param root the root for the broadcast operation (default is 0).
	 */
        void mpiBroadcast(MPI_Communication& comm, int root = 0) {
	    namespace ph = std::placeholders;
            syncData(std::bind(&MPI_Communication::broadcast, comm, ph::_1, ph::_2, ph::_3, root));
        }

	/**
	 * Execute a all reduce (max) operation on the bundle.
	 * @param comm the MPI communicator.
	 */
        void mpiAllMax(MPI_Communication& comm) {
	    namespace ph = std::placeholders;
            syncData(std::bind(&MPI_Communication::all_reduce, comm, MPI_IN_PLACE, ph::_1, ph::_2, ph::_3, MPI_MAX));
        }

	/**
	 * Execute a all reduce (sum) operation on the bundle.
	 * @param comm the MPI communicator.
	 */
        void mpiAllSum(MPI_Communication& comm) {
	    namespace ph = std::placeholders;
            syncData(std::bind(&MPI_Communication::all_reduce, comm, MPI_IN_PLACE, ph::_1, ph::_2, ph::_3, MPI_SUM));
        }
        
    };
    
};

#endif
