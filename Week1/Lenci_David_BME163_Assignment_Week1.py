#David Lenci_
#Assignment 1
#Code for generating template figures.

#Import necessary packages:
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import math

#Set style:
plt.style.use('BME163')

#Figure dimensions:
figureHeight=2
figureWidth=3.42

plt.figure(figsize=(figureWidth,figureHeight))

#Panel Dimensions:
panelWidth=1
panelHeight=1

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

# left,bottom, width,height
panel1=plt.axes([0.1,0.2,relativePanelWidth,relativePanelHeight])
panel2=plt.axes([0.55,0.2,relativePanelWidth,relativePanelHeight])

#color tuples:
blue=(0,0,1)
red=(1,0,0)
green=(0,1,0)
yellow=(1,1,0)
black=(0,0,0)
white=(1,1,1)

#Generate top right quadrant for unit circle:
xList=np.linspace(0,(math.pi/2),25)

#For loop for generating exact x and y values
#Then plots top right quadrant of unit circle
#where the x coordinate determines color.
for value in xList:
    xvalue=np.cos(value)
    yvalue=np.sin(value)
    panel1.plot(xvalue,yvalue,
                marker='o',
                markerfacecolor=(xvalue,xvalue,xvalue),
                markeredgecolor='black',
                markersize=2,
                markeredgewidth=0,
                linewidth=0)
panel1.tick_params(axis='both',bottom=False,top=False,left=False,labelbottom=False,labelleft=False )

#For loop for generating 100 rectangles within
#a 1 by 1 block. The color of the rectangles is
#then determined by the x and y coordinates.
for j in np.arange(0,1,0.1):
    for i in np.arange(0,1,0.1):
        rectangle=mplpatches.Rectangle([j,i],0.1,0.1,
                                facecolor=(j,i,1),
                                edgecolor='black',
                                linewidth=1)
        panel2.add_patch(rectangle)
panel2.set_xlim(0,1)
panel2.set_ylim(0,1)
panel2.tick_params(axis='both',bottom=False,top=False,left=False,labelbottom=False,labelleft=False )

#Save the figure:
plt.savefig('Lenci_David_BME163_Assignment_Week1.png',dpi=600)
