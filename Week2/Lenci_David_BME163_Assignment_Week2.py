import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import math
import numpy as np
import argparse

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-i', '--input_file', default='BME163_Input_Data_1.txt')
# parser.add_argument('-s', '--style_sheet', default='BME163')
parser.add_argument('-o', '--output_file', default='Lenci_David_BME163_Assignment_Week2')
args = parser.parse_args()

plt.rcParams.update({'font.size': 8})

# Argument Variables:
inputFile = args.input_file
infile = open(inputFile, 'r')
outputFile = args.output_file
#styleSheet = args.style_sheet

# Style sheet:
# plt.style.use(styleSheet)
plt.style.use('BME163')
# Figure/Panel Dimensions
figureHeight = 2
figureWidth = 5

plt.figure(figsize=(figureWidth, figureHeight))

# Main Panel:
mainPanelWidth = 1
mainPanelHeight = 1
secPanelWidth = 0.25
secPanelHeight = 0.25

relativeMainPanelWidth = mainPanelWidth/figureWidth
relativeMainPanelHeight = mainPanelHeight/figureHeight
relativeSecPanelWidth = secPanelWidth/figureWidth
relativeSecPanelHeight = secPanelHeight/figureHeight


panel1 = plt.axes([0.14, 0.15, relativeMainPanelWidth, relativeMainPanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel1.set_xlim(0, 15)
panel1.set_ylim(0, 15)

panel1x = plt.axes([0.14, 0.685, relativeMainPanelWidth, relativeSecPanelHeight])

panel1x.tick_params(bottom=False, labelbottom=False,
                    left=True, labelleft=True,
                    right=False, labelright=False,
                    top=False, labeltop=False)
panel1x.set_xlim(0, 15)
panel1x.set_ylim(0, 20)

panel1y = plt.axes([0.076, 0.15, relativeSecPanelWidth, relativeMainPanelHeight])

panel1y.tick_params(bottom=True, labelbottom=True,
                    left=True, labelleft=True,
                    right=False, labelright=False,
                    top=False, labeltop=False)
panel1y.set_xlim(20, 0)
panel1y.set_ylim(0, 15)

xListLog2 = []
yListLog2 = []
for line in infile:
    splitLine = line.strip().split('\t')
    name = splitLine[0]
    xListLog2.append(math.log2(int(splitLine[1])+1))
    yListLog2.append(math.log2(int(splitLine[2])+1))

panel1.plot(xListLog2, yListLog2,
            marker='o',
            markerfacecolor='black',
            markeredgecolor='black',
            markersize=1.45,
            markeredgewidth=0,
            linewidth=0,
            alpha=0.1)


xHisto, xbins = np.histogram(xListLog2, np.arange(0, 15, 0.5))

for i in range(0, len(xHisto), 1):
    bottom = 0
    left = xbins[i]
    width = xbins[i+1]-left
    height = math.log2(xHisto[i]+1)
    rectangle = mplpatches.Rectangle([left, bottom], width, height,
                                     facecolor=(0.5, 0.5, 0.5),
                                     edgecolor='black',
                                     linewidth=0.1)
    panel1x.add_patch(rectangle)

yHisto, ybins = np.histogram(yListLog2, np.arange(0, 15, 0.5))


for i in range(0, len(yHisto), 1):
    bottom = 0
    left = ybins[i]
    width = ybins[i+1]-left
    height = math.log2(yHisto[i]+1)
    rectangle = mplpatches.Rectangle([bottom, left], height, width,
                                     facecolor=(0.5, 0.5, 0.5),
                                     edgecolor='black',
                                     linewidth=0.1)
    panel1y.add_patch(rectangle)

plt.savefig(outputFile, dpi=600)
