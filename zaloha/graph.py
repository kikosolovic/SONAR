import numpy as np
import matplotlib.pyplot as plt
import random
xi = []
yi = []
elevationi = []
p = 0
h = -1
with open('pleso.txt', 'r') as file:
    for line in file:
        if line != "\n":
            data = [d.strip() for d in line.split(",")]
            if data[2+p]:
                xi.append(float(data[1+p]))
                yi.append(float(data[0+p]))
                elevationi.append(float(data[2+p]))

minx = min(xi)
miny = min(yi)
mine = min(elevationi)
gpstoMeter = 111319.49079327358 #1 stupen 
xi= [(i - minx)*gpstoMeter for i in xi]
yi= [(i - miny)*gpstoMeter for i in yi]
proportion = (max(xi)/max(elevationi) + max(yi)/max(elevationi))/2
elevationi= [((i-mine)/proportion)*h for i in elevationi]

x = np.array(xi)
y = np.array(yi)
elevation = np.array(elevationi)

z = elevation


fig = plt.figure(num="Dno")
ax = fig.add_subplot(111, projection="3d")

scatter = ax.scatter(x, y, elevation, c=elevation, cmap='terrain_r', marker='')

ax.plot_trisurf(x, y, elevation, cmap='terrain', edgecolor='none')
cbar = plt.colorbar(scatter, ax=ax, label='Hĺbka')
cbar.ax.invert_yaxis()
cbar.ax.invert_xaxis()
plt.show()
