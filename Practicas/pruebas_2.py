from IPython.utils.warn import info
from scipy.integrate import odeint
from numpy import linspace, sin, matrix, array
import sympy as sym
from control import tf, step

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

    if (ts == tiempos).all() and (xs == valores).all():
        print("Perfecto!")
    else:
        if (ts != tiempos).any():
            info("Quiero 100 puntos desde el tiempo 0 hasta el tiempo 10")
        else:
            if valores[0] != x0:
                info("Revisa tus condiciones iniciales")
            else:
                if (xs !=  valores).any():
                    info("Revisa tu funcion G")

def prueba_2_3(solucion):
    sim_t = sym.var("t")
    sim_x = sym.Function("x")(sim_t)
    ecuacion = sim_x.diff("t") - sim_x**2 + 5*sim_x

    sol_sim = sym.dsolve(ecuacion, sim_x)

    if solucion.equals(sol_sim):
        print("Muy bien! ◕‿↼")
    else:
        info("Revisa tu ecuación diferencial")

def prueba_2_4(solucion):
    def G(X, t):
        A = matrix([[0, 1],[-15, -8]])
        B = matrix([[0], [1]])
        return array((A*matrix(X).T + B).T).tolist()[0]

    ts = linspace(0, 10, 100)
    xs = odeint(func=G, y0=[0, 0], t=ts)
    if (solucion == xs).all():
        print("Nice!")
    else:
        info("Revisa tus matrices")

def prueba_2_5(tiempo, estado):
    G = tf([0, 0, 1], [1, 8, 15])
    xs, ts = step(G, tiempo)

    if (estado == xs).all():
        print("Muy bien!")
    else:
         info("Revisa tu función de transferencia")
