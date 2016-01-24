from IPython.utils.warn import info
from control import tf, step
from numpy import linspace, sin, matrix, array

def prueba_3_1(t1, x1, t2, x2):

    def suspension(m, c, k, F):
        G = tf([0, 0, 1/m], [1, c/m, k/m])
        K = tf([F], [1])
        t = linspace(0, 10, 1000)

        y, t = step(K*G, t)

        return t, y

    tiempos, valores1 = suspension(1200, 1500, 15000, 500*9.81)
    tiempos, valores2 = suspension(1200, 1500, 15000, 1000*9.81)

    if (tiempos == t1).all() and (valores1 == x1).all() and (valores2 == x2).all() :
        print("Bien hecho!")
    else:
        if (valores1 != x1).any():
            info("Revisa tu primer simulacion")
        else:
            if (valores2 != x2).any():
                info("Revisa la segunda simulacion")
