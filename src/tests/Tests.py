"""
Class used to run singular tests for specific features.
"""

import importlib
import inspect
import os

from tests.TestDynamicLoading import TestDynamicLoading
from tests.TestPrimitiveBox import TestPrimitiveBox

testPath = "src/tests/"

class Tests():
    def __init__(self):
        pass

    @staticmethod
    def printRunning(name):
        print("Running test: " + name + "...")
    
    @staticmethod
    def printDone(name):
        print("Test " + name + " done!")

    @staticmethod
    def runTest(name):
        """
        Run a test with the given name

        Args:
            name (str): name of the test to run, case insensitive
        """

        # case insensitive
        name = name.lower()

        Tests.printRunning(name)

        #lists of supported tests
        if name == "dynamicloading":
            t = TestDynamicLoading()
        elif name == "primitivebox":
            t = TestPrimitiveBox()
        elif name == "emptytest":
            print("Running empty test...")
        else:
            print("Test not found!")
        
        Tests.printDone(name)