lear = pGrid.getObjectById('mainplayer')
lear.setPlayable(False)
baloons.push('Lear', 'Eccoti finalmente!', 'mainplayer')
baloons.push('Lear', 'È un\'ora che ti cerco.', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
customCamera.moveCameraAtObject(luna)
###pause
baloons.push('Luna', 'Non sapevo dove altro andare.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraAtObject(lear)
###pause
lear = pGrid.getObjectById('mainplayer')
baloons.push('Lear', 'Ti stanno aspettando i dottori!', 'mainplayer')
lear.setPlayable(True)
