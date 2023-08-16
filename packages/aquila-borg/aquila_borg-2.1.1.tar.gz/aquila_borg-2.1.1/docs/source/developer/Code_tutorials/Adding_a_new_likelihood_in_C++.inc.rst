Adding a new likelihood in C++
==============================

Steps to wire a C++ likelihood in hades3.

Preamble
--------

Forward models can self register now. Unfortunately likelihood cannot. So more
work is required. First one must think that there are three variants of
implementing a new likelihood. One of the three options are possible, depending
on the complexity and level of code reuse that is sought about (from more
abstract/more code-reuse to less abstract-more flexible):

1. rely on the generic framework (see
   ``extra/borg/libLSS/physics/likelihoods/gaussian.hpp`` for example)
2. use the base class of HADES
   ``extra/hades/libLSS/samplers/hades/base_likelihood.hpp``
3. implement a full likelihood from scratch

Use generic framework
---------------------

The generic framework provides more *turnkey* models at the price of
more programming abstraction.

*Warning! The following was written by Fabian. To be checked by
Guilhem.*

This works best by copying some existing classes using the generic
framework. The generic framework separates the posterior into "bias
model" and "likelihood", which then form a "bundle". Two basic working examples can be checked
to give a better impression:

- *bias:* e.g., ``extra/borg/libLSS/physics/bias/power_law.hpp`` (the Power law
  bias model)
- *likelihood:* e.g., ``extra/borg/libLSS/physics/likelihoods/gaussian.hpp``
  (the per voxel Gaussian likelihood)

Note that you do not need to recreate both likelihood and bias, if one is
sufficient for your needs (e.g., you can bundle a new bias model to an existing
likelihood). Of course, your classes can be defined with additional template
parameters, although we shall assume there are none here.

We will now see the three steps involved in the creation and link of a generic bias model.

Writing a bias model
~~~~~~~~~~~~~~~~~~~~

We will consider the noop (for no operation) bias model, which does nothing to
the input density contrast to demonstrate the steps involved in the modification
and development of a bias model. The full code is available in
``extra/borg/libLSS/physics/bias/noop.hpp``. The model requires an ample use of
templates. The reason is that a number of the exchanged arrays in the process
have very complicated types: they are not necessarily simple
``boost::multi_array_ref``, they can also be expressions. The advantage of using
expressions is the global reduction of the number of mathematical operations if
the data is masked, and the strong reduction of Input/Output memory operations,
which is generally a bottleneck in modern computers. The disadvantage is that
the compilation becomes longer and the compilation error may become obscure.

Here is a simplification of the NoopBias class (defined as a ``struct`` here which has a default visibility of public to all members):

.. code:: c++

     struct Noop {

        static constexpr const bool NmeanIsBias = true;
        static const int numParams = 1;

        selection::SimpleAdaptor selection_adaptor;

        double nmean;

        // Default constructor
        Noop(LikelihoodInfo const& = LikelihoodInfo()) {}

        // Setup the default bias parameters
        template <typename B>
        static inline void setup_default(B &params) {}

        // Prepare the bias model for computations
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_updated, MetaSelect _select = MetaSelect()) {
          nmean = params[0];
        }

        // Cleanup the bias model
        void cleanup() {}

        // This function is a relic required by the API. You can return 1 and it
        // will be fine.
        inline double get_linear_bias() const { return 1; }

        // Check whether the given array like object passes the constraints of the bias model.
        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return true;
        }

        // Compute a tuple of biased densities. The computation may be lazy or not.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(b_va_fused<double>(
                [nmean](double delta) { return nmean*(1 + delta); }, array));
        }

        // Compute a tuple of adjoint gradient on the biased densities.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          return std::make_tuple(b_va_fused<double>(
              [](double g) { return g; },
              std::move(std::get<0>(grad_array))));
        }


The bias model can be decomposed in:

1. a setup phase, with the constructor, the ``setup_default``, ``get_linear_bias``
2. a sanity check phase with ``check_bias_constraints``
3. a pre-computation, cleanup phase with ``prepare`` and ``cleanup``
4. the actual computation in ``compute_density`` and ``apply_adjoint_gradient``.

The life cycle of a computation is following roughly the above steps:

1. construct
2. setup
3. prepare computation
4. compute density
5. (optionally) compute adjoint gradient
6. cleanup

As you can see in the above most functions are templatized, for the reason
expressed before the code. As a reminder, the name of of each template indicated
after the keyword ``typename X`` indicates that we need a potentially different
type, which is discovered at the use of the specific function or class.

Let us focus on ``compute_density``:

.. code:: c++

        // Compute a tuple of biased densities. The computation may be lazy or not.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(b_va_fused<double>(
                [nmean](double delta) { return nmean*(1 + delta); }, array));
        }

Conventionally, it accepts an object which must behave, **syntaxically**, like
an a ``boost::multi_array``. In case a concrete, memory-backed, array is needed,
one has to allocate it and copy the content of ``array`` to the newly allocated
array. The member function must return a tuple (type ``std::tuple<T1, T2,
...>``) of array-like objects. As this type is complicated, we leverage a C++14
feature which allows the compiler to decide the returned type of the function by
inspecting the value provided to ``return``. Here, this is the value returned by
``make_tuple``, which is built out of a single "fused" array. The fused array is
built out of a function that is evaluated for each element of the array provided
as a second argument to ``b_va_fused``. In practice if we call ``a`` that array,
the element at i, j, k is ``a[i][j][k]`` would be strictly equal to
``nmean*(1+delta[i][j][k])``.

Writing a likelihood model
~~~~~~~~~~~~~~~~~~~~~~~~~~


Linking your bias/likelihood bundle to BORG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose then you have ``mybias.hpp``, ``mylike.hpp``, which define classes
``MyBias, MyLikelihood``. If you have encapsulated the classes in their
own namespace, make sure they are visible in the ``bias::`` namespace
(in case of MyBias) and the root namespace (in case of MyLikelihood). The
rationale behind that is to avoid polluting namespaces and avoid name collisions
while combining different headers/C++ modules.

1. each bias class has to declare the following two parameters in
   ``extra/borg/physics/bias/biases.cpp`` (which are defined in
   ``mybias.hpp``; make sure to also ``#include "mybias.hpp"``):

.. code:: c++
   
   const int LibLSS::bias::mynamespace::MyBias::numParams;
   const bool LibLSS::bias::mynamespace::EFTBias::NmeanIsBias;

2. Then, you have to *register your bundle:* in
   ``extra/hades/src/hades_bundle_init.hpp``, under
   
.. code:: c++

    std::map<
            std::string,
            std::function<std::shared_ptr<VirtualGenericBundle>(
                ptree &, std::shared_ptr<GridDensityLikelihoodBase<3>> &,
                markov_ptr &, markov_ptr &, markov_ptr &,
                std::function<MarkovSampler *(int, int)> &, LikelihoodInfo &)>>
            generic_map{ // ...
    
add your bundle:

.. code:: c++

          {"MY_BIAS_LIKE", create_generic_bundle<bias::MyBias, MyLikelihood,ptree &>}

In addition, in
``extra/borg/libLSS/samplers/generic/impl_gaussian.cpp``, add

.. code:: c++

    #include "mybias.hpp"
    #include "mylike.hpp"

as well as

.. code:: c++

    FORCE_INSTANCE(bias::MyBias, MyLikelihood, number_of_parameters);

where ``number_of_parameters`` stands for the number of free parameters
this bundle expects (i.e. bias as well as likelihood parameters). *(FS:
always impl\_gaussian?)*

*(FS: I am interpolating here...)* If on the other hand you want to
bundle your bias model with an existing likelihood, register it in
``extra/borg/src/bias_generator.cpp`` under
``LibLSS::setup_biased_density_generator``; e.g. for the Gaussian
likelihood:

.. code:: c++

     {"GAUSSIAN_MYBIAS",
       mt(generate_biased_density<AdaptBias_Gauss<bias::MyBias>>, nullMapper)},


.. todo::

   A global registry (like ``ForwardRegistry``) would be needed for this
   mechanism as well. That would save compilation time and avoid modifying the
   different bundles that rely on the generic framework.

Make an automatic test case
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to enable the *gradient test* for your bias/likelihood combination, add
a section to ``extra/borg/libLSS/tests/borg_gradients.py_config``:

.. code:: python

    'mybundle': {
        'includes':
        inc + [
            "libLSS/samplers/generic/generic_hmc_likelihood.hpp",
            "libLSS/physics/bias/mybias.hpp",
            # FS: not sure how generic this is
            "libLSS/physics/adapt_classic_to_gauss.hpp",
            "libLSS/physics/likelihoods/mylike.hpp"
        ],
        'likelihood':
        'LibLSS::GenericHMCLikelihood<LibLSS::bias::MyBias, LibLSS::MyLikelihood>',
        'model':
        default_model,
        'model_args': 'comm, box, 1e-5'
    },


Define new configuration options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to read **custom fields from the ini file**, you should edit
``extra/hades/src/likelihood_info.cpp``. Also, set default values in
``extra/hades/libLSS/tests/generic_gradient_test.cpp``;
``extra/hades/libLSS/tests/setup_hades_test_run.cpp``.

Bonus point: map the bundle to a forward model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since 2.1, all the bias generic models can be mapped to a standard
`BORGForwardModel`. The advantage is that they can be recombined in different
ways, and notably apply bias before applying specific transforms as redshift
space distortions.

This can be done easily by adding a new line in
``extra/borg/libLSS/physics/forwards/adapt_generic_bias.cpp`` in the function ``bias_registrator()``. Here is for
example the case of the linear bias model:

.. code:: c++

    ForwardRegistry::instance().registerFactory("bias::Linear", create_bias<bias::LinearBias>);

This call creates a new forward model element called ``bias::Linear`` which can
be created dynamically. The bias parameters through
``BORGForwardModel::setModelParams`` with the dictionnary entry
``biasParameters`` which must point to 1d ``boost::multi_array`` of the adequate
size. By default the adopted bias parameters are provided by the underlying
generic bias model class through ``setup_default()``.

Of course the amount of information that can be transferred is much more
limited. For example the bias model cannot at the moment produce more than one
field. All the others will be ignored. To do so would mean transforming the
forward model into an object with :math:`N` output pins (:math:`N\geq 2`).

As a final note, the forward model created that way becomes immediately
available in Python through the mechanism provided by
`:meth:aquila_borg.forward.models.newModel`. In C++ it can be accessed through the
``ForwardRegistry`` (defined in
``extra/hades/libLSS/physics/forwards/registry.hpp``).

Use HADES base class
--------------------

This framework assumes that the model is composed of a set of bias
coefficients in ``galaxy_bias_XXX`` (XXX being the number) and that the
likelihood only depends on the final matter state. An example of
likelihoods implemented on top of it is
``extra/hades/libLSS/samplers/hades/hades_linear_likelihood.cpp``, which
is a basic Gaussian likelihood.

The mechanism of applying selection effects is to be done by the new
implementation however.

With this framework one has to override a number of virtual functions. I
will discuss that on the specific case of the ``MyNewLikelihood`` which
will implement a very rudimentary Gaussian likelihood:

.. code:: c++

    class MyNewLikelihood : public HadesBaseDensityLikelihood {
    public:
        // Type alias for the supertype of this class
        typedef HadesBaseDensityLikelihood super_t;
        // Type alias for the supertype of the base class
        typedef HadesBaseDensityLikelihood::super_t grid_t;
        
    public:
        // One has to define a constructor which takes a LikelihoodInfo.
        MyNewLikelihood(LikelihoodInfo &info);
        virtual ~MyNewLikelihood();

        // This is called to setup the default bias parameters of a galaxy catalog
        void setupDefaultParameters(MarkovState &state, int catalog) override;
        
        // This is called when a mock catalog is required. The function
        // receives the matter density from the forward model and the state
        // that needs to be filled with mock data.
        void
        generateMockSpecific(ArrayRef const &matter_density, MarkovState &state) override;
        
        // This evaluates the likelihood based solely on the matter field
        // that is provided (as well as the eventual bias parameters). One
        // cannot interrogate the forward model for more fields.
        // This function must return the logarithm of the *negative* of log l
        // likelihood
        double logLikelihoodSpecific(ArrayRef const &matter_field) override;
        
        // This computes the gradient of the function implemented in
        // logLikelihoodSpecific
        void gradientLikelihoodSpecific(
            ArrayRef const &matter_field, ArrayRef &gradient_matter) override;
            
        // This is called before having resumed or initialized the chain. 
        // One should create and allocate all auxiliary fields that are 
        // required to run the chain at that moment, and mark the fields
        // of interest to be stored in the mcmc_XXXX.h5 files.
        void initializeLikelihood(MarkovState &state) override;
    };

The above declaration must go in a ``.hpp`` file such as
``my_new_likelihood.hpp``, that would be customary to be placed in
``libLSS/samplers/fancy_likelihood``. The source code itself will be
placed in ``my_new_likelihood.cpp`` in the same directory.

Constructor
~~~~~~~~~~~

The first function to implement is the constructor of the class.

.. code:: c++

    MyNewLikelihood::MyNewLikelihood(LikelihoodInfo &info)
        : super_t(info, 1 /* number of bias parameter */) {}

The constructor has to provide the ``info`` to the base class and
indicate the number of bias parameters that will be needed.

Setup default parameter
~~~~~~~~~~~~~~~~~~~~~~~

The second function allows the developer to fill up the default values
for bias parameters and other auxiliary parameters. They are auxiliary
with respect to the density field inference. In the Bayesian framework,
they are just regular parameters.

.. code:: c++

    void MyNewLikelihood::setupDefaultParameters(MarkovState& state, int catalog) {
        // Retrieve the bias array from the state dictionnary
        // This return an "ArrayStateElement *" object
        // Note that "formatGet" applies string formatting. No need to
        // call boost::format.
        auto bias = state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog);
        // This extracts the actually boost::multi_array from the state element.
        // We take a reference here.
        auto &bias_c = *bias->array;
        // Similarly, if needed, we can retrieve the nmean
        auto &nmean_c = state.formatGetScalar<double>("galaxy_nmean_%d", catalog);

        // Now we can fill up the array and value.
        bias_c[0] = 1.0;
        nmean_c = 1;
    }

Note in the above that we asked for ``auto&`` reference types for
``bias_c`` and ``nmean_c``. The ``auto`` asks the compiler to figure out
the type by itself. However it will not build a reference by default.
This is achieved by adding the ``&`` symbol. That way any value written
into this variable will be reflected in the original container. This
**would not** be the case without the reference. Also note that the
``galaxy_bias_%d`` is already allocated to hold the number of parameters
indicated to the constructor to the base class.

Initialize the likelihood
~~~~~~~~~~~~~~~~~~~~~~~~~

The initialization done by the base class already takes care of
allocating ``galaxy_bias_%d``, ``BORG_final_density``, checking on the
size of ``galaxy_data_%d``. One could then do the minimum amount of
work, i.e. not even override that function or putting a single statement
like this:

.. code:: c++

    void MyNewLikelihood::initializeLikelihood(MarkovState &state) {
        super_t::initializeLikelihood(state);
    }

If more fields are required to be saved/dumped and allocated, this would
otherwise be the perfect place for it. However keep in mind that it is
possible that the content of fields in ``MarkovState`` is not
initialized. You may rely on the info provided to the constructor in
``LikelihoodInfo`` for such cases.

Evaluate the log likelihood
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we arrive at the last piece. The class
``HadesBaseDensityLikelihood`` offers a great simplification compared to
recoding everything including the management of the forward model for
the evaluation of the log likelihood and its adjoint gradient.

.. warning::

    The function is called logLikelihoodSpecific but it is actually the
    negative of the log likelihood.

    .. math::  \mathrm{logLikelihoodSpecific}(\delta_\mathrm{m})  = -\log \mathcal{L}(\delta_\mathrm{m}) 

    This sign is for historical reason as the Hamiltonian Markov Chain
    algorithm requires the gradient of that function to proceed.

    **[FS: actually when using the generic framework, it seems
    log\_probability actually returns log( P )...]**

As an example we will consider here the case of the Gaussian likelihood.
The noise in each voxel are all i.i.d. thus we can factorize the
likelihood into smaller pieces, one for each voxel:

.. math::  \mathcal{L}(\{N_{i,g}\}|\{\delta_{i,\text{m}}\}) = \prod \mathcal{L}(N_{i,g}|\delta_{i,\text{m}}) 

The likelihood for each voxel is:

.. math::  \mathcal{L}(N_g|\delta_\text{m},b,\bar{N}) \propto \frac{1}{\sqrt{R\bar{N}}} \exp\left(-\frac{1}{2 R\bar{N}} \left(N_g - R \bar{N}(1+b\delta_m\right)^2 \right) 

We will implement that computation. The first function that we will
consider is the evaluation of the log likelihood itself.

.. code:: c++

    double
    MyNewLikelihood::logLikelihoodSpecific(ArrayRef const &delta) {
    // First create a variable to accumulate the log-likelihood.
    double logLikelihood = 0;
    // Gather the information on the final output sizes of the gridded
    // density.
    // "model" is provided by the base class, which is of type 
    // std::shared_ptr<BORGForwardModel>, more details in the text
    size_t const startN0 = model->out_mgr->startN0;
    size_t const endN0 = startN0 + model->out_mgr->localN0;
    size_t const N1 = model->out_mgr->N1;
    size_t const N2 = model->out_mgr->N2;

    // Now we may loop on all catalogs, "Ncat" is also provided
    // by the base class as well as "sel_field", "nmean", "bias" and 
    // "data"
    for (int c = 0; c < Ncat; c++) {
        // This extract the 3d selection array of the catalog "c"
        // The arrays follow the same scheme as "setupDefaultParameters"
        auto &sel_array = *(sel_field[c]);
        // Here we do not request a Read/Write access to nmean. We can copy
        // the value which is more efficient.
        double nmean_c = nmean[c];
        double bias_c = (*(bias[c]))[0];
        auto &data_c = *(data[c]);

        // Once a catalog is selected we may start doing work on voxels.
        // The openmp statement is to allow the collapse of the 3-loops
    #pragma omp parallel for collapse(3) reduction(+:logLikelihood)
        for (size_t n0 = startN0; n0 < endN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
            for (size_t n2 = 0; n2 < N2; n2++) {
            // Grab the selection value in voxel n0xn1xn2
            double selection = sel_array[n0][n1][n2];

            // if the voxel is non-zero, it must be counted
            if (selection > 0) {
                double Nobs = data_c[n0][n1][n2];
                // bias the matter field
                double d_galaxy = bias_c * delta[n0][n1][n2];

                // Here is the argument of the exponential
                logLikelihood += square(selection * nmean_c * (1 + d_galaxy) - Nobs) /
                    (selection * nmean_c) + log(R nmean_c);
            }
            }
        }
        }
    }

    return logLikelihood;
    }

This completes the likelihood. As one can see there is not much going
on. It is basically a sum of squared differences in a triple loop.

The adjoint gradient defined as

.. math::  \mathrm{adjoint\_gradient}(\delta_\mathrm{m})  = -\nabla \log \mathcal{L}(\delta_\mathrm{m}) 

follows the same logic, except that instead of a scalar, the function
returns a vector under the shape of a mesh. Note that ``ArrayRef`` is
actually a ``boost::multi_array_ref`` with the adequate type.

.. code:: c++

    void MyNewLikelihood::gradientLikelihoodSpecific(
        ArrayRef const &delta, ArrayRef &grad_array) {
    // Grab the mesh description as for the likelihood
    size_t const startN0 = model->out_mgr->startN0;
    size_t const endN0 = startN0 + model->out_mgr->localN0;
    size_t const N1 = model->out_mgr->N1;
    size_t const N2 = model->out_mgr->N2;

    // A shortcut to put zero in all entries of the array.
    // "fwrap(array)" becomes a vectorized expression
    fwrap(grad_array) = 0;
    
    for (int c = 0; c < Ncat; c++) {
        auto &sel_array = *(sel_field[c]);
        auto &data_c = *(data[c]);
        double bias_c = (*bias[c])[0];
        double nmean_c = nmean[c];

    #pragma omp parallel for collapse(3)
        for (size_t n0 = startN0; n0 < endN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
            for (size_t n2 = 0; n2 < N2; n2++) {
            double deltaElement = delta[n0][n1][n2];
            double d_galaxy = bias_c * deltaElement;
            double d_galaxy_prime = bias_c;
            double response = sel_array[n0][n1][n2];
            double Nobs = data_c[n0][n1][n2];

            // If selection/mask is zero, we can safely skip that 
            // particular voxel. It will not produce any gradient value.
            if (response == 0)
                continue;

            // Otherwise, we accumulate the gradient
            grad_array[n0][n1][n2] +=
                (nmean_c * response * (1 + d_galaxy) - Nobs) * d_galaxy_prime
            }
        }
        }
    }
    }

Adding the code to the build infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are in the ``borg`` module, you must open the file named
``libLSS/borg.cmake``. It contains the instruction to compile the
``borg`` module into ``libLSS``. To do that it is sufficient to add the
new source files to the ``EXTRA_LIBLSS`` cmake variable. As one can see
from the cmake file there is a variable to indicate the directory of
``libLSS`` in ``borg``: it is called ``BASE_BORG_LIBLSS``. One can then
add the new source file like this:

.. code:: CMake

    SET(EXTRA_LIBLSS ${EXTRA_LIBLSS}
        ${BASE_BORG_LIBLSS}/samplers/fancy_likelihood/my_new_likelihood.cpp
        # The rest is left out only for the purpose of this documentation
    )

Then the new file will be built into ``libLSS``.

Linking the new likelihood to hades
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this it is unfortunately necessary to hack into
``extra/hades/src/hades_bundle_init.hpp``, which holds the
initialization logic for ``hades3`` specific set of likelihood, bias,
and forward models. The relevant lines in the source code are the
following ones:

.. code:: c++

    if (lh_type == "LINEAR") {
        bundle.hades_bundle = std::make_unique<LinearBundle>(like_info);
        likelihood = bundle.hades_bundle->likelihood;
        }
    #ifdef HADES_SUPPORT_BORG
        else if (lh_type == "BORG_POISSON") {

In the above ``lh_type`` is a ``std::string`` containing the value of
the field ``likelihood`` in the ini file. Here we check whether it is
``"LINEAR"`` or ``"BORG_POISSON"``.

To add a new likelihood ``"NEW_LIKELIHOOD"`` we shall add the following
lines:

.. code:: c++

    if (lh_type == "LINEAR") {
        bundle.hades_bundle = std::make_unique<LinearBundle>(like_info);
        likelihood = bundle.hades_bundle->likelihood;
        }
    #ifdef HADES_SUPPORT_BORG
        else if (lh_type == "NEW_LIKELIHOOD") {
        typedef HadesBundle<MyNewLikelihood> NewBundle;
        bundle.hades_bundle = std::make_unique<NewBundle>(like_info);
        likelihood = bundle.hades_bundle->likelihood;
        }
        else if (lh_type == "BORG_POISSON") {

while also adding

.. code:: c++

    #include "libLSS/samplers/fancy_likelihood/my_new_likelihood.hpp"

towards the top of the file.

The above piece of code define a new bundle using the template class
``HadesBundle<T>``. ``T`` can be any class that derives from
``HadesBaseDensityLikelihood``. Then this bundle is constructed,
providing the likelihood info object in ``like_info``. Finally the built
likelihood object is copied into ``likelihood`` for further processing
by the rest of the code.

.. note::

    If you need to query more parameters from the ini file (for example the
    ``[likelihood]`` section), you need to look for them using ``params``.
    For example ``params.template get<float>("likelihood.k_max")`` will
    retrieve a float value from the field ``k_max`` in ``[likelihood]``
    section. You can then store it in ``like_info`` (which is a
    `std::map <http://www.cplusplus.com/reference/map/map/>`__ in
    practice)

    .. code:: c++

        like_info["good_k_max"] = params.template get<float>("likelihood.k_max");

    In your constructor you can then retrieve the value from the new entry
    as: 

    .. code:: c++

        boost::any_cast<float>(like_info["good_k_max"])

And now you are done! You can now set
``likelihood=NEW_LIKELIHOOD`` in the ini file and your new code will be
used by hades.

Implement from scratch
----------------------

*to be written even later*
