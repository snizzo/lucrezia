if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == False:
        persistence.save("corridoioTempState", 1)
        baloons.push('Ellen', 'Ma quanto è lungo...', 'ellen')
        ellen = pGrid.getObjectById("ellen")
        ellen.speed = 2.5
