from math import *


def distance(point_a, point_b):
    return int(sqrt(pow((point_a.x - point_b.x), 2) + pow((point_a.y - point_b.y), 2)))


def draw_line(point_a, point_b, canvas, **kwargs):
    return canvas.create_line(point_a.x,  point_a.y, point_b.x, point_b.y, **kwargs)


def getangle(point, event):
    dx = event.x - point.x
    dy = event.y - point.y
    return atan2(dy, dx)


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __call__(self, rad, center):
        _x = (self.x-center.x)*cos(rad) - (self.y-center.y)*sin(rad) + center.x
        _y = (self.x-center.x)*sin(rad) + (self.y-center.y)*cos(rad) + center.y

        return Point(_x, _y)

class RegularPolygon:

    def __init__(self, n_sides, bbox, start):
        self.center = start
        self.num_sides = int(n_sides)
        self.s_len = 2 * (bbox / 2) * sin(pi / self.num_sides)
        self.apo = self.s_len / (2 * tan(pi / self.num_sides))
        self.points = [Point(self.center.x - self.s_len // 2, self.center.y - self.apo)]
        self.make_points()
        self.lines = []
        self.make_lines()


    def __call__(self, canvas, rad, **kwargs):
        self.points = [p(rad, self.center) for p in self.points]
        self.lines = []
        self.make_lines()
        canvas.delete(self._id)
        self._id = canvas.create_polygon(*self.lines,**kwargs)
        return self._id, self

    def make_points(self):
        _angle = 2 * pi    / self.num_sides
        for pdx in range(self.num_sides):
            angle = _angle * pdx
            _x = cos(angle) * self.s_len
            _y = sin(angle) * self.s_len
            self.points.append(self.points[-1] + Point(_x, _y))


    def make_lines(self):
        for p0, p1 in zip(self.points[:-1], self.points[1:]):
            self.lines.append((*p0, *p1))

    
    def draw(self, canvas, **kwargs):
        self._id = canvas.create_polygon(*self.lines, **kwargs)
        return self._id, self
