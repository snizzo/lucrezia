###pause
if persistence.load("gameState") == 3:
    if persistence.load("kateSpeak3") == 3:
        baloons.pushThought('Ellen', 'Io...', 'ellen')
        baloons.pushThought('Ellen', 'Cosa...', 'ellen')
        baloons.pushThought('Ellen', 'Cosa ho fatto...', 'ellen')
        persistence.save("kateSpeak3", 4)
###pause
if persistence.load("gameState") == 3:
    if persistence.load("kateSpeak3") == 2:
        baloons.pushThought('Ellen', 'Non mi sento le gambe.', 'ellen')
        baloons.push('Ellen', 'Kate?', 'ellen')
        baloons.push('Kate', 'Sentiamo.', 'kate')
        baloons.push('Ellen', 'Kate posso...', 'ellen')
        baloons.pushThought('Ellen', 'Sento l\'abisso che mi trascina giù.', 'ellen')
        baloons.push('Ellen', '...', 'ellen')
        baloons.push('Ellen', '... posso abbracciarti?', 'ellen')
        baloons.push('Kate', 'BAH!', 'kate')
        baloons.push('Ellen', '...', 'ellen')
        baloons.pushThought('Ellen', 'Oh... cristo.', 'ellen')
        baloons.pushThought('Ellen', 'No... devo andarmene!', 'ellen')
        persistence.save("kateSpeak3", 3)
        persistence.save("hasAskedForHug", "yes")
###pause
if persistence.load("gameState") == 3:
    if persistence.load("kateSpeak3") == 1:
        baloons.push('Kate', '.....', 'kate')
        baloons.pushThought('Ellen', 'Ormai l\'ho persa..', 'ellen')
        baloons.pushThought('Ellen', 'O forse ho capito male?', 'ellen')
        baloons.push('Ellen', '... ... Kate..?', 'ellen')
        persistence.save("kateSpeak3", 2)
###pause
if persistence.load("gameState") == 3:
    if persistence.load("kateSpeak3") == 2:
        kate = pGrid.getObjectById("kate")
        kate.npc_push_walk("up", 2)
###pause
if persistence.load("gameState") == 3:
    if persistence.load("kateSpeak3") == False:
        baloons.pushThought('Ellen', 'Ti prego Ellen, non mandare tutto in merda di nuovo!', 'ellen')
        baloons.push('Ellen', '.....', 'ellen')
        persistence.save("kateSpeak3", 1)
###pause
if persistence.load("gameState") == 9999:
    baloons.pushThought('Ellen', 'Ti prego Ellen, non mandare tutto in merda di nuovo!', 'ellen')
    kate = pGrid.getObjectById("kate")
    kate.npc_push_walk("down", 2)
    kate.npc_push_walk("left", 2)
    kate.npc_push_walk("right", 2)
    kate.npc_push_walk("up", 2)

