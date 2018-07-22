import argparse
from random import randint, seed
import math
from PIL import Image
import csv

BLACK = (0, 0, 0)
GREY = (155, 155, 155)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
VISIBILITY = 8

class World:
    def __init__(self):
        """
        Initializes a new World instance

        - Parameters -

        - Return -
        None
        """
        size = (0, 0)
        # We store holes in hashtables.
        # The key is the x/y coordinate and the values are a list of y/x coordinates.
        # This format allows us to easily see what holes are infront of the Earthworm.
        self.columns = {}
        self.rows = {}
        self.holes = set()
        self.visited = []
        self.width = 0
        self.height = 0
    def add(self, earthworm):
        """
        add adds an earthworm to the world.

        - Parameters -
        earthworm: Earthworm instance to add to the world.

        - Return -
        None
        """
        self.earthworm = earthworm
        self.columns[earthworm.x] = [earthworm.y]
        self.rows[earthworm.y] = [earthworm.x]
        self.holes.add(earthworm.position())
        self.minX = earthworm.x
        self.maxX = earthworm.x
        self.minY = earthworm.y
        self.maxY = earthworm.y
    def update(self):
        """
        Simulates one step of the Earthworm random walk.

        - Parameters -

        - Return -
        None
        """
        self.update_earthworm()
        self.update_particles()
        self.update_stats()

    def update_earthworm(self):
        """
        Updates the position of the earthworm. Should not be called outside of World.update().

        - Parameters -

        - Return -
        None
        """
        self.earthworm.rotate()
        self.earthworm.move()
        self.visited.append(earthworm.position())
    def update_particles(self):
        """
        Update the particles in our world. Should not be called outside of World.update().

        - Parameters -

        - Return -
        None
        """
        # Below is the logic for the particle physics
        # For each direction the earthworm can be facing there are 3 scenarios:
        #  1) We moved into a hole. In this case we aren't pushing dirt so don't do anything
        #  2) We move into a particle with dirt and there is a hole somewhere in front of us.
        #     In this case we need to find that hole and fill it
        #  3) We move into a particle with dirt and there isn't a hole in from of us. In this
        #     case we just need to create a hole at our current location.
        if self.earthworm.isFacingUp():
            # Nothing happens if an earthworm moves into a hole
            if self.earthworm.position() in self.holes:
                pass
            else:
                if self.columns.has_key(self.earthworm.x):
                    holesAbove = [y for y in self.columns[self.earthworm.x] if y > self.earthworm.y]
                    # If we have holes above then fill in the closest hole.
                    if len(holesAbove) > 0:
                        closestHole = min(holesAbove)
                        self.fillHole((self.earthworm.x, closestHole))
                self.addHole(self.earthworm.position())
        if self.earthworm.isFacingRight():
            if self.earthworm.position() in self.holes:
                pass
            else:
                if self.rows.has_key(self.earthworm.y):
                    holesToRight = [x for x in self.rows[self.earthworm.y] if x > self.earthworm.x]
                    if len(holesToRight) > 0:
                        closestHole = min(holesToRight)
                        self.fillHole((closestHole, self.earthworm.y))
                self.addHole(self.earthworm.position())
        if self.earthworm.isFacingDown():
            if self.earthworm.position() in self.holes:
                pass
            else:
                if self.columns.has_key(self.earthworm.x):
                    holesBelow = [y for y in self.columns[self.earthworm.x] if y < self.earthworm.y]
                    if len(holesBelow) > 0:
                        closestHole = max(holesBelow)
                        self.fillHole((self.earthworm.x, closestHole))
                self.addHole(self.earthworm.position())
        if self.earthworm.isFacingLeft():
            # Nothing happens if an earthworm moves into a hole
            if self.earthworm.position() in self.holes:
                pass
            else:
                if self.rows.has_key(self.earthworm.y):
                    holesToLeft = [x for x in self.rows[self.earthworm.y] if x < self.earthworm.x]
                    # If we have holes above then fill in the closest hole.
                    if len(holesToLeft) > 0:
                        closestHole = max(holesToLeft)
                        self.fillHole((closestHole, self.earthworm.y))
                self.addHole(self.earthworm.position())
    def update_stats(self):
        """
        Update the boundary of the world. Should not be called outside of World.update().

        - Parameters -

        - Return -
        None
        """
        if self.earthworm.x > self.maxX: self.maxX = self.earthworm.x
        if self.earthworm.x < self.minX: self.minX = self.earthworm.x
        if self.earthworm.y > self.maxY: self.maxY = self.earthworm.y
        if self.earthworm.y < self.minY: self.minY = self.earthworm.y
    def addHole(self, pos):
        """
        Adds a hole to our set of holes and updates our hashtables of holes. Should not be called outside
        of World.update().

        - Parameters -
        pos: (x: Int, y: Int) a pair of integers representing a point in the world.

        - Return -
        None
        """
        x = pos[0]
        y = pos[1]
        self.holes.add(pos)
        if self.columns.has_key(x):
            self.columns[x].append(y)
        else:
            self.columns[x] = [y]
        if self.rows.has_key(y):
            self.rows[y].append(x)
        else:
            self.rows[y] = [x]
    def fillHole(self, pos):
        """
        Removes a hole from our set of holes and updates our hashtables of holes. Should not be called outside
        of World.update().

        - Parameters -
        pos: (x: Int, y: Int) a pair of integers representing a point in the world.

        - Return -
        None
        """
        #print "At: " + str(self.earthworm.position()) + " - Filling: " + str(pos)
        x = pos[0]
        y = pos[1]
        self.holes.remove(pos)
        colIndex = self.columns[x].index(y)
        self.columns[x].pop(colIndex)
        rowIndex = self.rows[y].index(x)
        self.rows[y].pop(rowIndex)

class Earthworm:
    def __init__(self, pos = (0, 0)):
        """
        Initializes a new Earthworm instance

        - Parameters -

        - Return -
        None
        """
        self.x = pos[0]
        self.y = pos[1]
        self.rotate()
    def rotate(self):
        """
        Rotates the Earthworm in a random direction

        - Parameters -

        - Return -
        None
        """
        self.orientation = randint(1, 4)
    def move(self):
        """
        Moves the Earthworm one unit forward

        - Parameters -

        - Return -
        None
        """
        # UP
        if self.orientation == 1:
            self.y += 1
        # RIGHT
        if self.orientation == 2:
            self.x += 1
        # DOWN
        if self.orientation == 3:
            self.y -= 1
        # LEFT
        if self.orientation == 4:
            self.x -= 1
    def isFacingUp(self):
        """
        Boolean representing the orientation of the Earthworm

        - Parameters -

        - Return -
        True if the Earthworm is facing up.
        """
        return self.orientation == 1
    def isFacingRight(self):
        """
        Boolean representing the orientation of the Earthworm

        - Parameters -

        - Return -
        True if the Earthworm is facing right.
        """
        return self.orientation == 2
    def isFacingDown(self):
        """
        Boolean representing the orientation of the Earthworm

        - Parameters -

        - Return -
        True if the Earthworm is facing down.
        """
        return self.orientation == 3
    def isFacingLeft(self):
        """
        Boolean representing the orientation of the Earthworm

        - Parameters -

        - Return -
        True if the Earthworm is facing left.
        """
        return self.orientation == 4
    def position(self):
        """
        The position of the earthworm

        - Parameters -

        - Return -
        (x: Int, y: Int) a pair of numbers representing the Earthworm's position.
        """
        return (self.x, self.y)

def genFrontierPoints(vertices):
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

    # Add all the points around our random walk
    outsidePoints = set([(minX, y) for y in range(minY, maxY + 1)])
    outsidePoints = outsidePoints | set([(x, minY) for x in range(minX, maxX + 1)])
    outsidePoints = outsidePoints | set([(maxX, y) for y in range(minY, maxY + 1)])
    outsidePoints = outsidePoints | set([(x, maxY) for x in range(minX, maxX + 1)])

    # Frontier points are points that are part of the outside and part of the random walk
    frontierPoints = outsidePoints & vertices

    # Remove all points that are part of the random walk
    outsidePoints = outsidePoints - vertices
    recentlyDiscoveredPoints = outsidePoints # Our Queue

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

                # If it's our first loop we need to make sure we don't include any points outside of our boundary because we can grow outwards forever
                if isFirstLoop:
                    px, py = newPoint
                    if px < minX or px >= maxX:
                        continue
                    if py < minY or py >= maxY:
                        continue

                if newPoint in vertices:
                    frontierPoints.add(newPoint)
                    continue
                if newPoint not in outsidePoints:
                    justDiscoveredPoints.add(newPoint)
        recentlyDiscoveredPoints = justDiscoveredPoints
        outsidePoints = outsidePoints | recentlyDiscoveredPoints

        isFirstLoop = False
    return frontierPoints

class Disjoint():
    def __init__(self, s):
        """
        Initiate a new disjoint set with the items in s

        - Parameters -
        s: Set A set of items

        - Return -
        None
        """
        self.djSets = {}
        for e in s:
            self.djSets[e] = set([e])

    def find(self, e):
        """
        Get the key for an element e in the disjoint set

        - Parameters -
        s: Set A set of items

        - Return -
        e: an element from the original set
        """
        if self.djSets.has_key(e):
            key = e
            if type(self.djSets[e]) is set:
                return e
            return self.find(self.djSets[e])

    def getSets(self):
        """
        Get the sets in the Disjoint set

        - Parameters -

        - Return -
        [Set()] A list of sets.
        """
        return [self.djSets[key] for key in self.djSets.keys() if type(self.djSets[key]) is set]

    # Combines the sets that e1 and e2 are in and sets e2's representative to e1's.
    def union(self, e1, e2):
        """
        Performs a union on two sets

        - Parameters -
        e1 the key for the first set
        e2 the key for the second set

        - Return -
        None
        """
        e1Rep = self.find(e1)
        e2Rep = self.find(e2)
        # If we have two elements of the same set do nothing
        if e1Rep == e2Rep:
            return

        self.djSets[e1Rep] = self.djSets[e1Rep].union(self.djSets[e2Rep])
        self.djSets[e2Rep] = e1Rep


def getSegments(holes):
    """
    Returns

    - Parameters -
    holes: Set((x: Int, y: Int)) a set of points represented as integer pairs

    - Return -
    dj: Disjoint a Disjoint object representing a disjoint set where each set contains points
        that are connected.
    """
    dj = Disjoint(holes)
    for hole in holes:
        x = hole[0]
        y = hole[1]
        surroundingPoints = []
        for theta in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
            surroundingPoints.append((int(math.cos(theta)) + x, int(math.sin(theta)) + y))
        touchingHoles = [p for p in surroundingPoints if p in holes]
        [dj.union(hole, touching) for touching in touchingHoles]
    return dj

def saveImage(earthworm, filename=None, visited = False, frontier = None, show_image = False, show_frontier = True):
    img = Image.new('RGB', (abs(self.maxX - self.minX)+1, abs(self.maxY - self.minY)+1), "black")
    pixels = img.load()
    #print (self.minX, self.minY), (self.maxX, self.maxY)

    if visited:
        for p in self.visited:
            x = p[0] + abs(earthworm.minX)
            y = p[1] + abs(earthworm.minY)
            r, g, b = pixels[x, y]
            pixels[x, y] = (int(r + VISIBILITY), int(g + VISIBILITY), int(b + VISIBILITY))

    for p in list(earthworm.holes):
        x = p[0] + abs(earthworm.minX)
        y = p[1] + abs(earthworm.minY)
        pixels[x, y] = WHITE

    if frontier and show_frontier:
        for p in frontier:
            x = p[0] + abs(earthworm.minX)
            y = p[1] + abs(earthworm.minY)
            pixels[x, y] = RED
    if show_image:
        img.show()

    if filename:
        if visited:
            filename = filename + "-visited"
        img.save(filename + ".bmp")

parser = argparse.ArgumentParser(description='Generate earthworm data')
parser.add_argument('-n','--steps', help='Number of steps to take', required=True)
parser.add_argument('-f','--file', help='Path to save data', required=False)
parser.add_argument('-i','--image', help='Path to save data', required=False)
parser.add_argument('-v','--visited', help='Show visited points', required=False)
parser.add_argument('--show_image', dest='show_image', action='store_true')
parser.add_argument('--show_visited', dest='isVisited', action='store_true')
parser.add_argument('--show_frontier', dest='isFrontier', action='store_true')
args = vars(parser.parse_args())

ground = World()
earthworm = Earthworm()
ground.add(earthworm)

for n in range(int(args['steps'])):
    ground.update()

frontier = genFrontierPoints(ground.holes)

if args['file']:

    holes = list(ground.holes)
    segments = list(getSegments(holes).getSets())
    rows = []
    for i in range(len(holes)):
        x, y = holes[i]
        isFrontier = holes[i] in frontier
        numSegments = -1
        if i < len(segments):
            numSegments = len(segments[i])
        rows.append((x, y, isFrontier, numSegments))

    with open(args['file'], 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(rows)

ground.saveImage(filename = args['image'], visited = args['isVisited'], frontier = frontier, show_image = args['show_image'], show_frontier = args['isFrontier'])
