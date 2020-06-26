import matplotlib.pyplot as plt
import numpy as np
import argparse
import random

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-i', '--input_file', default='BME163_Input_Data_3.txt')
# parser.add_argument('-s', '--style_sheet', default='BME163')
parser.add_argument('-o', '--output_file',
                    default='Lenci_David_BME163_Assignment_Week4.png')
args = parser.parse_args()

# Argument Variables:
inputFile = args.input_file
infile = open(inputFile, 'r')
outputFile = args.output_file

# Style sheet:
# plt.style.use(styleSheet)
plt.style.use('BME163')
# Figure/Panel Dimensions and Aesthetics
figureHeight = 2
figureWidth = 4.667

plt.figure(figsize=(figureWidth, figureHeight))

PanelWidth = 3.333
PanelHeight = 1.333

relativePanelWidth = PanelWidth/figureWidth
relativePanelHeight = PanelHeight/figureHeight

# Create panel, and apply general aesthetics.
panel1 = plt.axes([0.0667, 0.1333, relativePanelWidth, relativePanelHeight])

panel1.tick_params(bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False)
panel1.set_xlim(0.25, 11.75)
panel1.set_ylim(75, 100)
panel1.set_yticks(range(75, 105, 5))
panel1.set_xticks(np.arange(1, 12, 1))
panel1.set_xticklabels(['1', '2', '3', '4', '5', '6',
                        '7', '8', '9', '10', '>11'])

panel1.set_xlabel('Subread Coverage')
panel1.set_ylabel('Identity %')

# Read in data, and save in dictionary for each coverage.
dataDict = {}
for coverage in range(1, 12, 1):
    dataDict[coverage] = []

for line in infile:
    splitLine = line.strip().split('\t')

    ID = splitLine[0].split('_')
    coverage = int(ID[3])

    perc = float(splitLine[1])

    if coverage < 11:
        dataDict[coverage].append(perc)
    else:
        dataDict[11].append(perc)

yList = []
for coverage in range(1, 12, 1):
    yList.append(dataDict[coverage])

# Swarm plot function:
# Takes list of y values, location of swarm plot along x axis, the panel,
# the min and max x and y values, the panel dimensions, font size, and
# width of swarm plots desired. Then checks for points that are overlapping,
# and slowly moves the points a long the x-axis until no points are overlapping.
# If the plot reaches the width constraint then the loop is broken, and whatever
# points were saved are plotted.


def swarm(yList, xValue, panel, xmin, xmax, ymin, ymax,
          panelW, panelH, font, width):
    # Sample Data:
    list = random.sample(yList, 1000)
    # Lists of saved values:
    endXValues = []
    endYValues = []
    # Starting values, set all x values to 0:
    initYValues = list
    initXValues = np.zeros(len(initYValues))

    xrange = xmax - xmin
    yrange = ymax - ymin

    fSize = font
    # Min distance required:
    minDist = fSize/72

    # Iterates through all plotted points, and calculates the distance for
    # new point. If a point is found that is too close the function ends,
    # and returns that distance.
    def determineDist(newYValue, newXValue, yValues, xValues, xrange,
                      yrange, panelW, panelH, minDist):
        closest = [1000, 0, 0]
        for index in range(0, len(yValues), 1):
            oldY = yValues[index]
            oldX = xValues[index]
            curY = newYValue
            curX = newXValue

            xDistance = ((oldX-curX)/xrange)*panelW
            yDistance = ((oldY-curY)/yrange)*panelH
            totalDistance = (xDistance**2 + yDistance**2)**(1/2)

            if totalDistance < closest[0]:
                closest[0] = totalDistance
                closest[1] = oldX
                closest[2] = oldY
                if closest[0] < minDist:
                    break
        return(closest)

    endXValues.append(initXValues[0])
    endYValues.append(initYValues[0])

    for y in range(1, len(initYValues), 1):
        closestInfo = determineDist(initYValues[y], initXValues[y], endYValues,
                                    endXValues, xrange, yrange, panelW, panelH,
                                    minDist)

        dist = closestInfo[0]
        # Find closest value.If it is far enough away save in list
        # else adjust x value:
        if dist > minDist:
            endYValues.append(initYValues[y])
            endXValues.append(initXValues[y])
        else:
            initX = initXValues[y]
            initY = initYValues[y]

            adjX = initX

            for adj in np.arange(0, 1/2, 0.001):
                newLX = adjX - adj

                newLClosest = determineDist(initY, newLX, endYValues,
                                            endXValues, xrange, yrange, panelW,
                                            panelH, minDist)
                newLDist = newLClosest[0]

                newX = adjX + adj
                newClosest = determineDist(initY, newX, endYValues, endXValues,
                                           xrange, yrange, panelW, panelH,
                                           minDist)
                newDist = newClosest[0]

                if newLDist < minDist and newDist < minDist:
                    continue
                elif newLDist > minDist:
                    saveY = initY
                    saveX = newLX
                    break
                elif newDist > minDist:
                    saveY = initY
                    saveX = newX
                    break
            if saveX < width/2:
                endXValues.append(saveX)
                endYValues.append(saveY)
            else:
                endXValues.append(saveX)
                endYValues.append(saveY)
                break

    xShift = endXValues

    for x in range(0, len(endXValues), 1):
        xShift[x] = (endXValues[x] + xValue)

    panel.plot(xShift, endYValues,
               marker='o',
               markerfacecolor='black',
               markeredgecolor='black',
               markersize=fSize,
               markeredgewidth=0,
               linewidth=0)


# Iterate through dictionary, and call swarm function:
for i in range(1, len(dataDict)+1, 1):

    yList = dataDict[i]
    xValue = i
    swarm(yList, xValue, panel1, 0.25, 11.75, 75, 100, PanelWidth,
          PanelHeight, 0.48, 0.57)

# Create median lines:
medians = []
for key in range(1, 12, 1):
    median = np.median(dataDict[key])
    medians.append(median)

for i in range(0, len(medians), 1):
    mid = i + 1
    width = 0.4
    bottom = medians[i]
    panel1.plot([mid-width, mid+width], [bottom, bottom], lw=1,
                color='red')

# set dashed 95% line
panel1.plot([-0.135, 12], [95, 95], lw=0.5, ls='--', color='black',
            dashes=[1, 2, 2, 2])

plt.savefig(outputFile, dpi=600)
