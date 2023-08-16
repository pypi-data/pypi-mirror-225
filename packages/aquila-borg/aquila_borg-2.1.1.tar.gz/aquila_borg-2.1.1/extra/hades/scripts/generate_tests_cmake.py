# +
#   ARES/HADES/BORG Package -- -- ./scripts/generate_tests_cmake.py
#   Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2019)
#
#   This program is free software; you can redistribute it and/or modify it
#   under the terms of either the CeCILL license or the GNU General Public
#   license, as included with the software package.
#
#   The text of the license is located in Licence_CeCILL_V2.1-en.txt
#   and GPL.txt in the root directory of the source package.
# +

import os
import sys
import filecmp

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
        base_code = test.get("base_code", "generic_gradient_test.cpp")
        includes = test['includes']
        likelihood = test['likelihood']
        info_code = test.get('info_code', '')
        model_code = ""

        f.write("""
add_executable(test_gradient_%(test_name)s %(base_dir)s/%(test_source)s)
target_link_libraries(test_gradient_%(test_name)s test_library_LSS LSS ${LIBS})
ares_add_test_targets(test_gradient_%(test_name)s)
target_include_directories(test_gradient_%(test_name)s PRIVATE %(input_config_path)s)
""" % dict(test_name=test_name,
           base_dir=base_dir,
           input_config_path=input_config_path,
           test_source="test_%s_gradient.cpp" % (test_name, )))

        includes_str = \
            "\n".join(
                map(lambda x: "#include \"%s\"" % (x,), includes)
            )

        downgrade = test.get('downgrade', 1)

        if 'model' in test:
            if isinstance(test['model'], list):
                model_string = ""
                args = test.get('model_args', ['comm, box,box, 0.001'] +
                                ['comm, box, box, 1'] *
                                (len(test['model']) - 1))
                extra_code = test.get('model_extra', [""] * len(test['model']))
                extra_code_prev = test.get('model_extra_prev', [""] * len(test['model']))
                for m, a, e, eprev in zip(test['model'], args, extra_code, extra_code_prev):
                    model_string += f"""
            {{
              {eprev}
              auto m = std::make_shared<{m}>({a});
              {e}
              chain->addModel(m);
            }}"""

                model_code = f"""
          auto makeModel(LibLSS::MPI_Communication * comm, LibLSS::MarkovState& state, LibLSS::BoxModel box, LibLSS::BoxModel box2) {{
            using namespace LibLSS;
            auto chain = std::make_shared<ChainForwardModel>(comm, box);
            {model_string}
            return chain;
          }}
          """
            else:
                args = test.get('model_args', 'comm, box, box, 0.001')
                extra_prev = test.get('model_extra_prev', "")
                extra = test.get('model_extra', "")
                model_code = f"""
                auto makeModel(LibLSS::MPI_Communication * comm, LibLSS::MarkovState& state, LibLSS::BoxModel box, LibLSS::BoxModel box2) {{
                  using namespace LibLSS;
                  {extra_prev}
                  auto m = std::make_shared<{test['model']}>({args});
                  {extra}
                  return m;
                }}
                """
        else:
            assert 'model_code' in test
            model_code = test['model_code']

        if 'data_setup' in test:
            data_setup = '#include "%s"\n#define DATA_SETUP %s\n' % (
                test['data_setup'])
        else:
            data_setup = ''

        newfile = os.path.join(base_dir,
                               "test_%s_gradient.cpp_tmp" % (test_name, ))
        finalfile = os.path.join(base_dir,
                                 "test_%s_gradient.cpp" % (test_name, ))

        with open(newfile, mode="wt") as f2:
            f2.write("""%(includes)s
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
%(data_setup_header)s

namespace L = LibLSS::Likelihood;
using LibLSS::LikelihoodInfo;
using LibLSS::HMCDensitySampler;

static const int DOWNGRADE_DATA = %(downgrade)d;

HMCDensitySampler::Likelihood_t makeLikelihood(LikelihoodInfo& info) {
  %(additional_info_code)s
  return std::make_shared<%(likelihood)s>(info);
}

%(model_code)s

#include "%(base_code)s"
""" % dict(includes=includes_str,
            data_setup_header=data_setup,
            additional_info_code=info_code,
            likelihood=likelihood,
            model_code=model_code,
            downgrade=downgrade,
            base_code=base_code))

        try:
            os.stat(finalfile)
            if not filecmp.cmp(finalfile, newfile):
                os.rename(newfile, finalfile)
            else:
                os.unlink(newfile)
        except FileNotFoundError:
            os.rename(newfile, finalfile)

# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2019
