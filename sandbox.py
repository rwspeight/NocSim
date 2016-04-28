#!/usr/bin/python
import math
from math import tan
from random import random
import networkx as nx
import matplotlib.pyplot as plt
import wire as w

wi = w.WireRegionIndex()

wi.add(w.Wire(math.pi/4, 0, 0, 2))
wi.add(w.Wire(math.pi*3/4, 4.8, 0, 2))
wi.add(w.Wire(1, 50, 50, 100))
print wi.get_neighbors(w.Wire(-math.pi, 3.41, 0, 2))
