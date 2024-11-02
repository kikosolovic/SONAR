import numpy as np
import matplotlib.pyplot as plt
xi = []
yi = []
elevationi = []
# posun iindexu dat
p = 0
# polariita hlbky 
h = -1
# odchylka medianu
odchylka = 1.3

MinimalDepth = 0
MaximalDepth = 15
with open('belianske.txt', 'r') as file:
    for line in file:
        if line != "\n":
            data = [d.strip() for d in line.split(",")]
            if data[2+p]:
                xi.append(float(data[1+p]))
                yi.append(float(data[0+p]))
                elevationi.append(float(data[2+p]))


# check for odchzlka 
toDelete = []
lenght = len(elevationi)
for id in range(lenght):
    if id > 0 and id < lenght-1 :
        avg =(elevationi[id-1] + elevationi[id+1])/2
        if max(elevationi[id],avg)/min(elevationi[id],avg) < odchylka:
            # continue
            if(MinimalDepth < elevationi[id] < MaximalDepth):
                continue
    toDelete.append(id)

for shift, id in enumerate(toDelete):
    elevationi.pop(id - shift)
    xi.pop(id - shift)
    yi.pop(id - shift)


xi.append(0)
yi.append(0)
elevationi.append(100)


minx = min(xi)
miny = min(yi)
mine = min(elevationi)
gpstoMeter = 111319.49079327358 #1 stupen 
xi= [(i - minx)*gpstoMeter for i in xi]
yi= [(i - miny)*gpstoMeter for i in yi]
# proportion = (max(xi)/max(elevationi) + max(yi)/max(elevationi))/2
proportion = 1
elevationi= [((i-mine)/proportion)*h for i in elevationi]

x = np.array(xi)
y = np.array(yi)
elevation = np.array(elevationi)

z = elevation


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
colormap = 'ocean'
scatter = ax.scatter(x, y, elevation,c=elevation, cmap=colormap, marker='')

ax.plot_trisurf(x, y, elevation, cmap=colormap, edgecolor='none')
cbar = plt.colorbar(scatter, ax=ax, label='Hlbka')

plt.show()
