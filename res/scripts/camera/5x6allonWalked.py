if persistence.load("gameState") == 3:
    baloons.push('Ellen', 'Ciao...', 'ellen')
    baloons.push('Kate', '...', 'kate')
###pause
if persistence.load("gameState") == 3:
    messenger.send('changeMap', ['corridoio.map','3,1','up'])
