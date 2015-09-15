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


if persistence.load("lampCameraState") == 2:
    baloons.push('Kate', 'Spegni la sveglia', 'kate')
    persistence.save("scrivaniaCameraState", 2)
    ###pause
if persistence.load("lampCameraState") == 2:
    kate = pGrid.getObjectById("kate")
    kate.npc_push_walk("down", 2)
    ###pause
if persistence.load("lampCameraState") == 2:
    kate = pGrid.getObjectById("kate")
    kate.npc_push_walk("left", 3)
    ###pause
if persistence.load("lampCameraState") == 2:
    pGrid.getObjectById("kate").face('down')
    baloons.push('Ellen', 'Oddio Kate! Mi farai venire un infarto.', 'ellen')
    ###pause
if persistence.load("lampCameraState") == 2:
    ellen = pGrid.getObjectById("ellen")
    ellen.npc_push_walk("up", 2)
    ###pause
if persistence.load("lampCameraState") == 2:
    ellen = pGrid.getObjectById("ellen")
    ###pause
if persistence.load("lampCameraState") == 2:
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
    baloons.push('Kate', 'NON è come sto che importa, quando ti dico interessati delle persone', 'kate')
    baloons.push('Kate', 'intendo di quello che fanno, di quello che pensano, di quello che amano.', 'kate')
    baloons.push('Kate', 'Hai una vaga idea di cosa voglia fare all\'università l\'anno prossimo?', 'kate')
    baloons.push('Ellen', 'Io non...', 'ellen')
    baloons.push('Kate', 'Non mi hai MAI MAI chiesto niente.', 'kate')
    baloons.push('Kate', 'A me, come, immagino, al resto dell\'umanità che ti sta intorno.', 'kate')
    baloons.push('Kate', 'Non la vedi; anzi la vedi solo lì, tutta riunita nell\'unico interesse di farti del male.', 'kate')
    baloons.push('Kate', 'E non mi raccontare che sei timido perchè non ti si chiede di entrare nell\'intimità delle persone,', 'kate')
    baloons.push('Kate', 'solo di avere con loro un dialogo il cui soggetto non sia tu.', 'kate')
    baloons.push('Kate', 'Detto questo, non ho altro da aggiungere.', 'kate')
    baloons.push('Kate', 'Ci vedremo quando verrò occasionalmente, senza assolutamente alcun rancore', 'kate')
    baloons.push('Kate', 'ma per il momento basta messaggi, chiamate o chat.', 'kate')
    baloons.push('Ellen', 'E queste storie.. da dove saltano fuori??', 'ellen')
    baloons.push('Ellen', 'A questo punto se vuoi ti lascio stare, ma definitivamente', 'ellen')
    baloons.push('Ellen', 'perchè non è concepibile una cosa del genere.', 'ellen')
    baloons.push('Ellen', 'Gli amici servono a farti vedere gli errori, non a farteli pesare!', 'ellen')
    baloons.push('Ellen', 'Non ha senso che continui a riptermi i miei sbagli.', 'ellen')
    baloons.push('Ellen', 'Anche se ancora non capisco...', 'ellen')
    baloons.push('Kate', 'Mi sembra di parlare al muro!', 'kate')
    baloons.push('Ellen', 'Se potessimo parlarne...', 'ellen')
    baloons.push('Kate', 'Vattene da qui.', 'kate')
    baloons.push('Kate', 'Tornatene a casa, Kate.', 'kate', 0.1)
    baloons.push('Ellen', 'Come vuoi.', 'ellen', 0.1)
    ###pause
if persistence.load("lampCameraState") == 2:
    pGrid.getObjectById("kate").npc_push_walk("right", 1)
    ###pause
if persistence.load("lampCameraState") == 2:
    pGrid.getObjectById("kate").npc_push_walk("up", 1)
    ###pause
if persistence.load("lampCameraState") == 2:
    pGrid.getObjectById("kate").face('left')
    persistence.save('cameraState', 2)
'''
K: Avevo unicamente intenzione di dirti che non ho smesso di volerti bene o sia arrabbiata.
K: Sono stufa.
K: Non ne posso più del tuo egocentrismo illimitato e in un paio di giorni in montagna mi hai veramente saturata.
K: Ne avevo fin sopra ai capelli dei tuoi musi, delle tue continue nenie
K: perchè in fondo ti diverti a lamentarti se, ovunque, riesci a trovarne motivo.
E: ...
K: Non voglio assolutamente litigare con te ma ti chiedo solo di lasciarmi stare.
K: Dei tuoi problemi ti ho detto tutto quello che ti potevo dire. Piantala di pensare unicamente a te stesso e a come stai tu, pretendendo che gli altri se ne interessino, se degli altri a te non importa veramente niente.
K: NON è come sto che importa, quando ti dico interessati delle persone intendo di quello che fanno, di quello che pensano, di quello che amano.
K: Hai una vaga idea di cosa voglia fare all'università l'anno prossimo?
K: Non mi hai MAI MAI chiesto niente.
K: A me, come, immagino, al resto dell'umanità che ti sta intorno.
K: Non la vedi; anzi la vedi solo lì, tutta riunita nell'unico interesse di farti del male.
K: E non mi raccontare che sei timido perchè non ti si chiede di entrare nell'intimità delle persone, solo di avere con loro un dialogo il cui soggetto non sia tu. 
K: Detto questo, non ho altro da aggiungere.
K: Ci vedremo quando verrò occasionalmente, senza assolutamente alcun rancore, ma per il momento basta messaggi, chiamate o chat.
E: E va bene, non posso dire di non averci provato.
E: A questo punto se vuoi ti lascio stare, ma definitivamente perchè non è concepibile una cosa del genere.
E: Gli amici servono a farti vedere gli errori, non a farteli pesare.
K: Mi sembra di parlare al muro. 
E: Ma che discorsi sono? Pensi che dicendomi di non parlarti più perchè sono un nauseante egocentrico non abbia le sue conseguenze?
E: Mi dispiace ma non posso fare finta di niente.
E: Non sono qua per sentirmi dire che non me ne è mai fregato niente di te quando invece ti pensavo MOLTO più di quanto tu possa immaginare.
K: Vattene da qui, tornatene a casa.
''' 
###pause
if persistence.load("lampCameraState") == 2:
    persistence.save("lampCameraState", 1)
