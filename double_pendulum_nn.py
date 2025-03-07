import argparse
import random

from models.double_pendulum import DoublePendulum
from models.double_pendulum_on_cart import DoublePendulumOnCart

"""
Generate datasets and animations of the double pendulum and the double pendulum on cart. 

usage: double_pendulum_nn.py {pendulum,pendulum_cart} {dataset,animation} n_simulations

positional arguments:
    {pendulum,pendulum_cart}    Model of the system (str)
    {dataset,animation}         Mode of the script (str)
    n_simulations               Number of simulations to run (int)
"""

parser = argparse.ArgumentParser(description='Generate datasets and animations of the double pendulum and the double pendulum on cart.')
parser.add_argument('model', type=str, choices=['pendulum', 'pendulum_cart'], help='Model of the system (str)')
parser.add_argument('mode', type=str, choices=['dataset', 'animation'], help='Mode of the script (str)')
parser.add_argument('n_simulations', type=int, help='Number of simulations to run (int)')

args = parser.parse_args()

PATH = "./dataset/"
EXT = ".csv"

if args.model == "pendulum":
    pendulum = DoublePendulum()
    path = PATH + "double_pendulum/series_"
    for i in range(args.n_simulations):

        th1 = random.uniform(0, 360)
        th2 = random.uniform(0, 360)

        w1 = random.uniform(-180, 180)
        w2 = random.uniform(-180, 180)

        pendulum.set_initial_conditions(th1, w1, th2, w2)

        pendulum.solve()

        if args.mode == "dataset":
            filename = path + str(i+1) + EXT
            pendulum.save(filename)
        elif args.mode == "animation":
            pendulum.animate()

elif args.model == "pendulum_cart":
    pendulum = DoublePendulumOnCart()
    path = PATH + "double_pendulum_on_cart/series_"
    for i in range(args.n_simulations):

        th1 = random.uniform(0, 360)
        th2 = random.uniform(0, 360)

        w1 = random.uniform(-180, 180)
        w2 = random.uniform(-180, 180)

        pendulum.set_initial_conditions(th1, w1, th2, w2, 0, 0)

        pendulum.set_random_control_force(-10, 10)

        pendulum.solve()

        if args.mode == "dataset":
            filename = path + str(i+1) + EXT
            pendulum.save(filename)
        elif args.mode == "animation":
            pendulum.animate()