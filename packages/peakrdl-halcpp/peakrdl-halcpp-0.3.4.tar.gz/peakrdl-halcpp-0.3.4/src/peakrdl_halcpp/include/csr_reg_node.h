#ifndef _CSR_REG_NODE_H_
#define _CSR_REG_NODE_H_

#include <stdint.h>
#include <type_traits>
#include "halcpp_utils.h"
#include "reg_node.h"

namespace halcpp{

template<typename BASE_TYPE>
class CsrRegWrMixin : public BASE_TYPE { // TODO merge with RegWrMixin create a new CsrRegBase and do if constexpr for different calls
public:
    using parent = typename BASE_TYPE::parent_type;
    static constexpr bool has_set() { return true; };

    static inline void set(typename BASE_TYPE::dataType val) {
        parent::set_csr(BASE_TYPE::rel_base, val);
    }

    template<uint32_t CONST_WIDTH, uint32_t CONST_VAL>
    static inline void set(const Const<CONST_WIDTH, CONST_VAL> &a){
        static_assert(BASE_TYPE::width == CONST_WIDTH, "You need to provide all the bits for concatenation.");
        parent::set_csr(BASE_TYPE::rel_base, a.val);
    }
    // Dont bother with operator= equal as its going to be overriden by inherited class anyways

};

template <typename BASE_TYPE>
class CsrRegRdMixin : public BASE_TYPE {
private:
    using parent = typename BASE_TYPE::parent_type;

public:
    static constexpr bool has_get() { return true; };

    static typename BASE_TYPE::dataType get() {
        return parent::get_csr(BASE_TYPE::rel_base);
    }

    template <typename T>
    inline operator const T() {
        static_assert(std::is_integral<T>::value, "T must be an integral type.");
        static_assert(
            sizeof(T) >= (float)(BASE_TYPE::width / 8),
            "T must be smaller than or equal to Field width, otherwise data will be lost");
        return static_cast<T>(get());
    }
};

template <uint32_t BASE, uint32_t WIDTH, typename PARENT_TYPE>
using CsrRegRO = RegNode<CsrRegRdMixin< RegBase< BASE, WIDTH, PARENT_TYPE> > >;

template <uint32_t BASE, uint32_t WIDTH, typename PARENT_TYPE>
using CsrRegWO = RegNode<CsrRegWrMixin< RegBase< BASE, WIDTH, PARENT_TYPE> > >;

template <uint32_t BASE, uint32_t WIDTH, typename PARENT_TYPE>
using CsrRegRW = RegNode<CsrRegWrMixin< RegBase< BASE, WIDTH, PARENT_TYPE> >, CsrRegRdMixin< RegBase< BASE, WIDTH, PARENT_TYPE> >  >;

}


#endif
