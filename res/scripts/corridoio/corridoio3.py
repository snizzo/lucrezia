if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == 2:
        baloons.pushThought('Ellen', 'Ugh...', 'ellen')
        baloons.pushThought('Ellen', 'Mi viene da vomitare.', 'ellen')
        persistence.save("corridoioTempState", 3)
        persistence.save("gameState", 4)
        ellen = pGrid.getObjectById("ellen")
        ellen.setSpeed(1.5)
