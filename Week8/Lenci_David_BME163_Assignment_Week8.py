import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse

# ArgParse Implementation:
parser = argparse.ArgumentParser()

# ArgParse Options:
parser.add_argument('-i1', '--input_file1', default='BME163_Input_Data_5.psl')
parser.add_argument('-i2', '--input_file2', default='BME163_Input_Data_6.psl')
parser.add_argument('-g', '--gtf_file', default='gencode.vM12.annotation.gtf')
parser.add_argument('-o', '--output_file', default='Lenci_David_BME163_Assignment_Final.png')
args = parser.parse_args()

# Argument Variables:
inputFile1 = args.input_file1
inputFile2 = args.input_file2
gtfFile = args.gtf_file
outputFile = args.output_file
#styleSheet = args.style_sheet

# Style sheet:
# plt.style.use(styleSheet)
plt.style.use('BME163')
# Figure/Panel Dimensions
figureHeight = 5
figureWidth = 10

plt.figure(figsize=(figureWidth, figureHeight))

panelWidth = 10
panelHeight = 1.25

relativePanelWidth = panelWidth/figureWidth
relativePanelHeight = panelHeight/figureHeight

panel1 = plt.axes([0, 0.05, relativePanelWidth, relativePanelHeight])
panel2 = plt.axes([0, 0.35, relativePanelWidth, relativePanelHeight])
panel3 = plt.axes([0, 0.65, relativePanelWidth, relativePanelHeight])

target = ['chr7', 45232945, 45240000]

for panel in [panel1, panel2, panel3]:
    panel.tick_params(bottom=False, labelbottom=False,
                      left=False, labelleft=False,
                      right=False, labelright=False,
                      top=False, labeltop=False)
    panel.axes.get_yaxis().set_ticks([])
    panel.axes.get_xaxis().set_ticks([])
    panel.set_xlim(target[1], target[2])


def readData(inputFile):
    readList = []
    openFile = open(inputFile, 'r')
    for line in openFile:
        a = line.strip().split('\t')
        chromosome = a[13]
        start = int(a[15])
        end = int(a[16])
        blockstarts = np.array(a[20].split(',')[:-1], dtype=int)
        blockwidths = np.array(a[18].split(',')[:-1], dtype=int)
        read = [chromosome, start, end, blockstarts, blockwidths, False]
        readList.append(read)
    return readList


def readGTF(inFile):
    transcriptList = []
    gtfdict = {}
    for line in open(inFile):
        if line[0] != '#':
            a = line.strip().split('\t')
            chromosome = a[0]
            type1 = a[2]

            if type1 in ['exon', 'CDS']:
                start = int(a[3])
                end = int(a[4])
                transcript = a[8].split(' transcript_id "')[1].split('"')[0]
                if transcript not in gtfdict:
                    gtfdict[transcript] = []
                gtfdict[transcript].append([chromosome, start, end, type1])

    for transcript, parts in gtfdict.items():
        starts = []
        ends = []
        blockstarts = []
        blockwidths = []
        types = []
        for part in parts:
            starts.append(part[1])
            ends.append(part[2])
            blockstarts.append(part[1])
            blockwidths.append(part[2] - part[1])
            chromosome = part[0]
            types.append(part[3])
        transcriptList.append([chromosome, min(starts), max(ends), blockstarts, blockwidths, False, types])

    return transcriptList

def plotReads(panel, readList, target):
    genome_chrom, genome_start, genome_end = target[0], target[1], target[2]
    bottom = 1
    filteredReadList = []
    for read in readList:
        chromosome, start, end, blockstarts, blockwidths, plotted = read[0], read[1], read[2], read[3], read[4], read[5]

        if chromosome == genome_chrom:
            if genome_start < start < genome_end or genome_start < end < genome_end:
                filteredReadList.append(read)

    for ypos in range(1, len(filteredReadList), 1):
        LastReadEnd = 0
        #finalY = 1
        for read in filteredReadList:
            if read[5] is False:
                finalY = ypos
                chromosome, start, end, blockstarts, blockwidths, plotted = read[0], read[1], read[2], read[3], read[4], read[5]
                if start > LastReadEnd:
                    rectangle = mplpatches.Rectangle([start, ypos+0.2], end-start, 0.1,
                                                     facecolor='black',
                                                     edgecolor='black',
                                                     linewidth=0)
                    panel.add_patch(rectangle)
                    bottom += 1

                    for index in np.arange(0, len(blockstarts), 1):
                        blockstart = blockstarts[index]
                        blockwidth = blockwidths[index]
                        if len(read) == 7:
                            type = read[6][index]
                            if type == 'exon':
                                rectangle = mplpatches.Rectangle([blockstart, ypos+0.12], blockwidth, 0.25,
                                                                 facecolor='black',
                                                                 edgecolor='black',
                                                                 linewidth=0)
                            else:
                                rectangle = mplpatches.Rectangle([blockstart, ypos], blockwidth, 0.5,
                                                                 facecolor='black',
                                                                 edgecolor='black',
                                                                 linewidth=0)
                        else:
                            rectangle = mplpatches.Rectangle([blockstart, ypos], blockwidth, 0.5,
                                                             facecolor='black',
                                                             edgecolor='black',
                                                             linewidth=0)
                        panel.add_patch(rectangle)
                    LastReadEnd = end
                    read[5] = True

    return finalY


readList1 = readData(inputFile1)
sorted_readList1 = sorted(readList1, key=lambda x: x[2])
readList2 = readData(inputFile2)
sorted_readList2 = sorted(readList2, key=lambda x: x[2])

readList3 = readGTF(gtfFile)
sorted_readList3 = sorted(readList3, key=lambda x: x[2])


bottom1 = plotReads(panel1, sorted_readList1, target)
bottom1 = bottom1 + (0.10*bottom1)
panel1.set_ylim(0.235, bottom1)

bottom2 = plotReads(panel2, sorted_readList2, target)
bottom2 = bottom2 + (0.12*bottom2)
panel2.set_ylim(0.235, bottom2)

bottom3 = plotReads(panel3, sorted_readList3, target)
panel3.set_ylim(0.235, bottom3+2.05)

plt.savefig(outputFile, dpi=3200)
