from abc import ABC

from neuronautics.analysis.type.abstract_analysis import AbstractAnalysis, AnalysisType
from neuronautics.analysis.type.palette import Palette
import matplotlib.pyplot as plt


class ImageAnalysis(AbstractAnalysis, ABC):

    def type(self):
        return AnalysisType.IMAGE

    def plot(self, xlabel='', ylabel='', title='', cmap=None, *args, **kwargs):
        matrix = self.run(*args, **kwargs)

        fig, ax = plt.subplots(figsize=(10, 6))

        if cmap:
            ax = ax.imshow(matrix, cmap=cmap)
            plt.colorbar(ax)
        else:
            ax.imshow(matrix)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(False)

        return fig
