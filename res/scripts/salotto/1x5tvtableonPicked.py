if persistence.load('tvtable_salotto') == 0:
    baloons.push('Carlo Conti', 'E per 50 mila euro...', 'ellen')
    baloons.push('Carlo Conti', 'Di cosa parlava il romanzo "Il mondo di Sofia"?', 'ellen')
    baloons.pushThought('Ellen', 'Spazzatura...', 'ellen')
    persistence.save('tvtable_salotto', 1)
elif persistence.load('tvtable_salotto') == 1:
    baloons.pushThought('Ellen', 'Ancora spazzatura...', 'ellen')
