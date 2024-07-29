#!/usr/bin/env python

from datamoshers import add_subparsers, parse_args
import pathlib
import argparse
import numpy as np

def main(args):
    if args.seed is None:
        args.seed = np.random.randint(0, 10000000)
        print("Seed:", args.seed)
    datamosher = parse_args(args.datamosher, args)
    datamosher.datamosh()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("in_pathobj", type=pathlib.Path)
    ap.add_argument("out_pathobj", type=pathlib.Path)
    subparsers = ap.add_subparsers(dest="datamosher")
    subparsers.required = True
    add_subparsers(subparsers)

    ap.add_argument("--skip-head", type=int, default=0)
    ap.add_argument("--skip-tail", type=int, default=-1)
    ap.add_argument("--block-size", type=int, default=4096)
    ap.add_argument("--seed")
    main(ap.parse_args())
