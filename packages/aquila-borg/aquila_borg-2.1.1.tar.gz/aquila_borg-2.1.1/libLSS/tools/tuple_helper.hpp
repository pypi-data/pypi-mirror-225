/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/tuple_helper.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TUPLE_HELPER_HPP
#define __LIBLSS_TUPLE_HELPER_HPP

#include <tuple>
#include <utility> 

namespace LibLSS {

    template<size_t start, size_t N, typename Tuple>
    struct _tuple_last_helper
    {
        template<typename... Args>
        static inline 
        auto convert(Tuple t, Args&&... args) 
            -> decltype(
                _tuple_last_helper<start,N-1,Tuple>::convert(t, 
                    std::get<start+N-1>(t), 
                    std::forward<Args>(args)...))
        {
            return _tuple_last_helper<start,N-1,Tuple>::convert(t, std::get<start+N-1>(t), std::forward<Args>(args)...);
        }
    };

    template<size_t start, typename Tuple>
    struct _tuple_last_helper<start,0,Tuple>
    {
        template<typename... Args>
        static inline 
        auto convert(Tuple t, Args&&... args) 
            -> decltype( std::make_tuple(std::forward<Args>(args)...) )
        {
            return std::make_tuple(std::forward<Args>(args)...);
        }
    };


    template<size_t start, typename Tuple>
    auto last_of_tuple(Tuple t) 
        -> decltype(_tuple_last_helper<start, std::tuple_size<Tuple>::value-start, Tuple>::convert(t))
    {
        return _tuple_last_helper<start, std::tuple_size<Tuple>::value-start, Tuple>::convert(t);
    }


//https://stackoverflow.com/questions/1198260/how-can-you-iterate-over-the-elements-of-an-stdtuple

   template<std::size_t I = 0, typename FuncT, typename... Tp>
   inline typename std::enable_if<I == sizeof...(Tp), void>::type
   tuple_for_each(std::tuple<Tp...> const&, FuncT&&) // Unused arguments are given no names.
   { }

   template<std::size_t I = 0, typename FuncT, typename... Tp>
   inline typename std::enable_if<I < sizeof...(Tp), void>::type
   tuple_for_each(std::tuple<Tp...> const& t, FuncT&& f)
   {
       f(std::get<I>(t));
       tuple_for_each<I + 1, FuncT, Tp...>(t, std::forward<FuncT>(f));
   }

   template<std::size_t I = 0, typename FuncT, typename... Tp>
   inline typename std::enable_if<I < sizeof...(Tp), void>::type
   tuple_for_each(std::tuple<Tp...>&& t, FuncT&& f)
   {
       f(std::get<I>(t));
       tuple_for_each<I + 1, FuncT, Tp...>(std::forward<std::tuple<Tp...>&&>(t), std::forward<FuncT>(f));
   }

}

#endif
