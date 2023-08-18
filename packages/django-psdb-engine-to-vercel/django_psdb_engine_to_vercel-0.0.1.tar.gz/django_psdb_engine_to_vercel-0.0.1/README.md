# comu

init

    from j.joy import Joy
    
    j = Joy(35)

    while True:
        print(j.read())

escala

    from j.joy import Joy
    
    j=Joy(35,escala=(-10,10))

    while True:
        print(j.read())

inverter o valor

    from j.joy import Joy
    
    j=Joy(35, invert=True)

    while True:
        print(j.read())