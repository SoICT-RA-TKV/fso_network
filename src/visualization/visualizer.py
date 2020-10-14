import json
import sys
from matplotlib import pyplot as plt
import os

def visualizeGroundFSO(output, FSOs, xmin=0, xmax=200, ymin=0, ymax=200):
    plt.scatter([fso.x for fso in FSOs],
        [fso.y for fso in FSOs],
        marker='+')
    axes = plt.gca()
    axes.set_aspect('equal', 'box')
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    plt.savefig(output, dpi=300)
    plt.clf()

def visualizeClusters(output, clusters, FSOs, HAPs, R, xmin=0, xmax=200, ymin=0, ymax=200):
    dtFSOs = dict()
    dtHAPs = dict()
    for hap in HAPs:
        dtHAPs[hap.index] = hap
    for fso in FSOs:
        dtFSOs[fso.index] = fso
    plt.scatter([fso.x for fso in FSOs],
        [fso.y for fso in FSOs],
        marker='+', zorder=10, c='g')
    for cluster in clusters:
        xhap, yhap = cluster[0].x, cluster[0].y
        plt.scatter([xhap], [yhap], marker='o', zorder=20, c='r')
        plt.gcf().gca().add_artist(
            plt.Circle((xhap, yhap),
                R,
                edgecolor = 'r',
                linewidth = 2,
                fill = False))
        for fso in cluster[1]:
            plt.plot([xhap, fso.x], [yhap, fso.y], zorder=0, c='b')
    axes = plt.gca()
    axes.set_aspect('equal', 'box')
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    plt.savefig(output, dpi=300)
    plt.clf()

def visualizeHAP(output, HAPs, clusters, xmin=0, xmax=200, ymin=0, ymax=200):
    for cluster in clusters:
        xhap, yhap = cluster[0].x, cluster[0].y
        plt.scatter([xhap], [yhap], marker='o', zorder=20, c='r')
    for hap in HAPs:
        plt.scatter([hap.x], [hap.y], marker='o', zorder=10, c='b')
    axes = plt.gca()
    axes.set_aspect('equal', 'box')
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    plt.savefig(output, dpi=300)
    plt.clf()

def visualizeHAPTopology(output, HAPs, clusters, matching, usedLinks, xmin=0, xmax=200, ymin=0, ymax=200):
    dtHAPs = dict()
    for hap in HAPs:
        dtHAPs[hap.index] = hap
    for cluster in clusters:
        xhap, yhap = cluster[0].x, cluster[0].y
        plt.scatter([xhap], [yhap], marker='o', zorder=20, c='r')
    for hap in HAPs:
        plt.scatter([hap.x], [hap.y], marker='o', zorder=10, c='b')
    for h in matching:
        h1 = dtHAPs[h]
        h2 = dtHAPs[matching[h]]
        plt.plot([h1.x, h2.x], [h1.y, h2.y], linestyle='-.', c='b', zorder=5)
    for l in usedLinks:
        h1 = dtHAPs[l[0]]
        h2 = dtHAPs[l[1]]
        plt.plot([h1.x, h2.x], [h1.y, h2.y], c='r', zorder=0)
    axes = plt.gca()
    axes.set_aspect('equal', 'box')
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    plt.savefig(output, dpi=300)
    plt.clf()

if __name__ == '__main__':  
    from collections import namedtuple
    HAP = namedtuple('HAP', ['index', 'x', 'y', 'z'])
    FSO = namedtuple('FSO', ['index', 'x', 'y', 'z'])
    FSOs = [FSO(0, 1, 1, 0), FSO(1, 20, 20, 0)]
    HAPs = [HAP(0, 2, 2, 20), HAP(1, 25, 25, 20), HAP(2, 8, 12, 20), HAP(3, 16, 14, 20)]
    clusters = [(HAPs[0], [FSOs[0]]), (HAPs[1], [FSOs[1]])]
    matching = {0: 2, 1: 3}
    usedLinks = [(0, 2), (1, 3), (0, 1)]
    R = 7.5
    visualizeGroundFSO('00.png', FSOs)
    visualizeClusters('01.png', clusters, FSOs, HAPs, R)
    visualizeHAP('02.png', HAPs, clusters)
    visualizeHAPTopology('03.png', HAPs, clusters, matching, usedLinks)