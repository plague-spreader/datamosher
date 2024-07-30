from datamoshers import Datamosher
import numpy as np
import argparse
import pathlib


class MyDatamosher(Datamosher):
    def __init__(self,
                 a: int,
                 b: int,
                 *,
                 path_obj_in: pathlib.Path,
                 path_obj_out: pathlib.Path,
                 skip_head: int = 0,
                 skip_tail: int = -1,
                 block_size: int = 4096):
        super().__init__(path_obj_in=path_obj_in,
                         path_obj_out=path_obj_out,
                         skip_head=skip_head,
                         skip_tail=skip_tail,
                         block_size=block_size)
        self.a = a
        self.b = b

    def _datamosh(self, data_in: bytes) -> bytes:
        to_write = np.frombuffer(data_in, dtype=np.uint8)
        rand_data = []
        x = 0
        while len(rand_data) < len(data_in):
            x = (self.a * x + self.b) % 256
            rand_data.append(x)
        rand_data = np.array(rand_data, dtype=np.uint8)
        return np.bitwise_xor(to_write, rand_data)


def add_subparser_definitions(str_datamosher: str,
                              subparsers: argparse._SubParsersAction):
    ap = subparsers.add_parser(str_datamosher, description="""\
Using LCG (https://en.wikipedia.org/wiki/Linear_congruential_generator),
generate random data and bitwise_xor them with the input data bytes.
Mostly useless tbh.""")
    ap.add_argument("a", type=int, help="The LCG multiplier")
    ap.add_argument("b", type=int, help="The LCG increment")

def parse_args(args: argparse.Namespace):
    return MyDatamosher(args.a, args.b,
                        path_obj_in=args.in_pathobj,
                        path_obj_out=args.out_pathobj,
                        skip_head=args.skip_head,
                        skip_tail=args.skip_tail,
                        block_size=args.block_size)
