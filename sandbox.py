#!/usr/bin/python
import math
from math import tan
from random import random
import networkx as nx
import matplotlib.pyplot as plt

# Initialization
#~ Define grid width/height
#~ Define grid x/y resolution factor (smallest addressable area)
#~ Create x/y address lists
#~ 

# Addressing line equation (r, theta, l)
#~ Divide length of line by resolution factor for number of steps
#~ Round length of line to nearest whole step
#~ Calculate list of continuous addresses:  
#o = range(0, steps)
#o = map(lambda v: (r + v*cos(theta), r + v*sin(theta), o) 

#~ For the x coords translate them into discrete addresses
#~ For the y coords translate the into discrete addresses
#~ zip the x/y coords back together


# Translation
#~ Use bisect to find index in addressing list.  This is the grid address in that dimension as it's the cell the line traverses
#	NOTE:  This later could be optimized to take advantage of the close proximity
#	of subsequent lookups by setting a narrow range on the list that is in the neighborhood
#	of the last lookup
	
# Record occupied space
#~ Given base list of address tuples add an extra
#	occupation space to the right only if a cell does
#	not have at least one left/right neighbor (i.e 
#	diagonal neighbors do not count).  This handles
#	The case of two lines intersecting at 45 degrees
#	not sampling down to sharing space even though
#	they obvious intersect.

# How do I handle a jumble of close intersections?  Is it a single node or multiple closely spaced nodes?  What is the minimum size of a node?

x = lambda theta1, theta2, x1, x2, y1, y2: (y2 - y1 + tan(theta1)*x1 - tan(theta2)*x2) / (tan(theta1) - tan(theta2))
y = lambda theta, x, x1, y1: tan(theta)*(x - x1) + y1
wires = []
g = nx.Graph()
for i in range(50):
	size = 10
	a1 = random() * 2 * math.pi	
	l1 = random()*5
	new = (a1, random()*size, random()*size, l1)
	
	
	for w in wires:

		sharedX = x(a1, w[0], new[1], w[1], new[2], w[2])
		sharedY = y(a1, sharedX, new[1], new[2])

		length = math.sqrt(sharedX**2 + sharedY**2)
		
		if length < l1 and length <= w[3]:
			g.add_edge(new, w, length=length)

	wires.append(new)

nx.draw(g)
plt.show()