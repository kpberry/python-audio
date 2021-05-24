from math import sqrt, pi, sin, cos
from random import random

from tqdm import tqdm


class Point:
    def __init__(self, x, y, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def show(self):
        # point(self.x, self.y, self.z)
        raise NotImplementedError()

    def dist(self, p):
        return (p - self).n()

    def lproj(self, l):  # projection onto line
        return l.a + (self - l.a).proj(l.vec())

    def tproj(self, t):  # projection onto plane/triangle
        n = t.normal()
        ap = self - t.a
        return t.a + (ap - ap.proj(n))

    def pproj(self, p):  # projection onto plane
        return self.tproj(p)

    def ray_dist(self, r):
        return ((self - r.a) - (self.lproj(r) - r.a)).n()

    def line_dist(self, l):
        lv = l.vec()

        ac = self - l.a
        if ac.dot(lv) > 0:  # to the right of a
            bc = self - l.b
            if bc.dot(lv) > 0:  # to the right of b
                return self.dist(l.b)
            else:  # between a and b
                return self.ray_dist(l)
        else:  # to the left of a
            return self.dist(l.a)

    def plane_dist(self, p):
        return ((self - p.a) - (self.pproj(p) - p.a)).n()

    def triangle_dist(self, t):
        # https://math.stackexchange.com/questions/544946/determine-if-projection-of-3d-point-onto-plane-is-within-a-triangle
        u = t.b - t.a
        v = t.c - t.a
        w = self - t.a
        n = u.cross(v)
        # barycentric coordinates of point must be within triangle for projection to be closest point
        gamma = u.cross(w).dot(n) / n.n2()
        if 0 <= gamma <= 1:
            beta = w.cross(v).dot(n) / n.n2()
            if 0 <= beta <= 1:
                alpha = 1 - gamma - beta
                if 0 <= alpha <= 1:
                    return self.plane_dist(t)
        return min(self.dist(t.a), self.dist(t.b), self.dist(t.c))

    def __sub__(self, p):
        return Vec(self.x - p.x, self.y - p.y, self.z - p.z)

    def __add__(self, v):
        return Point(self.x + v.x, self.y + v.y, self.z + v.z)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'P({}, {}, {})'.format(self.x, self.y, self.z)


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def vec(self):
        return Vec(self.b.x - self.a.x, self.b.y - self.a.y, self.b.z - self.a.z)

    def show(self):
        # line(self.a.x, self.a.y, self.a.z, self.b.x, self.b.y, self.b.z)
        raise NotImplementedError()

    def ray_intersection(self, r):
        n = self.vec().pnormal(r.vec())
        rv = r.vec()
        num = (self.a - r.a).dot(n)
        den = rv.dot(n)
        if den == 0:
            if num == 0:
                d = 0
            else:
                return None
        else:
            d = num / den
        i = r.a + rv * d
        if rv.dot(i - r.a) > 0 and i in self:
            return i
        else:
            return None

    def ray_reflection(self, r):
        q = self.ray_intersection(r)
        if q is None:
            return None
        v = r.vec().u()
        n = self.vec().pnormal(v).u()
        direction = v - v.proj(n) * 2
        return Line(q, q + direction)

    def __contains__(self, p):
        return p.line_dist(self) < 0.00001

    def len(self):
        return self.vec().n()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'L({}, {})'.format(self.a, self.b)


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def show(self):
        # beginShape()
        # vertex(self.a.x, self.a.y, self.a.z)
        # vertex(self.b.x, self.b.y, self.b.z)
        # vertex(self.c.x, self.c.y, self.c.z)
        # vertex(self.a.x, self.a.y, self.a.z)
        # endShape()
        raise NotImplementedError()

    def normal(self):
        return (self.b - self.a).cross(self.c - self.a)

    def ray_intersection(self, r):
        n = self.normal()
        rv = r.vec()
        num = (self.a - r.a).dot(n)
        den = rv.dot(n)
        if den == 0:
            if num == 0:
                d = 0
            else:
                return None
        else:
            d = num / den
        i = r.a + rv * d
        if rv.dot(i - r.a) > 0 and i in self:
            return i
        else:
            return None

    def ray_reflection(self, r):
        q = self.ray_intersection(r)
        if q is None:
            return None
        v = r.vec().u()
        n = self.normal().u()
        direction = v - v.proj(n) * 2
        return Line(q, q + direction)

    def __contains__(self, p):
        return p.triangle_dist(self) < 0.00001

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'T({}, {}, {})'.format(self.a, self.b, self.c)


class Quad:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.ta = Triangle(self.a, self.b, self.c)
        self.tb = Triangle(self.a, self.c, self.d)

    def show(self):
        # beginShape()
        # vertex(self.a.x, self.a.y, self.a.z)
        # vertex(self.b.x, self.b.y, self.b.z)
        # vertex(self.c.x, self.c.y, self.c.z)
        # vertex(self.d.x, self.d.y, self.d.z)
        # vertex(self.a.x, self.a.y, self.a.z)
        # endShape()
        raise NotImplementedError()

    def normal(self):
        return self.ta.normal()

    def ray_intersection(self, r):
        return self.ta.ray_intersection(r) or self.tb.ray_intersection(r)

    def ray_reflection(self, r):
        return self.ta.ray_reflection(r) or self.tb.ray_reflection(r)

    def __contains__(self, p):
        return p in self.ta or p in self.tb

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'R({}, {}, {}, {})'.format(self.a, self.b, self.c, self.d)


class Vec:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def show(self, p):
        # line(p.x, p.y, p.z, p.x + self.x, p.y + self.y, p.z + self.z)
        raise NotImplementedError()

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        return Vec(self.y * v.z - self.z * v.y,
                   self.z * v.x - self.x * v.z,
                   self.x * v.y - self.y * v.x)

    def det(self, v):
        # equivalent to self.cross(v).n() but avoids a square root
        return sqrt(self.n2() * v.n2() - self.dot(v) ** 2)

    def n(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def n2(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def pnormal(self, pv):
        # normal to this vector in the same plane as pv
        c = self.cross(pv)
        return self.cross(c)

    def __truediv__(self, f):
        if f == 0:
            return Vec(0, 0, 0)
        return Vec(self.x / f, self.y / f, self.z / f)

    def __mul__(self, f):
        return Vec(self.x * f, self.y * f, self.z * f)

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y, self.z - v.z)

    def __neg__(self):
        return Vec(-self.x, -self.y, -self.z)

    def u(self):
        return self / self.n()

    def proj(self, v):
        return v * self.dot(v) / v.n2()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'V({}, {}, {})'.format(self.x, self.y, self.z)


class Sphere:
    def __init__(self, c, r):
        self.c = c
        self.r = r

    def show(self):
        # pushMatrix()
        # pushStyle()
        # noFill()
        # translate(self.c.x, self.c.y, self.c.z)
        # sphere(self.r)
        # popStyle()
        # popMatrix()
        # self.c.show()
        raise NotImplementedError()

    def ray_intersection(self, l):
        p = self.c.lproj(l)
        d = p.dist(self.c)
        if self.r < d:
            return None
        else:
            offset = sqrt(self.r * self.r - d * d)
            u = (p - l.a).u()
            intersections = (p + u * offset, p + -u * offset)
            q = min(intersections, key=lambda i: i.dist(l.a))
            return q

    def ray_reflection(self, r):
        q = self.ray_intersection(r)
        if q is None:
            return None
        v = r.vec().u()
        n = (q - self.c).u()
        direction = v - v.proj(n) * 2
        reflection = Line(q, q + direction)
        return reflection


def make_box(w, h, d, c, f=True):
    wo = Vec(w, 0, 0)
    ho = Vec(0, h, 0)
    do = Vec(0, 0, d)
    result = [
        Quad(c, c + wo, c + wo + ho, c + ho),  # back
        Quad(c + wo, c + wo + ho, c + wo + ho + do, c + wo + do),  # right
        Quad(c, c + ho, c + ho + do, c + do),  # left
        Quad(c, c + do, c + wo + do, c + wo),  # top,
        Quad(c + ho, c + ho + do, c + wo + ho + do, c + wo + ho)  # bottom
    ]
    if f:
        result.append(Quad(c + do, c + wo + do, c + wo + ho + do, c + ho + do))
    return result


def profile_room(room, speaker, microphone, samples=1000, bounces=10, max_delay=1000, speed_of_sound=343, decay=0.1,
                 base_impulse=1000, sample_rate=44100):
    hits = []
    i_speed_of_sound = 1.0 / speed_of_sound

    for _ in tqdm(range(samples)):
        u = (random() - 0.5) * 2
        t = random() * pi * 2

        # spherical point sampling is actually nontrivial; https://mathworld.wolfram.com/SpherePointPicking.html
        x = sqrt(1 - u ** 2) * cos(t)
        y = sqrt(1 - u ** 2) * sin(t)
        z = u
        p = Point(x, y, z)

        r = Line(speaker, speaker + p)

        last_target = None

        distance_traveled = 0
        for n in range(bounces):
            if distance_traveled * i_speed_of_sound > max_delay:
                break

            closest_intersection = None
            closest_intersection_target = None
            for obj in room:
                if obj is not last_target:
                    intersection = obj.ray_intersection(r)
                    if closest_intersection is None or intersection is not None and r.a.dist(intersection) < r.a.dist(
                            closest_intersection):
                        closest_intersection = intersection
                        closest_intersection_target = obj

            if closest_intersection is None:
                break

            intersection_dist = r.a.dist(closest_intersection)
            distance_traveled += intersection_dist
            last_target = closest_intersection_target

            hit = microphone.ray_intersection(r)
            if hit is not None:
                hit_dist = r.a.dist(hit)
                if hit_dist <= intersection_dist:
                    hits.append((n, hit_dist + distance_traveled))

            r = closest_intersection_target.ray_reflection(r)

    sample_timings = [round(sample_rate * d * i_speed_of_sound) for _, d in hits]
    energies = [base_impulse / (d + 1) ** 2 * (1 - decay) ** b for b, d in hits]
    kernel = [0] * (max(sample_timings) + 1)
    for timing, energy in sorted(zip(sample_timings, energies)):
        kernel[timing] += energy
    max_k = max(kernel)
    kernel = [k / max_k for k in kernel]
    return kernel
