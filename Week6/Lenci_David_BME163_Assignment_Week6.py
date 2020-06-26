import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-i', '--input_file', default='BME163_Input_Data_4.txt')
# parser.add_argument('-s', '--style_sheet', default='BME163')
parser.add_argument('-o', '--output_file',
                    default='Lenci_David_BME163_Assignment_Week6.png')
args = parser.parse_args()

# Argument Variables:
inputFile = args.input_file
infile = open(inputFile, 'r')
outputFile = args.output_file
# styleSheet = args.style_sheet

# Style sheet:
# plt.style.use(styleSheet)
plt.style.use('BME163')
# Figure/Panel Dimensions
figureHeight = 3
figureWidth = 5

plt.figure(figsize=(figureWidth, figureHeight))

mainPanelWidth = 0.75
mainPanelHeight = 2.5

relativePanelWidth = mainPanelWidth/figureWidth
relativePanelHeight = mainPanelHeight/figureHeight

panel1 = plt.axes([0.10, 0.10, relativePanelWidth, relativePanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)

panel1.set_xlim(0, 16)
panel1.set_ylim(0, 1262)

panel1.set_xlabel('CT')
panel1.set_ylabel('Number of genes')

panel1.set_xticks([1, 3, 5, 7, 9, 11, 13, 15])
panel1.set_xticklabels(['0', '', '6', '', '12', '',
                        '18', ''])

R = np.linspace(255/255, 56/255, 101)
G = np.linspace(225/255, 66/255, 101)
B = np.linspace(40/255, 157/255, 101)

# Read in text file ignoring first line:
first = True

data_List = []

for line in infile:
    if first:
        first = False
    else:
        split = line.strip().split('\t')
        data_List.append([int(split[4]),
                          int(split[5]),
                          int(split[6]),
                          int(split[7]),
                          int(split[8]),
                          int(split[9]),
                          int(split[10]),
                          int(split[11]),
                          float(split[13])])

# Sort data:
data_List.sort(reverse=True, key=lambda x: x[8])

# Nornalize each row and generate rectangles:
yValue = 0
for row in data_List:
    xValue = 0
    values = np.array([row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                      row[7]])
    normalized = ((values-min(values))/(max(values)-min(values))) * 100
    for i in normalized:
        rectangle = mplpatches.Rectangle([xValue, yValue], 3, 1,
                                         facecolor=(R[int(i)], G[int(i)], B[int(i)]),
                                         linewidth=0)
        panel1.add_patch(rectangle)
        xValue = xValue+2
    yValue = yValue+1


plt.savefig(outputFile, dpi=600)
