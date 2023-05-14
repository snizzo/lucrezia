lear = pGrid.getObjectById('mainplayer')
lear.setCinematic(True)
baloons.push('Lear', 'Luna!', 'mainplayer')
baloons.push('Lear', 'Ma dov’eri scomparsa?', 'mainplayer')
###pause
flow.wait(1)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 1)
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'È una settimana che ti cerchiamo dappertutto!', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
baloons.push('Lear', 'Mi sono preoccupato.', 'mainplayer')
baloons.push('Lear', 'Non dovresti stare qui, fa freddo.', 'mainplayer')
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("down")
###pause
flow.wait(1.5)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Alla fine mi hai trovato.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 2.5)
###pause
baloons.push('Lear', 'C\'è poco da scherzare!', 'mainplayer')
baloons.push('Lear', 'Lo sai quanti soldi ho speso?', 'mainplayer')
baloons.push('Lear', 'Ho dovuto prendere due treni, pagare un portiere perchè ci facesse passare.', 'mainplayer')
baloons.push('Lear', 'Per non parlare delle multe!', 'mainplayer')
###pause
flow.wait(2)
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("right", 2.5)
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Ti chiedo scusa.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Mi dispiace, davvero.', 'luna')
baloons.push('Luna', 'Non volevo che tu mi vedessi così.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("right", 2.5)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("up")
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'Dai entriamo.', 'mainplayer')
baloons.push('Lear', 'Fa un freddo insopportabile qui fuori.', 'mainplayer')
###pause
flow.wait(2.5)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
flow.wait(2.5)
###pause
baloons.pushThought('Lear', '...', 'mainplayer')
baloons.push('Lear', 'Luna?', 'mainplayer')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Io non credo che verrò.', 'luna')
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("right")
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("left")
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("down")
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("up")
###pause
flow.wait(0.5)
###pause
baloons.push('Lear', 'Mi vuoi spiegare quello che sta succedendo?', 'mainplayer')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Vorrei tornare indietro nel tempo.', 'luna')
baloons.push('Luna', 'Cambiare il passato.', 'luna')
baloons.push('Luna', 'Credevo di avere infinite possibilità per fare quello che volevo…', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'ma non era così.', 'luna')
###pause
flow.wait(0.75)
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("up", 1)
###pause
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'La mia vita è una collezione di rimpianti, frasi non dette.', 'luna')
baloons.push('Luna', 'Altre invece non le avrei volute dire.', 'luna')
###pause
flow.wait(0.75)
###pause
baloons.push('Luna', 'Non sono una brava persona.', 'luna')
###pause
flow.wait(1)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("right", 1)
lear.npc_push_walk("up", 1)
###pause
flow.wait(0.5)
###pause
baloons.push('Lear', 'Non riesco a seguirti.', 'mainplayer')
baloons.push('Lear', 'Cosa c’entra adesso tutto questo?', 'mainplayer')
baloons.push('Lear', 'Tutti si fanno un po’ schifo.', 'mainplayer')
###pause
flow.wait(0.5)
###pause
baloons.push('Lear', 'C’è una parte di noi che ci piace e una invece che vorremmo non avere.', 'mainplayer')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Sai di cosa mi pento?', 'luna')
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("right")
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("left")
###pause
flow.wait(0.35)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.face("up")
###pause
flow.wait(0.5)
###pause
baloons.push('Lear', 'No.', 'mainplayer')
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("left", 4)
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Alla festa di fine scuola.', 'luna')
baloons.push('Luna', 'Io e le altre bambine abbiamo fatto un gioco.', 'luna')
baloons.push('Luna', 'Io ovviamente ero impacciata e scomposta, non potevo vincere.', 'luna')
baloons.push('Luna', 'Però mai avrei immaginato la punizione.', 'luna')
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
flow.wait(0.7)
###pause
luna = pGrid.getObjectById('luna')
luna.face("right")
###pause
flow.wait(2)
###pause
baloons.push('Luna', 'Dovevo darti un bacio.', 'luna')
###pause
flow.wait(2)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("up", 2)
lear.npc_push_walk("left", 1)
###pause
lear = pGrid.getObjectById('mainplayer')
luna = pGrid.getObjectById('luna')
customCamera.moveCameraBetweenObjects(luna, lear)
###pause
baloons.push('Lear', 'Me lo ricordo.', 'mainplayer')
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Tutte le altre ragazze mi incitavano a farlo, ma solo perchè pensavano che fosse una punizione adeguata.', 'luna')
baloons.push('Luna', 'A me invece piacevi.', 'luna')
baloons.push('Luna', 'Ti ricordi cosa ho fatto dopo?', 'luna')
###pause
flow.wait(1)
audioManager.playMusic("soundtrack/emotional1.ogg", 5)
###pause
baloons.push('Lear', 'Sei scappata.', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
luna.face("right")
###pause
baloons.push('Luna', 'Non volevo che pensassero fossi diversa da loro.', 'luna')
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("left", 1)
###pause
baloons.push('Lear', 'Se davvero volevi baciarmi perchè non l’hai fatto?', 'mainplayer')
baloons.push('Lear', 'Avresti potuto dire che non avresti voluto e ti avrebbero creduto di sicuro.', 'mainplayer')
baloons.push('Lear', 'In fondo la tua è stata una scelta.', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("right", 1)
###pause
baloons.push('Luna', 'Non volevo neanche questo.', 'luna')
baloons.push('Luna', 'Non volevo farti stare male, deridendoti e trattandoti come un\'essere repellente.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'Ma allora...', 'mainplayer')
baloons.push('Lear', 'Non capisco dove sia il tuo rimpianto.', 'mainplayer')
baloons.push('Lear', 'Hai fatto esattamente quello che volevi fare, giusto?', 'mainplayer')
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Già.', 'luna')
baloons.push('Luna', 'Era quello che pensavo anch\'io.', 'luna')
###pause
flow.wait(0.5)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("left", 0.5)
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Per quanto mi illudevo di non aver avuto scelta…', 'luna')
baloons.push('Luna', 'Ignoravo la terza opzione.', 'luna')
baloons.push('Luna', 'Avrei dovuto appoggiare le mie labbra alle tue, come si fa con una persona che si ama.', 'luna')
baloons.push('Luna', 'Invece ho avuto paura di essere me stessa e mi sono fatta condizionare.', 'luna')
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("up", 0.2)
###pause
flow.wait(3)
###pause
baloons.push('Luna', 'Pensavo che mi avrebbero preso in giro.', "luna")
###pause
flow.wait(2)
###pause
baloons.pushThought('Lear', '...', 'lear')
###pause
flow.wait(2)
###pause
baloons.push('Luna', 'I bambini sanno essere crudeli a volte.', 'luna')
baloons.push('Luna', 'Sanno dove colpirti e ti umiliano.', 'luna')
baloons.push('Luna', 'Se sei troppo alta o troppo bassa.', 'luna')
baloons.push('Luna', 'Se ti capita di voler bene a qualcuno, sai…', 'luna')
###pause
flow.wait(0.8)
###pause
luna = pGrid.getObjectById('luna')
luna.face("right")
###pause
flow.wait(1.5)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
flow.wait(0.8)
###pause
baloons.push('Luna', 'più degli altri.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Lear', 'Perchè mi stai raccontando queste cose?', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("down", 0.3)
luna.npc_push_walk("right", 2)
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Il tempo non è infinito ed ogni istante che ci è concesso in questa vita è unico.', 'luna')
baloons.push('Luna', 'Lo vediamo arrivare.', 'luna')
baloons.push('Luna', 'Succede.', 'luna')
baloons.push('Luna', 'E poi se ne va per sempre.', 'luna')
baloons.push('Luna', 'Nessuno è in grado di far scorrere gli orologi al contrario.', 'luna')
baloons.push('Luna', 'Neanche io.', 'luna')
###pause
audioManager.stopMusic(4)
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
flow.wait(1)
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("left", 2)
###pause
flow.wait(2)
###pause
baloons.push('Luna', 'Neanche io.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Ho perso la mia occasione di creare un ricordo meraviglioso per entrambi.', 'luna')
baloons.push('Luna', 'È questo il mio rimpianto.', 'luna')
###pause
flow.wait(1)
##pause
baloons.push('Lear', 'Ma ci saranno altri momenti, no?', 'lear')
###pause
flow.wait(6)
audioManager.playMusic("soundtrack/Peaks_and_Valleys_Holon.ogg", 5)
###pause
baloons.push('Luna', 'Per me non c\'è più tempo.', 'luna')
###pause
flow.wait(1)
###pause
lear = pGrid.getObjectById('mainplayer')
lear.npc_push_walk("left",1)
###pause
baloons.push('Lear', 'Cosa intendi dire?!', 'mainplayer')
###pause
flow.wait(2)
###pause
baloons.push('Luna', 'Non sono qui perchè mi piace giocare a nascondino Lear.', 'luna')
baloons.push('Luna', 'Mi hanno messa qui perchè pensano che io abbia perso.', 'luna')
###pause
flow.wait(1)
###pause
baloons.push('Luna', 'Mi sono spaventata parecchio. Ci ho quasi creduto.', 'luna')
baloons.push('Luna', 'Ma adesso...', 'luna')
###pause
flow.wait(1)
###pause
baloons.pushThought('Lear', '...adesso?', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
luna.npc_push_walk("right",0.5)
###pause
baloons.push('Luna', 'Adesso che sei arrivato tu una possibilità c\'è.', 'luna')
baloons.push('Luna', 'Spalanca bene le orecchie perchè non abbiamo più tempo!', 'luna')
baloons.push('Luna', 'In questo momento stanno venendo a prenderci e questa è la nostra ultima chance.', 'luna')
baloons.push('Lear', 'Mi fai paura!', 'mainplayer')
baloons.push('Lear', 'Non capisco di cosa stai parlando!', 'mainplayer')
baloons.push('Luna', 'Io ti spedirò indietro nel tempo e tu dovrai salvarmi.', 'luna')
baloons.push('Luna', 'Non siamo sempre stati affiatati. Non te lo sto chiedendo a cuor leggero.', 'luna')
baloons.push('Luna', 'Ma mi dovrai dare una mano.', 'luna')
baloons.push('Luna', 'Devi cercare un modo per tirarmi fuori di qui!', 'luna')
baloons.push('Lear', 'Fuori da qui?', 'mainplayer')
baloons.push('Lear', 'Ma se neanche so come ci sei entrata!', 'mainplayer')
baloons.push('Lear', 'Forse è il caso di chiamare i dottori.', 'mainplayer')
###pause
luna = pGrid.getObjectById('luna')
luna.face("right")
###pause
flow.wait(0.35)
###pause
luna = pGrid.getObjectById('luna')
luna.face("left")
###pause
flow.wait(0.35)
###pause
luna = pGrid.getObjectById('luna')
luna.face("down")
###pause
flow.wait(0.35)
###pause
luna = pGrid.getObjectById('luna')
luna.face("up")
###pause
flow.wait(0.5)
###pause
baloons.push('Luna', 'Ti chiedo scusa Lear.', 'luna')
baloons.push('Luna', 'Scusa per tutto.', 'luna')
baloons.push('Luna', 'Ma mi servi un\'ultima volta.', 'luna')
baloons.push('Lear', 'Cos-', 'mainplayer')
baloons.push('Luna', 'Solo per questa ultima volta.', 'luna')
baloons.pushThought('Lear', 'Cos-', 'mainplayer')
###pause
audioManager.playEffect('sfx/time_machine.ogg')
persistence.save('cameraStatus', 'afterTettoTeleport')
luna = pGrid.getObjectById('luna')
lear = pGrid.getObjectById('mainplayer')
customCamera.moveCameraAtPoint(8,5)
###pause
messenger.send('changeMap', ['camera.map','2,3','down','flyall'])
