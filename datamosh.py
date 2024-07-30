#!/usr/bin/env python

from datamoshers import add_subparsers, parse_args
import random
import pathlib
import argparse

def main(args: argparse.ArgumentParser):
    if args.seed is None:
        args.seed = random.randint(0, 10000000)
        print("Seed:", args.seed)
    datamosher = parse_args(args.datamosher, args)
    datamosher.datamosh()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="""\
What is datamosing? http://datamoshing.com/

Python program for aiding your datamoshing demands""")
    ap.add_argument("in_pathobj", type=pathlib.Path,
                    help="The input file to datamosh")
    ap.add_argument("out_pathobj", type=pathlib.Path,
                    help="The datamoshed output file")
    subparsers = ap.add_subparsers(dest="datamosher", help="Datamosher to use")
    subparsers.required = True
    add_subparsers(subparsers)

    ap.add_argument("--skip-head", type=int, default=0,
                    help="Skip the first N bytes")
    ap.add_argument("--skip-tail", type=int, default=-1,
                    help="Skip the last N bytes")
    ap.add_argument("--block-size", type=int, default=4096,
                    help="Read the input data using this block size")
    ap.add_argument("--seed",
                    help="Random seed. Same values yield same results")
    main(ap.parse_args())
