import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import time
import scipy.stats as stats

plt.style.use('BME163')

figureHeight=4
figureWidth=11

plt.figure(figsize=(figureWidth,figureHeight))

panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

# left,bottom, width,height


#Mean,stdev,number of points
xList=np.random.normal(120,20,10000)
yList1=np.random.normal(120,20,10000)
yList2=xList
yList3=xList**10
yList4=np.sin(xList)

xShift=0.1
for yList in [yList1,yList2,yList3,yList4]:
    panel1=plt.axes([xShift,0.1,relativePanelWidth,relativePanelHeight])
    xShift+=0.20
    panel1.plot(xList,yList,
                marker='o',
                markerfacecolor=(56/255,66/255,156/255),
                markeredgecolor='black',
                markersize=2,
                markeredgewidth=0,
                linewidth=0,
                alpha=0.1)
    panel1.text(0,0,'r='+str(round(stats.spearmanr(xList,yList)[0],2)))
    print(round(stats.spearmanr(xList,yList)[0],2))
    panel1.set_xlim(0,max(xList))
    panel1.set_ylim(0,max(yList))




panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=True, labelright=False,
                   top=False, labeltop=True)

panel2=plt.axes([0.1,0.5,0.8,relativePanelHeight])

panel2.bar(3,np.average(yList1),width=0.5,
           facecolor='grey',
           edgecolor='black',
           linewidth=0.1,
           yerr=np.std(yList1))


plt.savefig('Vollmers_Lecture5.png',dpi=300)
