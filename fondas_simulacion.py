import mesa
import random
import time
# Agentes: Consumidores y Locales de venta
def crearMatriz(x,y):
    matriz=[]
    for i in range(x):
        columna=[]
        for j in range(y):
            columna.append(0)
        matriz.append(columna)
    return matriz
class ConsumidoresAgent(mesa.Agent):
    movimientos=[[1,1],[1,0],[0,1],[-1,-1],[-1,0],[0,-1],[1,-1],[-1,1]]
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.deseoCompra = []
        self.tiempoEntrada=0
        self.tiempoSalida=0
        self.Inicial=[]
        self.ultimaPos=[]
        self.productosComprados=[]
        self.posicion=[0,0]
        self.cantidadPersonas=0
        self.espera=0
        #agregar numero de personas por agente
    def setDatosIniciales(self):
        for i in range(len(self.model.comida)):
            self.deseoCompra.append(round(random.uniform(-1,1),2))
            self.tiempoEntrada=random.randint(1,self.model.horario)
            self.tiempoSalida=random.randint(self.tiempoEntrada,self.model.horario)
            self.Inicial=self.model.entradas[random.randint(0,2)]
            self.cantidadPersonas=random.randint(1,5)
            #self.posicion=self.Inicial
        print(self.tiempoEntrada,"este es mi tiempo de entrada")
    def moverse(self):
        mov=self.movimientos[random.randint(0,7)]
        nuevaPos=[(self.posicion[0]+mov[0]),(self.posicion[1]+mov[1])]
        if (nuevaPos[0]>8 or nuevaPos[0]<0 or nuevaPos[1]>48 or nuevaPos[1]<0 or nuevaPos==self.ultimaPos):
            return self.moverse()
        print(self.posicion,'vieja pos')
        print(mov,'movimiento')
        print(nuevaPos,'nueva pos')
        self.model.ambienteCantidadPersonas[nuevaPos[0]][nuevaPos[1]] += self.cantidadPersonas
        self.model.ambienteCantidadPersonas[self.posicion[0]][self.posicion[1]] -= self.cantidadPersonas
        self.ultimaPos=self.posicion
        self.posicion=nuevaPos
        
    def step(self):
        #print('funciono y soy el consumidor ', str(self.unique_id),'y mi entrada es:\n',self.Inicial)
        if(self.model.stepCounter==self.tiempoEntrada):
            self.posicion=self.Inicial
            self.model.ambienteCantidadPersonas[self.posicion[0]][self.posicion[1]] += self.cantidadPersonas
            print('Soy el consumidor ', str(self.unique_id),'y mi entrada es:\n',self.Inicial)
        if(self.model.stepCounter>self.tiempoEntrada and self.model.stepCounter<self.tiempoSalida):
            print('Soy el consumidor ', str(self.unique_id),'y me muevo')
            self.moverse()
        if (self.model.stepCounter>=self.model.horario or self.model.stepCounter==self.tiempoSalida):
            self.salir()
    def salir(self):
        print('Tengo que salir')
class LocalVentaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.CantidadVendedores = 1
        self.CantidadProductosDisponibles=[]
        self.oportunidadVenta=[]
        self.posicion=[]
        #Tamaño maximo de fila es 10.
        self.fila=0
        self.visitas=0
    def setDatosIniciales(self):
        self.CantidadVendedores=random.randint(1,self.model.cantMaxVendedores)
        for i in range(len(self.model.comida)):
            self.CantidadProductosDisponibles.append(random.randint(0,100))
            self.oportunidadVenta.append(round(random.uniform(0,1),2))
        self.posicionar()
    def posicionar(self):
        self.posicion=[random.randint(0,len(self.model.ambiente)-1), random.randint(0,len(self.model.ambiente[0])-1)]
        if (self.model.ambiente[self.posicion[0]][self.posicion[1]] == 0):
            self.model.ambiente[self.posicion[0]][self.posicion[1]]=self.unique_id
        else:
            self.posicionar()
    def step(self):
        pass
        #print('funciono y soy el local de venta ', str(self.unique_id),' y mi posicion es:',self.posicion)
    def atencion(self):
        pass


class FondaModel(mesa.Model):
    def __init__(self, NC, NV,cantMaxVendedores,tiempoAtencion,Comida):
        self.numConsumidores = int(NC)
        self.numLocalesVenta = int(NV)
        self.cantMaxVendedores=int(cantMaxVendedores)
        self.horario=1000#13*60
        self.comida=Comida
        self.tiempoAtencion=int(tiempoAtencion)
        self.stepCounter=0
        self.ambiente=crearMatriz(9,49)
        self.ambienteCantidadPersonas=crearMatriz(9,49)
        self.entradas=[[4,0],[8,27],[6,48]]
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.numConsumidores):
            a= ConsumidoresAgent(i, self)
            a.setDatosIniciales()
            self.schedule.add(a)
        for j in range(self.numLocalesVenta):
            b=LocalVentaAgent(self.numConsumidores+j,self)
            b.setDatosIniciales()
            self.schedule.add(b)
        input("Press Enter to continue...")
    def step(self):
        self.stepCounter+=1
        self.schedule.step()
        for i in range(len(self.ambienteCantidadPersonas)):
            print('\n')
            print(self.ambienteCantidadPersonas[i])
        print(self.stepCounter)
        input("Press Enter to continue...")
        
