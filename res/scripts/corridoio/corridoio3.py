if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == 2:
        baloons.push('Ellen', 'Ugh...', 'ellen')
        baloons.push('Ellen', 'Mi viene da vomitare.', 'ellen')
        persistence.save("corridoioTempState", 3)
        persistence.save("gameState", 4)
        ellen = pGrid.getObjectById("ellen")
        ellen.speed = 1.5
