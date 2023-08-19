from systemrdl.node import Node, AddrmapNode, RegNode, RootNode, MemNode, FieldNode, AddressableNode
from typing import List, Dict

class HalBase: # TODO make abstract
    def __init__(self, 
                 node : Node,
                 parent : 'HalBase|None',
                 ):
        self.node = node
        self.parent = parent

    def get_docstring(self) -> str:
        desc = "/*\n"
        if self.node.get_property('desc') is not None:
            for l in self.node.get_property('desc').splitlines():
                desc = desc + "* " + l + "\n"
            return desc + "*/"
        return  ""

    @property
    def cpp_type(self) -> str:
        raise NotImplementedError("You need to overload this method in inherited class")

    def get_template_line(self):
        raise NotImplementedError("You need to overload this method in inherited class")

    def get_cls_tmpl_spec(self, just_tmpl=False) -> str:
        raise NotImplementedError("You need to overload this method in inherited class")
    
    @property
    def type_name(self) -> str:
        return self.orig_type_name


    @property
    def addr_offset(self) -> int:
        raise NotImplementedError("You need to overload this method in inherited class")

    @property
    def orig_type_name(self) -> str:
        if self.node.orig_type_name is not None:
            return self.node.orig_type_name
        else:
            return self.node.inst_name

    def get_parent_haladdrmap(self) -> 'HalAddrmap':
        if isinstance(self.parent, HalAddrmap):
            return self.parent
        assert self.parent is not None
        return self.parent.get_parent_haladdrmap()
        
class HalField(HalBase):

    def __init__(self, 
                 node: FieldNode,
                 parent : 'HalReg',
                 ):
        super().__init__(node, parent)
        self.node = node # TODO REMOVE
        self.parent = parent

    @property
    def width(self) -> int:
        return self.node.width

    def has_enum(self) -> bool:
        return self.node.get_property('encode', default=False) != False

    def get_enum(self):
        encode = self.node.get_property('encode')
        namespace_enums = self.get_namespace_enums()
        if encode is not None:
            name = encode.__name__
            if name in namespace_enums:
                if namespace_enums[name][-1] == self.node.owning_addrmap: # TODO WHAT???
                    return False, None, None, None, None, None
            enum_strings = []
            enum_values = []
            enum_desc = []
            for k, v in encode.members.items():
                enum_strings.append(encode.members[k].name)
                enum_values.append(encode.members[k].value)
                enum_desc.append(encode.members[k].rdl_desc)

            const_width = max(enum_values).bit_length()

            namespace_enums[name] = [enum_strings, enum_values, enum_desc, const_width, self.node.owning_addrmap]
            return True, name, enum_strings, enum_values, enum_desc, const_width
        
        return False, None, None, None, None, None

    def get_enum_name(self):
        encode = self.node.get_property('encode')
        if encode is not None:
            return encode.__name__

    def get_namespace_enums(self) -> 'Dict':
        return self.get_parent_haladdrmap().enums

    @property
    def cpp_type(self) -> str:
        out = ""
        if self.node.is_sw_readable and self.node.is_sw_writable:
            return "FieldRW"
        elif self.node.is_sw_writable and not self.node.is_sw_readable:
            return "FieldWO"
        elif self.node.is_sw_readable:
            return "FieldRO"
        return out

    def get_template_line(self) -> str:
        assert False, "You should not create a class from a FieldNode"

    def get_cls_tmpl_spec(self, just_tmpl=False) -> str:
        assert False, "You should not extend FieldNode classes"

class HalReg(HalBase):
    
    def __init__(self, 
                 node : RegNode,
                 parent : 'HalAddrmap',
                 bus_offset : int = 0,
                 ):
        super().__init__(node, parent)
        self.node = node # TODO REMOVE
        self.parent = parent
        self.bus_offset = bus_offset

        self.fields = self.get_fields()
    
    @property # TODO move to base?
    def is_array(self) -> bool:
        return self.node.is_array

    @property
    def width(self) -> int:
        return max([c.node.high for c in self.fields]) + 1

    def get_fields(self) -> 'List[HalField]':
        return [HalField(c, self) for c in self.node.children() if isinstance(c, FieldNode)]

    @property
    def cpp_type(self):
        if self.parent.node.get_property("zicsr", default=False) or self.node.get_property("zicsr", default=False):
            prefix = "Csr"
        else:
            prefix = ""
        if self.node.has_sw_readable and self.node.has_sw_writable:
            return prefix + "RegRW"
        elif self.node.has_sw_writable and not self.node.has_sw_readable:
            return prefix + "RegWO"
        elif self.node.has_sw_readable:
            return prefix + "RegRO"
        assert False

    def get_template_line(self) -> str:
        return f"template<uint32_t BASE, uint32_t WIDTH, typename PARENT_TYPE>"

    def get_cls_tmpl_spec(self, just_tmpl=False) -> str:
        str = self.type_name.upper() if not just_tmpl else ""
        return str + "<BASE, WIDTH, PARENT_TYPE>"

    @property
    def addr_offset(self) -> int:
        return self.bus_offset + self.node.address_offset


class HalArrReg(HalReg):
    def __init__(self, 
                 node : RegNode,
                 parent : 'HalAddrmap',
                 bus_offset : int = 0,
                 ):
        super().__init__(node, parent)
        self.node = node # TODO REMOVE
        self.bus_offset = bus_offset

        assert node.is_array, "Register Node is not array"

        assert self.node.size == self.node.array_stride, f"Different stride than regwidth is not supported {self.node.size} {self.node.array_stride}"

    @property
    def addr_offset(self):
        return self.bus_offset + next(self.node.unrolled()).address_offset # type: ignore


class HalMem(HalBase):
    
    def __init__(self, 
                 node : MemNode,
                 parent : 'HalAddrmap',
                 bus_offset : int = 0,
                 ):
        super().__init__(node, parent)
        self.node = node
        self.parent = parent
        self.bus_offset = bus_offset

        for c in self.parent.node.children():
            if isinstance(c, AddressableNode):
                assert c == self.node, f"Addrmaps with anything else than one memory node is currently not allowed, it could be easily added"

    @property
    def size(self) -> int:
        return self.node.size

    @property
    def width(self) -> int: # TODO probably not good
        return self.size

    def get_template_line(self) -> str:
        return f"template<uint32_t BASE, uint32_t SIZE, typename PARENT_TYPE>"

    @property
    def cpp_type(self) -> str:
        assert False, "cpp_type should not be called on HalMem class"

    def get_cls_tmpl_spec(self, just_tmpl=False) -> str:
        str = self.type_name.upper() if not just_tmpl else ""
        return str + "<BASE, SIZE, PARENT_TYPE>"

    @property
    def type_name(self) -> str:
        return self.parent.orig_type_name

    @property
    def addr_offset(self) -> int:
        return self.bus_offset + self.node.address_offset

class HalAddrmap(HalBase):
    def __init__(self,
            node : AddrmapNode,
            parent : 'HalAddrmap|None' = None,
            bus_offset : int = 0,
            ):
        super().__init__(node, parent)
        self.node = node # TODO REMOVE
        self.parent = parent
        self.bus_offset = bus_offset

        assert (self.parent == None) == isinstance(self.node.parent, RootNode)

        self.regs = self.get_regs()
        self.mems = self.get_mems()
        self.addrmaps = self.get_addrmaps()

        self.enums = {}

    @property
    def is_root_node(self) -> bool:
        return self.parent == None

    def get_regs(self) -> 'List[HalReg]':
        regs = []
        for c in self.node.children():
            if isinstance(c, RegNode):
                reg = HalArrReg(c, self) if c.is_array else HalReg(c, self)
                regs.append(reg)
        return regs
        # return [HalReg(c) for c in self.node.children() if isinstance(c, RegNode)]

    def get_mems(self) -> 'List[HalMem]':
        return [HalMem(c, self) for c in self.node.children() if isinstance(c, MemNode)]

    def get_addrmaps(self) -> 'List[HalAddrmap]':
        return [HalAddrmap(c, self) for c in self.node.children() if isinstance(c, AddrmapNode)]

    def remove_buses(self):
        for c in self.addrmaps:
            c.remove_buses()
            if c.is_bus(): # Doesnt have registers or memories, only addrmaps
                for subc in c.addrmaps: # Change parent
                    subc.bus_offset += c.addr_offset
                    subc.parent = self
                self.addrmaps.remove(c)
                self.addrmaps.extend(c.addrmaps) # Steal all addrmaps from a bus

    def is_bus(self) -> bool:
        if len(self.regs) == 0 and len(self.mems) == 0:
            return True
        return False

    def get_template_line(self) -> str:
        if self.is_root_node:
            return "template <uint32_t BASE, typename PARENT_TYPE=void>"
        return "template <uint32_t BASE, typename PARENT_TYPE>"
    
    @property
    def type_name(self) -> str:
        return self.orig_type_name + "_hal"

    def get_cls_tmpl_spec(self, just_tmpl=False) -> str:
        str = self.type_name.upper() if not just_tmpl else ""

        if self.is_root_node:
            return str + "<BASE, PARENT_TYPE>"
        return str + "<BASE, PARENT_TYPE>"

    def get_addrmaps_recursive(self):
        addrmaps = self.addrmaps.copy()
        for c in self.addrmaps:
            addrmaps.extend(c.get_addrmaps_recursive())
        if self.is_root_node:
            addrmaps.insert(0, self)
        return addrmaps

    @property
    def addr_offset(self) -> int:
        return self.bus_offset + self.node.address_offset

