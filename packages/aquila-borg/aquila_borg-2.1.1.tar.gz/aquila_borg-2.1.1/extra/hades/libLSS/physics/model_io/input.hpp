/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io/input.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
namespace LibLSS {

  namespace detail_input {
    template <typename Ref>
    struct ref_retriever {

      template <typename U>
      using detect = typename std::enable_if<
          std::is_same<U *, Ref *>::value ||
              std::is_same<U *, Ref const *>::value,
          Ref const *>::type;
      template <typename U>
      using not_detect = typename std::enable_if<
          !(std::is_same<U *, Ref *>::value ||
            std::is_same<U *, Ref const *>::value),
          Ref const *>::type;

      template <typename U>
      detect<U> operator()(U *u) {
        return u;
      }
      template <typename U>
      not_detect<U> operator()(U *u) {
        throw boost::bad_get();
      }
    };

    template <size_t Nd>
    using BoxModelIO = NBoxModel<Nd>;

    template <typename T, size_t Nd>
    struct _normalization {};

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::CArrayRef, Nd> {
      static double fwd(BoxModelIO<Nd> const &b) { return 1.0 / b.volume(); }
      static double adj(BoxModelIO<Nd> const &b) {
        return b.volume() / b.numElements();
      }
    };

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::CArray, Nd>
        : _normalization<typename ModelIO<Nd>::CArrayRef, Nd> {};

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::ArrayRef, Nd> {
      static double fwd(BoxModelIO<Nd> const &b) {
        return b.volume() / b.numElements();
      }
      static double adj(BoxModelIO<Nd> const &b) { return 1.0 / b.volume(); }
    };

    template <size_t Nd>
    struct _normalization<typename ModelIO<Nd>::Array, Nd>
        : _normalization<typename ModelIO<Nd>::ArrayRef, Nd> {};

    template <typename T, size_t Nd>
    using normalization = _normalization<std::remove_cv_t<T>, Nd>;

    template <size_t Nd, typename Super = ModelIO<Nd>>
    class ModelInputBase : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;
      double scaler;
      bool protect;

    public:
      template <typename T>
      static inline typename std::add_const<T>::type &rdonly(T &t) {
        return t;
      }

      ModelInputBase() : super_t() {}

      template <typename T>
      ModelInputBase(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original_,
          double scaler_)
          : super_t(mgr_, box_, t, original_), scaler(scaler_) {}

      template <typename T>
      ModelInputBase(Mgr_p mgr_, BoxModelIO const &box_, T &t, double scaler_)
          : super_t(mgr_, box_, t), scaler(scaler_) {}

      void needDestroyInput();
      void setRequestedIO(PreferredIO opt);

      ArrayRef const &getRealConst() const {
        if (this->ioIsTransformed)
          return this->tmp_real->get_array();
        return *boost::apply_visitor(ref_retriever<ArrayRef>(), this->holder);
      }

      CArrayRef const &getFourierConst() const {
        if (this->ioIsTransformed)
          return this->tmp_fourier->get_array();
        return *boost::apply_visitor(ref_retriever<CArrayRef>(), this->holder);
      }

      ArrayRef &getReal() {
        if (this->ioIsTransformed)
          return this->tmp_real->get_array();
        try {
          return *boost::get<ArrayRef *>(this->holder);
        } catch (boost::bad_get const &e) {
          error_helper<ErrorBadState>(
              "Invalid RW access to input: " + std::string(e.what()));
        }
      }

      CArrayRef &getFourier() {
        if (this->ioIsTransformed)
          return this->tmp_fourier->get_array();
        try {
          return *boost::get<CArrayRef *>(this->holder);
        } catch (boost::bad_get const &e) {
          error_helper<ErrorBadState>(
              "Invalid RW access to input: " + std::string(e.what()));
        }
      }

      void transformInputRealToFourier();
      void transformInputFourierToReal();

      double scaleFactor() const { return scaler; }

      super_t &operator=(super_t const &) = delete;

    protected:
      void transfer(ModelInputBase<Nd> &&other) {
        super_t::transfer(std::move(other));
        scaler = other.scaler;
      }
    };

    template <size_t Nd, typename Super = ModelInputBase<Nd>>
    class ModelInput : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;

    public:
      ModelInput() : super_t() {}
      ModelInput(ModelInput<Nd> &&other) { this->operator=(std::move(other)); }

      template <typename T>
      ModelInput(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original_,
          bool prenormed = false, double scale = 1.0)
          : super_t(
                mgr_, box_, t, original_,
                scale * (prenormed ? 1 : normalization<T, Nd>::fwd(box_))) {}

      template <typename T>
      ModelInput(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, bool prenormed = false,
          double scale = 1.0)
          : super_t(
                mgr_, box_, t,
                scale * (prenormed ? 1 : normalization<T, Nd>::fwd(box_))) {}

      ModelInput &&operator=(ModelInput &&other) {
        super_t::transfer(std::move(other));
        return std::move(*this);
      }

      ModelInput<Nd> shallowClone();
    };

    template <size_t Nd, typename Super = ModelInputBase<Nd>>
    class ModelInputAdjoint : public Super {
    protected:
      typedef Super super_t;
      typedef typename super_t::Mgr_p Mgr_p;
      typedef typename super_t::CArrayRef CArrayRef;
      typedef typename super_t::ArrayRef ArrayRef;
      typedef typename super_t::BoxModelIO BoxModelIO;
      typedef typename super_t::Holder Holder;

    public:
      ModelInputAdjoint() : super_t() {}
      ModelInputAdjoint(ModelInputAdjoint<Nd> &&other) {
        this->operator=(std::move(other));
      }

      template <typename T>
      ModelInputAdjoint(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, bool prenormed = false,
          double scale = 1.0)
          : super_t(
                mgr_, box_, t,
                scale * (prenormed ? 1 : normalization<T, Nd>::adj(box_))) {}

      template <typename T>
      ModelInputAdjoint(
          Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original_,
          bool prenormed = false, double scale = 1.0)
          : super_t(
                mgr_, box_, t, original_,
                scale * (prenormed ? 1 : normalization<T, Nd>::adj(box_))) {}

      ModelInputAdjoint<Nd> &&operator=(ModelInputAdjoint<Nd> &&other) {
        super_t::transfer(std::move(other));
        return std::move(*this);
      }

      ModelInputAdjoint<Nd> shallowClone();
    };
  } // namespace detail_input
} // namespace LibLSS

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
