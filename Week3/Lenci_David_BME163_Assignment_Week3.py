import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import math
import numpy as np
import argparse

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-i', '--input_file', default='BME163_Input_Data_2.txt')
# parser.add_argument('-s', '--style_sheet', default='BME163')
parser.add_argument('-o', '--output_file', default='Lenci_David_BME163_Assignment_Week3.png')
args = parser.parse_args()

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
figureWidth = 2

plt.figure(figsize=(figureWidth, figureHeight))

mainPanelWidth = 1.33
mainPanelHeight = 1.33

relativePanelWidth = mainPanelWidth/figureWidth
relativePanelHeight = mainPanelHeight/figureHeight

panel1 = plt.axes([0.111, 0.111, relativePanelWidth, relativePanelHeight])

xlogFoldChange = []
ypValue = []
xfoldChange = []
geneName = []
for line in infile:
    splitLine = line.strip().split('\t')
    name = splitLine[0]
    if splitLine[1] == 'NA':
        splitLine[1] = 0
    if splitLine[2] == 'NA':
        splitLine[2] = 1
    geneName.append(name)
    xlogFoldChange.append(float(splitLine[1]))
    ypValue.append(-np.log10(float(splitLine[2])))
    xfoldChange.append(2**(float(splitLine[1])))

panel1.set_xlim(-12, 12)
panel1.set_ylim(0, 60)

panel1.set_xlabel(r'log$_\mathrm{2}$(fold change)')
panel1.set_ylabel(r'-log$_\mathrm{10}$(p-value)')

panel1.plot(xlogFoldChange, ypValue,
            marker='o',
            markerfacecolor='black',
            markeredgecolor='black',
            markersize=1.4,
            markeredgewidth=0,
            linewidth=0)

for i in range(0, len(xfoldChange), 1):
    if xfoldChange[i] > 10 and ypValue[i] > 8 or xfoldChange[i] < 0.1 and ypValue[i] > 8:
        panel1.plot(xlogFoldChange[i], ypValue[i],
                    marker='o',
                    markerfacecolor='red',
                    markeredgecolor='black',
                    markersize=1.4,
                    markeredgewidth=0,
                    linewidth=0)

    if xfoldChange[i] < 0.1 and ypValue[i] > 30:
        panel1.text(xlogFoldChange[i]-0.25, ypValue[i],
                    geneName[i],
                    va='center',
                    ha='right',
                    fontsize=4)

plt.savefig(outputFile, dpi=600)
