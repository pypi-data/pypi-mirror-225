from abc import ABC

from neuronautics.analysis.type.abstract_analysis import AbstractAnalysis, AnalysisType
from neuronautics.config.layout import Layout
from neuronautics.analysis.type.palette import Palette
import networkx as nx
import matplotlib.pyplot as plt


class GraphAnalysis(AbstractAnalysis, ABC):

    def type(self):
        return AnalysisType.GRAPH

    def plot(self, title='', *args, **kwargs):
        layout = Layout()
        layout.load()
        layout_mat = layout.current()
        electrode_positions = {int(id)-1: (j, i) for i, row in enumerate(layout_mat) for j, id in enumerate(row) if id}
        connectivity_matrix = self.run(*args, **kwargs)

        # Create a graph from the connectivity matrix
        G = nx.from_numpy_array(connectivity_matrix)

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Draw the graph with fixed node positions
        nx.draw(G, pos=electrode_positions, with_labels=True, node_size=350, node_shape='h',
                node_color='white', edgecolors=Palette.node_edge_color, font_size=8, font_color=Palette.label_color,
                edge_color=Palette.link_color, connectionstyle='arc3,rad=0.4', arrows=True, ax=ax)

        # Set plot labels and title
        ax.set_aspect('equal')
        ax.set_title(title)

        return fig
