/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_has_member.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <typeinfo>
#include <boost/utility/enable_if.hpp>
#include <iostream>
#include "libLSS/tools/checkmem.hpp"

using namespace std;

HAS_MEM_FUNC(checkMember, has_check_member);

struct NoStruct
{

   int a;
};

struct YesStruct
{

   double c;
   
   void checkMember() { cout << "Cool" << endl; }
};

template<typename T>
typename boost::enable_if<has_check_member<T, void (T::*)()> >::type
exec_fun() {

    cout << typeid(T).name() << " has the member" << endl;
    
    T a;
    a.checkMember();
}

template<typename T>
typename boost::disable_if<has_check_member<T, void (T::*)()> >::type
exec_fun() {
    cout << typeid(T).name() << " does not have the member" << endl;
}

int main()
{
    cout << "has_check_member<NoStruct>::value = " << has_check_member<NoStruct, void (NoStruct::*)()>::value << endl;
    
    cout << "has_check_member<YesStruct>::value = " << has_check_member<YesStruct, void (YesStruct::*)()>::value << endl;

    exec_fun<NoStruct>();
    exec_fun<YesStruct>();

    return 0;
}
