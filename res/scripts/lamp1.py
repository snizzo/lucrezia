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


if persistence.load("gameState") == 2:
    baloons.push('Kate', 'Spegni la sveglia', 'kate')
    persistence.save("scrivaniaCameraState", 2)
    ###pause
if persistence.load("gameState") == 2:
    kate = pGrid.getObjectById("kate")
    kate.npc_push_walk("down", 2)
    kate.npc_push_walk("left", 3)
    ###pause
if persistence.load("gameState") == 2:
    pGrid.getObjectById("kate").face('down')
    baloons.push('Ellen', 'Oddio Kate! Mi farai venire un infarto.', 'ellen')
    ###pause
if persistence.load("gameState") == 2:
    ellen = pGrid.getObjectById("ellen")
    ellen.npc_push_walk("up", 2)
    ###pause
if persistence.load("gameState") == 2:
    ellen = pGrid.getObjectById("ellen")
    ###pause
if persistence.load("gameState") == 2:
    baloons.push('Ellen', 'Sai, pensavo che mi sarei potuta fermare qualche gior...', 'ellen')
    audioManager.stopLongEffect('alarm')
    baloons.push('Ellen', 'Finalmente...', 'ellen')
    baloons.push('Kate', 'Avevo unicamente intenzione di dirti che non ho smesso di volerti bene o sia arrabbiata.', 'kate')
    baloons.push('Kate', 'Sono stufa.', 'kate')
    audioManager.playMusic('soundtrack/gone.ogg')
    baloons.push('Kate', 'Non ne posso più del tuo egocentrismo illimitato e in un paio di giorni in montagna', 'kate')
    baloons.push('Kate', 'mi hai veramente saturata.', 'kate')
    baloons.push('Kate', 'Ne avevo fin sopra ai capelli dei tuoi musi, delle tue continue nenie', 'kate')
    baloons.push('Kate', 'perchè in fondo ti diverti a lamentarti se, ovunque, riesci a trovarne motivo.', 'kate')
    baloons.push('Ellen', 'Ma... Cosa stai dic-', 'ellen')
    baloons.push('Kate', 'Non voglio assolutamente litigare con te ma ti chiedo solo di lasciarmi stare.', 'kate')
    baloons.push('Kate', 'Dei tuoi problemi ti ho detto tutto quello che ti potevo dire.', 'kate')
    baloons.push('Kate', 'Piantala di pensare unicamente a te stesso e a come stai tu, pretendendo che gli altri se ne interessino,', 'kate')
    baloons.push('Kate', 'se degli altri a te non importa veramente niente.', 'kate')
    baloons.push('Kate', 'Non è "come sto" che importa.', 'kate')
    baloons.push('Kate', 'Quando ti dico interessati delle persone intendo di quello che fanno', 'kate')
    baloons.push('Kate', 'Di quello che pensano.', 'kate')
    baloons.push('Kate', '...di quello che amano.', 'kate')
    baloons.push('Kate', 'Hai una vaga idea di cosa voglia fare all\'università l\'anno prossimo?', 'kate')
    baloons.push('Ellen', 'Io non...', 'ellen')
    baloons.push('Ellen', '.....', 'ellen')
    baloons.push('Kate', 'Non mi hai mai mai chiesto niente.', 'kate')
    baloons.push('Kate', 'A me, come immagino, al resto dell\'umanità che ti sta intorno.', 'kate')
    baloons.push('Kate', 'Non la vedi.', 'kate')
    baloons.push('Kate', 'Anzi la vedi solo lì, tutta riunita nell\'unico interesse di farti del male.', 'kate')
    baloons.push('Kate', 'E non mi raccontare che sei timida!', 'kate')
    baloons.push('Kate', 'Perchè non ti si chiede di entrare nell\'intimità delle persone!', 'kate')
    baloons.push('Kate', 'Solo di avere con loro un dialogo il cui soggetto non sia tu.', 'kate')
    baloons.push('Kate', 'Detto questo, non ho altro da aggiungere.', 'kate')
    baloons.push('Kate', 'Ci vedremo quando verrò occasionalmente, senza assolutamente alcun rancore', 'kate')
    baloons.push('Kate', 'Ma per il momento basta messaggi, chiamate o chat.', 'kate')
    baloons.push('Ellen', 'E queste storie.. da dove saltano fuori??', 'ellen')
    baloons.push('Ellen', 'Ti ho già detto che mi dispiace!', 'ellen')
    baloons.push('Ellen', 'Questo è il mio modo di essere.', 'ellen')
    baloons.push('Ellen', 'Come sono fatta.', 'ellen')
    baloons.push('Ellen', 'Lo sapresti se solo avessi cercato di conoscermi anche tu!', 'ellen')
    baloons.push('Kate', 'Mi sembra di parlare al muro!', 'kate')
    baloons.push('Ellen', 'L\'altra sera, quando parlavamo al telefono...', 'ellen')
    baloons.push('Ellen', 'Ci sono rimasta male.', 'ellen')
    baloons.push('Ellen', 'Non me l\'aspettavo.', 'ellen')
    baloons.push('Kate', 'Basta non ce la faccio più!', 'kate', 0.02)
    baloons.push('Kate', 'Mi hai nauseata a tal punto che non riesco più a parlarti!', 'kate', 0.02)
    baloons.push('Kate', 'Lasciami stare!!', 'kate', 0.02)
    baloons.push('Ellen', '.....', 'ellen', 0.5)
    ###pause
if persistence.load("gameState") == 2:
    pGrid.getObjectById("kate").npc_push_walk("right", 4)
    pGrid.getObjectById("kate").npc_push_walk("up", 3)
    ###pause
if persistence.load("gameState") == 2:
    pGrid.getObjectById("kate").face('down')
    persistence.save('gameState', 3)
