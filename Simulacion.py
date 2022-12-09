from fondas_simulacion import FondaModel
f = open ('datos.txt','r')
datos = f.read()
NC,NV,cantMaxVendedores,tiempoAtencion,Comida=datos.split('\n')
Comida=Comida.split(',')
f.close()
simulacion=FondaModel(NC,NV,cantMaxVendedores,tiempoAtencion,Comida)
simulacion.step()
for i in range(1000):
   simulacion.step()
#for i in range(simulacion.schedule.get_agent_count()):
   # print(simulacion.schedule.agents[i].unique_id)