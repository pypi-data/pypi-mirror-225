/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io/output.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
namespace LibLSS {
  namespace detail_output {
    template <size_t Nd>
    using BoxModelIO = NBoxModel<Nd>;

    template <typename T, size_t Nd>
    struct _normalization;

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::CArrayRef, Nd> {
      static double fwd(BoxModelIO<Nd> const &b) {
        return b.volume() / b.numElements();
      }
      static double adj(BoxModelIO<Nd> const &b) { return 1 / b.volume(); }
    };

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::CArray, Nd>
        : _normalization<typename ModelIO<Nd>::CArrayRef, Nd> {};

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::ArrayRef, Nd> {
      static double fwd(BoxModelIO<Nd> const &b) { return 1 / b.volume(); }
      static double adj(BoxModelIO<Nd> const &b) {
        return b.volume() / b.numElements();
      }
    };

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::Array, Nd>
        : _normalization<typename ModelIO<Nd>::ArrayRef, Nd> {};

    template <typename T, size_t Nd>
    using normalization = _normalization<
        typename std::remove_const<
            typename std::remove_reference<T>::type>::type,
        Nd>;

    template <size_t Nd, typename Super = ModelIO<Nd>>
    class ModelOutputBase : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;
      double scaler;
      bool alreadyTransformed;

      template <typename T>
      using is_not_a_const =
          typename std::enable_if<!std::is_const<T>::value, void>::type;

      template <typename T>
      using is_a_const =
          typename std::enable_if<!std::is_const<T>::value, void>::type;

    public:
      ModelOutputBase() : super_t(), alreadyTransformed(false) {}

      template <typename T, typename = is_not_a_const<T>>
      ModelOutputBase(Mgr_p mgr_, BoxModel const &box_, T &t, double scaler_)
          : super_t(mgr_, box_, t), scaler(scaler_), alreadyTransformed(false) {
      }

      template <typename T, typename = is_not_a_const<T>>
      ModelOutputBase(
          Mgr_p mgr_, BoxModel const &box_, T &t, Holder original_,
          double scaler_)
          : super_t(mgr_, box_, t, original_), scaler(scaler_),
            alreadyTransformed(false) {}

      ~ModelOutputBase();

      void setRequestedIO(PreferredIO opt);

      inline ArrayRef &getRealOutput() {
        if (this->active != PREFERRED_REAL) 
          error_helper<ErrorBadState>("Requesting (REAL) wrong output");
        try {
          return this->ioIsTransformed ? this->tmp_real->get_array()
                                       : *boost::get<ArrayRef *>(this->holder);
        } catch (boost::bad_get const &e) {
          error_helper<ErrorBadState>(
              "Bad access to output: " + std::string(e.what()));
        }
      }

      inline CArrayRef &getFourierOutput() {
        if (this->active != PREFERRED_FOURIER) 
          error_helper<ErrorBadState>("Requesting (FOURIER) wrong output");
        try {
          return this->ioIsTransformed ? this->tmp_fourier->get_array()
                                       : *boost::get<CArrayRef *>(this->holder);
        } catch (boost::bad_get const &e) {
          error_helper<ErrorBadState>(
              "Bad access to output: " + std::string(e.what()));
        }
      }

      void copyFrom(ModelOutputBase<Nd, Super> &other);

      void transformOutputRealToFourier();
      void transformOutputFourierToReal();

    protected:
      void triggerTransform();

      void transfer(ModelOutputBase &&other) {
        scaler = other.scaler;
        super_t::transfer(std::move(other));
      }
    };

    /**
     * @brief Class to handle output arrays from forward models.
     */
    template <size_t Nd, typename Super = ModelOutputBase<Nd>>
    class ModelOutput : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;

    public:
      /**
       * @brief Construct an empty output.
       *
       * The object is marked as uninitialized.
       */
      ModelOutput() : super_t() {}

      /**
       * @brief Construct an output
       *
       * @param Mgr_p FFT manager associated
       * @param BoxModelIO Object describing the physical size of the output.
       * @param T an array that must come from a boost::multi_array/boost::multi_array_ref
       */
      template <typename T>
      ModelOutput(Mgr_p mgr_, BoxModelIO const &box_, T &t)
          : super_t(mgr_, box_, t, normalization<T, Nd>::fwd(box_)) {}

      /**
       * @brief Construct an output
       *
       * @param Mgr_p FFT manager associated
       * @param BoxModelIO Object describing the physical size of the output.
       * @param T an array that must come from a boost::multi_array/boost::multi_array_ref
       * @param Holder a shared_ptr object that can be used to prevent the memory from being deallocated.
       */
      template <typename T>
      ModelOutput(Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original_)
          : super_t(mgr_, box_, t, original_, normalization<T, Nd>::fwd(box_)) {
      }

      /**
       * @brief Move constructor
       */
      ModelOutput(ModelOutput<Nd> &&other) {
        this->operator=(std::move(other));
      }

      /**
       * @brief Move assignment
       */
      ModelOutput &&operator=(ModelOutput &&other) {
        super_t::transfer(std::move(other));
        return std::move(*this);
      }

      /**
       * @brief Construct a model output with a memory backing that has the same property as the original
       *
       * The memory is allocated but *not* initialized.
       */
      ModelOutput<Nd> makeTempLike();

      ModelOutput<Nd> shallowClone();
    };

    template <size_t Nd, typename Super = ModelOutputBase<Nd>>
    class ModelOutputAdjoint : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;

    public:
      /**
       * @brief Construct an empty adjoint gradient output.
       *
       * The object is marked as uninitialized.
       */
      ModelOutputAdjoint() : super_t() {}

      /**
       * @brief Construct an adjoint gradient output
       *
       * @param Mgr_p FFT manager associated
       * @param BoxModelIO Object describing the physical size of the output.
       * @param T an array that must come from a boost::multi_array/boost::multi_array_ref
       */
      template <typename T>
      ModelOutputAdjoint(Mgr_p mgr_, BoxModelIO const &box_, T &t)
          : super_t(mgr_, box_, t, normalization<T, Nd>::adj(box_)) {}

      /**
       * @brief Construct an adjoint gradient output
       *
       * @param Mgr_p FFT manager associated
       * @param BoxModelIO Object describing the physical size of the output.
       * @param T an array that must come from a boost::multi_array/boost::multi_array_ref
       * @param Holder a shared_ptr object that can be used to prevent the memory from being deallocated.
       */
      template <typename T>
      ModelOutputAdjoint(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original_)
          : super_t(mgr_, box_, t, original_, normalization<T, Nd>::adj(box_)) {
      }

      ModelOutputAdjoint(ModelOutputAdjoint &&other) {
        this->operator=(std::move(other));
      }

      ModelOutputAdjoint &&operator=(ModelOutputAdjoint &&other) {
        super_t::transfer(std::move(other));
        return std::move(*this);
      }

      /**
       * @brief Construct a model output with a memory backing that has the same property as the original
       *
       * The memory is allocated but *not* initialized.
       */
      ModelOutputAdjoint<Nd> makeTempLike();

      ModelOutputAdjoint<Nd> shallowClone();
    };
  } // namespace detail_output
} // namespace LibLSS

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
