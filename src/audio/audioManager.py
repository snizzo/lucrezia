from direct.showbase.DirectObject import DirectObject

class AudioManager(DirectObject):
    def __init__ (self):
    
        self.effects = []
        # presa in input una stringa, l'audio manager va a ricercare il path assoluto del file e riproduce la musica di background
    def playMusic(self, bgmusic):
        path = resourceManager.getResource(bgmusic)
        self.mySound = base.loader.loadSfx(path)
        self.mySound.setVolume(1)
        self.mySound.setLoop(True)
        self.mySound.play()
        print path
    """
    # preso in input un vettore, l'audio manager va a cercare il path assoluto del file e riproduce il o gli effetti sonori
    def playEffect(self, effect):
        path = resourceManager.getResource(effect)
        effect = base.loader.loadSfx(path)
        effect.setVolume(1)
        self.effect.append(effect)
        effect.play()
        print path"""