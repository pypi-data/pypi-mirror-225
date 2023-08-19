#ifndef _ADDRMAP_NODE_H_
#define _ADDRMAP_NODE_H_

#include "arch_io.h"
#include <cstdint>

// TODO define architecture type size, so it replaces uint32_t

template <uint32_t BASE, typename PARENT_TYPE = void>
class AddrmapNode {
public:
    static constexpr uint32_t get_abs_addr() { return PARENT_TYPE().get_abs_addr() + BASE; }

    static inline uint32_t get(const uint32_t addr) { return PARENT_TYPE::get(addr + BASE); }
    static inline void set(const uint32_t addr, uint32_t val) {
        PARENT_TYPE::set(addr + BASE, val);
    }

    static inline uint32_t get_csr(const uint32_t addr) { return PARENT_TYPE::get_csr(addr + BASE); }
    static inline void set_csr(const uint32_t addr, uint32_t val) {
        PARENT_TYPE::set_csr(addr + BASE, val);
    }
};

/* Specialization for the Top hierarchy addrmap
 *  Top node does not have a parent.
 *  Insted it inherits ArchIoNode, that implements memory access for architecture
 */
template <uint32_t BASE>
class AddrmapNode <BASE, void> : public ArchIoNode {
public:

    static constexpr uint32_t get_abs_addr() { return BASE; }

    static inline void set(uint32_t addr, uint32_t val) {
        ArchIoNode::write32(addr + BASE, val);
    }
    static inline uint32_t get(uint32_t addr) { return ArchIoNode::read32(addr + BASE); }

    static inline void set_csr(uint32_t addr, uint32_t val) {
        ArchIoNode::csr_write32(addr + BASE, val);
    }
    static inline uint32_t get_csr(uint32_t addr) { return ArchIoNode::csr_read32(addr + BASE); }
};

#endif // !_ADDRMAP_NODE_H_
