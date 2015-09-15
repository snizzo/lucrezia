'''
PERSISTENCE HELP:
cameraState handles all the camera possible states
1: fresh new game
2: kate has talked to ellen
'''

#set the very first state to the camera
if persistence.load("cameraState") == False:
    persistence.save("cameraState", 1)

if persistence.load("cameraState") == 1:
    pGrid.getObjectById("lamp1").setOff()
    
    audioManager.playLongEffect('alarm', 'sfx/alarm_clock.ogg')
    
    baloons.push('Ellen', 'UGH!', 'ellen')
    baloons.push('Ellen', 'Non sopporto più questa merdosa sveglia.', 'ellen')
    baloons.push('Ellen', 'Meglio se accendo le luci.', 'ellen')
    
    persistence.save('lampCameraState', 2)
    ###pause
    
    
