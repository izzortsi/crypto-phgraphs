# %%
from graph_tool.all import Graph
import graph_tool.all as gt
import numpy as np
import numpy.random as npr

# from numpy.linalg import norm
from matplotlib import cm
import matplotlib.colors as mplc
import os, sys
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib
from sklearn.neighbors import NearestNeighbors


# %%


class ConnectedSparseGraph(Graph):
    def __init__(self, M, d=np.linalg.norm, **kwargs):

        self.M = M
        self.d = d
        self.n = len(M)
        # self.D = self._compute_distances()

        super().__init__(**kwargs)

    def compute_distances(self):

        M = self.M
        d = self.d

        n = self.n
        D = np.empty((n, n))

        for i in range(n):
            for j in range(n):
                x = M[i]
                y = M[j]
                D[i, j] = d(x - y)
        return D


# %%


# %%
# nbrs = NearestNeighbors(n_neighbors=1, algorithm="ball_tree").fit(M)

# adj1 = nbrs.kneighbors_graph(M, n_neighbors=1).toarray()
# adj2 = nbrs.kneighbors_graph(M, n_neighbors=2).toarray()
# (adj2 - adj1)


# %%


def build_csg(s: ConnectedSparseGraph, nn_algorithm="brute"):

    i = 0
    s.clear_edges()

    nbrs = NearestNeighbors(algorithm=nn_algorithm).fit(s.M)

    adj_0 = nbrs.kneighbors_graph(
        s.M, n_neighbors=1
    ).toarray()  # the first neighbors are the vertices themselves

    adj_1 = nbrs.kneighbors_graph(s.M, n_neighbors=2).toarray()

    adj_seq = [adj_0, adj_1]
    add_seq = [adj_1 - adj_0]

    adj_matrix = np.triu(add_seq[0])
    s.add_edge_list(np.transpose(adj_matrix.nonzero()))
    comp, hist = gt.label_components(s)

    while len(hist) > 1:

        i += 1

        adj = nbrs.kneighbors_graph(s.M, n_neighbors=i + 2).toarray()
        to_add = adj - adj_seq[-1]

        adj_seq.append(adj)
        add_seq.append(to_add)

        partial_adj_matrix = np.triu(to_add)

        s.add_edge_list(np.transpose(partial_adj_matrix.nonzero()))

        comp, hist = gt.label_components(s)


# %%

ConnectedSparseGraph.build = build_csg
# %%
# M = npr.random((2000, 2))
# csg = ConnectedSparseGraph(M, directed=False)
#
# # %%
# csg.build()
# # %%
#
# gt.graph_draw(csg, vertex_size=2)
