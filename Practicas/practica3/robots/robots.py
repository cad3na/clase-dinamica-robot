class Robot:
    def __init__(self, nombre, configuracion, longitudes, angulos, parametros, modo):
        
        self.nombre = nombre
        self.ngdl = len(configuracion)
        self.configuracion = configuracion
        self.pos_art = [0 for car in configuracion]
        self.longs = longitudes
        self.angs = angulos
        self.esp_parametros = parametros
        self.actualizar_estado()
        self.modo = modo
        
        if modo == "cinematico":
            self.puerto_referencias = "5551"
        if modo == "dinamico":
            self.puerto_referencias = "5551"
            self.puerto_sensores = "5552"
        if modo == "matematico":
            self.puerto_transformaciones = "5553"
        
    def visualizador(self):
        from matplotlib.pyplot import figure
        from mpl_toolkits.mplot3d import Axes3D
        from time import time, sleep
        
        from .utilidades import arr_coordenados
        from .graficacion import configuracion_grafica, eje_rotacional

        fig = figure(figsize=(4, 4))
        ax = Axes3D(fig)
        configuracion_grafica(ax)

        xs, ys, zs = arr_coordenados(self.pos_tar)

        linea, = ax.plot(xs, ys, zs, "k", solid_joinstyle="round")

        fig.canvas.draw()

        while True:
            try:
                self.actualizar_pos_art()

            except KeyboardInterrupt:
                break

            except:
                self.actualizar_estado()
                xs, ys, zs = arr_coordenados(self.pos_tar)

                ax.clear()
                configuracion_grafica(ax)
                linea, = ax.plot(xs, ys, zs, "k", solid_joinstyle="round")
                
                for i, c in enumerate(self.configuracion):
                    if c == "R":
                        eje_rotacional(ax, self.pos_tar[i], self.rot_tar[i], self.pos_art[i])
                    else:
                        raise NotImplementedError

                fig.canvas.draw()
                sleep(0.00001)
        
    def actualizar_param(self):
        parametros = []
        for param in self.esp_parametros:
            ps = [0 if p==0 else
                  self.longs[int(p[1])-1] if p[0]=="l" else
                  self.angs[int(p[1])-1] if p[0]=="θ" else
                  self.pos_art[int(p[1])-1] for p in param]
            parametros.append(ps)
        self.parametros = parametros
        
    def actualizar_estado(self):
        self.actualizar_param()
        self.actualizar_trans()
        self.actualizar_pos_tar()
        self.actualizar_ori_tar()
        
    def actualizar_pos_art(self):
        from zmq import NOBLOCK
        from msgpack import unpackb
        from numpy import radians
        
        if self.modo == "cinematico":
            m_pos_art = unpackb(self.socket_referencias.recv(flags=NOBLOCK))
            self.pos_art = radians(m_pos_art).tolist()
        if self.modo == "dinamico":
            raise NotImplementedError
        if self.modo == "matematico":
            raise NotImplementedError
        
    def actualizar_pos_tar(self):
        from .utilidades import pos_articulaciones
        
        self.pos_tar = pos_articulaciones(self.transformaciones)
        
    def actualizar_ori_tar(self):
        from .utilidades import ori_articulaciones
        
        self.rot_tar = ori_articulaciones(self.transformaciones)
        
    def actualizar_trans(self):
        from .utilidades import DH
        
        transformaciones = []
        for param in self.parametros:
            transformaciones.append(DH(param))
            
        self.transformaciones = transformaciones
        
    def inicializar_puertos(self):
        from zmq import Context, SUB, SUBSCRIBE
        
        if self.modo == "cinematico":
            context = Context()
            self.socket_referencias = context.socket(SUB)
            self.socket_referencias.connect("tcp://localhost:" + self.puerto_referencias)
            self.socket_referencias.setsockopt(SUBSCRIBE, b'')
        if self.modo == "dinamico":
            raise NotImplementedError
        if self.modo == "matematico":
            raise NotImplementedError