/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/variant.hpp>
#include <memory>
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/tools/overload.hpp"

using namespace LibLSS;

using boost::multi_array_types::index_range;

template <size_t Nd, typename Super>
void LibLSS::ModelInputBase<Nd, Super>::setRequestedIO(PreferredIO opt) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  this->active = opt;
  if (opt == this->current)
    return;
  switch (opt) {
  case PREFERRED_FOURIER:
    transformInputRealToFourier();
    break;
  case PREFERRED_REAL:
    transformInputFourierToReal();
    break;
  default:
    Console::instance().c_assert(false, "Invalid IO");
    break;
  }
  this->ioIsTransformed = true;
}

template <size_t Nd, typename Super>
void ModelInputBase<Nd, Super>::needDestroyInput() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  typedef typename ModelIO<Nd>::HolderType HolderType;

  this->holder = boost::apply_visitor(
      overload(
          [&ctx](auto *v) {
            ctx.print("Pass through");
            return HolderType(v);
          },
          [&](CArrayRef const *v) {
            ctx.print("Protect complex");
            auto p = this->mgr->allocate_ptr_complex_array();
            fwrap(*p) = fwrap(*v);
            auto h = HolderType(&p->get_array());
            this->hold_original = std::move(p);
            return h;
          },
          [&](ArrayRef const *v) {
            ctx.print("Protect real");
            auto p = this->mgr->allocate_ptr_array();
            fwrap(*p) = fwrap(*v);
            auto h = HolderType(&p->get_array());
            this->hold_original = std::move(p);
            return h;
          }),
      this->holder);
}

template <size_t Nd, typename Super>
void ModelInputBase<Nd, Super>::transformInputRealToFourier() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  if (!this->tmp_fourier) {
    this->tmp_fourier = this->mgr->allocate_ptr_complex_array();
  }
  auto volatile_real = this->mgr->allocate_array();

  auto plan = this->mgr->create_r2c_plan(
      volatile_real.get_array().data(), this->tmp_fourier->get_array().data());

  needDestroyInput();
  try {
    this->mgr->execute_r2c(
        plan, boost::get<ArrayRef *>(this->holder)->data(),
        this->tmp_fourier->get_array().data());
  } catch (boost::bad_get const &e) {
    error_helper<ErrorBadState>(
        "Runtime error thrown: " + std::string(e.what()));
  }
  this->mgr->destroy_plan(plan);

  if (scaler != 1) {
    ctx.format(" -> Scaler %g", scaler);
    auto w_c = fwrap(this->tmp_fourier->get_array());
    w_c = w_c * scaler;
  }

  //this->hermitic_fixer(this->tmp_fourier->get_array());
}

template <size_t Nd, typename Super>
void ModelInputBase<Nd, Super>::transformInputFourierToReal() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  if (!this->tmp_real) {
    this->tmp_real = this->mgr->allocate_ptr_array();
  }
  auto volatile_fourier = this->mgr->allocate_complex_array();

  auto plan = this->mgr->create_c2r_plan(
      volatile_fourier.get_array().data(), this->tmp_real->get_array().data());

  needDestroyInput();
  try {
    this->mgr->execute_c2r(
        plan, boost::get<CArrayRef *>(this->holder)->data(),
        this->tmp_real->get_array().data());
  } catch (boost::bad_get const &e) {
    error_helper<ErrorBadState>(
        "Runtime error thrown: " + std::string(e.what()));
  }

  this->mgr->destroy_plan(plan);

  if (scaler != 1) {
    ctx.format(" -> Scaler %g", scaler);
    auto w_r = fwrap(this->tmp_real->get_array());
    w_r = w_r * scaler;
  }
}

template <size_t Nd, typename Super>
void ModelOutputBase<Nd, Super>::transformOutputFourierToReal() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  auto volatile_fourier = this->mgr->allocate_ptr_complex_array();

  try {
    auto &array = *boost::get<ArrayRef *>(this->holder);
    auto plan = this->mgr->create_c2r_plan(
        volatile_fourier->get_array().data(), array.data());

    this->mgr->execute_c2r(
        plan, this->tmp_fourier->get_array().data(), array.data());
    this->mgr->destroy_plan(plan);

    if (scaler != 1) {
      ctx.format(" -> Scaler %g", scaler);
      auto w_h = fwrap(array);
      w_h = w_h * scaler;
    }
  } catch (boost::bad_get const &e) {
    error_helper<ErrorBadState>(
        "Runtime error thrown: " + std::string(e.what()));
  }
}

template <size_t Nd, typename Super>
void ModelOutputBase<Nd, Super>::transformOutputRealToFourier() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  auto volatile_real = this->mgr->allocate_ptr_array();
  try {
    auto &c_array = *boost::get<CArrayRef *>(this->holder);
    auto plan = this->mgr->create_r2c_plan(
        volatile_real->get_array().data(), c_array.data());

    this->mgr->execute_r2c(
        plan, this->tmp_real->get_array().data(), c_array.data());

    this->mgr->destroy_plan(plan);

    if (scaler != 1) {
      ctx.format(" -> Scaler %g", scaler);
      auto w_ch = fwrap(c_array);
      w_ch = w_ch * scaler;
    }
  } catch (boost::bad_get const &e) {
    error_helper<ErrorBadState>(
        "Runtime error thrown: " + std::string(e.what()));
  }
}

template <size_t Nd, typename Super>
void ModelOutputBase<Nd, Super>::triggerTransform() {
  if (this->alreadyTransformed || this->uninitialized)
    return;
  if (this->ioIsTransformed) {
    switch (this->current) {
    case PREFERRED_FOURIER:
      transformOutputRealToFourier();
      break;
    case PREFERRED_REAL:
      transformOutputFourierToReal();
      break;
    default:
      Console::instance().c_assert(false, "Invalid IO");
      break;
    }
  }
  alreadyTransformed = true;
}

template <size_t Nd, typename Super>
ModelOutputBase<Nd, Super>::~ModelOutputBase() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  triggerTransform();
}

template <size_t Nd, typename Super>
void ModelOutputBase<Nd, Super>::setRequestedIO(PreferredIO opt) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  this->active = opt;
  if (opt == this->current)
    return;
  Console::instance().c_assert(
      !this->ioIsTransformed, "Transformation already requested.");
  switch (this->current) {
  case PREFERRED_FOURIER:
    // then opt is REAL
    ctx.print("Want real ");
    this->tmp_real = this->mgr->allocate_ptr_array();
    break;
  case PREFERRED_REAL:
    ctx.print("Want fourier");
    this->tmp_fourier = this->mgr->allocate_ptr_complex_array();
    break;
  default:
    Console::instance().c_assert(false, "Invalid IO");
    break;
  }
  this->ioIsTransformed = true;
}

template <size_t Nd, typename Super>
void ModelOutputBase<Nd, Super>::copyFrom(ModelOutputBase<Nd, Super> &other) {
  Console::instance().c_assert(
      !this->uninitialized, "Model must be initialized");
  //other.triggerTransform();
  Console::instance().c_assert(
      this->active == other.active,
      "this->active and other.active are different");
  switch (other.active) {
  case PREFERRED_FOURIER:
    fwrap(this->getFourierOutput()) = other.getFourierOutput();
    break;
  case PREFERRED_REAL:
    fwrap(this->getRealOutput()) = other.getRealOutput();
    break;
  default:
    Console::instance().c_assert(false, "Invalid IO");
    break;
  }
}

template <size_t Nd, typename Super>
ModelInput<Nd> ModelInput<Nd, Super>::shallowClone() {
  return boost::apply_visitor(
      [this](auto const *v) {
        return ModelInput<Nd>(
            this->mgr, this->box, *v, this->hold_original, true, this->scaler);
      },
      this->holder);
}

template <size_t Nd, typename Super>
ModelInputAdjoint<Nd> ModelInputAdjoint<Nd, Super>::shallowClone() {
  return boost::apply_visitor(
      [this](auto const *v) {
        return ModelInputAdjoint<Nd>(
            this->mgr, this->box, *v, this->hold_original, true, this->scaler);
      },
      this->holder);
}

template <size_t Nd, typename Super>
ModelOutput<Nd> ModelOutput<Nd, Super>::shallowClone() {
  return boost::apply_visitor(
      overload(
          [this](auto const *v) {
            error_helper<ErrorBadState>("Output cannot be const");
            return ModelOutput<Nd>();
          },
          [this](auto *v) {
            return ModelOutput<Nd>(
                this->mgr, this->box, *v, this->hold_original);
          }),
      this->holder);
}

template <size_t Nd, typename Super>
ModelOutputAdjoint<Nd> ModelOutputAdjoint<Nd, Super>::shallowClone() {
  return boost::apply_visitor(
      overload(
          [this](auto const *v) {
            error_helper<ErrorBadState>("Output cannot be const");
            return ModelOutputAdjoint<Nd>();
          },
          [this](auto *v) {
            return ModelOutputAdjoint<Nd>(
                this->mgr, this->box, *v, this->hold_original);
          }),
      this->holder);
}

template <size_t Nd, typename Super>
ModelOutput<Nd> ModelOutput<Nd, Super>::makeTempLike() {
  return boost::apply_visitor(
      overload(
          [this](CArrayRef const *v) {
            auto tmp_p = this->mgr->allocate_ptr_complex_array();
            auto &tmp = tmp_p->get_array();
            return ModelOutput<Nd>(this->mgr, this->box, tmp, std::move(tmp_p));
          },
          [this](ArrayRef const *v) {
            auto tmp_p = this->mgr->allocate_ptr_array();
            auto &tmp = tmp_p->get_array();
            return ModelOutput<Nd>(this->mgr, this->box, tmp, std::move(tmp_p));
          }),
      this->holder);
}

template <size_t Nd, typename Super>
ModelOutputAdjoint<Nd> ModelOutputAdjoint<Nd, Super>::makeTempLike() {
  return boost::apply_visitor(
      overload(
          [this](CArrayRef const *v) {
            auto tmp_p = this->mgr->allocate_ptr_complex_array();
            auto &tmp = tmp_p->get_array();
            return ModelOutputAdjoint<Nd>(
                this->mgr, this->box, tmp, std::move(tmp_p));
          },
          [this](ArrayRef const *v) {
            auto tmp_p = this->mgr->allocate_ptr_array();
            auto &tmp = tmp_p->get_array();
            return ModelOutputAdjoint<Nd>(
                this->mgr, this->box, tmp, std::move(tmp_p));
          }),
      this->holder);
}

#define FORCE_IO_SET(q)                                                        \
  template class LibLSS::detail_input::ModelInputBase<q>;                      \
  template class LibLSS::detail_output::ModelOutputBase<q>;                    \
  template class LibLSS::detail_input::ModelInput<q>;                          \
  template class LibLSS::detail_input::ModelInputAdjoint<q>;                   \
  template class LibLSS::detail_output::ModelOutput<q>;                        \
  template class LibLSS::detail_output::ModelOutputAdjoint<q>;

// 2d does not work yet because of FFTW_Manager
//FORCE_IO_SET(2);
FORCE_IO_SET(3);

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
