import FreeCAD as App
import FreeCADGui as Gui
import sys
import importlib

# edit this path
sys.path.append('path/to/this/dir')

import fc_plumbing as fcp
importlib.reload(fcp)

holeIdx = 0


def findEdgeIdx(needle, haystack):
    result = 0
    while needle.CenterOfMass != haystack[result].CenterOfMass:
        result += 1
    return result


def findVertexIdx(needle, haystack):
    result = 0
    while needle.X != haystack[result].X or \
            needle.Y != haystack[result].Y or \
            needle.Z != haystack[result].Z:
        result += 1
    return result


class SwitchHole(fcp.Sketch):
    def __init__(self, body, face):
        global holeIdx
        holeIdx += 1
        support = [(body.Tip, 'Vertex' + str(vIdx + 1)) for vIdx in
                   [findVertexIdx(faceVertex, body.Shape.Vertexes)
                    for faceVertex in face.Vertexes]
                   ]
        super().__init__('SwitchHole' + str(holeIdx), body, support, 'InertialCS')
        e1 = self.addG(
            fcp.Line(-1, -1, -1, 1),
            construction=False,
            constraints=[
                fcp.Vertical(fcp.CURRENT)
            ])
        e2 = self.addG(
            fcp.Line(-1, 1, 1, 1),
            construction=False,
            constraints=[
                fcp.Horizontal(fcp.CURRENT),
                fcp.Coincident(e1, fcp.END_POINT,
                               fcp.CURRENT, fcp.START_POINT),
            ])
        e3 = self.addG(
            fcp.Line(1, 1, 1, -1),
            construction=False,
            constraints=[
                fcp.Vertical(fcp.CURRENT),
                fcp.Coincident(e2, fcp.END_POINT, fcp.CURRENT, fcp.START_POINT)
            ])
        e4 = self.addG(
            fcp.Line(1, -1, -1, -1),
            construction=False,
            constraints=[
                fcp.Horizontal(fcp.CURRENT),
                fcp.Coincident(e3, fcp.END_POINT,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Coincident(e1, fcp.START_POINT, fcp.CURRENT, fcp.END_POINT)
            ])
        self.addC(fcp.Equal(e1, e2))
        self.addC(fcp.Distance(e1, 14))
        self.addC(fcp.Symmetric(e1, fcp.START_POINT, e2, fcp.END_POINT,
                                fcp.X_AXIS, fcp.START_POINT))


def punchHole(body, face):
    faceIdx = 0
    while body.Shape.Faces[faceIdx].CenterOfMass != face.CenterOfMass:
        faceIdx += 1
    square = SwitchHole(body, face)
    hole = body.newObject('PartDesign::Pocket', square.name + 'Pocket')
    square.sketch.Visibility = False
    hole.Profile = square.sketch
    hole.Midplane = 1
    hole.Type = 1
    hole.UpToFace = None


[selectedBody] = Gui.Selection.getCompleteSelection()
keepPunching = True
while keepPunching:
    keepPunching = False
    for f in selectedBody.Shape.Faces:
        # Only punching in faces with exactly 4 edges
        if len(f.Edges) != 4:
            continue
        correctLenEdges = [e for e in f.Edges
                           if e.Length >= 18.0 and e.Length <= 20.0]
        # If those edges are of the expected length
        if len(correctLenEdges) != len(f.Edges):
            continue
        punchHole(selectedBody, f)
        App.ActiveDocument.recompute()
        keepPunching = True
        break
