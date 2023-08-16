/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/mcmcfile_parsing.hpp
    Copyright (C) 2017-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __BORG_FORWARD_MCMCFILE_PARSING_HPP
#define __BORG_FORWARD_MCMCFILE_PARSING_HPP

#include <string>
#include <boost/regex.hpp>
#include <boost/lexical_cast.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/console.hpp"

struct FailedDetection : virtual LibLSS::ErrorBase {
  FailedDetection() : ErrorBase("Failed detection") {}
};

int find_iteration(const std::string &fname, bool randswitch) {
  using boost::format;
  using LibLSS::Console;
  using LibLSS::LOG_ERROR;
  Console &cons = Console::instance();

  if (randswitch) {
    // In case of randomness, just convert fname to int
    try {
      return boost::lexical_cast<int>(fname);
    } catch (boost::bad_lexical_cast const &exc) {
      cons.print<LOG_ERROR>(
          format("Failed to convert '%s' to integer. Be aware that when "
                 "generating random realizations we expect just an integer and "
                 "not the mcmc-file.") %
          fname);
      throw FailedDetection();
    }
  }

  boost::regex e("^[\\.\\/a-zA-Z0-9_\\-]+_([0-9]+)\\.h5$");
  boost::smatch what;
  std::string f2 = fname;

  if (boost::regex_match(f2, what, e, boost::match_extra)) {

    if (what.size() != 2) {
      cons.print<LOG_ERROR>("Failed to understand pattern in the input file");
      cons.print<LOG_ERROR>(format("What.size = %d") % what.size());
      for (int i = 0; i < what.size(); i++) {
	    cons.print<LOG_ERROR>(format("Capture(%d) = %s") % i % what[i].str());
      }
      throw FailedDetection();
    }

    return boost::lexical_cast<int>(what[1].str());
  }

  cons.print<LOG_ERROR>("No match to input filename pattern");
  throw FailedDetection();
}

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2017-2019
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
