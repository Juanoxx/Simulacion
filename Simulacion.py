from fondas_simulacion import FondaModel
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2
from os import remove
from os import path
f = open ('datos.txt','r')
datos = f.read()
NC,NV,cantMaxVendedores,tiempoAtencion,Comida=datos.split('\n')
Comida=Comida.split(',')
f.close()
simulacion=FondaModel(NC,NV,cantMaxVendedores,tiempoAtencion,Comida)
print(simulacion.schedule.agents[40].unique_id)
for i in range(20):
   simulacion.step()
print(simulacion.visitas)
print(simulacion.CantidadProductosVendidos)
imagenes=[]
for j in range(20):
   imagenes.append(cv2.imread(str(j+1)+'.png'))
height, width  = imagenes[9].shape[:2]
video = cv2.VideoWriter('recorrido.wmv',cv2.VideoWriter_fourcc(*'mp4v'),2,(width,height))
for k in range(20):
   video.write(imagenes[k])
   if path.exists(str(k+1)+".png"):
    remove(str(k+1)+".png")
video.release()


plt.figure(1, figsize=(27,5))
data = pd.DataFrame(simulacion.CantidadProductosVendidos,
                    index= simulacion.comida)
total = data.sum(axis=1)
plt.bar(total.index, total)

plt.savefig('ProductosVendidos.png')

plt.figure(0, figsize=(27,5))

top_diez = []
index = []
for x in range(10):
    maximo = max(simulacion.visitas) 
    maxIndex  = simulacion.visitas.index(maximo)
    index.append('Local: '+str(maxIndex))
    top_diez.append(maximo)  
    top = simulacion.visitas.remove(maximo)  

data = pd.DataFrame(top_diez,
                    index)
total = data.sum(axis=1)
plt.bar(total.index, total)

plt.savefig('ProductosVendidosPorLocal.png')
