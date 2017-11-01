'''randomWalk.py is a script to generate random walk data. The script is run using "python randomWalk.py -n numberOfSteps -f /path/to/save/file.csv". There is also an additional option, "-i /path/to/image.png" to save an image of the random walk (This requires the PIL package). Random walk data is saved as a csv file. Each row in the file is a point. The first column is the x coordinate. The second column is the y coordinate. The final column is a 1 (True) or 0 (False) flag that denotes if the point is a frontier point.
'''

from random import randint
from sys import argv
import math
import argparse
from PIL import Image
import csv

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Command Line argument parsing
parser = argparse.ArgumentParser(description='Genrate random walk data')
parser.add_argument('-n','--steps', help='Number of steps to take', required=True)
parser.add_argument('-f','--file', help='Path to save data', required=True)
parser.add_argument('-i','--image', help='Path to save image', required=False)
args = vars(parser.parse_args())

# Helper functions
def genRandomWalk(nSteps):
    # The random walk is recorded by a list of points.
    vertices = [(0, 0)]
    for i in range(int(nSteps)):
        x, y = vertices[-1]
        direction = randint(1, 4)
        if direction == 1:
            y += 1
        if direction == 2:
            x += 1
        if direction == 3:
            y -= 1
        if direction == 4:
            x -= 1

        vertices.append((x, y))
    return vertices

# The idea behind this point is to create a tight border around our shape. From this border, take all the points that are not part of the shape and grow them inward. As we grow these regions outside of our shape they will run into the border of our shape. When this happens, add the points we run into to our set of border points.
def genBorderPoints(vertices):
# Find the min/max for our points
    maxX = 0
    maxY = 0
    minX = 0
    minY = 0
    for (x, y) in vertices:
        if x > maxX: maxX = x
        if x < minX: minX = x
        if y > maxY: maxY = y
        if y < minY: minY = y
    height = abs(maxY - minY) + 1
    width = abs(maxX - minX) + 1

    # Add all the points around our random walk. We are making a tight border around our shape
    outsidePoints = set([(minX, y) for y in range(minY, maxY + 1)])
    outsidePoints = outsidePoints | set([(x, minY) for x in range(minX, maxX + 1)])
    outsidePoints = outsidePoints | set([(maxX, y) for y in range(minY, maxY + 1)])
    outsidePoints = outsidePoints | set([(x, maxY) for x in range(minX, maxX + 1)])

    # Frontier points are points that are part of the outside and part of the random walk
    frontierPoints = outsidePoints & vertices

    # Remove all points that are part of the random walk
    outsidePoints = outsidePoints - vertices
    recentlyDiscoveredPoints = outsidePoints

    # While we still have recentlyDiscoveredPoints we will continue to look for more boundary points
    isFirstLoop = True
    while len(recentlyDiscoveredPoints) != 0:
        # justDiscoveredPoints will hold all the points we are about to find
        justDiscoveredPoints = set()

        # For every point we just found look around it for undiscovered points or boundary points.
        for point in recentlyDiscoveredPoints:
            x, y = point
            # Generate a set of points above, below and to the sides of our point.
            for theta in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:

                newPoint = (int(math.cos(theta)) + x, int(math.sin(theta)) + y)

                # Sanity Check. If it's our first loop we need to make sure we don't grow outside of our boundary because we can grow outwards forever.
                if isFirstLoop:
                    px, py = newPoint
                    if px < minX or px >= maxX:
                        continue
                    if py < minY or py >= maxY:
                        continue

                # From all of the points we have grown into, if any of them are part of the random walk shape they must be border points.
                if newPoint in vertices:
                    frontierPoints.add(newPoint)
                    continue

                # If these points aren't part of the shape then add them to the set of points we will grow from during the next iteration.
                if newPoint not in outsidePoints:
                    justDiscoveredPoints.add(newPoint)
                    
        recentlyDiscoveredPoints = justDiscoveredPoints
        outsidePoints = outsidePoints | recentlyDiscoveredPoints

        isFirstLoop = False
    return frontierPoints

def makeImg(points, path):
    # Find the min/max for our points
    maxX = 0
    maxY = 0
    minX = 0
    minY = 0
    for (x, y, _) in points:
        if x > maxX: maxX = x
        if x < minX: minX = x
        if y > maxY: maxY = y
        if y < minY: minY = y
        height = abs(maxY - minY) + 1
        width = abs(maxX - minX) + 1

    img = Image.new('RGB', (width, height), "white")
    pixels = img.load()

    for (x, y, isFrontierPoint) in points:
        #print (x - minX, y - minY, isFrontierPoint)
        color = BLACK
        if isFrontierPoint:
            color = (255, 0, 0)
        pixels[x - minX, y - minY] = color
    img.save(path)


# CODE
vertices = set(genRandomWalk(args['steps']))
frontier = genBorderPoints(vertices)

points = set()
for (x, y) in vertices:
    points.add((x, y, int((x, y) in frontier)))

with open(args['file'], 'w') as fp:
    writer = csv.writer(fp, delimiter=',')
    writer.writerows(points)

if args['image']:
    makeImg(points, args['image'])
