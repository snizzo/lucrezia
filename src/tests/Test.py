"""
Empty test to be subclassed by other tests
"""

from direct.showbase.DirectObject import DirectObject

class Test(DirectObject):
    def __init__(self):
        print(__class__.__name__)