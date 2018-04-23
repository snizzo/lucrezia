lear = pGrid.getObjectById('mainplayer')
lear.setCinematic(True)
baloons.push('Lear', 'Eccoti finalmente!', 'mainplayer')
baloons.push('Lear', 'È un\'ora che ti cerco.', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 1)
lear.npc_push_walk("left", 2)
lear.npc_push_walk("up", 2)
lear.npc_push_walk("right", 1)
###pause
flow.wait(3)
###pause
baloons.push('Luna', 'Non sapevo dove altro andare.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraAtObject(lear)
###pause
lear = pGrid.getObjectById('mainplayer')
baloons.push('Lear', 'Ti stanno aspettando i dottori! prova prova prova prova prova prova prova prova prova prova', 'mainplayer')
lear.setCinematic(False)
