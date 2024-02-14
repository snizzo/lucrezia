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
    
    def getNode(self):
        '''
        Used to reparent gizmo to other stuff, to move them around
        '''
        return self.node_path

    def reparentTo(self, parent):
        if not self.isLoadedCheck():
            return
        self.node_path.reparentTo(parent)

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

    # TODO: duplicate code of setPosition
    def setPos(self, x, y, z):
        if not self.isLoadedCheck():
            return
        self.node_path.setPos(x, y, z)

    # TODO: duplicate code of setPos
    def setPosition(self, x, y, z):
        if not self.isLoadedCheck():
            return
        self.node_path.setPos(x, y, z)

    def setScale(self, scale_x, scale_y, scale_z):
        if not self.isLoadedCheck():
            return
        self.node_path.setScale(scale_x, scale_y, scale_z)

    #TODO: ugly but functional, maybe improve this?
    def setColor(self, r, g=None, b=None, a=None):
        if not self.isLoadedCheck():
            return

        if isinstance(r, tuple):
            # If r is a tuple, unpack the values
            r, g, b, a = r

        if a is None:
            a = 1.0

        self.node_path.setColor(r, g, b, a)
    
    def setAlpha(self, alpha):
        if not self.isLoadedCheck():
            return
        self.node_path.setTransparency(1)
        self.node_path.setAlphaScale(alpha)
    
    def setShader(self, shader):
        if not self.isLoadedCheck():
            return
        self.node_path.setShader(shader)

    def setVisible(self, visible=True):
        if not self.isLoadedCheck():
            return
        self.node_path.show() if visible else self.node_path.hide()

    #enable per pixel lightning
    def setPPL(self, ppl=False):
        if not self.isLoadedCheck():
            return
        self.node_path.setShaderAuto() if ppl else self.node_path.clearShader()
    
    def setWireframe(self, wireframe=True):
        if not self.isLoadedCheck():
            return
        self.node_path.setRenderModeWireframe() if wireframe else self.node_path.setRenderModeFilled()