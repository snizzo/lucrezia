"""
Empty test to be subclassed by other tests

Can be used to accept events and other common tasks
"""

from direct.showbase.DirectObject import DirectObject

class Test(DirectObject):
    def __init__(self):
        print(__class__.__name__)