#ifndef _ARCH_IO_H_
#define _ARCH_IO_H_

#include <cstdint>


class MemIoNode {
public:
    static inline uint32_t read32(uint32_t addr) { return *(volatile uint32_t*)addr; }
    static inline void write32(uint32_t addr, uint32_t val) { *(volatile uint32_t*)addr = val; }

};

class CsrIoNode {
public:
    static inline uint32_t csr_read32(uint32_t addr) { return *(volatile uint32_t*)addr; }
    static inline void csr_write32(uint32_t addr, uint32_t val) { *(volatile uint32_t*)addr = val; }

};

class ArchIoNode : public MemIoNode, public CsrIoNode {
public:

};

#endif // !_ARCH_IO_H_
