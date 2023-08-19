from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin #pylint: disable=import-error
from peakrdl.config import schema #pylint: disable=import-error

# from peakrdl.main import main
from .exporter import  HalExporter
import sys

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode


class Exporter(ExporterSubcommandPlugin):
    short_desc = "Generate CPP Hardware Abstraction Layer libraries"
    long_desc = "Generate CPP Hardware Abstraction Layer libraries"


    def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:

        arg_group.add_argument(
                "--ext",
                nargs="*", 
                help="list of addrmap modules that have implemented <name>_EXT class in <name>_ext.h header file, used for extending functionality"
                )

        arg_group.add_argument(
            "--list-files",
            dest="list_files",
            default=False,
            action="store_true",
            help="Dont generate files, but instead just list the files that will be generated, and external files that need to be included"
        )

        arg_group.add_argument(
            "--keep-buses",
            dest="keep_buses",
            default=False,
            action="store_true",
            help="If there is an addrmap containing only addrmaps, not registers, by default it will be ommited in hierarchy, it is possible to keep it by passing --keep-buses flag"
        )


    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        hal = HalExporter()
        hal.export(
            nodes=top_node,
            outdir=options.output,
            list_files=options.list_files,
            ext=options.ext,
            keep_buses=options.keep_buses,
        )

        # if "-DUSE_ZICSR=1" not in sys.argv:
        #     sys.argv.append("-DUSE_ZICSR=1")
        #     main()
