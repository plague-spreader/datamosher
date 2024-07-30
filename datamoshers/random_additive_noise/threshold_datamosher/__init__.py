from datamoshers.random_additive_noise.random_datamosher\
        import RandomDatamosher
import numpy as np
import argparse


class Interval:
    def __init__(self, left_limit, right_limit):
        self._left_limit = left_limit
        self._right_limit = right_limit

    def contains(self, x: np.array):
        # cannot use __contains__ dunder method here because when calling "in"
        # operator python will do bool(self.__contains__(x)) and that external
        # bool() call will give the "the truth value of an array with more than
        # blah blah blah" error message
        return (x > self._left_limit) & (x < self._right_limit)

    def __repr__(self):
        return f'({self._left_limit}, {self._right_limit})'


class RNG:
    def __init__(self, *, seed, interval: Interval):
        # virgin numpy default_rng vs CHAD python random.seed()...
        if not isinstance(seed, int):
            seed = hash(seed)
        seed = abs(seed)

        self._rng = np.random.default_rng(seed)
        self._interval = interval

    def random_data(self, num_bytes: int):
        random_sample = self._generate_random_bits(num_bytes)
        thresholded_bits = self._interval.contains(random_sample).\
                astype(np.uint8)
        thresholded_bits = thresholded_bits << np.arange(0, 8).reshape(1, -1)
        return np.bitwise_or.reduce(thresholded_bits, axis=1, dtype=np.uint8)

    def _generate_random_bits(self, num_bytes: int):
        return NotImplemented


class UniformRNG(RNG):
    def __init__(self, lower, upper, *, seed, interval: Interval):
        super().__init__(seed=seed, interval=interval)
        self._lower = lower
        self._upper = upper

    def _generate_random_bits(self, num_bytes: int):
        return self.rng.uniform(self._lower, self._upper, size=(num_bytes, 8))


class ExponentialRNG(RNG):
    def __init__(self, mean: float, *, seed, interval: Interval):
        super().__init__(seed=seed, interval=interval)
        self._mean = mean

    def _generate_random_bits(self, num_bytes: int):
        return self._rng.exponential(scale=self._mean, size=(num_bytes, 8))


class GaussianRNG(RNG):
    def __init__(self, mean: float, stddev: float, *, seed,
                 interval: Interval):
        super().__init__(seed=seed, interval=interval)
        self._mean = mean
        self._stddev = stddev

    def _generate_random_bits(self, num_bytes):
        return self._rng.normal(loc=self._mean, scale=self._stddev,
                                size=(num_bytes, 8))


def add_subparser_definitions(str_datamosher: str,
                              subparser: argparse._SubParsersAction):
    ap = subparser.add_parser(str_datamosher, description="""\
Generate random bits using some distribution (3rd parameter) and set the bits
to 1 whether the distribution samples are between the 1st and 2nd parameter
float values""")
    ap.add_argument("left_probability_threshold", type=float,
                    help="The left threshold. Can be inf, -inf and nan")
    ap.add_argument("right_probability_threshold", type=float,
                    help="The right threshold. Can be inf, -inf and nan")
    distribution = ap.add_subparsers(dest="distribution",
                                     help="The distribution to use")
    distribution.required = True
    uniform = distribution.add_parser("uniform",
                                      help="Uniform random variable")
    uniform.add_argument("--lower", type=float, default=0,
                         help="Lower bound. Default=0")
    uniform.add_argument("--upper", type=float, default=1,
                         help="Upper bound. Default=1")
    exponential = distribution.add_parser("exponential",
                                          help="Exponential random variable")
    exponential.add_argument("--mean", type=float, default=1,
                             help="The mean value i.e. 1/lambda. Default=1")
    gaussian = distribution.add_parser("gaussian",
                                       help="Gaussian/Normal random variable")
    gaussian.add_argument("--mean", type=float, default=0,
                          help="The mean value. Default=0")
    gaussian.add_argument("--stddev", type=float, default=1,
                          help="The standard deviation. Default=1")

def parse_args(args: argparse.Namespace):
    rng = None
    interval = Interval(args.left_probability_threshold,
                        args.right_probability_threshold)
    if args.distribution == "uniform":
        rng = UniformRNG(args.lower, args.upper,
                         seed=args.seed, interval=interval)
    elif args.distribution == "exponential":
        rng = ExponentialRNG(args.mean, seed=args.seed, interval=interval)
    elif args.distribution == "gaussian":
        rng = GaussianRNG(args.mean, args.stddev,
                          seed=args.seed, interval=interval)
    else:
        raise ValueError(f'Unexpected distribution "{args.distribution}"')

    return RandomDatamosher(rng,
                            path_obj_in=args.in_pathobj,
                            path_obj_out=args.out_pathobj,
                            skip_head=args.skip_head,
                            skip_tail=args.skip_tail,
                            block_size=args.block_size)
