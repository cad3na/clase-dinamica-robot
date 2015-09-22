from IPython.utils.warn import info
from scipy.integrate import odeint
from numpy import linspace, sin

def prueba_2_1(var0, var1, var2, var3, ans):
    x0 = 1
    Δt = 1

    F = lambda x : -x
    x1 = x0 + F(x0)*Δt
    x2 = x1 + F(x1)*Δt
    x3 = x2 + F(x2)*Δt

    if x0 == var0 and x1 == var1 and x2 == var2 and x3 == var3 and ans == var2:
        print("Buen trabajo! ☺")
    else:
        if x0 != var0 or x1 != var1 or x2 != var2:
            info("¿Estas ejecutando las cosas fuera de orden? (╯°□°）╯︵ ┻━┻")
        else:
            if x3 != var3:
                info("Revisa tus calculos")
            else:
                if ans != var3:
                    info("¿Desplegaste tu resultado?")

def prueba_2_2(tiempos, valores):
    ts = linspace(0, 10, 100)
    x0 = 1

    F = lambda x, t : x**2 - 5*x + 0.5*sin(x) - 2

    xs = odeint(func=F, y0=x0, t=ts)

    if ts == tiempos and xs == valores:
        print("Perfecto!")
    else:
        if ts != tiempos:
            info("Quiero 100 puntos desde el tiempo 0 hasta el tiempo 10")
        else:
            if xs !=  valores:
                info("Revisa tu funcion F")    
