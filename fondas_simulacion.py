import mesa
import random
# Agentes: Consumidores y Locales de venta

class ConsumidoresAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.deseoCompra = []
        self.TiempoDisponible=0
        self.Inicial=[]
        self.rutasRecorridas=[]
        self.productosComprados=[]
    def setDatosIniciales(self,comida,Horario):
        for i in range(len(comida)):
            self.deseoCompra.append(round(random.uniform(-1,1),2))
            self.TiempoDisponible=random.randint(1,Horario*60)
    def step(self):
        print('funciono y soy el consumidor ', str(self.unique_id),'y mi tiempo es:\n',self.TiempoDisponible)

class LocalVentaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.CantidadVendedores = 1
        self.CantidadProductosDisponibles=[]
        self.oportunidadVenta=[]
    def setDatosIniciales(self,comida,cantMaxVendedores):
        self.CantidadVendedores=random.randint(1,cantMaxVendedores)
        for i in range(len(comida)):
            self.CantidadProductosDisponibles.append(random.randint(10,100))
            self.oportunidadVenta.append(round(random.uniform(0,1),2))
    def step(self):
        print('funciono y soy el local de venta ', str(self.unique_id),' y mi cantidad de vendedores es:',self.CantidadVendedores)
    def atencion(self):
        self.CantidadVendedores+=1


class FondaModel(mesa.Model):
    def __init__(self, NC, NV,Horario,cantMaxVendedores,Comida):
        self.numConsumidores = int(NC)
        self.numLocalesVenta = int(NV)
        self.cantMaxVendedores=int(cantMaxVendedores)
        self.horario=int(Horario)
        self.comida=Comida
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        for i in range(self.numConsumidores):
            a= ConsumidoresAgent(i, self)
            a.setDatosIniciales(self.comida,self.horario)
            self.schedule.add(a)
        for j in range(self.numLocalesVenta):
            b=LocalVentaAgent(self.numConsumidores+j,self)
            b.setDatosIniciales(self.comida,self.cantMaxVendedores)
            self.schedule.add(b)
    def step(self):
        self.schedule.step()
