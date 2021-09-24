import FreeCAD as App
import Part
import sys
import Sketcher


class Constant(object):
    def __init__(self, _underlying):
        self._underlying = _underlying

    def toUnderlying(self):
        return self._underlying


# Which point of an edge does a constraint refer to
ENTIRETY = Constant(0)
START_POINT = Constant(1)
END_POINT = Constant(2)
CENTER = Constant(3)

CURRENT = Constant(sys.maxsize)
X_AXIS = Constant(-1)
Y_AXIS = Constant(-2)


class Sketch(object):
    def __init__(self, name, body, support):
        self.name = name
        self.external_counter = -2
        print(body)
        self.sketch = body.newObject('Sketcher::SketchObject', name)
        self.sketch.Support = support
        self.sketch.MapMode = 'FlatFace'

    def addG(self, geometry, construction, constraints=[]):
        handle = self.sketch.addGeometry(geometry, construction)
        for c in constraints:
            self.addC(c, handle)
        return handle

    def addC(self, constraint, current_handle=None):
        if current_handle is not None:
            constraint = [current_handle if c == CURRENT else c
                          for c in constraint]
        constraint = [c.toUnderlying() if isinstance(c, Constant) else c
                      for c in constraint]
        self.sketch.addConstraint(Sketcher.Constraint(*constraint))

    def addE(self, external_sketch, edge):
        self.sketch.addExternal(external_sketch.Tip.Name, edge)
        self.external_counter -= 1
        return self.external_counter


def Line(x1, y1, x2, y2):
    return Part.LineSegment(App.Vector(x1, y1, 0), App.Vector(x2, y2, 0))


def Arc(centerX, centerY, radius, startRadians, endRadians):
    return Part.ArcOfCircle(
        Part.Circle(App.Vector(centerX, centerY, 0),
                    App.Vector(0, 0, 1),
                    radius),
        startRadians, endRadians)


class Constraint(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        print(args)
        return [self.name] + list(args)


Coincident = Constraint('Coincident')
Vertical = Constraint('Vertical')
Horizontal = Constraint('Horizontal')
Distance = Constraint('Distance')
DistanceY = Constraint('DistanceY')
DistanceX = Constraint('DistanceX')
Tangent = Constraint('Tangent')
Equal = Constraint('Equal')
PointOnObject = Constraint('PointOnObject')
Perpendicular = Constraint('Perpendicular')
Parallel = Constraint('Parallel')
