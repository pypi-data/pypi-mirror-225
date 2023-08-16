/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_overload.cpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE overload
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>
#include <boost/variant.hpp>
#include "libLSS/tools/overload.hpp"

using namespace LibLSS;

BOOST_AUTO_TEST_CASE(basic) {
  boost::variant<int> a(2);
  {
    int value = boost::apply_visitor([](int b) { return b; }, a);

    BOOST_CHECK_EQUAL(value, 2);
  }

  {
    int value = boost::apply_visitor(overload([](int b) { return b; }), a);
    BOOST_CHECK_EQUAL(value, 2);
  }
}

BOOST_AUTO_TEST_CASE(multiple) {
  boost::variant<int, std::string> a(2);
  {
    int value = boost::apply_visitor(
        overload([](int b) { return b; }, [](std::string s) { return -1; }), a);

    BOOST_CHECK_EQUAL(value, 2);
  }
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
