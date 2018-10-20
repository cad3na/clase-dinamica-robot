def DH(params):
    '''
    Esta función toma los parametros DH de la articulación de un robot manipulador
    y calcula la matriz de transformación homogénea de la articulación, la regresa
    como una matriz de numpy.
    
    >>> from robots.utilidades import DH
    >>> from numpy import pi
    >>> DH([0.8, 0, pi/2, pi/6])
    
    matrix([[ 8.66025404e-01, -3.06161700e-17,  5.00000000e-01, 6.92820323e-01],
            [ 5.00000000e-01,  5.30287619e-17, -8.66025404e-01, 4.00000000e-01],
            [ 0.00000000e+00,  1.00000000e+00,  6.12323400e-17, 0.00000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]])
    '''
    from numpy import matrix, sin, cos
    a, d, α, θ = params
    A = matrix([[cos(θ), -sin(θ)*cos(α), sin(θ)*sin(α), a*cos(θ)],
                [sin(θ), cos(θ)*cos(α), -cos(θ)*sin(α), a*sin(θ)],
                [0, sin(α), cos(α), d],
                [0, 0, 0, 1]])
    return A

def pos_articulaciones(transformaciones):
    '''
    Esta función toma una lista (o arreglo) con las transformaciones de un robot
    manipulador, y devuelve una lista con las posiciones de cada articulación del
    manipulador.
    
    >>> from robots.utilidades import DH, pos_articulaciones
    >>> from numpy import pi
    >>> l1, l2, l3 = 1, 0.7, 0.5
    >>> q1, q2, q3 = pi/6, pi/8, pi/6
    >>> A1 = DH([0, l1, pi/2, q1])
    >>> A2 = DH([l2, 0, 0, q2])
    >>> A3 = DH([l3, 0, 0, q3])
    >>> pos_articulaciones([A1, A2, A3])
    
    [array([[0.],
            [0.],
            [0.]]),
     matrix([[0.],
             [0.],
             [1.]]),
     matrix([[0.5600722 ],
             [0.32335784],
             [1.2678784 ]]),
     matrix([[0.82367363],
             [0.47554819],
             [1.66455507]])]
    '''
    from numpy import eye
    tot = eye(4)
    posiciones = [tot[:3, 3:]]
    
    for tran in transformaciones:
        tot = tot*tran
        posiciones.append(tot[:3, 3:])
        
    return posiciones

def ori_articulaciones(transformaciones):
    '''
    Esta función toma una lista (o arreglo) con las transformaciones de un robot
    manipulador, y devuelve una lista con las matrices de rotación que dan la
    orientación del marco de referencia asociado a cada articulación.
    
    >>> from robots.utilidades import DH, ori_articulaciones
    >>> from numpy import pi
    >>> l1, l2, l3 = 1, 0.7, 0.5
    >>> q1, q2, q3 = pi/6, pi/8, pi/6
    >>> A1 = DH([0, l1, pi/2, q1])
    >>> A2 = DH([l2, 0, 0, q2])
    >>> A3 = DH([l3, 0, 0, q3])
    >>> ori_articulaciones([A1, A2, A3])
    
    [array([[1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]]),
     matrix([[ 8.66025404e-01, -3.06161700e-17,  5.00000000e-01],
             [ 5.00000000e-01,  5.30287619e-17, -8.66025404e-01],
             [ 0.00000000e+00,  1.00000000e+00,  6.12323400e-17]]),
     matrix([[ 8.00103145e-01, -3.31413574e-01,  5.00000000e-01],
             [ 4.61939766e-01, -1.91341716e-01, -8.66025404e-01],
             [ 3.82683432e-01,  9.23879533e-01,  6.12323400e-17]]),
     matrix([[ 5.27202862e-01, -6.87064147e-01,  5.00000000e-01],
             [ 3.04380715e-01, -3.96676670e-01, -8.66025404e-01],
             [ 7.93353340e-01,  6.08761429e-01,  6.12323400e-17]])]
    '''
    from numpy import eye
    tot = eye(4)
    rotaciones = [tot[:3, :3]]
    
    for tran in transformaciones:
        tot = tot*tran
        rotaciones.append(tot[:3, :3])
        
    return rotaciones

def arr_coordenados(posiciones):
    '''
    Esta función toma una lista (o arreglo) de posiciones y los convierte
    a tres listas, cada uno con las coordenadas x, y y z de todas las
    posiciones originales.
    
    >>> from robots.utilidades import DH, pos_articulaciones, arr_coordenados
    >>> from numpy import pi
    >>> l1, l2, l3 = 1, 0.7, 0.5
    >>> q1, q2, q3 = pi/6, pi/8, pi/6
    >>> A1 = DH([0, l1, pi/2, q1])
    >>> A2 = DH([l2, 0, 0, q2])
    >>> A3 = DH([l3, 0, 0, q3])
    >>> posiciones = pos_articulaciones([A1, A2, A3])
    >>> arr_coordenados(posiciones)
    
    ([0.0, 0.0, 0.5600722016338858, 0.8236736328167205],
     [0.0, 0.0, 0.32335783637895027, 0.47554819363113043],
     [0.0, 1.0, 1.2678784026555627, 1.6645550728011804])
    '''
    xs = [posicion.item(0) for posicion in posiciones]
    ys = [posicion.item(1) for posicion in posiciones]
    zs = [posicion.item(2) for posicion in posiciones]
    
    return xs, ys, zs

def grad_rad(grado):
    '''
    Esta función convierte grados a radianes
    '''
    from numpy import pi
    return grado*pi/180