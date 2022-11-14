import mesa

# Agentes: Consumidores y Locales de venta

class ConsumidoresAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.deseoCompra = []
        self.TiempoDisponible=0
        self.Inicial=[]
        self.rutasRecorridas=[]
        self.productosComprados=[]
    def step(self):
        print('funciono y soy el consumidor ', str(self.unique_id))

class LocalVentaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.CantidadVendedores = 1
        self.CantidadProductosDisponibles=[]
        self.oportunidadVenta=[]
    def step(self):
        print('funciono y soy el local de venta ', str(self.unique_id))
    def atencion(self):
        self.CantidadVendedores+=1


class FondaModel(mesa.Model):
    def __init__(self, NC, NV):
        self.numConsumidores = NC
        self.numLocalesVenta = NV
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        for i in range(self.numConsumidores):
            a= ConsumidoresAgent(i, self)
            self.schedule.add(a)
        for j in range(self.numLocalesVenta):
            b=LocalVentaAgent(NC+j,self)
            self.schedule.add(b)
    def step(self):
        self.schedule.step()
