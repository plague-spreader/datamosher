import importlib
import argparse
import pathlib

class Datamosher:
    def __init__(self,
                 *,
                 path_obj_in: pathlib.Path,
                 path_obj_out: pathlib.Path,
                 skip_head: int = 0,
                 skip_tail: int = -1,
                 block_size: int = 4096):
        self.path_obj_in = path_obj_in
        self.path_obj_out = path_obj_out
        self.skip_head = skip_head
        self.skip_tail = skip_tail
        self.block_size = block_size

    def datamosh(self):
        last_byte_to_randomize = self.path_obj_in.stat().st_size
        if self.skip_tail != -1:
            last_byte_to_randomize -= self.skip_tail

        with self.path_obj_in.open(mode="rb") as f_in:
            with self.path_obj_out.open(mode="wb") as f_out:
                f_out.write(f_in.read(self.skip_head))
                num_bytes_read = self.skip_head

                while True:
                    block_size = min(self.block_size,
                                     last_byte_to_randomize - num_bytes_read)
                    data_in = f_in.read(block_size)
                    num_bytes_read += len(data_in)
                    if block_size == 0 or len(data_in) == 0:
                        break
                    f_out.write(self._datamosh(data_in))

                f_out.write(f_in.read())

    def _datamosh(self, data_in: bytes) -> bytes:
        return NotImplemented


def add_subparsers(subparsers: argparse._SubParsersAction):
    for datamosher in pathlib.Path("datamoshers").glob("**/__init__.py"):
        str_datamosher = str(datamosher)
        if str_datamosher == "datamoshers/__init__.py":
            continue
        str_datamosher = str_datamosher[12:-12].replace("/", ".")
        subparser = subparsers.add_parser(str_datamosher)
        lib = importlib.import_module("datamoshers." + str_datamosher)
        lib.add_arguments(subparser)

def parse_args(str_datamosher: str, args: argparse.Namespace) -> Datamosher:
    lib = importlib.import_module("datamoshers." + str_datamosher)
    return lib.parse_args(args)
