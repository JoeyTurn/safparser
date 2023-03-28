import xml.etree.ElementTree
import xml.etree.ElementInclude
import matplotlib.pyplot as plt
import numpy as np

class SAFParser:
    def __init__(self, safpath):
        self.safpath = safpath
       
    #plots the histograms loaded in
    def plot_saf(self):
        _ = self.load_saf()
        for i in range(len(self.titles)):
            self.h = np.histogram([], bins=np.linspace(self.minvals[i], self.maxvals[i], self.nboxes[i]+1))
            self.counts, self.bins = self.h
            self.counts.dtype = float
            for j in range(10):
                self.counts[j] = self.datas[i][j+1]
            plt.hist(self.bins[:-1], self.bins, weights=self.counts)
            plt.title(self.titles[i])
            plt.show()
            print("Number of events: " + str(self.stats[i][0]))
            print("Underflow: " + str(self.datas[i][0]))
            print("Overflow: " + str(self.datas[i][-1]))
    
    #loads all relevant data
    def load_saf(self):
        self.tree = xml.etree.ElementTree.parse(self.safpath)
        self.root = self.tree.getroot()
        self.titles = []
        self.nboxes = []
        self.minvals = []
        self.maxvals = []
        self.stats = []
        self.datas = []
        for hist in self.root.iter("Histo"):
            self.title, self.nbox, self.minval, self.maxval = self.get_desc(hist.find("Description"))
            self.stat = self.get_stats(hist.find("Statistics"))
            self.data = self.get_data(hist.find("Data"), self.nbox)
            self.titles.append(self.title); self.nboxes.append(self.nbox)
            self.minvals.append(self.minval); self.maxvals.append(self.maxval)
            self.stats.append(self.stat); self.datas.append(self.data)
        return self.titles, self.nboxes, self.minvals, self.maxvals, self.stats, self.datas
    
    #helper function in get_desc to eliminate whitespace
    def next_str(self, text):
        return text[text.find(" "):].strip(" ")

    #gets the valuable information from the description section
    def get_desc(self, desc):
        self.title = (desc.text.strip("\n").split("\n"))[0].strip(" ").strip("\"")
        self.s = desc.text.strip("\n").split("\n")[2].strip(" ")
        self.nbox = int(self.s[:self.s.find(" ")])
        self.s = self.next_str(self.s)
        self.minval = float(self.s[:self.s.find(" ")])
        self.s = self.next_str(self.s)
        self.maxval = float(self.s)
        return self.title, self.nbox, self.minval, self.maxval

    #gets information from the statistics section
    def get_stats(self, stat):
        self.arr = stat.text.strip("\n").strip(" ").split("\n")
        return [float(self.arr[i].strip(" ")[:self.arr[i].strip(" ").find(" ")]) for i in range(7)]

    #gets the values for the boxes of the histogram
    #lot of overlap between this and get_stats but it works fine
    def get_data(self, data, nbox):
        self.arr = data.text.strip("\n").strip(" ").split("\n")
        return [float(self.arr[i].strip(" ")[:self.arr[i].strip(" ").find(" ")]) for i in range(nbox+2)]