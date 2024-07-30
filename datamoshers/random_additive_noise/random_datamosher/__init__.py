from datamoshers import Datamosher
import numpy as np
import argparse
import pathlib


class RandomDatamosher(Datamosher):
    def __init__(self,
                 rng: np.random.Generator,
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
        self.rng = rng

    def _datamosh(self, data_in: bytes) -> bytes:
        to_write = np.frombuffer(data_in, dtype=np.uint8)
        rand_data = self.rng.random_data(len(data_in))
        return np.bitwise_xor(to_write, rand_data)


class MyRNG:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)

    def random_data(self, num_bytes):
        return self.rng.integers(256, size=(num_bytes,),dtype=np.uint8)


def add_subparser_definitions(str_datamosher: str,
                              subparser: argparse._SubParsersAction):
    subparser.add_parser(str_datamosher, description="""\
This datamosher will just generate random numbers and bitwise_xor them with the
bytes of the input file""")

def parse_args(args: argparse.Namespace):
    return RandomDatamosher(MyRNG(args.seed),
                            path_obj_in=args.in_pathobj,
                            path_obj_out=args.out_pathobj,
                            skip_head=args.skip_head,
                            skip_tail=args.skip_tail,
                            block_size=args.block_size)
