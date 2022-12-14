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
NC,NV,tiempoAtencion,Comida=datos.split('\n')
Comida=Comida.split(',')
f.close()
simulacion=FondaModel(NC,NV,tiempoAtencion,Comida)
print(simulacion.schedule.agents[40].unique_id)
for i in range(10):
   simulacion.step()
print(simulacion.visitas)
print(simulacion.CantidadProductosVendidos)
print(simulacion.comida)
imagenes=[]
for j in range(10):
   imagenes.append(cv2.imread(str(j+1)+'.png'))
height, width  = imagenes[9].shape[:2]
video = cv2.VideoWriter('recorrido.wmv',cv2.VideoWriter_fourcc(*'mp4v'),2,(width,height))
for k in range(10):
   video.write(imagenes[k])
   if path.exists(str(k+1)+".png"):
    remove(str(k+1)+".png")
video.release()


plt.figure(1, figsize=(27,5))
data = pd.DataFrame(simulacion.CantidadProductosVendidos,
                    index=('Choripanes','Terremoto','Terremoto sin alcohol','Anticucho','Empanadas','Churros','Papas fritas','Cerveza','Chicha','Tsunami'))
total = data.sum(axis=1)
plt.bar(total.index, total)

plt.savefig('ProductosVendidos.png')

plt.figure(0, figsize=(27,5))

r = range(0, len(simulacion.visitas))
index = []
for n in r:
  index.append('Local: '+ str(n))

data = pd.DataFrame(simulacion.visitas,
                    index)
total = data.sum(axis=1)
plt.bar(total.index, total)

plt.savefig('ProductosVendidosPorLocal.png')
