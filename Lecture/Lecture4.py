import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np


plt.style.use('BME163')

figureHeight=2
figureWidth=7

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

# left,bottom, width,height
panel1=plt.axes([0.1,0.1,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.4,0.1,relativePanelWidth,relativePanelHeight])
panel3=plt.axes([0.7,0.1,relativePanelWidth,relativePanelHeight])


blue=(0,0,1)
red=(1,0,0)
green=(0,1,0)
yellow=(1,1,0)
black=(0,0,0)
white=(1,1,1)

R=np.linspace(yellow[0],blue[0],101)
G=np.linspace(yellow[1],blue[1],101)
B=np.linspace(yellow[2],blue[2],101)
print(R)


xList=np.random.normal(120,20,10000)
yList=np.random.normal(120,20,10000)

panel1.plot(xList,yList,
            marker='o',
            markerfacecolor=(56/255, 66/255, 156/255),
            markeredgecolor='black',
            markersize=2,
            markeredgewidth=0,
            linewidth=0,
            alpha=0.1)

#for i in range(0,len(xList),1):
#    xvalue=xList[i]
#    yvalue=yList[i]
#    panel2.plot(xvalue, yvalue,
#                marker='o',
#                markerfacecolor=(56/255, 66/255, 156/255),
#                markeredgecolor='black',
#                markersize=2,
#                markeredgewidth=0,
#                linewidth=0,
#                alpha=0.1)

for panel in [panel1, panel2, panel3]:
    panel.set_xlim(0,250)
    panel.set_ylim(0,250)

sizes=[]
colors=[]
for i in range(0,len(xList),1):
    xvalue=xList[i]
    yvalue=yList[i]
    sizes.append(xvalue)
    colors.append(xvalue/255, yvalue/255, 1-(xvalue/255))

panel3.scatter(xList,yList,
               s=sizes,
               facecolor='black',
               linewidth=0)

plt.savefig('Vollmers_Lecture4.png',dpi=300)
