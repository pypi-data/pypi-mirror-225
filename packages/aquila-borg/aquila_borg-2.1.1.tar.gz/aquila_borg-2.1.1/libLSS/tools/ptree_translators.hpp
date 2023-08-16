/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/ptree_translators.hpp
    Copyright (C) 2016-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PTREE_TRANSLATORS_HPP
#define __LIBLSS_PTREE_TRANSLATORS_HPP

#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/string_tools.hpp"

namespace LibLSS {

  namespace PTreeTools {

    // Custom translator for bool (only supports std::string)
    struct BoolTranslator {
      typedef std::string internal_type;
      typedef bool external_type;

      // Converts a string to bool
      boost::optional<external_type> get_value(const internal_type &str) {
        Console::instance().print<LOG_VERBOSE>("Translating " + str);

        if (!str.empty()) {
          using boost::algorithm::iequals;

          if (iequals(str, "true") || iequals(str, "yes") || str == "1")
            return boost::optional<external_type>(true);
          else if (iequals(str, "false") || iequals(str, "no") || str == "0")
            return boost::optional<external_type>(false);
          else {
            Console::instance().print<LOG_ERROR>(
                "Error while translating to boolean.");
            throw ErrorBadCast(
                "String '" + str + "' cannot be cast to boolean");
          }
        } else {
          Console::instance().print<LOG_VERBOSE>("  =+= String empty");
          return boost::optional<external_type>(boost::none);
        }
      }

      // Converts a bool to string
      boost::optional<internal_type> put_value(const external_type &b) {
        return boost::optional<internal_type>(b ? "true" : "false");
      }
    };
  } // namespace PTreeTools
} // namespace LibLSS

/*  Specialize translator_between so that it uses our custom translator for
    bool value types. Specialization must be in boost::property_tree
    namespace. */
namespace boost {
  namespace property_tree {

    template <typename Ch, typename Traits, typename Alloc>
    struct translator_between<std::basic_string<Ch, Traits, Alloc>, bool> {
      typedef LibLSS::PTreeTools::BoolTranslator type;
    };

  } // namespace property_tree

} // namespace boost

namespace LibLSS { namespace PTreeTools {

  template <typename T>
  using RangeType = std::tuple<T, T>;

  template <typename T>
  struct RangeConverter {
    typedef std::string internal_type;
    typedef RangeType<T> external_type;

    boost::optional<external_type> get_value(const internal_type &str) {
      auto &cons = Console::instance();

      cons.print<LOG_VERBOSE>("Translating range string " + str);

      if (!str.empty()) {
        auto strRange = tokenize(str,"-");
        if (strRange.size() != 2) {
          cons.print<LOG_ERROR>("Invalid range");
          return boost::optional<external_type>(boost::none);
        }
        auto translate =
            boost::property_tree::translator_between<std::string, T>::type();
        auto minRange = translate.get_value(strRange[0]);
        auto maxRange = translate.get_value(strRange[1]);
        return boost::optional<external_type>(RangeType<T>(minRange, maxRange));
      } else {
        cons.print<LOG_VERBOSE>("Empty string...");
        return boost::optional<external_type>(boost::none);
      }
    }
  };
} } // namespace LibLSS::PTreeTools

/*  Specialize translator_between so that it uses our custom translator for
    bool value types. Specialization must be in boost::property_tree
    namespace. */
namespace boost {
  namespace property_tree {

    template <typename T, typename Ch, typename Traits, typename Alloc>
    struct translator_between<
        std::basic_string<Ch, Traits, Alloc>,
        LibLSS::PTreeTools::RangeType<T>> {
      typedef LibLSS::PTreeTools::RangeConverter<T> type;
    };

  } // namespace property_tree

} // namespace boost

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2016-2018
