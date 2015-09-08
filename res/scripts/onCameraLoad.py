lamp = pGrid.getObjectById("lamp1")
if persistence.load("camera_lamp1_ison") == True:
    lamp.setOn()
    
audioManager.playLongEffect('rain', 'sfx/rain_indoor.ogg')
