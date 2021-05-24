from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


class PointMass:
    def __init__(self, m, x, v, a):
        self.m = m
        self.x = x
        self.v = v
        self.a = a
        self.last_a = 0

    def apply_force(self, f):
        self.a += f / self.m

    def act(self):
        self.last_a = self.a
        self.v += self.a
        self.x += self.v
        self.a = 0

    def __repr__(self):
        return f'({self.m}, {self.x}, {self.v}, {self.last_a})'


class SpringChain:
    def __init__(self, n_springs, l, k, m, g: float = 0):
        self.masses: Any = self._get_masses(n_springs, l, m)
        self.l = l
        self.k = k
        self.g = g

    @classmethod
    def _get_masses(cls, n_springs, l, m):
        return [PointMass(m, l * i, 0, 0) for i in range(n_springs + 1)]

    def act(self):
        l, k, g = self.l, self.k, self.g
        for left, right in zip(self.masses, self.masses[1:]):
            d = (right.x - left.x)
            f = k * (d - l)
            left.apply_force(f)
            right.apply_force(-f)

        for mass in self.masses:
            f = -mass.v * self.g
            mass.apply_force(f)

        for mass in self.masses:
            mass.act()

    def get_mass(self, i):
        return self.masses[i]

    def apply_force_left(self, f):
        self.masses[0].apply_force(f)

    def get_force_at_right(self):
        return self.masses[-1].m * self.masses[-1].last_a


class FastSpringChain(SpringChain):
    @classmethod
    def _get_masses(cls, n_springs, l, m):
        return np.array([[m, l * i, 0, 0, 0] for i in range(n_springs + 1)])

    def act(self):
        d = self.masses[1:, 1] - self.masses[:-1, 1]  # calculate all displacements
        f = self.k * (d - self.l)  # calculate all forces
        self.masses[:-1, 3] += f / self.masses[:-1, 0]  # apply force the left mass of each spring
        self.masses[1:, 3] += -f / self.masses[1:, 0]  # apply force to the right mass of each spring
        self.masses[:, 3] += -self.masses[:, 2] * self.g / self.masses[:, 0]  # apply damping force to each mass

        self.masses[:, 4] = self.masses[:, 3]  # store the last acceleration value
        self.masses[:, 2] += self.masses[:, 3]  # v <- v + a
        self.masses[:, 1] += self.masses[:, 2]  # x <- x + v
        self.masses[:, 3] = 0  # a <- 0

    def apply_force_left(self, f):
        self.masses[0][3] += f / self.masses[0][0]

    def get_mass(self, i):
        mass = self.masses[i]
        return PointMass(mass[0], mass[1], mass[2], mass[3])

    def get_force_at_right(self):
        return self.masses[-1][0] * self.masses[-1][4]


def plot_spring_impulse_simulation(chain: SpringChain, steps=1000, impulse=1):
    chain.apply_force_left(impulse)
    xs = [[] for _ in range(len(chain.masses))]
    for _ in tqdm(range(steps)):
        chain.act()
        for i, mass in enumerate(chain.masses):
            xs[i].append(chain.get_mass(i).x)
    for x in xs:
        plt.plot(x)
    plt.show()
