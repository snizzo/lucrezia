if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == False:
        persistence.save("corridoioTempState", 1)
        baloons.pushThought('Ellen', 'Ma quanto è lungo...', 'ellen')
        ellen = pGrid.getObjectById("ellen")
        ellen.setSpeed(2.5)
