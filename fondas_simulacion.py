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

class LocalVentaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.CantidadVendedores = 1
        self.CantidadProductosDisponibles=[]
        self.oportunidadVenta=[]
    def atencion(self):
        self.CantidadVendedores+=1


class ConsumidoresModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N):
        self.num_agents = N
        # Create agents
        for i in range(self.num_agents):
            a = ConsumidoresAgent(i, self)


class LocalVentaModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N):
        self.num_agents = N

        # Create agents
        for i in range(self.num_agents):
            a = LocalVentaAgent(i, self)
local1=LocalVentaAgent(1,'modelo')
local1.atencion()
print(local1.CantidadVendedores)
