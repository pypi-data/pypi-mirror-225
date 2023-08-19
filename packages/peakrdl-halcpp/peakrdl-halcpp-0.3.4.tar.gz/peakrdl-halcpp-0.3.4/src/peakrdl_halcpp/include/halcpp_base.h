#ifndef _HALCPP_BASE_H_
#define _HALCPP_BASE_H_

#include <stdint.h>
#include <type_traits>
#include "field_node.h"
#include "reg_node.h"
#include "csr_reg_node.h"
#include "reg_arr_node.h"
#include "addrmap_node.h"


template <uint32_t BASE, uint32_t SIZE, typename PARENT_TYPE>
class MemNode {
public:

    static constexpr uint32_t base = BASE;
    static constexpr uint32_t size = SIZE;

    inline uint32_t get(const uint32_t addr) { return PARENT_TYPE::get(addr + BASE); }
    inline void set(const uint32_t addr, uint32_t val) { PARENT_TYPE::set(addr + BASE, val); }
    static constexpr uint32_t get_abs_addr() { return PARENT_TYPE().get_abs_addr() + BASE; }
    constexpr uint32_t get_size() { return SIZE; }
};

#endif
