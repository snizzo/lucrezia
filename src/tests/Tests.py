"""
Class used to run singular tests for specific features.
"""

import importlib
import inspect
import os

testPath = "src/tests/"

class Tests():
    def __init__(self):
        self.modules = {} # dict of modules containing tests

    def autoImport(self):
        """
        Automatically import all tests in src/tests/ and populate the self.modules dict
        """

        # get all files in src/tests/
        files = os.listdir(testPath)

        # for each file
        for file in files:
            # if it's a python file
            if file.endswith(".py"):
                classname = file[:-3]
                # import it
                module = importlib.import_module("tests." + file[:-3])

                # add test class to modules dict
                self.modules[classname] = module
    
    def listTests(self):
        """
        List all tests in src/tests/
        """

        print("Tests:")
        
        for test in self.modules:
            
            #don't print Test class
            if test == "Test" or test == "Tests":
                continue

            #remove Test prefix
            if test.startswith("Test"):
                print(" - " + test[4:])

    def runTest(self, name):
        """
        Run a test with the given name

        Args:
            name (str): name of the test to run
        """
        
        print("Running test: " + name)

        if self.modules.get(name) is not None:
            module = self.modules[name]
            obj = module.__dict__[name]()
        elif self.modules.get("Test" + name) is not None:
            module = self.modules["Test" + name]
            obj = module.__dict__["Test" + name]()
        else:
            print("Test not found!")
        
        print("Test done!")