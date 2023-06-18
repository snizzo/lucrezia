from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, TransparencyAttrib
from panda3d.core import Point3, Vec4

from geometries.Primitive import Primitive


class PrimitiveSphere(Primitive):
    def __init__(self, size=1.0, method="load"):
        Primitive.__init__(self, size, method)

    def load(self):
        """
        Load a box from a model file.
        """
        self.node_path = loader.loadModel("geometries/models/sphere.bam")
        self.node_path.setScale(self.size, self.size, self.size)

    def create(self):
        """
        Programmatically create a sphere primitive.
        """
        print("WARNING: PrimitiveSphere.create() not implemented yet!")