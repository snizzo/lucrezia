from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, TransparencyAttrib
from panda3d.core import Point3, Vec4


class PrimitiveBox:
    def __init__(self, size=1.0):
        self.size = size
        self.node_path = None

    def createBox(self):
        # Create vertex data format
        format_obj = GeomVertexFormat.get_v3n3c4()

        # Create vertex data container
        vdata = GeomVertexData("cube_data", format_obj, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")

        # Define vertices of the cube
        vertices = [
            Point3(-self.size, -self.size, self.size),
            Point3(self.size, -self.size, self.size),
            Point3(self.size, self.size, self.size),
            Point3(-self.size, self.size, self.size),
            Point3(-self.size, -self.size, -self.size),
            Point3(self.size, -self.size, -self.size),
            Point3(self.size, self.size, -self.size),
            Point3(-self.size, self.size, -self.size)
        ]

        # Define the cube's normals
        normals = [
            Vec4(0, 0, 1, 0),
            Vec4(1, 0, 0, 0),
            Vec4(0, 0, -1, 0),
            Vec4(-1, 0, 0, 0),
            Vec4(0, 1, 0, 0),
            Vec4(0, -1, 0, 0)
        ]

        # Define the cube's colors
        colors = [
            Vec4(1, 0, 0, 1),  # Red
            Vec4(0, 1, 0, 1),  # Green
            Vec4(0, 0, 1, 1),  # Blue
            Vec4(1, 1, 0, 1),  # Yellow
            Vec4(1, 0, 1, 1),  # Magenta
            Vec4(0, 1, 1, 1)   # Cyan
        ]

        # Define the cube's faces
        faces = [
            # Front face
            (0, 1, 2),
            (2, 3, 0),
            # Right face
            (1, 5, 6),
            (6, 2, 1),
            # Back face
            (7, 6, 5),
            (5, 4, 7),
            # Left face
            (4, 0, 3),
            (3, 7, 4),
            # Top face
            (3, 2, 6),
            (6, 7, 3),
            # Bottom face
            (4, 5, 1),
            (1, 0, 4)
        ]

        # Add vertices, normals, and colors to the vertex data
        for i, vertex_pos in enumerate(vertices):
            vertex.addData3f(vertex_pos)
        for i, vertex_pos in enumerate(normals):
            normal.addData4f(normals[i])
        for i, vertex_pos in enumerate(colors):
            color.addData4f(colors[i % len(colors)])

        # Create the geometry
        geom = Geom(vdata)

        # Create triangles for each face
        for face in faces:
            primitive = GeomTriangles(Geom.UHStatic)
            primitive.addVertices(*face)
            primitive.closePrimitive()
            geom.addPrimitive(primitive)

        # Create the geometry node and attach the geometry
        geom_node = GeomNode("box_geom")
        geom_node.addGeom(geom)

        # Create the node path
        self.node_path = NodePath(geom_node)

    def setPosition(self, x, y, z):
        self.node_path.setPos(x, y, z)

    def setScale(self, scale_x, scale_y, scale_z):
        self.node_path.setScale(scale_x, scale_y, scale_z)

    def setColor(self, r, g, b, a=1.0):
        self.node_path.setColorScale(r, g, b, a)