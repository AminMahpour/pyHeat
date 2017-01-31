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


def get_value_from_pos(bwurl, bed, filename="out.txt", min=50, max=60):
    bw = BigwigObj(bwurl)
    data = []
    data_output = []
    for i in bedreader(bed):
        scores = None
        print("processing position", i)

        try:
            scores = bw.get_scores(i)
        except Exception as e:
            print("Error occurred: {0}".format(e))

        if not np.isnan(np.mean(scores)):
            data_output.append([i, scores, np.mean(scores[min:max])])
            scores = [np.mean(scores[50:60])] + scores

            data.append(scores)

    # sort stuff
    data = sorted(data, key=operator.itemgetter(0))

    for i in data:
        print(i)
    # out = open(filename, mode="w")

    for i in data_output:
        print("{0} {1} {2}\t".format(str(i[0][0]), str(i[0][1]), str(i[0][2])))
        sys.stdout.flush()
        # out.write("{0} {1} {2}\t".format(str(i[0][0]), str(i[0][1]), str(i[0][2])))
        # out.write("\t".join([str(x) for x in i[1]]))
        # out.write("\t{0}".format(str(i[2])))
        # out.write("\n")
    # out.close()

    return data


bw_file = sys.argv[1]
bed_file = sys.argv[0]
pdf_file = sys.argv[2]
data = get_value_from_pos(bw_file, bed_file, "dnase.txt")
rand = np.array(data)

fig = pp.figure(figsize=(3, 6), dpi=600)

pp.pcolor(rand, cmap=pp.cm.bwr)
pp.clim(-4, 4)
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
