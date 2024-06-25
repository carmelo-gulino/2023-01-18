import copy
from random import randint

import networkx as nx
from geopy.distance import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.result = None
        self.best_sol = None
        self.nodes = None
        self.providers = DAO.get_all_providers()
        self.graph = None

    def build_graph(self, provider, distanza):
        self.graph = nx.Graph()
        self.nodes = DAO.get_nodes(provider)
        self.graph.add_nodes_from(self.nodes)
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if u != v:
                    dist = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude)).km
                    if dist <= distanza:
                        self.graph.add_edge(u, v, weight=dist)
        return self.graph

    def get_max_vicini(self):
        max_vicini = [(n, len(list(self.graph.neighbors(n)))) for n in self.graph.nodes]
        max_vicini.sort(key=lambda t: t[1], reverse=True)
        self.result = [t for t in max_vicini if t[1] == max_vicini[0][1]]
        return self.result

    def get_percorso(self, target, string):
        self.best_sol = []
        i = randint(0, len(self.result) - 1)
        source = self.result[i][0]
        parziale = [source]
        self.ricorsione(parziale, target, string)
        return self.best_sol

    def ricorsione(self, parziale, target, string):
        ultimo = parziale[-1]
        if len(parziale) > len(self.best_sol) and ultimo == target:
            self.best_sol = copy.deepcopy(parziale)
            print(parziale)
        for neighbor in self.graph.neighbors(ultimo):
            if neighbor not in parziale and string not in neighbor.Location:
                parziale.append(neighbor)
                self.ricorsione(parziale, target, string)
                parziale.pop()
