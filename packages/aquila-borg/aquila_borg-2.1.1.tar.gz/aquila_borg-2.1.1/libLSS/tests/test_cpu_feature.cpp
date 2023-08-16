#include <string>
#include <iostream>
#include "libLSS/tools/cpu/feature_check.hpp"

int main()
{
	std::string s;
	LibLSS::check_compatibility(s);
	std::cout << s << std::endl;
	return 0;
}
