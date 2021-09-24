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


class SwitchHole(fcp.Sketch):
    def __init__(self, body, support, face):
        global holeIdx
        holeIdx += 1
        super().__init__('SwitchHole' + str(holeIdx), body, support)
        # Pick the edge that's opposite of face.Edges[0]
        secondFaceEdgeIdx = 1
        while face.Edges[0].distToShape(face.Edges[secondFaceEdgeIdx]) == 0:
            secondFaceEdgeIdx += 1
        # Find indexes of the two opposing face edges in the list of edges of
        # the entire body
        externalIdxs = [findEdgeIdx(face.Edges[0], body.Shape.Edges),
                        findEdgeIdx(face.Edges[secondFaceEdgeIdx], body.Shape.Edges)]

        # Let's carefully choose which of the endpoints in the second external
        # edge we are going to use for constraints. We want to pick the one
        # that's farthest from the starting point of the first edge. I.e., we
        # want to make sure that the external vertices we are going to use in
        # constraints lie on a diagonal of the rectangle that's the wire of the
        # face in which we are punching a hole
        firstEdgeStartPoint = face.Edges[0].firstVertex()
        secondEdgeStartPoint = face.Edges[secondFaceEdgeIdx].firstVertex()
        secondEdgeEndPoint = face.Edges[secondFaceEdgeIdx].lastVertex()
        secondFaceEdgeVertexSel = fcp.START_POINT
        if firstEdgeStartPoint.distToShape(secondEdgeEndPoint) > firstEdgeStartPoint.distToShape(secondEdgeStartPoint):
            secondFaceEdgeVertexSel = fcp.END_POINT

        # Import them
        externals = [self.addE(body, 'Edge' + str(i + 1))
                     for i in externalIdxs]
        e1 = self.addG(
            fcp.Line(-100, -100, 100, -100),
            construction=False)
        e2 = self.addG(
            fcp.Line(100, -100, 100, 100),
            construction=False,
            constraints=[
                fcp.Coincident(e1, fcp.END_POINT,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Perpendicular(e1, fcp.CURRENT),
                fcp.Equal(e1, fcp.CURRENT)
            ])
        e3 = self.addG(
            fcp.Line(100, 100, -100, 100),
            construction=False,
            constraints=[
                fcp.Coincident(e2, fcp.END_POINT,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Perpendicular(e2, fcp.CURRENT),
                fcp.Equal(e2, fcp.CURRENT)
            ])
        e4 = self.addG(
            fcp.Line(-100, 100, -100, -100),
            construction=False,
            constraints=[
                fcp.Coincident(e3, fcp.END_POINT,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Coincident(fcp.CURRENT, fcp.END_POINT,
                               e1, fcp.START_POINT),
                fcp.Distance(fcp.CURRENT, 14)
            ])
        print("externals=%s" % (str(externals)))
        diag1 = self.addG(
            fcp.Line(-1, -1, 0, 0),
            construction=True,
            constraints=[
                fcp.Coincident(externals[0], fcp.START_POINT,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Coincident(e1, fcp.START_POINT,
                               fcp.CURRENT, fcp.END_POINT)
            ])
        diag2 = self.addG(
            fcp.Line(2, 2, 1, 1),
            construction=True,
            constraints=[
                fcp.Coincident(externals[1], secondFaceEdgeVertexSel,
                               fcp.CURRENT, fcp.START_POINT),
                fcp.Coincident(e3, fcp.START_POINT,
                               fcp.CURRENT, fcp.END_POINT),
                fcp.PointOnObject(e1, fcp.START_POINT, fcp.CURRENT),
                fcp.Equal(diag1, fcp.CURRENT),
                fcp.Parallel(diag1, fcp.CURRENT)
            ])


def punchHole(body, face):
    print(face)
    faceIdx = 0
    while body.Shape.Faces[faceIdx].CenterOfMass != face.CenterOfMass:
        print(faceIdx)
        faceIdx += 1
    support = (body.Tip, ['Face' + str(faceIdx + 1)])
    print(support)
    square = SwitchHole(body, support, face)
    hole = body.newObject('PartDesign::Pocket', square.name + 'Pocket')
    square.sketch.Visibility = False
    hole.Profile = square.sketch
    hole.Length = 5.000000
    hole.Length2 = 100.000000
    hole.Type = 1
    hole.UpToFace = None
    pass


[selectedBody] = Gui.Selection.getCompleteSelection()
keepPunching = True
while keepPunching:
    keepPunching = False
    for f in selectedBody.Shape.Faces:
        print(f)
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
