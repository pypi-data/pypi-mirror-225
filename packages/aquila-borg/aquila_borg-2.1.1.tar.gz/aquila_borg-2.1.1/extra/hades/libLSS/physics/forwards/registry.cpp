#include "libLSS/tools/console.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/static_init.hpp"

using namespace LibLSS;

namespace {
  RegisterStaticInit init_registry([]() {
    auto &cons = Console::instance();

    cons.print<LOG_INFO_SINGLE>("Registered forward models:");
    for (auto k : ForwardRegistry::instance().list()) {
      cons.print<LOG_INFO_SINGLE>("  - " + k.first);
    }
  });
}

ForwardRegistry::ForwardRegistry() {}

ForwardRegistry &ForwardRegistry::instance() {
  static ForwardRegistry this_instance;

  return this_instance;
}

ForwardModelFactory ForwardRegistry::get(std::string const &n) {
  auto iter = forwardRegistry.find(n);
  if (iter == forwardRegistry.end())
    error_helper<ErrorParams>("Invalid model name");
  return iter->second;
}

ForwardModelFactory LibLSS::setup_forward_model(std::string const &n) {
  return ForwardRegistry::instance().get(n);
}
