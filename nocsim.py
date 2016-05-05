#!/usr/bin/python
from argparse import ArgumentParser as ap
from generators import get_distributions
from simulate import simulate


p = ap(
	prog="sandbox", epilog="="*60,
	description="NoC random assembly modeling simulation.")

p.add_argument(
	"-w", "--wires", dest="wire_range", nargs=2, type=int,
	metavar=("{from}", "{to}"), help="Wire count range.")

p.add_argument(
	"-l", "--lengths", dest="length_range", nargs=2, type=int,
	metavar=("{from}", "{to}"), help="Wire length range.")

p.add_argument(
	"-s", "--step", nargs=1, dest="step", type=int,
	metavar="{step}", help="Wire count range step size")

p.add_argument(
	"-W", "--width", nargs=1, dest="width", type=int,
	metavar="{width}", help="Width of the N x N chip to simulate")

p.add_argument(
	"-t", "--trials", nargs=1, dest="trials", type=int,
	metavar="{trails}", help="Number of trials to run with the given parameters")

p.add_argument(
	"-d", "--dist", nargs=1, dest="distribution", type=str,
	help="Wire distribution to use.", 
	choices=[k for k in dict(get_distributions())])

simulate(p.parse_args())

