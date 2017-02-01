#!/usr/bin/env python3
import operator
import pyBigWig
import sys

import matplotlib.pyplot as pp
import numpy as np


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


def get_value_from_pos(bwurl, bed, min=50, max=60):
    bw = BigwigObj(bwurl)
    data = []
    data_output = []
    data_out = bed+".sorted.txt"

    for i in bedreader(bed):
        scores = None
        #print("processing position", i)

        try:
            scores = bw.get_scores(i)
        except Exception as e:
            print("Error occurred: {0}".format(e))
        if scores != None:
            if not np.isnan(np.mean(scores)):
                data_output.append([i, np.mean(scores[min:max]), scores])
    data = sorted(data_output, key=operator.itemgetter(1))

    out = open(data_out ,mode="w")
    for i in data:
        out.write("{0}\t{1}\t{2}\n".format(i[0][0],i[0][1],i[0][2]))
        print(i[0])
    out.close()

    return data




bed_file = sys.argv[1]
bw_file = sys.argv[2]
pdf_file = sys.argv[3]


data = get_value_from_pos(bw_file, bed_file)
rand = np.array([x[2] for x in data])

fig = pp.figure(figsize=(3, 10), dpi=600)

blrd_color= pp.cm.bwr
hot_color = pp.cm.hot


pp.pcolor(rand, cmap=hot_color)
pp.clim(0, 200)
pp.colorbar()
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
