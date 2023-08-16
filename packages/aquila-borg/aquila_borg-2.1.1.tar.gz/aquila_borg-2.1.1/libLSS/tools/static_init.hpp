/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/static_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_STATIC_INIT_HPP
#define __LIBLSS_STATIC_INIT_HPP

#include <vector>
#include <queue>
#include <boost/function.hpp>
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"

namespace LibLSS {

#if !defined(DOXYGEN_SHOULD_SKIP_THIS)
    class RegisterStaticInitBase {
    protected:
        int priority;
        std::string text;
        friend struct CompareStaticInit;
        friend struct CompareStaticFinal;
        friend class StaticInit;
    public:
        virtual void executeStaticInit() = 0;
        virtual void executeStaticFinal() = 0;
        virtual ~RegisterStaticInitBase() {}
    };

    struct CompareStaticInit {
        bool operator()(RegisterStaticInitBase *a, RegisterStaticInitBase *b) {
            return a->priority >= b->priority;
        }
    };

    struct CompareStaticFinal {
        bool operator()(RegisterStaticInitBase *a, RegisterStaticInitBase *b) {
            return a->priority <= b->priority;
        }
    };
#endif

    /**
     * Helper class to handle initialization of some global state. 
     * There is by design only one instance of this class. It may obtained
     * through the static method StaticInit::instance(). 
     * Nearly all test cases give an example of the use this API. Typically,
     * this is the first line of code and the last line of code in the "main" 
     * function.
     * @code
     *   int main() {
     *     StaticInit::initialize();
     *     // Do something
     *     StaticInit::finalize();
     *     return 0;
     *   }
     * @endcode
     * The initializers and finalizers are executed according to their priority code,
     * provided at the registration.
     *
     * @see LibLSS::RegisterStaticInit
     * @see LibLSS::Console
     */
    class StaticInit {
    private:
        StaticInit() {}

        void _execute() {
            while (!all_initializers.empty()) {
                RegisterStaticInitBase *i = all_initializers.top();
                if (i->text.length() > 0) {
                    Console::instance().print<LOG_DEBUG>("INIT: " + i->text);
                }
                i->executeStaticInit();
                all_initializers.pop();
            }
        }

        void _finalize() {
            while (!all_finalizers.empty()) {
                RegisterStaticInitBase *i = all_finalizers.top();
                if (i->text.length() > 0) {
                    Console::instance().print<LOG_DEBUG>("CLEANUP: " + i->text);
                }
                i->executeStaticFinal();
                all_finalizers.pop();
            }
        }

    public:
        static const int MAX_PRIORITY = 0;
        static const int MIN_PRIORITY = 99;
        typedef std::priority_queue<RegisterStaticInitBase *, std::vector<RegisterStaticInitBase *>, CompareStaticInit> InitList;
        typedef std::priority_queue<RegisterStaticInitBase *, std::vector<RegisterStaticInitBase *>, CompareStaticFinal> FinalList;
        InitList all_initializers;
        FinalList all_finalizers;
        
        static StaticInit& instance();
        
	/**
	 * @see LibLSS::RegisterStaticInit
	 */
        void add(RegisterStaticInitBase *b) {
            all_initializers.push(b);
            all_finalizers.push(b);
        }

	/**
	 * Run all initializers.
	 */
        static void execute() {
            instance()._execute();
        }

	/**
	 * Run all finalizers.
	 */
        static void finalize() {
            instance()._finalize();
        }
 
    };
    
    /**
     * Specific implementation of a registrator for static initializer .
     * It introduces itself directly in the queue of the sole instance of the class LibLSS::StaticInit.
     * They then call the adequate functors in initialization or finalization stage.
     */
    class RegisterStaticInit: public RegisterStaticInitBase {
    public:
	/**
	 * Hold the initializer functor.
	 */
        std::function<void()> function;
	/**
	 * Hold the finalizer functor.
	 */
        std::function<void()> function_final;
        
	/**
	 * Constructor, without finalizer.
	 *
	 * @param f         The functor corresponding to initialization. There is no finalizer in this case.
	 * @param _priority The execution priority.
	 * @param _text     an information to print in debug mode.
	 */
        template<typename Derived>
        RegisterStaticInit(Derived f, int _priority = StaticInit::MIN_PRIORITY, const std::string& _text = "") {
            function = f;
            this->priority = _priority;
            this->text = _text;
            StaticInit::instance().all_initializers.push(this);
        }

	/**
	 * Constructor.
	 * @param f         The functor corresponding to initialization. 
	 * @param f2        The functor corresponding to finalization.
	 * @param _priority The execution priority.
	 * @param _text     an information to print in debug mode.
	 */
        template<typename Derived1, typename Derived2>
        RegisterStaticInit(Derived1 f, Derived2 f2, int _priority = StaticInit::MIN_PRIORITY, const std::string& _text = "") {
            function = f;
            function_final = f2;
            this->priority = _priority;
            this->text = _text;
            StaticInit::instance().all_initializers.push(this);
            StaticInit::instance().all_finalizers.push(this);
        }

	/**
	 * Do not use. This is called by the internal machinery.
	 */
        virtual void executeStaticInit() {
            function();
        }
 
	/**
	 * Do not use. This is called by the internal machinery.
	 */
        virtual void executeStaticFinal() {
            if (function_final)
	      function_final();
        }

    private:       
        RegisterStaticInit() {
        }        
    };

};

#endif
