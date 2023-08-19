from systemrdl.node import  Node, RootNode, AddrmapNode
import jinja2
from typing import List, Union, Any
import os
import shutil

from .haladdrmap import *
from .halutils import HalUtils

class HalExporter():
    def __init__(self):
        self.cpp_dir = "include"

        self.base_headers = [
                "halcpp_base.h",
                "halcpp_utils.h",
                "field_node.h",
                "reg_node.h",
                "csr_reg_node.h",
                "reg_arr_node.h",
                "addrmap_node.h",
                "arch_io.h",
                ]

    def list_files(self,
                   top : HalAddrmap,
                   outdir : str,
                   ):
        out_files = [os.path.join(outdir, addrmap.type_name + ".h") for addrmap in top.get_addrmaps_recursive()]
        out_files += [os.path.join(outdir, x) for x in self.base_headers] + out_files
        print(*out_files) # Print files to stdout

    def copy_base_headers(self, outdir):
        abspaths = [os.path.join(os.path.dirname(__file__), self.cpp_dir, x) for x in self.base_headers]
        outdir = os.path.join(outdir, "include")
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        [shutil.copy(x, outdir) for x in abspaths]

    def export(self,
            nodes: 'Union[Node, List[Node]]',
            outdir: str, 
            list_files: bool=False,
            ext : list=[],
            keep_buses : bool=False,
            **kwargs: 'Dict[str, Any]') -> None:


        # if not a list
        if not isinstance(nodes, list):
            nodes = [nodes]

        # If it is the root node, skip to top addrmap
        for i, node in enumerate(nodes):
            if isinstance(node, RootNode):
                nodes[i] = node.top

        if kwargs:
            raise TypeError("got an unexpected keyword argument '%s'" % list(kwargs.keys())[0])

        try:
            os.makedirs(outdir)
        except FileExistsError:
            pass

        halutils = HalUtils(ext)

        assert isinstance(nodes[-1], AddrmapNode)
        top = halutils.build_hierarchy(
                node=nodes[-1],
                remove_root=False, # TODO fix
                keep_buses=keep_buses,
                )


        if list_files:
            self.list_files(top, outdir)
        else:
            for halnode in top.get_addrmaps_recursive():
                context = {
                        'halnode'  : halnode,
                        'halutils' : halutils,
                        }
                text = self.process_template(context)
                out_file = os.path.join(outdir, halnode.type_name + ".h")
                with open(out_file, 'w') as f:
                    f.write(text)

            self.copy_base_headers(outdir)

    def process_template(self, context : dict) -> str:

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
            trim_blocks=True,
            lstrip_blocks=True)

        env.filters.update({
            'zip' : zip,
            })

        res = env.get_template("addrmap.j2").render(context)
        return res

