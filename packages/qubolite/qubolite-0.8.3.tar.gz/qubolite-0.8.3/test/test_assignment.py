import pytest

import networkx as nx



def make_graph(n: int, edges=None):
    G = nx.DiGraph()
    G.add_node('1')
    G.add_nodes_from([f'x{i}' for i in range(n)])
    if edges is not None:
        for e in edges:
            try:
                u, v, inv = e
            except ValueError:
                u, v = e
                inv = False
            G.add_edge(f'x{u}', f'x{v}', inverse=inv)
    return G


class TestPartialAssignment():

    def test_normalize_graph(self):
        G = make_graph(5, [(2,1), (4,0,True)])
        # TODO

    def test_to_expression(self):
        pass

    def test_from_expression(self):
        pass
