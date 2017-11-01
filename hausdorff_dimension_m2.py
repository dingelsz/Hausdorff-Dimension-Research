import argparse
from random import randint, seed
import math
from itertools import permutations
from PIL import Image
import csv

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def pointsWithin(point, radius):
    x = point[0]
    y = point[1]
    diff = range(-radius, radius + 1)
    surrounding = []
    for dx in diff:
        for dy in diff:
            surrounding.append((x + dx, y + dy))
    surrounding = [p for p in surrounding if distance(p, point) <= radius]
    return surrounding


parser = argparse.ArgumentParser(description='Calculate the Hausdorff Dimension for a random walk')
parser.add_argument('-f','--file', help='Path to the csv file to load', required=True)
parser.add_argument('-r','--radius', help='Radius to calculate the Hausdorff Dimension with', type=int, required=True)
args = vars(parser.parse_args())

# Load the csv file and get all the points it's own set
allRows = []
allPoints = set()
frontierPoints = set()
with open(args['file'], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        x, y, isFrontier, segment = row
        x = int(x)
        y = int(y)
        allRows.append((x, y, isFrontier, segment))
        allPoints.add((x, y))
        if isFrontier == "True":
            frontierPoints.add((x, y))

# for every point we are going to create a map. The keys for the map will be each point and the value will be the number of points within a given radius
closePointMap = {}
for point in allPoints:
    x, y = point
    # Get every point around our point within a given radius and filter out all the points that aren't part of all of our points
    surroundingPoints = pointsWithin(point, args['radius'])
    surroundingPoints = set([p for p in surroundingPoints if p in frontierPoints and point in frontierPoints])
    closePointMap[point] = len(surroundingPoints)

# The first row in the csv will be a header
rows = [('x', 'y', 'isFrontier', 'segment', 'within_' + str(args['radius']))]
for r in allRows:
    p = (r[0], r[1])
    rows.append((r[0], r[1], r[2], r[3], closePointMap[p]))

# Save a new csv file
newFilePath = args['file'].split(".")[0] + "_radius_" + str(args['radius']) + "_M2.csv"
with open(newFilePath, 'w') as fp:
    writer = csv.writer(fp, delimiter=',')
    writer.writerows(rows)
