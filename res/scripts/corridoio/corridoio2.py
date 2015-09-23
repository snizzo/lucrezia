if persistence.load("gameState") == 3:
    if persistence.load("corridoioTempState") == 1:
        baloons.push('Ellen', 'Mi pesano le gambe.', 'ellen')
        baloons.push('Ellen', 'Devo arrivare alle scale.', 'ellen')
        persistence.save("corridoioTempState", 2)
        ellen = pGrid.getObjectById("ellen")
        ellen.speed = 2.0
