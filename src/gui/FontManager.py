#self.font = loader.loadFont(resourceManager.getResource('fonts/gnu-freefont_freesans/FreeSans.ttf'))

#lucrezia imports
from gui.AssetListManager import AssetListManager

class FontManager(AssetListManager):

    @staticmethod
    def load():
        """
        used to invoke autoload when needed,
        loads only once
        """
        if not FontManager.isLoaded:
            FontManager.isLoaded = True

        if debug:
            print("FontManager: loading all fonts...")

        FontManager.add("FreeSans", loader.loadFont(resourceManager.getResource('fonts/gnu-freefont_freesans/FreeSans.ttf')))