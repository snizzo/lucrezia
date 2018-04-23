lear = pGrid.getObjectById('mainplayer')
lear.setCinematic(True)
baloons.push('Lear', 'Luna!', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
baloons.push('Lear', 'I\'ve been looking after you the whole afternoon!', 'mainplayer')
###pause
flow.wait(2.5)
###pause
baloons.push('Lear', 'We should go.', 'mainplayer')
baloons.push('Lear', 'Doctors will be here soon.', 'mainplayer')
###pause
flow.wait(2.5)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 3.5)
###pause
baloons.push('Lear', 'It\'s for your own sake, y\'know?', 'mainplayer')
###pause
flow.wait(2)
###pause
luna = pGrid.getObjectById('luna')
luna.face("down")
###pause
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
baloons.push('Luna', 'I couldn\'t think of anywhere else.', 'luna')
###pause
flow.wait(2)
###pause
baloons.push('Luna', 'Have you ever had the feeling of not having a place you could call... home?', 'luna')
baloons.push('Luna', 'Anywhere you go, there\'s no room for you.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'I\'m void.', 'luna')
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
baloons.push('Luna', 'And I try to fill that with stupid stuff.', 'luna')
baloons.push('Luna', 'Like smartphone, parties, silly friends.', 'luna')
baloons.push('Luna', 'It\'s not working, of course', 'luna')
###pause
baloons.push('Luna', 'I feel so bad.', 'luna')
###pause
audioManager.stopMusic(1)
flow.wait(1)
###pause
baloons.push('Lear', 'That\'s normal I guess.', 'mainplayer')
audioManager.playMusic("sfx/sh_enc.ogg", 5)
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'We all kind of suck, in the end.', 'mainplayer')
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'All we could do is stay close to people', 'mainplayer that are not complete trash to us.', 'mainplayer')
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 1)
lear.npc_push_walk("left", 2)
lear.npc_push_walk("up", 1)
lear.npc_push_walk("right", 1)
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
flow.wait(1)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("up")
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
baloons.push('Lear', 'You\'re not trash.', 'mainplayer')
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Thank you.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraAtPoint(8,12)
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'There\'s an ancient story about a girl who escaped her parents.', 'mainplayer')
baloons.push('Lear', 'She was kind and nice, but they kept hitting her even when she begged.', 'mainplayer')
baloons.push('Lear', 'Her friend, Teddy was far away from home but she went after him.', 'mainplayer')
###pause
flow.wait(2)
###pause
baloons.push('Lear', 'She fought against mother nature and bad people to get there.', 'mainplayer')
baloons.push('Lear', 'When she arrived they hugged, and spent the night talking.', 'mainplayer')
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'The morning after she discovered he raped her sister.', 'mainplayer')
baloons.push('Lear', 'One week after, she was home.', 'mainplayer')
baloons.push('Luna', 'What\'s the point?', 'luna')
###pause
flow.wait(3)
###pause
baloons.push('Lear', 'Sometimes we don\'t realize how much people around us love us.', 'mainplayer')
###pause
flow.wait(3)
###pause
baloons.push('Lear', 'Like me.', 'mainplayer')
