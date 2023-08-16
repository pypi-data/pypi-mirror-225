/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/random_number.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __RANDOM_NUMBER_HPP
#define __RANDOM_NUMBER_HPP

#include <cmath>
#include <boost/format.hpp>
#include <functional>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/openmp.hpp"
#include <H5Cpp.h>
#include <CosmoTool/hdf5_array.hpp>
#include <iostream>
#include "libLSS/tools/array_concepts.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS {

    class RandomNumber;
    namespace Random_details {
      // This is a workaround for a bug in GCC compiler which
      // has a problem using boost::bind on member function in declspec.
      inline unsigned int real_poisson(RandomNumber *rgen, double nmean);
      inline double real_gaussian(RandomNumber *rgen, double dev);
      inline unsigned int real_gamma(RandomNumber *rgen, double a, double b);
      inline unsigned int real_negative_binomial(RandomNumber *rgen, double p, double n);
    }

    /**
     * Fundamental class to provide random number generation.
     */ 
    class RandomNumber
    {
    public:
        virtual ~RandomNumber() {}
        /**
         * This returns a random 32-bit integer, uniformly distributed.
         * @return a random integer
         */ 
        virtual unsigned long int get() = 0;
        /**
         * This returns a uniformly distributed double precision floating point.
         * @param a random floating point.
         */
        virtual double uniform() = 0;

        /**
         * Provide a seed to initialize the Pseudo Random Number Generator.
         * @param s a seed value
         */
        virtual void seed(unsigned long int s) = 0;
        /**
         * Save the internal state of the PRNG into the provided HDF5 group.
         * @param s an HDF5 group.
         */
        virtual void save(H5_CommonFileGroup& s) = 0;
        /**
         * Restore the internal state of the PRNG from the provided HDF5 group.
         * @param s        an HDF5 group.
         * @param flexible specify if we accept some inconsistency in the input group (i.e. different thread count).
         */
        virtual void restore(H5_CommonFileGroup& s, bool flexible = false) = 0;

        double gaussian_ratio();

        /**
         * Generate a Poisson distributed random integer with the specified intensity.
         * @param mean Poisson intensity 
         */ 
        virtual unsigned int poisson(double mean) = 0;
        virtual unsigned int negative_binomial(double p, double n) = 0;

        /**
         * Generate numbers that are uniformly distributed. The actual value in wrap is ignored. It is only
         * used to determine the rank of the required array.
         * @param wrap a wrapped expression to provide the rank of the output array. 
         */ 
        template<typename Array, bool copy>
        void uniform(LibLSS::FuseWrapper_detail::Wrapper<Array,copy> wrap) {
          wrap = b_va_fused<double,Array::dimensionality>([this](int, ...)->double { return this->uniform(); });
        }

        // Only activate this overload if the type looks like an array
        template<typename Array, bool copy, typename Array2, bool copy2>
        auto gamma(LibLSS::FuseWrapper_detail::Wrapper<Array,copy> wrap, LibLSS::FuseWrapper_detail::Wrapper<Array2,copy2> wrap2)
        {
          return LibLSS::fwrap(
            LibLSS::b_va_fused<unsigned int>(
              std::bind(&LibLSS::Random_details::real_gamma,
                          this, std::placeholders::_1, std::placeholders::_2),
              wrap.forward_wrap(),
              wrap2.forward_wrap()
            )
          );
        }

        /**
         * Build an expression that generate random number that are distributed as a Negative Binomial
         * with an intensity as provided by the wrap expression, and an additional miss term with the second
         * expression.
         * @param wrap the expression providing the Poisson intensity.
         * @param wrap2 the expression providing the missed intensity.
         */
        template<typename Array, bool copy, typename Array2, bool copy2>
        auto negative_binomial(LibLSS::FuseWrapper_detail::Wrapper<Array,copy> wrap, LibLSS::FuseWrapper_detail::Wrapper<Array2,copy2> wrap2)
        {
          return LibLSS::fwrap(
            LibLSS::b_va_fused<unsigned int>(
              std::bind(&LibLSS::Random_details::real_negative_binomial,
                          this, std::placeholders::_1, std::placeholders::_2),
              wrap.forward_wrap(),
              wrap2.forward_wrap()
            )
          );
        }



        /**
         * Build an expression that generate random number that are Poisson distributed
         * with an intensity as provided by the wrap expression.
         * @param wrap the expression providing the Poisson intensity.
         */
        template<typename Array, bool copy>
        auto poisson(LibLSS::FuseWrapper_detail::Wrapper<Array,copy> wrap)
        {
          return LibLSS::fwrap(
            LibLSS::b_va_fused<unsigned int>(
              std::bind(&LibLSS::Random_details::real_poisson,
                          this, std::placeholders::_1),
              wrap.forward_wrap()
            )
          );
        }

        /**
         * Build an expression that generate gaussian random number whose standard deviation is determined
         * by the input wrapped expression. The mean is set to zero.
         * @param wrap the expression providing the standard deviation.
         */
        template<typename Array, bool copy>
        auto gaussian(LibLSS::FuseWrapper_detail::Wrapper<Array,copy> wrap)
        {
          return LibLSS::fwrap(
            LibLSS::b_va_fused<typename Array::element>(
              std::bind(&LibLSS::Random_details::real_gaussian,
                          this, std::placeholders::_1),
              wrap.forward_wrap()
            )
          );
        }


        /**
         * Return a single random number gaussian distributed 
         */
        double gaussian() { return gaussian_ratio(); }
        virtual double gamma(double a, double b) = 0;
    };

    namespace Random_details {
      inline  unsigned int real_poisson(RandomNumber *rgen, double nmean) {
          return rgen->poisson(nmean);
      }

      inline  unsigned int real_gamma(RandomNumber *rgen, double a, double b) {
          return rgen->gamma(a, b);
      }

      inline  unsigned int real_negative_binomial(RandomNumber *rgen, double a, double b) {
          return rgen->negative_binomial(a, b);
      }

      inline double real_gaussian(RandomNumber *rgen, double a) {
        return rgen->gaussian()*a;
      }
    }

    /**
     * A Random number generator that works in multi-threaded environment. 
     * The base class is provided through a template argument.
     */
    template<typename BaseGenerator>
    class RandomNumberThreaded: public RandomNumber {
    protected:
        RandomNumberThreaded()
            : gens(0), numGenerators(0) {

        }

    public:
        typedef BaseGenerator base_type;

        BaseGenerator *gens;
        int numGenerators;

        void realInit(BaseGenerator& b, int force_max) {
            using boost::format;

            numGenerators = (force_max < 0) ? smp_get_max_threads() : force_max;

            Console::instance().format<LOG_INFO>(
                        "Initializing %d threaded random number generators", numGenerators
                );

            gens = new BaseGenerator[numGenerators];

            // Not great entropy
            for (int i = 0; i < numGenerators; i++)
                gens[i].seed(b.get());
        }

        /**
         * Constructor.
         * @param force_max  an argument to specific the maximum number of threads that will
         *                   be used. If equal to -1, it will get the current limit from OpenMP.
         */
        RandomNumberThreaded(int force_max) {
            BaseGenerator b;

            realInit(b, force_max);
        }


        /**
         * Return the base generator for the current thread
         * @return the fundamental generator for the current thread.
         */
        BaseGenerator &base() {
            return gens[smp_get_thread_id()];
        }

        /**
         * Destructor.
         */
        virtual ~RandomNumberThreaded() {
            if (gens == 0)
                return;

            Console::instance().print<LOG_INFO>(
                        "Cleaning up parallel random number generators"
            );

            delete[] gens;
        }

        virtual void seed(unsigned long s) {
            BaseGenerator b;
            Console::instance().format<LOG_VERBOSE>("THREADED: Changing random number generation seed with %ld", s);

            b.seed(s);
            for (int i = 0; i < numGenerators; i++)
                gens[i].seed(b.get());
        }

        virtual unsigned long get() {
            return base().get();
        }

        virtual double uniform() {
            return base().uniform();
        }

        virtual unsigned int poisson(double mean) {
            return base().poisson(mean);
        }

        virtual double gamma(double a, double b) {
            return base().gamma(a, b);
        }

        virtual unsigned int negative_binomial(double p, double n) {
            return base().negative_binomial(p, n);
        }

        using RandomNumber::poisson;
        using RandomNumber::gamma;
        using RandomNumber::negative_binomial;
        using RandomNumber::gaussian;
        using RandomNumber::uniform;


        virtual void save(H5_CommonFileGroup& g) {
            using boost::str;
            using boost::format;
            boost::multi_array<int, 1> gen_array(boost::extents[1]);

            gen_array[0] = numGenerators;
            CosmoTool::hdf5_write_array(g, "num_generators", gen_array);
            for (int i = 0; i < numGenerators; i++) {
                H5::Group subg = g.createGroup(str(format("generator_%d") % i));
                gens[i].save(subg);
            }
        }

        virtual void restore(H5_CommonFileGroup& g, bool flexible = false) {
            using boost::str;
            using boost::format;
            boost::multi_array<int, 1> gen_array;

            CosmoTool::hdf5_read_array(g, "num_generators", gen_array);
            if (gen_array[0] != numGenerators) {
                std::string s = str(boost::format(
                          "The current number of threads (%d) is not compatible with file state (%d)")
                          % numGenerators % gen_array[0]);

                if (!flexible) {
                  error_helper<ErrorBadState>(s);
                } else {
                  Console::instance().print<LOG_WARNING>(s);
                }
            }

            int num_to_read = std::min(numGenerators, gen_array[0]);
            for (int i = 0; i < num_to_read; i++) {
                H5::Group subg = g.openGroup(str(format("generator_%d") % i));
                gens[i].restore(subg, flexible);
            }
        }
    };

    /**
     * A random number generator that works in MPI environment.
     */
    template<typename BaseGenerator>
    class RandomNumberMPI: public RandomNumberThreaded<BaseGenerator> {
    public:
        typedef RandomNumberThreaded<BaseGenerator> BaseClass;
        MPI_Communication *comm;

        /**
          * Constructor.
          * @param comm       an MPI communicator over which the PRNG must work.
          * @param force_max  sets the maximum number of threads per MPI task that will in parallel.
          */ 
        RandomNumberMPI(MPI_Communication *_comm, int force_max)
            : BaseClass(), comm(_comm) {
            BaseGenerator b;
            unsigned long int seedVal = 0;

            if (comm->rank() == 0) {
                for (int r = 1; r < comm->size(); r++) {
                    seedVal = b.get();
                    comm->send(&seedVal, 1, translateMPIType<unsigned long int>(), r, 0);
                }
            } else {
                comm->recv(&seedVal, 1, translateMPIType<unsigned long int>(), 0, 0);
            }

            b.seed(seedVal);

            this->realInit(b, force_max);
        }

        virtual void seed(unsigned long s) {
            BaseGenerator b;
            unsigned long int seedVal;

            Console::instance().format<LOG_VERBOSE>("MPI: Changing random number generation seed with %ld", s);
            b.seed(s);
            if (comm->rank() == 0) {
                for (int r = 1; r < comm->size(); r++) {
                    seedVal = b.get();
                    comm->send(&seedVal, 1, translateMPIType<unsigned long int>(), r, 0);
                }
                seedVal = b.get();
            } else {
                comm->recv(&seedVal, 1, translateMPIType<unsigned long int>(), 0, 0);
            }

            BaseClass::seed(seedVal);
        }
    };




#include "gaussian_ratio.tcc"

};

#endif
