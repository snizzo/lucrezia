import os

'''
Handles the retrieval of resources correct filepaths
'''
class ResourceManager:
    def __init__(self, resource_folder="res") -> None:
        self.resources = []
        self.path = os.getcwd()
        self.setResourceFolder(resource_folder)
    
    def setResourceFolder(self, folder):
        """
        Sets a custom resource folder path.

        Args:
            folder: resource folder name
        """
        self.resource_folder = folder

    def get_path(self):
        """
        Returns the current resource directory absolute path
        """
        return self.path + "/" + self.resource_folder + "/"
    
    def getResource(self, key):
        """
        Returns the full resource path for the given key

        Args:
            key: filename of the resource
        """
        object_path = self.path + "/" + self.resource_folder + "/" + key
        return object_path
