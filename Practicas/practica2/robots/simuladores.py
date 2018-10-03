def simulador(puerto_zmq, f, x0, dt):
    
    from scipy.integrate import ode
    from zmq import Context, PUB
    from msgpack import packb
    from matplotlib.pyplot import figure
    from time import time, sleep
    from numpy import sin, pi, degrees, array
    
    context = Context()
    socket = context.socket(PUB)
    socket.bind("tcp://*:" + puerto_zmq)
    
    def mandar_mensaje(señales):
        socket.send(packb(señales))
        
    fig = figure(figsize=(6,3))
    ax = fig.gca()
    t0 = time()
    ts = [0]
    ys = [array(x0)]
    sis = ode(f)
    sis.set_initial_value(x0, t0)
        
    while True:
        try:
            ys.append(degrees(sis.integrate(sis.t + dt)))
            
            while time() - t0 - ts[-1] < dt - 0.0004:
                sleep(dt*0.01)
                
            ts.append(time() - t0)
            mandar_mensaje(ys[-1].tolist()[0:2])
            ax.clear()
            if len(ys) > 100:
                ax.plot(ts[-100:], ys[-100:])
                #ax.text(0.05, 0.1,ts[-1]-ts[-2], transform=ax.transAxes)
            else:
                ax.plot(ts, ys)
                #ax.text(0.05, 0.1,ts[-1]-ts[-2], transform=ax.transAxes)
            fig.canvas.draw()
            
        except KeyboardInterrupt:
            break
            
    return ts, ys