import sys
import random

from models.double_pendulum import DoublePendulum
from models.double_pendulum_on_cart import DoublePendulumOnCart

"""
Main script to generate animations and datasets of random configurations
of the double pendulum and the double pendulum on cart. 

Usage: python double_pendulum_nn.py <pendulum|pendulum_cart> <dataset|animation> <simulations>
"""

if len(sys.argv) != 4:
    print("Usage: python double_pendulum_nn.py <pendulum|pendulum_cart> <dataset|animation> <simulations>")
    exit()

model = sys.argv[1].lower()
mode = sys.argv[2].lower()
n_simulations = int(sys.argv[3])

PATH = "./dataset/"
EXT = ".csv"

if model == "pendulum":
    pendulum = DoublePendulum()
    path = PATH + "double_pendulum/series_"
    for i in range(n_simulations):

        th1 = random.uniform(0, 360)
        th2 = random.uniform(0, 360)

        w1 = random.uniform(-180, 180)
        w2 = random.uniform(-180, 180)

        pendulum.set_initial_conditions(th1, w1, th2, w2)

        pendulum.solve()

        if mode == "dataset":
            filename = path + str(i+1) + EXT
            pendulum.save(filename)
        elif mode == "animation":
            pendulum.animate()
        else:
            print("Usage: python double_pendulum_nn.py <pendulum|pendulum_cart> <dataset|animation> <simulations>")
            exit()

elif model == "pendulum_cart":
    pendulum = DoublePendulumOnCart()
    path = PATH + "double_pendulum_on_cart/series_"
    for i in range(n_simulations):

        th1 = random.uniform(0, 360)
        th2 = random.uniform(0, 360)

        w1 = random.uniform(-180, 180)
        w2 = random.uniform(-180, 180)

        pendulum.set_initial_conditions(th1, w1, th2, w2, 0, 0)

        pendulum.set_random_control_force(-10, 10)

        pendulum.solve()

        if mode == "dataset":
            filename = path + str(i+1) + EXT
            pendulum.save(filename)
        elif mode == "animation":
            pendulum.animate()
        else:
            print("Usage: python double_pendulum_nn.py <pendulum|pendulum_cart> <dataset|animation> <simulations>")
            exit()
else:
    print("Usage: python double_pendulum_nn.py <pendulum|pendulum_cart> <dataset|animation> <simulations>")
    exit()