import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import argparse

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-f', '--fasta_file', default='Splice_Sequences.fasta')
parser.add_argument('-A', '--small_A', default='A_small.png')
parser.add_argument('-G', '--small_G', default='G_small.png')
parser.add_argument('-C', '--small_C', default='C_small.png')
parser.add_argument('-T', '--small_T', default='T_small.png')
parser.add_argument('-o', '--output_file',
                    default='Lenci_David_BME163_Assignment_Week5.png')
args = parser.parse_args()

# Argument Variables:
fastaFile = args.fasta_file
outputFile = args.output_file
smallA = args.small_A
smallG = args.small_G
smallC = args.small_C
smallT = args.small_T
# styleSheet = args.style_sheet

# Style sheet:
# plt.style.use(styleSheet)
plt.style.use('BME163')
# Figure/Panel Dimensions and aesthetics according to
# assignment specifications:
figureHeight = 2
figureWidth = 4

plt.figure(figsize=(figureWidth, figureHeight))

panelWidth = 1.6
panelHeight = 0.667

relativePanelWidth = panelWidth/figureWidth
relativePanelHeight = panelHeight/figureHeight

panelL = plt.axes([0.083, 0.3, relativePanelWidth, relativePanelHeight])
panelR = plt.axes([0.566, 0.3, relativePanelWidth, relativePanelHeight])

for panel in [panelL, panelR]:
    panel.set_xlim(0, 20)
    panel.set_ylim(0, 2.0)
    panel.set_xlabel('Distance to\nSplice Site')
    panel.set_xticklabels(np.arange(-10, 11, 5))

panelL.set_ylabel('Bits')
panelL.set_title('5\'SS')
panelR.set_title('3\'SS')

panelL.tick_params(axis='both', which='both',
                   bottom=True, labelbottom=True,
                   left=True, labelleft=True,
                   right=False, labelright=False,
                   top=False, labeltop=False,
                   labelsize=8)

panelR.tick_params(axis='both', which='both',
                   bottom=True, labelbottom=True,
                   left=False, labelleft=False,
                   right=False, labelright=False,
                   top=False, labeltop=False,
                   labelsize=8)

panelL.plot([10, 10], [0, 2], lw=1/2, color='black')
panelR.plot([10, 10], [0, 2], lw=1/2, color='black')

# Important Values:
upCounts = []
upHeights = []
downCounts = []
downHeights = []
upStreamSeqs = 0
downStreamSeqs = 0
sampleCorrection = 0


# For loop for reading in fasta:
upStream = True
for line in open(fastaFile):
    line = line.rstrip()
    if line[0] == '>':
        # Check if upstream
        if line[1] == '5':
            upStream = True
        else:
            upStream = False
    else:
        # Keep count of upstream/downstream seqs
        if upStream is True:
            upStreamSeqs += 1
        else:
            downStreamSeqs += 1
        # For nucleotide in sequence, if upstream sequence:
        #   copy dictionary for upCounts
        #   depending on count in sequence increase value in dictionary
        # else:
        #   do for donwstream
        for i in range(0, len(line), 1):
            if upStream is True:
                if len(upCounts) <= i:
                    upCounts.append({'A': 0, 'T': 0, 'C': 0, 'G': 0})
                upCounts[i][line[i]] += 1
            else:
                if len(downCounts) <= i:
                    downCounts.append({'A': 0, 'T': 0, 'C': 0, 'G': 0})
                downCounts[i][line[i]] += 1


def height(countDict, seqs):
    # Function for calculating heights given a dictionary
    # of counts and number of sequences. Returns height Values
    # as a dictionary in order to maintain nucleotide associated with
    # heights.
    relativeFreq = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    heights = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    correction = (4 - 1) / (np.log(2) * (2*seqs))

    relativeFreq = {}
    for x in countDict:
        if x == 0:
            relativeFreq[x] = 0
        else:
            relativeFreq[x] = (countDict[x]/seqs)

    sum = 0
    for x in relativeFreq:
        if relativeFreq[x] != 0:
            sum = sum + (relativeFreq[x] * np.log2(relativeFreq[x]))

    uncertainty = -1 * sum

    for x in relativeFreq:
        heights[x] = (relativeFreq[x]*(2-(uncertainty+correction)))

    return(heights)


# Get heights for up and down stream:
for x in range(0, len(upCounts)):
    heights = height(upCounts[x], upStreamSeqs)
    upHeights.append(heights)

for x in range(0, len(downCounts)):
    heights = height(downCounts[x], downStreamSeqs)
    downHeights.append(heights)

# Logos:
A = mpimg.imread(smallA)
G = mpimg.imread(smallG)
C = mpimg.imread(smallC)
T = mpimg.imread(smallT)

# For each set of heights sort heights by size then
# calculate extent values for imshow, and plot
for dict in range(0, len(upHeights), 1):
    heights = upHeights[dict]
    sortedHeights = sorted(heights.keys(), key=lambda k: heights[k])
    order = []
    for key in sortedHeights:
        order.append(key)
    newTop = 0

    for key in order:
        index = order.index(key)
        # Extent Values:
        bottom = newTop
        top = bottom+heights[key]
        newTop = top
        # Plot logos:
        if key == 'A':
            panelL.imshow(A, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'G':
            panelL.imshow(G, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'C':
            panelL.imshow(C, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'T':
            panelL.imshow(T, aspect='auto', extent=[dict, dict+1,
                          bottom, top])


for dict in range(0, len(downHeights), 1):
    heights = downHeights[dict]
    sortedHeights = sorted(heights.keys(), key=lambda k: heights[k])
    order = []
    for key in sortedHeights:
        order.append(key)
    newTop = 0

    for key in order:
        index = order.index(key)
        # Extent Values:
        bottom = newTop
        top = bottom+heights[key]
        newTop = top
        # Plot Logos:
        if key == 'A':
            panelR.imshow(A, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'G':
            panelR.imshow(G, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'C':
            panelR.imshow(C, aspect='auto', extent=[dict, dict+1,
                          bottom, top])
        elif key == 'T':
            panelR.imshow(T, aspect='auto', extent=[dict, dict+1,
                          bottom, top])


plt.savefig(outputFile, dpi=600)
