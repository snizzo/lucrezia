from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, TransparencyAttrib
from panda3d.core import Point3, Vec4

from geometries.PrimitiveArrow import PrimitiveArrow

class GizmoPos():
    def __init__(self, size=1.0, method="load"):
        Primitive.__init__(self, size, method)

    def load(self):
        """
        Load model file.
        """
        self.node_path = loader.loadModel("geometries/models/arrow.bam")
        self.node_path.setScale(self.size, self.size, self.size)

    def create(self):
        """
        Programmatically create a arrow primitive.
        """
        print("WARNING: PrimitiveArrow.create() not implemented yet!")