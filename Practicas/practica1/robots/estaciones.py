def estacion_3gdl(puerto_zmq = "5555"):
    '''
    Esta función crea un socket de 0MQ para publicar datos de tres referencias.
    
    >>> from robots.estaciones import estacion_3gdl
    >>> estacion_3gdl("5555")
    
    Iniciando estacion de referencias en el puerto 5555
    '''
    from zmq import Context, PUB
    from msgpack import packb
    from ipywidgets import interact
    
    context = Context()
    socket = context.socket(PUB)
    socket.bind("tcp://*:" + puerto_zmq)
    
    def mandar_mensaje(q1=0, q2=0, q3=0):
        socket.send(packb([q1, q2, q3]))
    
    print("Iniciando estacion de referencias en el puerto " + puerto_zmq)
    interact(mandar_mensaje, q1=(-180.0, 180.0), q2=(-180.0, 180.0), q3=(-180.0, 180.0));
    
def estacion_1gdl(puerto_zmq = "5555"):
    '''
    Esta función crea un socket de 0MQ para publicar datos de tres referencias.
    
    >>> from robots.estaciones import estacion_3gdl
    >>> estacion_3gdl("5555")
    
    Iniciando estacion de referencias en el puerto 5555
    '''
    from zmq import Context, PUB
    from msgpack import packb
    from ipywidgets import interact
    
    context = Context()
    socket = context.socket(PUB)
    socket.bind("tcp://*:" + puerto_zmq)
    
    def mandar_mensaje(q1=0):
        socket.send(packb([q1]))
    
    print("Iniciando estacion de referencias en el puerto " + puerto_zmq)
    interact(mandar_mensaje, q1=(-180.0, 180.0));
    
def gen_sen_3gdl(puerto_zmq, gen1=True, gen2=True, gen3=True):
    
    from zmq import Context, PUB
    from msgpack import packb
    from matplotlib.pyplot import figure
    from time import time, sleep
    from numpy import sin, pi
    
    context = Context()
    socket = context.socket(PUB)
    socket.bind("tcp://*:" + puerto_zmq)
    
    def mandar_mensaje(señal, g1, g2, g3):
        socket.send(packb([señal if gen else 0 for gen in [g1, g2, g3]]))
        
    fig = figure(figsize=(6,3))
    ax = fig.gca()
    t0 = time()
    ts = []
    ys = []
        
    while True:
        try:
            t = time()-t0
            if t >= 0.005:
                y = 30*sin(pi*t)
                mandar_mensaje(y, gen1, gen2, gen3)
                ts.append(t)
                ys.append(y)
                ax.clear()
                if len(ys) > 100:
                    ax.plot(ts[-100:], ys[-100:])
                else:
                    ax.plot(ts, ys)
                fig.canvas.draw()
            
        except KeyboardInterrupt:
            break