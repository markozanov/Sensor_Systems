from numpy import mean
from matplotlib import pyplot
import random
import math
import numpy as NP
from collections import Counter

nodes = []

N = 100
L = 100
f = int(input("Enter f:\n"))
R = int(input("Enter R:\n"))
r = int(input("Enter r:\n"))


def generate_nodes():
    while len(nodes) < N:
        x = random.randrange(L)
        y = random.randrange(L)
        if nodes.__contains__((x, y)):
            continue
        else:
            nodes.append([x, y, 0])


def calculate_distance(a, b):
    distance = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    return distance


def create_anchors(F):
    for i in range(0, F):
        nodes[i][2] = 1

    for i in range(F, N):
        if nodes[i][2] == 2:
            continue
        else:
            nodes[i][2] = 0


def reset_anchors(F):
    for i in range(0, F):
        nodes[i][2] = 1

    for i in range(F, N):
        nodes[i][2] = 0


def find_anchor_nodes(a, Range):
    if a[2] == 1:
        return []
    counter = 0
    anchors = []
    for i in range(0, N):
        if counter == 3:
            break
        if nodes[i][2] == 1 and calculate_distance(a, nodes[i]) <= Range:
            anchors.append(nodes[i])
            counter = counter + 1

    if len(anchors) == 3 and is_collinear(anchors[0], anchors[1], anchors[2]):
        return []
    else:
        return anchors


def is_collinear(a, b, c):
    ab = calculate_distance(a, b)
    ac = calculate_distance(a, c)
    bc = calculate_distance(b, c)
    if ab + ac == bc or ab + bc == ac or ac + bc == ab:
        return True
    else:
        return False


def trilaterate(anchor1, d1, anchor2, d2, anchor3, d3, noise):
    i1 = anchor1[0]
    i2 = anchor2[0]
    i3 = anchor3[0]

    j1 = anchor1[1]
    j2 = anchor2[1]
    j3 = anchor3[1]

    if noise != 0:
        d1 += random.randrange(-noise, noise) * d1 / 100
        d2 += random.randrange(-noise, noise) * d2 / 100
        d3 += random.randrange(-noise, noise) * d3 / 100

    if j1 == j2 and j1 != j3:
        j1, j3 = j3, j1
        i1, i3 = i3, i1

    x = (((2 * j3 - 2 * j2) * ((d1 * d1 - d2 * d2) + (i2 * i2 - i1 * i1) + (j2 * j2 - j1 * j1)) - (2 * j2 - 2 * j1) *
          ((d2 * d2 - d3 * d3) + (i3 * i3 - i2 * i2) + (j3 * j3 - j2 * j2))) / ((2 * i2 - 2 * i3) * (2 * j2 - 2 * j1) -
                                                                                (2 * i1 - 2 * i2) * (2 * j3 - 2 * j2)))

    y = ((d1 * d1 - d2 * d2) + (i2 * i2 - i1 * i1) + (j2 * j2 - j1 * j1) + (x * (2 * i1 - 2 * i2))) / (2 * j2 - 2 * j1)

    return int(x), int(y)


def find_node(p, Range, noise):
    anchors = find_anchor_nodes(p, Range)
    if len(anchors) < 3:
        return -1, -1
    return trilaterate(anchors[0], calculate_distance(p, anchors[0]),
                       anchors[1], calculate_distance(p, anchors[1]),
                       anchors[2], calculate_distance(p, anchors[2]), noise)


def ALE(Range, F, noise):
    results = {}
    num_experiments = 0
    reset_anchors(F)
    for Freq in range(F, 80, 10):
        num_experiments += 1
        create_anchors(F)
        counter = 0
        predictions = []
        error = 0
        for i in range(0, Freq):
            predictions.append(None)
        for i in range(Freq, N):
            predictions.append(find_node(nodes[i], Range, noise))

        for i in range(Freq, N):
            if predictions[i][0] == -1:
                continue
            else:
                counter = counter + 1
                error = error + calculate_distance(predictions[i], nodes[i])
                nodes[i][2] = 2
        results.update({Freq: (float(str(round(counter / (N - Freq) * 100, 2))),
                                float(str(round(error / (N - Freq), 2))))})

    return results


def calculate_average(data):
    sums = Counter()
    counters = Counter()
    for d in data:
        sums.update(d)
        counters.update(d.keys())

    ret = {}

    for key in sums.keys():
        res_1 = sum(sums[key][::2]) / counters[key]
        res_2 = sum(sums[key][1::2]) / counters[key]
        ret[key] = (res_1, res_2)

    return ret


reslist30 = []
reslist40 = []
reslist50 = []
for i in range(0, 15):
    generate_nodes()
    reslist30.append(ALE(30, f, r))
    reslist40.append(ALE(40, f, r))
    reslist50.append(ALE(50, f, r))


R30 = calculate_average(reslist30)
R40 = calculate_average(reslist40)
R50 = calculate_average(reslist50)


x30 = NP.array(list(map(lambda x: x, R30.keys())))
y30 = NP.array(list(map(lambda y: y[1], R30.values())))
pyplot.subplot(xlabel='% на anchor јазли', ylabel='просечна грешка при локализација',
               title='Итеративен алгоритам - бучава  = 5 ')
pyplot.plot(x30, y30, color='red', label='R = 30', marker='.')

x40 = NP.array(list(map(lambda x: x, R40.keys())))
y40 = NP.array(list(map(lambda y: y[1], R40.values())))
pyplot.plot(x40, y40, color='green', label='R = 40', marker='.')

x50 = NP.array(list(map(lambda x: x, R50.keys())))
y50 = NP.array(list(map(lambda y: y[1], R50.values())))
pyplot.plot(x50, y50, color='blue', label='R = 50', marker='.')
pyplot.legend(loc='best')
pyplot.show()
