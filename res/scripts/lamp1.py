lamp = pGrid.getObjectById("lamp1")
lamp.toggle()
audioManager.playEffect("sfx/light_switch.ogg")
persistence.save("camera_lamp1_ison", lamp.on)
