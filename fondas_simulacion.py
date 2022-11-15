import mesa
import random
# Agentes: Consumidores y Locales de venta
def crearMatriz(x,y):
    matriz=[]
    for i in range(x):
        columna=[]
        for j in range(y):
            columna.append('')
        matriz.append(columna)
    return matriz
class ConsumidoresAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.deseoCompra = []
        self.tiempoEntrada=0
        self.tiempoSalida=0
        self.Inicial=[]
        self.rutasRecorridas=[]
        self.productosComprados=[]
        self.posicion=[]
    def setDatosIniciales(self):
        for i in range(len(self.model.comida)):
            self.deseoCompra.append(round(random.uniform(-1,1),2))
            self.tiempoEntrada=random.randint(1,self.model.horario*60)
            self.tiempoSalida=random.randint(self.tiempoEntrada,self.model.horario*60)
            self.Inicial=self.model.entradas[random.randint(0,2)]
    def step(self):
        print('funciono y soy el consumidor ', str(self.unique_id),'y mi entrada es:\n',self.Inicial)
        if (self.model.stepCounter>=self.model.horario):
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
    def setDatosIniciales(self):
        self.CantidadVendedores=random.randint(1,self.model.cantMaxVendedores)
        for i in range(len(self.model.comida)):
            self.CantidadProductosDisponibles.append(random.randint(10,100))
            self.oportunidadVenta.append(round(random.uniform(0,1),2))
        self.posicion=[random.randint(0,len(self.model.ambiente)-1), random.randint(0,len(self.model.ambiente[0])-1) ]
    def step(self):
        print('funciono y soy el local de venta ', str(self.unique_id),' y mi posicion es:',self.posicion)
    def atencion(self):
        pass


class FondaModel(mesa.Model):
    def __init__(self, NC, NV,cantMaxVendedores,tiempoAtencion,Comida):
        self.numConsumidores = int(NC)
        self.numLocalesVenta = int(NV)
        self.cantMaxVendedores=int(cantMaxVendedores)
        self.horario=13*60
        self.comida=Comida
        self.tiempoAtencion=int(tiempoAtencion)
        self.stepCounter=0
        self.ambiente=crearMatriz(9,49)
        self.entradas=[[4,0],[7,27],[6,48]]
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.numConsumidores):
            a= ConsumidoresAgent(i, self)
            a.setDatosIniciales()
            self.schedule.add(a)
        for j in range(self.numLocalesVenta):
            b=LocalVentaAgent(self.numConsumidores+j,self)
            b.setDatosIniciales()
            self.schedule.add(b)
    def step(self):
        self.stepCounter+=1
        self.schedule.step()
