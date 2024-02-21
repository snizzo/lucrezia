
class AssetListManager:
    '''
    Static class used to manage a dictionary of assets, such as fonts, color codes, etc... using a key-value system.
    
    Can be subclassed to add more specific assets like colors or fonts.
    '''

    isLoaded = False
    assets = {}

    @staticmethod
    def load():
        pass

    @staticmethod
    def add(key, value):
        AssetListManager.assets[key] = value

    @staticmethod
    def get(key):

        if key not in AssetListManager.assets:
            print("AssetListManager: key not found: " + key)
            return None

        return AssetListManager.assets[key]
    
    @staticmethod
    def getAll():
        return AssetListManager.assets.keys()

AssetListManager.load()