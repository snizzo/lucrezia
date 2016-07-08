def macchinadasolaOnEmptyMessages():
    audioManager.stopMusic(0.1)
    audioManager.stopLongEffect('carengine')
    audioManager.playEffect('sfx/caraccident.ogg')
    messenger.send('changeMap', ['incidente.map','20,11'])


audioManager.stopLongEffect('wind')
audioManager.stopLongEffect('birds')
audioManager.playEffect('sfx/closed_door.ogg')
audioManager.playLongEffect('carengine', 'sfx/carengine.ogg')

taskMgr.doMethodLater(5, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Ho bisogno di un buon caffè caldo.","ellen"])
taskMgr.doMethodLater(10, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Perchè non ha mai detto quello che pensava di me sin dall'inizio?","ellen"])
taskMgr.doMethodLater(15, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Pensa che ci stia male solo lei?","ellen"])
taskMgr.doMethodLater(20, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","E poi sarei io l'egocentrica!","ellen"])
taskMgr.doMethodLater(26, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Le sue parole mi hanno attraversato il cuore da parte a parte e ora sento il dolore uscire OVUNQUE.","ellen"])
taskMgr.doMethodLater(27, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Ellen ora basta.","ellen"])
taskMgr.doMethodLater(28, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Smettila di pensare altrimenti diventi paranoica.","ellen"])
taskMgr.doMethodLater(35, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","Devi distrarti.","ellen"])
taskMgr.doMethodLater(40, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","dove ho messo quel cd... doveva essere sotto il sedile... ma qua...","ellen"])
taskMgr.doMethodLater(50, baloons.pushThought, 'selfspeak', extraArgs = ["Ellen","non c'è nulla... meglio dar un occhiata dopo altrimenti rischio un inci... Merda!","ellen"])
#execute them after filling last message 
taskMgr.doMethodLater(51, baloons.setOnEmptyCallback, 'setcallback', extraArgs = [macchinadasolaOnEmptyMessages])
