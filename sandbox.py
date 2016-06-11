#!/usr/local/bin/python3
import matplotlib.pyplot as p
import networkx as nx
import matplotlib.animation as animation
p.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
gs = []
g = nx.Graph()
g.add_edge(1,2)
gs.append(g)

g = nx.Graph()
g.add_edge(1,2)
g.add_edge(2,3)
gs.append(g)
g = nx.Graph()
g.add_edge(1,2)
g.add_edge(2,3)
g.add_edge(3,4)
gs.append(g)
g = nx.Graph()
g.add_edge(1,2)
g.add_edge(2,3)
g.add_edge(3,4)
g.add_edge(4,1)
gs.append(g)

f = lambda num: nx.draw(gs[num % len(gs)])

fig1 = p.figure()
line_ani = animation.FuncAnimation(fig1, f, 20, interval=30000)
#p.show()

Writer = animation.writers['ffmpeg']
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)
line_ani.save('lines.mp4', fps=6, writer=writer)