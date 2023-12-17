from abc import ABC, abstractmethod


class Primitive(ABC):
    def __init__(self, size=1.0, method="load"):
        """
        Args:
            method: can be have different values to describe the method used to generate the shape
                "programmatic": shape is defined inside the class and generated via cpu at runtime
                "load":         shape is predefined in the .bam file and loaded later as a 3d model
        """
        self.size = size
        self.node_path = None

        if method == "programmatic":
            self.create()
        elif method == "load":
            self.load()
    
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def create(self):
        pass

    def isLoadedCheck(self):
        if self.node_path is None:
            print("WARNING: Primitive not loaded!")
            return False
        else:
            return True

    def setPosition(self, x, y, z):
        if not self.isLoadedCheck():
            return
        self.node_path.setPos(x, y, z)

    def setScale(self, scale_x, scale_y, scale_z):
        if not self.isLoadedCheck():
            return
        self.node_path.setScale(scale_x, scale_y, scale_z)

    def setColor(self, r, g, b, a=1.0):
        if not self.isLoadedCheck():
            return
        self.node_path.setColor(r, g, b, a)
    
    def setShader(self, shader):
        if not self.isLoadedCheck():
            return
        self.node_path.setShader(shader)

    #enable per pixel lightning
    def setPPL(self, ppl=True):
        if not self.isLoadedCheck():
            return
        self.node_path.setShaderAuto() if ppl else self.node_path.clearShader()
    
    def setWireframe(self, wireframe=True):
        if not self.isLoadedCheck():
            return
        self.node_path.setRenderModeWireframe() if wireframe else self.node_path.setRenderModeFilled()