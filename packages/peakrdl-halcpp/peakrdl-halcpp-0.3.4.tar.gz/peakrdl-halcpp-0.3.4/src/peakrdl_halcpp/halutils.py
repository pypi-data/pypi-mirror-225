from typing import List
import getpass
import datetime

from .haladdrmap import *

class HalUtils():
    def __init__(self,
                 extern : List[str],
                 ) -> None:
        self.extern = extern

    def get_include_file(self, halnode : HalAddrmap) -> str:
        has_extern = self.has_extern(halnode)
        return halnode.orig_type_name + "_ext.h" if has_extern else halnode.type_name + ".h"

    def has_extern(self, halnode : HalAddrmap) -> bool:
        if halnode.orig_type_name in self.extern:
            return True
        return False

    def get_extern(self, halnode : HalAddrmap) -> str:
        if self.has_extern(halnode):
            return halnode.orig_type_name
        return halnode.type_name

    def get_unique_type_nodes(self, lst : 'List[HalBase]'):
        return list({node.type_name: node for node in lst}.values())

    def generate_file_header(self):
        username = getpass.getuser()
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = f"// Generated with PeakRD-halcpp : https://github.com/Risto97/PeakRDL-halcpp\n" 
        comment += f"// By user: {username} at: {current_datetime}\n"
        return comment

    def build_hierarchy(self,
                        node : AddrmapNode,
                        keep_buses   : bool = False,
                        remove_root  : bool = True,
                        ) -> HalAddrmap:
        top = HalAddrmap(node)

        # if remove_root:               # TODO check this
        #     addrmaps.remove(node)

        if keep_buses is False:
            top.remove_buses()

        return top
