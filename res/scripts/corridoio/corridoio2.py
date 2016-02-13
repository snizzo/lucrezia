if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == 1:
        baloons.pushThought('Ellen', 'Mi pesano le gambe.', 'ellen')
        baloons.pushThought('Ellen', 'Devo arrivare alle scale.', 'ellen')
        persistence.save("corridoioTempState", 2)
        ellen = pGrid.getObjectById("ellen")
        ellen.setSpeed(2.0)
