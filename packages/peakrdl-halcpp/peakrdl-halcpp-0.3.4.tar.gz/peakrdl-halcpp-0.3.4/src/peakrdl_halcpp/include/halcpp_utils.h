#ifndef _HALCPP_UTILS_H_
#define _HALCPP_UTILS_H_

#include <type_traits>
#include <cstdint>

namespace halcpp{

template<uint32_t WIDTH, uint32_t VAL>
class Const{
public:
    using dataType =
        typename std::conditional<(WIDTH) <= 8, uint8_t,
                                  typename std::conditional<(WIDTH) <= 16,
                                                            uint16_t, uint32_t>::type>::type;
    static constexpr dataType val = VAL;
    static constexpr uint32_t width = WIDTH;

    template<uint32_t OTHER_WIDTH, uint32_t OTHER_VAL>
    // inline const Const<OTHER_WIDTH+WIDTH, (OTHER_VAL << WIDTH) | VAL> operator,(const Const<OTHER_WIDTH, OTHER_VAL> &a) const{
        // return Const<OTHER_WIDTH+WIDTH, (OTHER_VAL << WIDTH) | VAL>();
    inline const Const<OTHER_WIDTH+WIDTH, (VAL << OTHER_WIDTH) | OTHER_VAL> operator,([[maybe_unused]]const Const<OTHER_WIDTH, OTHER_VAL> &a) const{
        return Const<OTHER_WIDTH+WIDTH, (VAL << OTHER_WIDTH) | OTHER_VAL>();
    }

};

template <class LIB, class = void>
struct node_has_set : std::false_type {};

template <class LIB>
struct node_has_set<LIB,
                    std::enable_if_t<std::is_invocable_r<bool, decltype(LIB::has_set)>::value>>
    : std::integral_constant<bool, LIB::has_set()> {};

template <class LIB>
constexpr bool node_has_set_v = node_has_set<LIB>::value;

template <class LIB, class = void>
struct node_has_get : std::false_type {};

template <class LIB>
struct node_has_get<LIB,
                    std::enable_if_t<std::is_invocable_r<bool, decltype(LIB::has_get)>::value>>
    : std::integral_constant<bool, LIB::has_get()> {};

template <class LIB>
constexpr bool node_has_get_v = node_has_get<LIB>::value;
}

#endif // !_HALCPP_UTILS_H_
