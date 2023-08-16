#include <iostream>
#include "special_math.hpp"

int main()
{

    std::cout << CosmoTool::log1p_exp(2.0) << std::endl;

    std::cout << CosmoTool::log_modified_bessel_first_kind(100.0, 0.1) << std::endl;
    return 0;
}
    
