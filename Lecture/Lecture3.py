import matplotlib
import numpy as np
import scipy

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches

plt.style.use('BME163')

figureHeight=2
figureWidth=4

plt.figure(figsize=(figureWidth, figureHeight))

panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

panel1=plt.axis([0.1,0.1,relativePanelWidth,relativePanelHeight])

blue=(0,0,1)
red=(1,0,0)
green=(0,1,0)
yellow=(1,1,0)
black=(0,0,0)
white=(1,1,1)

R=np.linspace(yellow[0],blue[0],101)
G=np.linspace(yellow[1],blue[1],101)
B=np.linspace(yellow[2],blue[2],101)

xList=np.arange(0,6.3,0.2)


for value in xList:
    xvalue=np.cos(value)
    yvalue=np.sin(value)
    panel1.plot(xvalue,yvalue,
                marker='o',
                markerfacecolor=(56/255,66/255,156/255),
                markeredgecolor='black',
                markersize=1,
                markeredgewidth=0,
                linewidth=0)
