#!/usr/bin/env python

from datamoshers.image import MyDatamosher
import argparse

def main(args):
    with args.in_fobj as f_in:
        with args.out_fobj as f_out:
            datamosher = MyDatamosher(f_in, f_out, 9823, -347)
            datamosher.datamosh()

def input_file(filename):
    return open(filename, mode="rb")

def output_file(filename):
    return open(filename, mode="wb")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("in_fobj", type=input_file)
    ap.add_argument("out_fobj", type=output_file)
    main(ap.parse_args())
