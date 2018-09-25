def rotacion_geom_3d(pathpatch, rotacion):
    '''
    Esta función toma un objeto asociado a una gráfica de matplotlib y aplica una matriz
    de rotación al objeto (convirtiendolo a tres dimensiones).
    
    >>> from robots.utilidades import DH
    >>> from robots.graficacion import rotacion_geom_3d
    >>> from matplotlib.pyplot import figure
    >>> from matplotlib.patches import Wedge
    >>> from numpy import pi
    >>> fig = figure()
    >>> ax = fig.gca()
    >>> marcador = Wedge([0, 0], 0.2, 0, mag*180/pi)
    >>> ax.add_patch(marcador)
    >>> ori = DH([0, 0, pi/2, pi/3])[:3, :3]
    >>> rotacion_geom_3d(marcador, array(ori))
    '''
    from numpy import array, eye, dot
    from mpl_toolkits.mplot3d import art3d
    
    path = pathpatch.get_path()
    trans = pathpatch.get_patch_transform()
    path = trans.transform_path(path)

    pathpatch.__class__ = art3d.PathPatch3D
    pathpatch._code3d = path.codes
    pathpatch._facecolor3d = pathpatch.get_facecolor  

    verts = path.vertices

    pathpatch._segment3d = array([dot(rotacion, (x, y, 0)) for x, y in verts])
    
def traslacion_geom_3d(pathpatch, delta):
    '''
    Esta función toma un objeto asociado a una gráfica de matplotlib y aplica una
    traslación dada como un arreglo de numpy (el objeto tiene que ser de tres
    dimensiones).
    
    >>> from robots.utilidades import DH
    >>> from robots.graficacion import rotacion_geom_3d
    >>> from matplotlib.pyplot import figure
    >>> from matplotlib.patches import Wedge
    >>> from numpy import pi
    >>> fig = figure()
    >>> ax = fig.gca()
    >>> marcador = Wedge([0, 0], 0.2, 0, mag*180/pi)
    >>> ax.add_patch(marcador)
    >>> ori = DH([0, 0, pi/2, pi/3])[:3, :3]
    >>> rotacion_geom_3d(marcador, array(ori))
    >>> traslacion_geom_3d(marcador, array([0,0,1]))
    '''
    pathpatch._segment3d += delta
    
def eje_rotacional(eje, pos, ori, mag):
    '''
    Esta función toma un eje de una grafica de matplotlib y dibuja un indicador del grado
    de libertad rotacional normal al eje de rotacion.
    
    >>> from robots.utilidades import DH
    >>> from robots.graficacion import rotacion_geom_3d
    >>> from matplotlib.pyplot import figure
    >>> from numpy import pi
    >>> fig = figure()
    >>> ax = fig.gca()
    >>> ori = DH([0, 0, pi/2, pi/3])[:3, :3]
    >>> pos = DH([0, 0, pi/2, pi/3])[:3, 3:]
    >>> eje_rotacional(ax, pos, ori, pi/3)
    '''
    from numpy import pi, array
    from matplotlib.patches import Wedge
    
    marcador = Wedge([0, 0], 0.2, 0, mag*180/pi, alpha=0.8)
    eje.add_patch(marcador)
    rotacion_geom_3d(marcador, array(ori))
    traslacion_geom_3d(marcador, array(pos.T.tolist()))
    
    marcador = Wedge([0, 0], 0.2, mag*180/pi, 360, ec="None", color="k", alpha=0.2)
    eje.add_patch(marcador)
    rotacion_geom_3d(marcador, array(ori))
    traslacion_geom_3d(marcador, array(pos.T.tolist()))
    
def configuracion_grafica(eje):
    '''
    Esta función configura el eje de una gráfica para desplegar consistentemente un estilo.
    
    >>> from robots.utilidades import DH
    >>> from robots.graficacion import rotacion_geom_3d
    >>> from matplotlib.pyplot import figure
    >>> from numpy import pi
    >>> fig = figure()
    >>> ax = fig.gca()
    >>> configuracion_grafica(ax)
    '''
    eje.set_facecolor((1.0, 1.0, 1.0, 1.0))
    #eje._axis3don = False
    eje.view_init(elev=30., azim=45.)
    eje.set_xlim3d([-0.6, 0.6])
    eje.set_ylim3d([-0.6, 0.6])
    eje.set_zlim3d([-0.1, 1.1])