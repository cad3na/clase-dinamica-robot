def simulador(f, x0, dt, puertos_zmq=["5551", "5552"], control=False):
    
    from scipy.integrate import ode
    from zmq import Context, PUB, NOBLOCK, SUB, SUBSCRIBE
    from msgpack import packb, unpackb
    from matplotlib.pyplot import figure
    from time import time, sleep
    from numpy import sin, pi, degrees, array, radians
    
    context = Context()
    socket_sal = context.socket(PUB)
    socket_sal.bind("tcp://*:" + puertos_zmq[0])
    
    if control:
        m_pos_art = [0]
        pos_art = radians(m_pos_art).tolist()
        socket_ref = context.socket(SUB)
        socket_ref.connect("tcp://localhost:" + puertos_zmq[1])
        socket_ref.setsockopt(SUBSCRIBE, b'')
    
    def mandar_mensaje(señales):
        socket_sal.send(packb(señales))
        
    def recibir_mensaje(mp):
        try:
            m = unpackb(socket_ref.recv(flags=NOBLOCK))
        except:
            m = mp
        return m
        
    fig = figure(figsize=(5,2.5))
    ax = fig.gca()
    t0 = time()
    ts = [0]
    ys = [array(x0)]
    sis = ode(f)
    sis.set_initial_value(x0, t0)
    if control:
        sis.set_f_params(pos_art)
    ngdl = int(len(x0)/2)
        
    while True:
        try:
            if control:
                m_pos_art = recibir_mensaje(m_pos_art)
                pos_art = radians(m_pos_art).tolist()
                sis.set_f_params(pos_art)
            ys.append(degrees(sis.integrate(sis.t + dt)))
            
            while time() - t0 - ts[-1] < dt - 0.0004:
                sleep(dt*0.01)
                
            ts.append(time() - t0)
            mandar_mensaje(ys[-1].tolist()[0:ngdl])
            ax.clear()
            if len(ys) > 100:
                ax.plot(ts[-100:], ys[-100:])
            else:
                ax.plot(ts, ys)
            fig.canvas.draw()
            
        except KeyboardInterrupt:
            break
            
    return ts, ys