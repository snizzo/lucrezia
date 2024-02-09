
# copy paste imports from main.py
#panda imports
from direct.filter.FilterManager import FilterManager
from panda3d.core import Shader

#libs imports

from tests.Test import Test



class TestFullscreenBloomShader(Test):
    def __init__(self):
        Test.__init__(self)

        self.panda = loader.loadModel("models/panda")
        self.panda.reparentTo(render)
        self.panda.setPos(0, 10, 0)
        # Create a filter manager to handle the fullscreen quad
        self.manager = FilterManager(base.win, base.cam)
        # Load a shader from a file and assign it to the quad
        self.shader = Shader.load(Shader.SL_GLSL, "shaders/bloom_fullscreen.glsl")
        self.quad = self.manager.renderSceneInto(colortex=self.manager.makeTexture())
        self.quad.setShader(self.shader)