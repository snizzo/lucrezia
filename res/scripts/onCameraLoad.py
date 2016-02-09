'''
PERSISTENCE HELP:
'''

#set the very first state to the camera
if persistence.load("gameState") == False:
    persistence.save("gameState", 1)

if persistence.load("gameState") == 1:
    pGrid.getObjectById("lamp1").setOff()
    pGrid.getObjectById("minilamp").setOff()
    
    audioManager.playLongEffect('alarm', 'sfx/alarm_clock.ogg')
    
    baloons.push('Ellen', 'UGH!', 'ellen')
    baloons.push('Ellen', 'Non sopporto più questa sveglia.', 'ellen')
    baloons.push('Ellen', 'Meglio se accendo le luci.', 'ellen')
    
    persistence.save('gameState', 2)
    ###pause
    
    
