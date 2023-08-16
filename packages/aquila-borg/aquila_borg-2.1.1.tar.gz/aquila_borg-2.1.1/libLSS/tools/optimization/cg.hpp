/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/optimization/cg.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_CG_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_CG_HPP

#include <algorithm>
#include <functional>

#include <boost/multi_array.hpp>
#include <boost/bind.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fused_array.hpp"

#include "libLSS/tools/fused_assign.hpp"

#include "libLSS/tools/optimization/array_helper.hpp"

namespace LibLSS {

  namespace Optimization {
    namespace details {
      template <typename T>
      T lazy_conj(T const &c) {
        return c;
      }

      template <typename T>
      std::complex<T> lazy_conj(std::complex<T> const &c) {
        return std::conj(c);
      }
    } // namespace details

    template <typename ArrayAllocator>
    struct CG {
    public:
      unsigned int cg_refresh;
      double epsilon;
      unsigned int T;
      typedef typename ArrayAllocator::array_t array_t;
      typedef std::function<void(array_t& out, array_t const& in)> Matrix_function_t;
      typedef std::function<void(array_t& out, array_t const& in, int s)> Precon_Matrix_function_t;

      public:
      CG(ArrayAllocator alloc_ = ArrayAllocator()):allocator(alloc_) {
        cg_refresh = 1000; // sets refreshing rate for conjugating directions
        epsilon = 1e-9;  // sets convergence criterion
        T = 40000000;       // sets maximum number of cg steps
      }

      ~CG() {}

      void
      run(Matrix_function_t A, array_t const &b,
          array_t &x) {

        ConsoleContext<LOG_VERBOSE> ctx("CG::run");
        Console &cons = Console::instance();

        auto r = allocator.new_like(x);
        auto d = allocator.new_like(x);
        auto q = allocator.new_like(x);
        auto wx = allocator.wrapper(x);
        auto wb = allocator.wrapper(b);

        double dnew  = 0.0;
	double dinit = 0.0;
        double dold  = 0.0;


        //apply matrix to x vector
        A(q.get(), x);

        //initialize values
        *r = b - *q;
        *d = *r;

        dinit = dotprod(wb,wb);
        dnew = dotprod(*r, *r);
        dold = dnew;

        int t = 0;

        Progress<LOG_INFO_SINGLE> &progress =
            cons.start_progress<LOG_INFO_SINGLE>(
                "applying conjugate gradient", T, 10);
	
        while ((t < T)) {

          //apply matrix to d vector
          A(q.get(), d.get());
	
	  double dq = dotprod(*d, *q);	
	  cons.print<LOG_DEBUG>(boost::format("residue is dq=%g ") % dq);
	  
          //now determine alpha
          double alpha = dnew / (dq+1e-40);

	  cons.print<LOG_DEBUG>(boost::format("alpha =%g ") % alpha);
	
          //now update x vector
          wx = wx + alpha * (*d);

	  bool exit= false; 	
          if (t % cg_refresh == 0) {

            A(q.get(), x);

	    *r = b -(*q);
	    exit=true;
	    cons.print<LOG_DEBUG>("Refresh! ");

          } else {

	    *r = r.get() - alpha*(*q);

          }

          dold = dnew;

          dnew = dotprod(*r, *r);

	  double const ratio = dnew/dinit;
	  cons.print<LOG_DEBUG>(boost::format("t=%g residue is dnew=%g / dinit=%g => ratio=%g") % t % dnew % dinit % ratio);

          double beta = dnew / dold;

	  cons.print<LOG_DEBUG>(boost::format("beta - 1 =%g ") % (beta-1.));

	  *d = *r + beta*(*d);
	
          t++;

          progress.update(t);
		
	  double const dcheck = dotprod(*r, *r);
          cons.print<LOG_DEBUG>(boost::format("residue is dnew=%g / dcheck=%g / dinit=%g") % dnew % dcheck % dinit);
	  if( (dcheck/dinit)<epsilon) { // or ( fabs(beta-1.) < epsilon ))
            A(q.get(), x);
	    double const dcheck2 = dotprod(*q - b, *q - b);
            cons.print<LOG_DEBUG>(boost::format("breaking at %g") % (dcheck/dinit));
            cons.print<LOG_DEBUG>(boost::format("breaking at %g??") % (dcheck2/dinit));
	    if ((dcheck2/dinit)<epsilon)
	      break;	
            cons.print<LOG_DEBUG>("no");
	  }

        }
	cons.print<LOG_DEBUG>("Done with CG");

        progress.destroy();
      }

    void
      run(Matrix_function_t A, Precon_Matrix_function_t M_inv, typename ArrayAllocator::array_t const&b,
          typename ArrayAllocator::array_t &x) {

        ConsoleContext<LOG_VERBOSE> ctx("CG::run");
        Console &cons = Console::instance();

	auto r = allocator.new_like(x);
	auto d = allocator.new_like(x);
	auto q = allocator.new_like(x);
	auto s = allocator.new_like(x);

        double dnew = 0.0;
	double dinit = 0.0;
        double dold = 0.0;

        //apply matrix to x vector
        A(q.get(), x);

        //initialize values
	*r = b - *q;

	//use preconditioner
	M_inv(d.get(), r.get(),1);

	dinit = dnew = dotprod(*r, *d);

        dold = dnew;

        int t = 0;

        Progress<LOG_INFO_SINGLE> &progress =
            cons.start_progress<LOG_INFO_SINGLE>(
                "applying conjugate gradient", T, 10);

	
        while ((t < T)) {// and (dinit > epsilon * epsilon)) {

          //apply matrix to d vector
          A(q.get(), d.get());

	  double dq = dotprod(*d, *q);

          //now determine alpha
          double alpha = dnew / (dq+1e-40);
	

          //now update x vector
          fwrap(x) = fwrap(x) + alpha*(*d);

	  bool exit=false;
          if (t % cg_refresh == 0) {

            A(q.get(), x);

	    *r = b -(*q);
	    exit=true;	
          } else {

	    *r = r.get() - alpha*(*q);

          }

	  M_inv(s.get(), r.get(),1);

	  dold = dnew;

          dnew = dotprod(*r, *s);


          double beta = dnew / dold;

	  *d = *s + beta*(*d);

          t++;

          progress.update(t);

	  double const dcheck = dotprod(*r, *r);
          cons.print<LOG_DEBUG>(boost::format("residue is dnew=%g / dcheck=%g / dinit=%g") % dnew % dcheck % dinit);
	  if( (dcheck/dinit)<epsilon) { // or ( fabs(beta-1.) < epsilon ))
            cons.print<LOG_DEBUG>(boost::format("breaking at %g") % (dcheck/dinit));
	    break;	
	  }

	

        }

        progress.destroy();

      }

      private:
      ArrayAllocator allocator;
    };


  } // namespace Optimization

  using Optimization::CG;

}; // namespace LibLSS

#endif
