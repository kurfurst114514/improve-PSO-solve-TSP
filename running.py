from tsp import *
from pso import *
from sa import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df=pd.read_csv('att48.tsp',sep=" ", skiprows=6, header=None)
city_x = np.array(df[1][0:len(df)-2])
city_y = np.array(df[2][0:len(df)-2])
city_location = list(zip(city_x, city_y))
map=Map(100,100)
for i in range(len(city_location)-1):
    map.add_point(city_x[i],city_y[i])
plt.subplot(2,2,1)
for i in map.List_point:
    plt.scatter(i[0],i[1],s=8,c='red')
plt.subplot(2,2,3)
for i in map.List_point:
    plt.scatter(i[0],i[1],s=8,c='red')
plt.subplot(2,2,4)
for i in map.List_point:
    plt.scatter(i[0],i[1],s=8,c='red')

pso=PSO_1(map)
res=pso.pso_algo(0.9,1,1,50,50)
#print(res)
X=[]
Y=[]
for i in range(len(res)):
    X.append(res[i][0])
    Y.append(res[i][1])
plt.subplot(2,2,1)
plt.plot(np.array(X),np.array(Y)) 
plt.subplot(2,2,2)
plt.plot(fitlist)   

fitlist.clear()
pso=PSO_2(map)
res=pso.pso_algo(0.9,1,1,50,50)
#print(res)
X=[]
Y=[]
for i in range(len(res)):
    X.append(res[i][0])
    Y.append(res[i][1])
plt.subplot(2,2,3)
plt.plot(np.array(X),np.array(Y)) 
plt.subplot(2,2,2)
plt.plot(fitlist)   

fitlist.clear()
pso=PSO_3(map)
res=pso.pso_algo(0.9,0.6,1,50,50,2,0.98,10,0.00001)
#print(res)
X=[]
Y=[]
for i in range(len(res)):
    X.append(res[i][0])
    Y.append(res[i][1])
plt.subplot(2,2,4)
plt.plot(np.array(X),np.array(Y)) 
plt.subplot(2,2,2)
plt.plot(fitlist) 

plt.show()