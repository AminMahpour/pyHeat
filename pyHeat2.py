#!/usr/bin/env python3

import operator
import pyBigWig
import sys
import matplotlib.pyplot as pp
import numpy as np


bed1 = ""
bw1 = ""
bw2 = ""

class BigwigObj:
    def __init__(self, url):
        myurl = url
        self.bw = pyBigWig.open(myurl)

    def get_scores(self, pos):
        return self.bw.values(*pos)

def bedreader(file, min=50, max=50):
    data = open(file, mode="r")
    for line in data:
        line = line.split("\t")
        line[1] = int(line[1]) - min
        line[2] = int(line[2]) + max
        out = (line[0], line[1], line[2])
        yield out

def get_value_from_pos(bwurl, bwurl2, bed, min=50, max=60):
    bw = BigwigObj(bwurl)
    bw2 = BigwigObj(bwurl2)
    data_output = []
    data_output2 = []

    for i in bedreader(bed):
        scores = None

        try:
            scores = bw.get_scores(i)
            #print( len(scores))
        except Exception as e:
            print("Error occurred: {0}".format(e))
        if scores != None:
            if not np.isnan(np.mean(scores)):
                data_output.append([i, np.mean(scores[min:max]), scores])
    data1 = sorted(data_output, key=operator.itemgetter(1))


    data2 = []
    for i in data1:
        coord = (i[0][0], int(i[0][1]), int(i[0][2]))
        try:
            scores = bw2.get_scores(coord)
            #print(len(scores))
        except Exception as e:
            print("Error occurred: {0}".format(e))

        if scores != None:
            if not np.isnan(np.mean(scores)):
                data_output2.append([coord, np.mean(scores[min:max]), scores])
    data2 = data_output2

    return data1, data2

bed_file = sys.argv[1]
bw_file = sys.argv[2]
bw2_file = sys.argv[3]
pdf_file = sys.argv[4]

print("calculating...")
data1, data2 = get_value_from_pos(bw_file,bw2_file, bed_file)
rand1 = np.array([x[2] for x in data1])
rand2 = np.array([x[2] for x in data2])

fig = pp.figure(figsize=(3, int(len(data1)/40) ), dpi=600)

blrd_color= pp.cm.bwr
hot_color = pp.cm.hot

print("plotting...")
pp.subplot(1,2,1)
pp.title("Conservation")
pp.pcolormesh(rand1, cmap=blrd_color)
pp.clim(-4, 4)

cbar = pp.colorbar(orientation="horizontal",ticks=[-4, -2, 0, 2, 4])
cbar.set_label("PhyloP", size=10)
cbar.ax.tick_params(labelsize=8)
frame1 = pp.gca()
pp.ylabel("n={0}".format(len(data1)), fontsize=16, color="black")
for xlabel_i in frame1.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in frame1.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
for tick in frame1.axes.get_xticklines():
    tick.set_visible(False)
for tick in frame1.axes.get_yticklines():
    tick.set_visible(False)

pp.subplot(1,2,2)
pp.title("DHS")
pp.pcolormesh(rand2, cmap=hot_color)
pp.clim(0, 200)

cbar = pp.colorbar(orientation="horizontal", ticks=[0, 100, 200])
cbar.set_label("Sensitivity", size=10)
cbar.ax.tick_params(labelsize=8)
frame1 = pp.gca()

for xlabel_i in frame1.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in frame1.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
for tick in frame1.axes.get_xticklines():
    tick.set_visible(False)
for tick in frame1.axes.get_yticklines():
    tick.set_visible(False)



#cbar = pp.colorbar()

frame1 = pp.gca()

for xlabel_i in frame1.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in frame1.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
for tick in frame1.axes.get_xticklines():
    tick.set_visible(False)
for tick in frame1.axes.get_yticklines():
    tick.set_visible(False)

pp.savefig(pdf_file)
