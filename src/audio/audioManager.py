from direct.showbase.DirectObject import DirectObject

class AudioManager(DirectObject):
    def __init__ (self):
        #for bgmusic
        self.isPlaying = False
        self.mySound = False
        
        #for long effects
        self.effects = []
        
    #apicall
    def playMusic(self, bgmusic):
        if(self.isPlaying):
            self.mySound.stop()
        path = resourceManager.getResource(bgmusic)
        self.mySound = base.loader.loadSfx(path)
        self.mySound.setVolume(1)
        self.mySound.setLoop(True)
        self.mySound.play()
        self.isPlaying = True
    
    def stopMusic(self):
        if(self.isPlaying):
            self.mySound.stop()
    
    #apicall
    def playEffect(self, effect):
        path = resourceManager.getResource(effect)
        effect = base.loader.loadSfx(path)
        effect.setVolume(1)
        effect.play()
        
    #apicall
    #name unused: fix this
    def playLongEffect(self, name, effect):
        path = resourceManager.getResource(effect)
        effect = base.loader.loadSfx(path)
        effect.setVolume(1)
        effect.setLoop(True)
        self.effects.append(effect)
        effect.play()
    
    #apicall
    def clearAllEffects(self):
        for e in self.effects[:]:
            e.stop()
            self.effects.remove(e)
    
