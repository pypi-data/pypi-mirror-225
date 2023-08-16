/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/biases.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/bias/noop.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"
#include "libLSS/physics/bias/eft_bias_marg.hpp"

constexpr const int LibLSS::bias::detail_noop::Noop::numParams;
constexpr const bool LibLSS::bias::detail_noop::Noop::NmeanIsBias;

constexpr int LibLSS::bias::detail_linear_bias::LinearBias::numParams;
constexpr const bool LibLSS::bias::detail_linear_bias::LinearBias::NmeanIsBias;

constexpr int LibLSS::bias::detail::PowerLaw::numParams;
constexpr double LibLSS::bias::detail::PowerLaw::EPSILON_VOIDS;
constexpr const bool LibLSS::bias::detail::PowerLaw::NmeanIsBias;

constexpr int LibLSS::bias::detail::DoubleBrokenPowerLaw::numParams;
constexpr const bool LibLSS::bias::detail::DoubleBrokenPowerLaw::NmeanIsBias;

constexpr int LibLSS::bias::detail::BrokenPowerLaw::numParams;
constexpr const bool LibLSS::bias::detail::BrokenPowerLaw::NmeanIsBias;

template<typename Levels> const int LibLSS::bias::ManyPower<Levels>::numParams;
template<typename Levels> const bool LibLSS::bias::ManyPower<Levels>::NmeanIsBias;

template struct LibLSS::bias::ManyPower<LibLSS::bias::ManyPowerLevels<double, 1>>;
template struct LibLSS::bias::ManyPower<LibLSS::bias::ManyPowerLevels<double, 1, 1>>;
template struct LibLSS::bias::ManyPower<LibLSS::bias::ManyPowerLevels<double, 1, 1, 1, 1>>;
template struct LibLSS::bias::ManyPower<LibLSS::bias::ManyPowerLevels<double, 2>>;
template struct LibLSS::bias::ManyPower<LibLSS::bias::ManyPowerLevels<double, 2, 2>>;

template<bool b> const int LibLSS::bias::detail_EFTBias::EFTBias<b>::numParams;
template<bool b> const bool LibLSS::bias::detail_EFTBias::EFTBias<b>::NmeanIsBias;

template struct LibLSS::bias::detail_EFTBias::EFTBias<false>;
template struct LibLSS::bias::detail_EFTBias::EFTBias<true>;


// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
