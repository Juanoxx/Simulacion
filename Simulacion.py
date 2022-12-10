from fondas_simulacion import FondaModel
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
for i in range(13*60):
   simulacion.step()
print(simulacion.visitas)
print(simulacion.CantidadProductosVendidos)
imagenes=[]
for j in range(13*60):
   imagenes.append(cv2.imread(str(j+1)+'.png'))
height, width  = imagenes[9].shape[:2]
video = cv2.VideoWriter('recorrido.wmv',cv2.VideoWriter_fourcc(*'mp4v'),2,(width,height))
for k in range(13*60):
   video.write(imagenes[k])
   if path.exists(str(k+1)+".png"):
    remove(str(k+1)+".png")
video.release()