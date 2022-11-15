from fondas_simulacion import FondaModel
f = open ('datos.txt','r')
datos = f.read()
print(datos.split('\n'))
NC,NV,cantMaxVendedores,tiempoAtencion,Comida=datos.split('\n')
Comida=Comida.split(',')
f.close()
simulacion=FondaModel(NC,NV,cantMaxVendedores,tiempoAtencion,Comida)
print(simulacion.horario)
for i in range(len(simulacion.ambiente)):
    print(simulacion.ambiente[0])
simulacion.step()