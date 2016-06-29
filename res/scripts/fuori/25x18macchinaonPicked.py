if persistence.load("canleave")=="yes":
	baloons.pushThought("Ellen", "Meglio entrare in macchina.", "ellen")
	baloons.pushThought("Ellen", "La mia testa sta per scoppiare.", "ellen")
else:
	baloons.pushThought("Ellen", "Ma dove ho messo le chiavi...", "ellen")

###pause
if persistence.load("canleave")=="yes":
    messenger.send('changeMap', ['macchinadasola.map','2,2'])
