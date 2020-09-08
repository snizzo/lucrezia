'''
PERSISTENCE HELP:
cameraState handles all the camera possible states
1: normal
2: need to switch off alarm clock
'''

lamp = pGrid.getObjectById("lamp1")
minilamp = pGrid.getObjectById("minilamp")
lamp.toggle()
minilamp.toggle()
audioManager.playEffect("sfx/light_switch.ogg")
persistence.save("camera_lamp1_ison", lamp.on)


