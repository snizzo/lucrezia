'''
PERSISTENCE HELP:
'''

#set the very first state to the camera
if persistence.load("gameState") == False:
    persistence.save("gameState", 1)

if persistence.load("gameState") == 1:
    pGrid.getObjectById("lamp1").setOff()
    pGrid.getObjectById("minilamp").setOff()
    
    baloons.pushThought('Ellen', 'Mh..', 'ellen')
    baloons.pushThought('Ellen', 'Dove mi trovo?', 'ellen')
    baloons.pushThought('Ellen', 'Ah giusto, sono in montagna. A casa di Louis.', 'ellen')
    baloons.pushThought('Ellen', 'Ma dov\'è Kate? Meglio accendere la luce.', 'ellen')
    
    persistence.save('gameState', 2)
    ###pause
    
    
