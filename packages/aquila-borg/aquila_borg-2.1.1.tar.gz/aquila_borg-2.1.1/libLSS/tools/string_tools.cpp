#include <string>
#include <vector>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>
#include "libLSS/tools/string_tools.hpp"

std::vector<std::string>
LibLSS::tokenize(std::string const &in, std::string const &seps) {
  using namespace boost::algorithm;
  std::vector<std::string> result;

  split(result, in, is_any_of(seps), token_compress_on);
  return result;
}
