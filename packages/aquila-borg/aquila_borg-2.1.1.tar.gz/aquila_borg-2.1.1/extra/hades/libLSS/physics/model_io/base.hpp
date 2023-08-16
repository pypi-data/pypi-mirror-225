/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io/base.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PHYSICS_MODELIO_BASE_HPP
#  define __LIBLSS_PHYSICS_MODELIO_BASE_HPP
#  include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  enum PreferredIO { PREFERRED_NONE, PREFERRED_FOURIER, PREFERRED_REAL };

  namespace detail_model {

    template <typename T>
    struct _getPreferredType {};

    template <>
    struct _getPreferredType<CArrayType::RefArrayType> {
      constexpr static const auto value = PREFERRED_FOURIER;
    };

    template <>
    struct _getPreferredType<CArrayType::ArrayType> {
      constexpr static const auto value = PREFERRED_FOURIER;
    };

    template <>
    struct _getPreferredType<ArrayType::RefArrayType> {
      constexpr static const auto value = PREFERRED_REAL;
    };

    template <>
    struct _getPreferredType<ArrayType::ArrayType> {
      constexpr static const auto value = PREFERRED_REAL;
    };

    template <typename T>
    using getPreferredType = _getPreferredType<std::remove_cv_t<T>>;

    /**
     * @brief Holder to capture different basis of representation of BORG vectors
     */
    template <size_t Nd>
    struct ModelIO {
    protected:
    public:
      enum { Ndims = Nd };
      typedef ArrayType::ArrayType Array;
      typedef ArrayType::RefArrayType ArrayRef;
      typedef CArrayType::ArrayType CArray;
      typedef CArrayType::RefArrayType CArrayRef;
      typedef NBoxModel<Nd> BoxModelIO;
      typedef std::shared_ptr<void> Holder;

      typedef FFTW_Manager<double, Nd> Mgr;
      typedef std::shared_ptr<Mgr> Mgr_p;
      typedef boost::variant<
          CArrayRef *, CArrayRef const *, ArrayRef *, ArrayRef const *>
          HolderType;

      Mgr_p mgr;
      BoxModelIO box;
      PreferredIO current, active;
      HolderType holder;
      enum Direction { INPUT, OUTPUT };

      typedef typename Mgr::U_ArrayReal U_ArrayReal;
      typedef typename Mgr::U_ArrayFourier U_ArrayFourier;

      std::unique_ptr<U_ArrayReal> tmp_real;
      std::unique_ptr<U_ArrayFourier> tmp_fourier;

      Direction direction;
      bool ioIsTransformed;
      bool uninitialized;

      Holder hold_original;

      /**
       * @brief Construct a new uninitialized Model IO object
       * 
       */
      ModelIO() : uninitialized(true), current(PREFERRED_NONE), active(PREFERRED_NONE) {}

      /**
       * @brief Construct a new Model IO object, with Fourier default representation
       * 
       * @param t 
       */
      template <typename T>
      ModelIO(Mgr_p mgr_, BoxModelIO const &box_, T &t, Holder original)
          : mgr(mgr_), box(box_), holder(&t),
            current(getPreferredType<T>::value), ioIsTransformed(false),
            uninitialized(false), hold_original(original) {
        active = current;
      }

      /**
       * @brief Construct a new Model IO object, with Fourier default representation
       * 
       * @param t 
       */
      template <typename T>
      ModelIO(Mgr_p mgr_, BoxModelIO const &box_, T &t)
          : mgr(mgr_), box(box_), holder(&t),
            current(getPreferredType<T>::value), ioIsTransformed(false),
            uninitialized(false) {
        active = current;
      }

      /**
       * @brief Obtain the primary IO buffer from the callee.
       * It is a variant type.
       */
      HolderType getHolder() { return holder; }

      /**
       * @brief Clear the associated memory. 
       *
       * WARNING: use of the object beyond this point is not advised.
       */
      void clear() { hold_original.reset(); }

      /**
       * @brief bool operator to check whether the IO object is empty/uninitialized.
       *
       * @return bool true if initialized, false otherwise.
       */
      operator bool() const { return !uninitialized; }

    protected:
      /**
       * @brief Transfer ownership of the IO
       * 
       * @param other 
       * @return ModelIO&& Return *this
       */
      void transfer(ModelIO &&other) {
        LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
        mgr = std::move(other.mgr);
        box = other.box;
        current = other.current;
        holder = std::move(other.holder);
        tmp_real = std::move(other.tmp_real);
        tmp_fourier = std::move(other.tmp_fourier);
        direction = other.direction;
        ioIsTransformed = other.ioIsTransformed;
        uninitialized = other.uninitialized;
        other.uninitialized = true;
        hold_original = std::move(other.hold_original);
        active = other.active;
      }

      void hermitic_fixer(CArrayRef &data);
    };
  } // namespace detail_model

  using detail_model::ModelIO;

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: author(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
