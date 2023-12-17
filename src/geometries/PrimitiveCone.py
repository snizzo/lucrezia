from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, TransparencyAttrib
from panda3d.core import Point3, Vec4

from geometries.Primitive import Primitive


class PrimitiveCone(Primitive):
    def __init__(self, size=1.0, method="load"):
        Primitive.__init__(self, size, method)

    def load(self):
        """
        Load model file.
        """
        self.node_path = loader.loadModel("geometries/models/cone.bam")
        self.node_path.setScale(self.size, self.size, self.size)

    def create(self):
        """
        Programmatically create a cone primitive.
        """
        print("WARNING: PrimitiveCone.create() not implemented yet!")