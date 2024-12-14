import numpy as np
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

if 2*width_offset > y_length:
    width_offset = 0

# creating X and Y points
x_pts = np.linspace(0, x_length, num_points)
y_pts = [0 + width_offset, y_length - width_offset]

amplitudes = []
for x in x_pts:
    curve_pt = amplitude_curves.PointAtNormalizedLength(x/x_length)
    amplitudes.append(curve_pt.Z)

# creating points in rows
pts = []
rows = []
for i, amplitude in enumerate(amplitudes):
    row = []
    for y in y_pts:
        row.append(rs.CreatePoint(x_pts[i], y, amplitude))  # create point
    rows.append(row)  # append row to rows
    pts.extend(row)   # flatten all points for mesh vertices

# creating the main mesh (top face)
mesh = rg.Mesh()
for pt in pts:
    mesh.Vertices.Add(pt.X, pt.Y, pt.Z)

# manually indexing faces
for i in range(len(rows) - 1):
    for j in range(len(rows[i]) - 1):
        p1 = i * len(y_pts) + j
        p2 = p1 + 1
        p3 = p1 + len(y_pts)
        p4 = p3 + 1
        mesh.Faces.AddFace(p1, p2, p4, p3)

# adding walls on each side
# left wall
for i in range(len(rows) - 1):
    base_p1 = rs.CreatePoint(x_pts[i], y_pts[0], 0)
    base_p2 = rs.CreatePoint(x_pts[i + 1], y_pts[0], 0)
    top_p1 = rows[i][0]
    top_p2 = rows[i + 1][0]

    # creting wall quads
    mesh.Vertices.Add(base_p1.X, base_p1.Y, base_p1.Z)
    mesh.Vertices.Add(base_p2.X, base_p2.Y, base_p2.Z)
    mesh.Vertices.Add(top_p2.X, top_p2.Y, top_p2.Z)
    mesh.Vertices.Add(top_p1.X, top_p1.Y, top_p1.Z)
    mesh.Faces.AddFace(len(mesh.Vertices) - 4, len(mesh.Vertices) - 3, len(mesh.Vertices) - 2, len(mesh.Vertices) - 1)

# right wall
for i in range(len(rows) - 1):
    base_p1 = rs.CreatePoint(x_pts[i], y_pts[1], 0)
    base_p2 = rs.CreatePoint(x_pts[i + 1], y_pts[1], 0)
    top_p1 = rows[i][1]
    top_p2 = rows[i + 1][1]

    # creating wall quads
    mesh.Vertices.Add(base_p1.X, base_p1.Y, base_p1.Z)
    mesh.Vertices.Add(base_p2.X, base_p2.Y, base_p2.Z)
    mesh.Vertices.Add(top_p2.X, top_p2.Y, top_p2.Z)
    mesh.Vertices.Add(top_p1.X, top_p1.Y, top_p1.Z)
    mesh.Faces.AddFace(len(mesh.Vertices) - 4, len(mesh.Vertices) - 3, len(mesh.Vertices) - 2, len(mesh.Vertices) - 1)

# front and back walls
p1 = rs.CreatePoint(x_pts[0], y_pts[0],0)
p2 = rs.CreatePoint(x_pts[0], y_pts[0],amplitudes[0])
p3 = rs.CreatePoint(x_pts[0], y_pts[1],amplitudes[0])
p4 = rs.CreatePoint(x_pts[0], y_pts[1],0)
mesh.Vertices.Add(p1)
mesh.Vertices.Add(p2)
mesh.Vertices.Add(p3)
mesh.Vertices.Add(p4)
mesh.Faces.AddFace(len(mesh.Vertices) - 4, len(mesh.Vertices) - 3, len(mesh.Vertices) - 2, len(mesh.Vertices) - 1)

p1 = rs.CreatePoint(x_pts[-1], y_pts[-1],0)
p2 = rs.CreatePoint(x_pts[-1], y_pts[-1],amplitudes[-1])
p3 = rs.CreatePoint(x_pts[-1], y_pts[-2],amplitudes[-1])
p4 = rs.CreatePoint(x_pts[-1], y_pts[-2],0)
mesh.Vertices.Add(p1)
mesh.Vertices.Add(p2)
mesh.Vertices.Add(p3)
mesh.Vertices.Add(p4)
mesh.Faces.AddFace(len(mesh.Vertices) - 4, len(mesh.Vertices) - 3, len(mesh.Vertices) - 2, len(mesh.Vertices) - 1)

# base face
p1 = rs.CreatePoint(x_pts[0], y_pts[0],0)
p2 = rs.CreatePoint(x_pts[-1], y_pts[0],0)
p3 = rs.CreatePoint(x_pts[-1], y_pts[-1],0)
p4 = rs.CreatePoint(x_pts[0], y_pts[-1],0)
mesh.Vertices.Add(p1)
mesh.Vertices.Add(p2)
mesh.Vertices.Add(p3)
mesh.Vertices.Add(p4)
mesh.Faces.AddFace(len(mesh.Vertices) - 4, len(mesh.Vertices) - 3, len(mesh.Vertices) - 2, len(mesh.Vertices) - 1)