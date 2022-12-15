import mesa
import random
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
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
        self.posicion=[0,0]
        self.cantidadPersonas=0
        self.espera=0
        self.enFonda=False
        #agregar numero de personas por agente
    def setDatosIniciales(self):
        for i in range(len(self.model.comida)):
            self.deseoCompra.append([round(random.uniform(-1,1),2),i])
            self.tiempoEntrada=random.randint(1,self.model.horario)
            self.tiempoSalida=random.randint(self.tiempoEntrada,self.model.horario)
            self.Inicial=self.model.entradas[random.randint(0,2)]
            self.cantidadPersonas=random.randint(1,5)
            #self.posicion=self.Inicial
        #print(self.tiempoEntrada,"este es mi tiempo de entrada")
    
        
    def step(self):
        #print('funciono y soy el consumidor ', str(self.unique_id),'y mi entrada es:\n',self.Inicial)
        if(self.model.stepCounter==self.tiempoEntrada):
            self.entrar()
            #print('Soy el consumidor ', str(self.unique_id),'y mi entrada es:\n',self.Inicial)
        elif(self.model.stepCounter>self.tiempoEntrada and self.model.stepCounter<self.tiempoSalida):
            #print('Soy el consumidor ', str(self.unique_id),'y me muevo')
            if(self.model.ambiente[self.posicion[0]][self.posicion[1]]!=0  ):
                #print("debug 1",self.unique_id)
                if(self.espera!=0):
                    #print("debug espera")
                    if(self.espera==1):
                        #print("debug 2",self.unique_id)
                        puesto=self.model.ambiente[self.posicion[0]][self.posicion[1]]
                        self.model.schedule.agents[puesto].fila-=1
                        self.comprar()
                        self.moverse()
                        
                    else:
                        #print("debug 3",self.unique_id)
                        self.espera-=1
                else:
                    #print("debug else",self.unique_id)
                    puesto=self.model.ambiente[self.posicion[0]][self.posicion[1]]
                    #print(puesto)
                    if(self.model.schedule.agents[puesto].fila < 10):                        
                        self.espera=self.model.tiempoAtencion
                        self.model.visitas[puesto-self.model.numConsumidores]+=1
                        self.model.schedule.agents[puesto].fila+=1
                    else:
                        self.moverse()
            else:
                self.moverse()            
        elif ( (self.model.stepCounter==self.model.horario or self.model.stepCounter==self.tiempoSalida) and self.enFonda):
            self.salir()
    def comprar(self):
        self.deseoCompra.sort(reverse=True)
        puesto=self.model.ambiente[self.posicion[0]][self.posicion[1]]
        counter=0
        while(True):
            if(self.model.schedule.agents[puesto].CantidadProductosDisponibles[self.deseoCompra[counter][1]]>self.cantidadPersonas):
                venta=round(random.uniform(0,1),2)
                #print("venta:", venta, "\noportunidad:",self.model.schedule.agents[puesto].oportunidadVenta[self.deseoCompra[counter][1]])
                if(venta<=self.model.schedule.agents[puesto].oportunidadVenta[self.deseoCompra[counter][1]]):
                    self.model.schedule.agents[puesto].CantidadProductosDisponibles[self.deseoCompra[counter][1]]-=self.cantidadPersonas
                    self.model.CantidadProductosVendidos[self.deseoCompra[counter][1]]+=self.cantidadPersonas
                    self.deseoCompra[counter][0]=-1.1
                    #print("lo compro")
                break
            counter+=1
            if(counter==len(self.model.comida)):
                #print("no compro")
                break
    def moverse(self):
        mov=self.movimientos[random.randint(0,7)]
        nuevaPos=[(self.posicion[0]+mov[0]),(self.posicion[1]+mov[1])]
        if (nuevaPos[0]>8 or nuevaPos[0]<0 or nuevaPos[1]>48 or nuevaPos[1]<0 or nuevaPos==self.ultimaPos):
            return self.moverse()
        #print(self.posicion,'vieja pos')
        #print(mov,'movimiento')
        #print(nuevaPos,'nueva pos')
        self.model.ambienteCantidadPersonas[nuevaPos[0]][nuevaPos[1]] += self.cantidadPersonas
        self.model.ambienteCantidadPersonas[self.posicion[0]][self.posicion[1]] -= self.cantidadPersonas
        self.ultimaPos=self.posicion
        self.posicion=nuevaPos
    def entrar(self):
        self.posicion=self.Inicial
        self.model.ambienteCantidadPersonas[self.posicion[0]][self.posicion[1]] += self.cantidadPersonas
        self.enFonda=True
    def salir(self):
        self.enFonda=False
        self.model.ambienteCantidadPersonas[self.posicion[0]][self.posicion[1]] -= self.cantidadPersonas
class LocalVentaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.CantidadProductosDisponibles=[]
        self.oportunidadVenta=[]
        self.posicion=[]
        #Tamaño maximo de fila es 10.
        self.fila=0
    def setDatosIniciales(self):
        for i in range(len(self.model.comida)):
            self.CantidadProductosDisponibles.append(random.randint(0,100))
            self.oportunidadVenta.append(round(random.uniform(0,1),2))
        self.posicionar()
    def posicionar(self):
        self.posicion=[random.randint(0,len(self.model.ambiente)-1), random.randint(0,len(self.model.ambiente[0])-1)]
        for i in range(len(self.model.entradas)):
            if (self.posicion==self.model.entradas[i]):
                return self.posicionar()
        if (self.model.ambiente[self.posicion[0]][self.posicion[1]] == 0):
            self.model.ambiente[self.posicion[0]][self.posicion[1]]=self.unique_id
        else:
            return self.posicionar()
    def step(self):
        pass
        #print('funciono y soy el local de venta ', str(self.unique_id),' y mi posicion es:',self.posicion)
    

def human_format(x,y, matriz):
    
    newMatriz=[]

    for i in range(x):
        columna=[]
        for j in range(y):
            num = matriz[i][j]/1000
            columna.append(num)
        newMatriz.append(columna)

    return newMatriz


class FondaModel(mesa.Model):
    def __init__(self, NC, NV,tiempoAtencion,Comida):
        self.numConsumidores = int(NC)
        self.numLocalesVenta = int(NV)
        self.horario=100
        self.comida=Comida
        self.tiempoAtencion=int(tiempoAtencion)
        self.stepCounter=0
        self.ambiente=crearMatriz(9,49)
        self.ambienteCantidadPersonas=crearMatriz(9,49)
        self.entradas=[[4,0],[8,27],[6,48]]        
        self.CantidadProductosVendidos=[]
        self.visitas=[]
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.numConsumidores):
            a= ConsumidoresAgent(i, self)
            a.setDatosIniciales()
            self.schedule.add(a)
        for j in range(self.numLocalesVenta):
            b=LocalVentaAgent(self.numConsumidores+j,self)
            b.setDatosIniciales()
            self.schedule.add(b)
            self.visitas.append(0)
            #print(b.unique_id)      
        
        for k in range(len(self.comida)):
            self.CantidadProductosVendidos.append(0)
        mapa = pd.DataFrame(
            self.ambiente
        )
        print(mapa)
        input("Press Enter to continue...")
    def step(self):
        self.stepCounter+=1
        self.schedule.step()
        print(self.stepCounter)
        print(human_format(9,49,self.ambienteCantidadPersonas))
        print(self.ambienteCantidadPersonas)
        usuarios = pd.DataFrame(
            self.ambienteCantidadPersonas
        )

        plt.figure(self.stepCounter, figsize=(27,5))
        ax = sns.heatmap(usuarios, cmap = "Blues")
        plt.savefig(str(self.stepCounter)+'.png')
        fig=plt.figure()
        matplotlib.use("Agg")
        #input("Press Enter to continue..."