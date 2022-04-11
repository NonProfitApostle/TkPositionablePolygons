from math import *

#distance bbetween 2 points.
def distance(point_a, point_b):
    return int(sqrt(pow((point_a.x - point_b.x), 2) + pow((point_a.y - point_b.y), 2)))

#this used to be on the Point class but moved off
def draw_line(point_a, point_b, canvas, **kwargs):
    return canvas.create_line(point_a.x,  point_a.y, point_b.x, point_b.y, **kwargs)

#angle between 2 points
def getangle(point, event):
    dx = event.x - point.x
    dy = event.y - point.y
    return atan2(dy, dx)


#base (x,y) class for arithmetic
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    #returns a Point rotated around center by a rad(radians)
    def __call__(self, rad, center):
        _x = (self.x-center.x)*cos(rad) - (self.y-center.y)*sin(rad) + center.x
        _y = (self.x-center.x)*sin(rad) + (self.y-center.y)*cos(rad) + center.y

        return Point(_x, _y)

    
#generates a n_sided Regular Polygon in bbox area, stores initial center for later rotation
class RegularPolygon:

    def __init__(self, n_sides, bbox, start):
        
        #initial click point
        self.center = start
        
        #number f sides on the polygon
        self.num_sides = int(n_sides)
        
        #length of each side of a regular polygon with n_sides and bbox area
        self.s_len = 2 * (bbox / 2) * sin(pi / self.num_sides)
        
        #apotem
        self.apo = self.s_len / (2 * tan(pi / self.num_sides))
        
        #stored point reference for later rotation
        self.points = [Point(self.center.x - self.s_len // 2, self.center.y - self.apo)]
        
        #find the x,y points of the polygon vertices
        self.make_points()
        self.lines = []
        
        #populate the point sequence for create_polygon
        self.make_lines()

        
    #deletes and redraws the polygon on supplied tk.canvas
    def __call__(self, canvas, rad, **kwargs):
        
        #call each Point object in the vertices to get the newly rotated points
        self.points = [p(rad, self.center) for p in self.points]
        
        #delete the old lines
        self.lines = []
        
        #regenerate the line sequence with the new points
        self.make_lines()
        
        #clear the container of former shapes
        canvas.delete(self._id)
        
        #generate the new CanvasId
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
