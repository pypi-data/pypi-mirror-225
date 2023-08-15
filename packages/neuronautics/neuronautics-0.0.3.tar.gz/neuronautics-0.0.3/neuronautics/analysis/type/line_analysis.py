from abc import ABC

from neuronautics.analysis.type.abstract_analysis import AbstractAnalysis, AnalysisType
from neuronautics.analysis.type.palette import Palette
import matplotlib.pyplot as plt


class LineAnalysis(AbstractAnalysis, ABC):

    def type(self):
        return AnalysisType.LINE

    def plot(self, xlabel='', ylabel='', title='', *args, **kwargs):
        dataframe = self.run(*args, **kwargs)

        x_values = dataframe.iloc[:, 0]
        y_values = dataframe.iloc[:, 1:]

        fig, ax = plt.subplots(figsize=(10, 6))

        for col in y_values.columns:
            ax.plot(x_values, y_values[col], label=col)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Place legend outside the plot on the right
        plt.grid(True)

        return fig
