#!/usr/bin/env python
# coding: utf-8

#  ***
#  <figure>
# <img src = "./Imagenes/Logo_Upc.png" alt = "Sol" style="width:550px"> </img>
# </figure>
# 
# ## <center>UNIVERSITAT POLITÈCNICA DE CATALUNYA - BARCELONATECH </center>
# ## <center>MASTER’S DEGREE IN CIVIL ENGINEERING </center>   
# 
# ## <center> ANÁLISIS Y PROCESO DE DATOS ARDUINO </center>
# ### <center>CÓDIGO      :     PYTHON </center>
# ### <center>LIBRERIAS   :     PYSERIAL </center>
# 
# ### <center>POR         <li> Londa Cañar Byron Fabian</li> </right>
# ### <center>             <li> Velásquez Huamán Victor Brian</li> </right>
# ### <center>FECHA       :     April, 2022</center>
# ***
# 
# 
# 
# >TEMA: Análisis e interpretación de datos registrados desde **Arduino** 
# 

# ***Importación de Librerias***

# In[1]:


import matplotlib.gridspec as gridspec
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import serial, time
import numpy as np
import Upcbasic 
import os
plt.style.use('bmh')
get_ipython().run_line_magic('matplotlib', 'notebook')


# ### 1.0 Definición del tiempo

# In[2]:


Tiempo_registro = 20                    #En segundos
List_Ds, List_Dh, List_dist, List_t0, List_t1, List_t2, List_t3, List_t4, List_tiempo, idtime = [],[],[],[],[],[],[],[],[],[]


# ### 2.0 Definición del espacio geometrico

# In[3]:


Coor_x = np.array([0, 0, -10, 10 ])
Coor_y = np.array([-7.5, 7.5, 0, 0])
Points = list(zip(Coor_x,Coor_y))

rRes = 0.5
xRange = np.arange(min(Coor_x),max(Coor_x) + rRes*10, rRes)
yRange = np.arange(min(Coor_y),max(Coor_y) + rRes*10, rRes)
gridX, gridY = np.meshgrid(xRange, yRange)

cm = plt.cm.get_cmap('YlOrRd')


# ### 3.0 Lectura de datos se arduino 1

# In[4]:


arduino = serial.Serial('COM3', 9600)
tiempo = 1  

fig = plt.figure(constrained_layout=True,figsize=(10,12))
gs = gridspec.GridSpec(5, 2, figure=fig, hspace=0.5)

Time_inicio = time.time()

while tiempo <= Tiempo_registro:
    #time.sleep(0.2)
    rawString = arduino.readline().strip()
    data = rawString.decode("utf-8").split(',')
    
    Temp_Ds = float(data[0])
    Temp_Dh = float(data[1])
    Distancia = float(data[2])
    Temp_A0 = float(data[3])
    Temp_A1 = float(data[4])
    Temp_A2 = float(data[5])
    Temp_A3 = float(data[6])
    
    List_Ds.append(Temp_Ds)
    List_Dh.append(Temp_Dh)
    List_dist.append(Distancia)
    List_t0.append(Temp_A0)
    List_t1.append(Temp_A1)
    List_t2.append(Temp_A2)
    List_t3.append(Temp_A3)
    List_tiempo.append(tiempo)
    
    fig.suptitle('$Registro\ de\ datos\ ' + ' P: '+ str(round(tiempo/Tiempo_registro*100,2)) +'\% $' , fontsize=14)
    
    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(List_tiempo, List_Ds,'ko--', linewidth=1.05, markersize=2.5, label=u'$\ max=' + str(max(List_t1))+'$')
    ax1.set_xlabel('$Tiempo - (seg)$')
    ax1.set_ylabel('$Temperatura $')
    ax1.set_title('$Sensor DS18B20$')
    #ax1.legend(loc="upper right")
    ax1.grid()
    
    ax2 = fig.add_subplot(gs[0,1])
    ax2.plot(List_tiempo, List_Dh,'go--', linewidth=1.05, markersize=2.5, label=u'$\ max=' + str(max(List_t1))+'$')
    ax2.set_xlabel('$Tiempo - (seg)$')
    ax2.set_ylabel('$Temperatura $')
    ax2.set_title('$Sensor DHT$')
    ax2.legend(loc="upper right")
    ax2.grid()
    
    ax7 = fig.add_subplot(gs[1,:])
    ax7.plot(List_tiempo, List_t0,'ro--', linewidth=1.05, markersize=2.5, label=u'$A0$')
    ax7.plot(List_tiempo, List_t1,'yo--', linewidth=1.05, markersize=2.5, label=u'$A1$')
    ax7.plot(List_tiempo, List_t2,'mo--', linewidth=1.05, markersize=2.5, label=u'$A2$')
    ax7.plot(List_tiempo, List_t3,'bo--', linewidth=1.05, markersize=2.5, label=u'$A3$')
    ax7.set_xlabel('$Tiempo - (seg)$')
    ax7.set_ylabel('$Temperatura$')
    ax7.set_title('$Analógicos $')
    ax7.legend(loc="upper right")
    ax7.grid()

    ax8 = fig.add_subplot(gs[2,:])
    Temp_circle = [Temp_A0, Temp_A1, Temp_A2, Temp_A3]
                   
    if Distancia >20:
        xd = -10
    else:
        xd = 10 - Distancia
        

    gra = ax8.scatter(Coor_x , Coor_y , s=20*np.array(Temp_circle), c=Temp_circle, alpha=0.5, vmin = min(Temp_circle), vmax =max(Temp_circle),cmap=cm)
    for i in range (0, len(Coor_x)):
        plt.annotate('$' + str(round(Temp_circle[i],2)) + '$', (Coor_x[i], Coor_y[i]))
        plt.annotate('$Td='+ str(Temp_Ds)+ '$', xy=(xd, 4), xytext=(xd*1.05, 4*1.05), arrowprops=dict(facecolor='k', shrink=0.002))
    ax8.set_xlabel('$x - (m)$')
    ax8.set_ylabel('$y - (m)$')
    ax8.set_title('$Analógicos\  y\  Digital $')
    plt.colorbar(gra)
    ax8.margins(0.1)
    ax8.grid()
    

    ax9 = fig.add_subplot(gs[3,:])
    gridTemp = griddata(Points, Temp_circle, (gridX,gridY), method='linear')
    grag = ax9.imshow(gridTemp)
    #Posicion en xd+10
    plt.annotate('$Td='+ str(Temp_Ds)+ '$', xy=(xd+10, 4), xytext=(xd*1.05, 4*1.05), arrowprops=dict(facecolor='k', shrink=0.002))
    ax9.set_xlabel('$Tiempo - (seg)$')
    ax9.set_ylabel('$Temperatura\ $')
    ax9.set_title('$Interpolacion IDW $')
    ax9.grid()
    plt.colorbar(grag)
    fig.canvas.draw()
    
    #Guardar imagenes
    if tiempo%5==0:
        fig.savefig("Imagenes\\Arduino" + str(tiempo) + ".png")
        idtime.append(tiempo)
    #fig.canvas.flush_events()
    
    fig.clf()
    tiempo+= 1
    
    
arduino.close()
Time_fin = time.time()


# In[10]:


arduino.close()


# In[11]:


Time_inicio-Time_fin


# ### 4.0 Análisis de datos registrados

# #### 4.1 Análisis de datos registrados del Sensor Temperatura DS18B20

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
Upcbasic.Grafica(List_tiempo,List_Ds,"Ds18b20")


# #### 4.2 Análisis de datos registrados del Sensor Temperatura DS18B20

# In[13]:


Upcbasic.Grafica(List_tiempo,List_Dh,"Dht")


# #### 4.3 Variabilidad entre sensores digitales

# In[14]:


Upcbasic.Grafica2T(List_tiempo, List_Ds, List_Dh, 'Sensor1', 'Sensor 2')


# #### 4.4 Variabilidad entre sensores analógicos

# In[15]:


Upcbasic.Grafica4T(List_tiempo, List_t0, List_t1, List_t2, List_t3,'A0', 'A1','A2','A3')


# #### 4.5 Generación de informe de datos históricos registrados

# In[16]:


data = [List_Ds]
Upcbasic.GraficaBoxPlot(data)


# In[17]:


Upcbasic.GraficaHistograma(List_Ds,"Ds18b20")
#Upcbasic.GraficaHistograma(List_Dh,"Dht")


# ### 5.0 Generación de informe de datos históricos registrados

# In[18]:


Moutput = np.zeros((len(List_tiempo),8))
Moutput[:,0] = List_tiempo
Moutput[:,1] = List_Ds
Moutput[:,2] = List_Dh
Moutput[:,3] = List_dist
Moutput[:,4] = List_t0
Moutput[:,5] = List_t1
Moutput[:,6] = List_t2
Moutput[:,7] = List_t3
idtime


# #### 5.1 Generacion reporte word

# In[19]:


Upcbasic.Reporte(Moutput,idtime)


# #### 5.2 Generación reporte excel 

# In[20]:


Upcbasic.ExportExcel(Moutput,'DataExp')


# In[21]:


ll = Moutput[:,7]
ll
