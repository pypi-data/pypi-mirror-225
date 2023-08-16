#+
#   ARES/HADES/BORG Package -- ./extra/hades/scripts/generate_benchmark_tests.py
#   Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+

import os
import sys

output_cmake_file = sys.argv[1]
input_config = sys.argv[2]
base_dir = sys.argv[3]
input_config_path = os.path.dirname(os.path.abspath(input_config))

with open(input_config, mode="r") as f:
  config = {}
  exec(f.read(), {}, config)
  config = config['tests']

tests = config['tests']

with open(output_cmake_file, "wt") as f:

    for test_name in tests:
      test = tests[test_name]
      includes = test['includes']
      likelihood = test['likelihood']
      info_code = test.get('info_code', '')
      downgrade = test.get('downgrade', 1)

      model_code=""

      f.write("""
add_executable(benchmark_gradient_%(test_name)s %(base_dir)s/%(test_source)s)
target_link_libraries(benchmark_gradient_%(test_name)s test_library_LSS LSS ${LIBS})
ares_add_test_targets(benchmark_gradient_%(test_name)s)
target_include_directories(benchmark_gradient_%(test_name)s PRIVATE %(input_config_path)s)
"""
         % dict(test_name=test_name, base_dir=base_dir, input_config_path=input_config_path, test_source="benchmark_%s.cpp" % (test_name,)
      ))

      includes_str = \
        "\n".join(
            map(lambda x: "#include \"%s\"" % (x,), includes)
        )

      if 'model' in test:
        if type(test['model']) is list:
             model_string = ""
             args = test.get(
                 'model_args', ['comm, box,box, 0.001'] + ['comm, box, box, 1']*(len(test['model'])-1))
             extra_code = test.get(
                 'model_extra', [""]*len(test['model'])
             )
             extra_code_prev = test.get(
                 'model_extra_prev', [""]*len(test['model'])
             )
             for m, a, e, eprev in zip(test['model'], args, extra_code, extra_code_prev):
                 model_string += f"""
                                  {{
                                    {eprev}
                                    auto m = std::make_shared<{m}>({a}); 
                                    {e}
                                    chain->addModel(m);
                                  }}"""
                 model_code = f"""
                                auto buildModel(LibLSS::MPI_Communication * comm, LibLSS::MarkovState& state, LibLSS::BoxModel box, LibLSS::BoxModel box2) {{
                                  using namespace LibLSS;
                                  auto chain = std::make_shared<ChainForwardModel>(comm, box);
                                  {model_string}
                                  return chain;
                                }}
                 """
        else:
          args = test.get('model_args', 'comm, box, box, 0.001')
          model_code="auto buildModel(LibLSS::MPI_Communication *comm, LibLSS::MarkovState& state, LibLSS::BoxModel const& box, LibLSS::BoxModel box2) { return std::make_shared<%(model)s>(%(model_args)s); }" % dict(model=test['model'],model_args=args )


      if 'data_setup' in test:
          data_setup='#include "%s"\n#define DATA_SETUP %s\n'%(test['data_setup'])
      else:
          data_setup=''

      with open(os.path.join(base_dir,"benchmark_%s.cpp" % (test_name,)), mode="wt") as f2:
        f2.write("""%(includes)s
#include "libLSS/physics/likelihoods/base.hpp"
%(data_setup_header)s

static const int DOWNGRADE_DATA = %(downgrade)d;

namespace L = LibLSS::Likelihood;
using LibLSS::LikelihoodInfo;

auto makeLikelihood(LikelihoodInfo& info) {
  %(additional_info_code)s
  return std::make_shared<%(likelihood)s>(info);
}

%(model_code)s

static constexpr bool RUN_RSD_TEST = false;
static std::string testName = "%(test_name)s";

#include "generic_gradient_benchmark.cpp"
""" % dict(includes=includes_str,data_setup_header=data_setup, additional_info_code=info_code,likelihood=likelihood,model_code=model_code,test_name=test_name,downgrade=downgrade))

# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2019
