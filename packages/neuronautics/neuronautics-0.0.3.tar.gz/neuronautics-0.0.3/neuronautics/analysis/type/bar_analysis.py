from abc import ABC

from neuronautics.analysis.type.abstract_analysis import AbstractAnalysis, AnalysisType
from neuronautics.config.layout import Layout
import networkx as nx
import matplotlib.pyplot as plt


class BarAnalysis(AbstractAnalysis, ABC):

    def type(self):
        return AnalysisType.BAR

    def plot(self, value_units='', stacked=True, vertical=True, title='', *args, **kwargs):
        dataframe = self.run(*args, **kwargs)

        fig, ax = plt.subplots(figsize=(10, 6))

        columns = list(dataframe.columns)

        value_columns = columns[1:]
        label = columns[0]

        kind = 'bar' if vertical else 'barh'
        if stacked:
            dataframe[value_columns].plot(kind=kind, stacked=True, ax=ax)
        else:
            dataframe[value_columns].plot(kind=kind, ax=ax)

        if vertical:
            plt.xticks(range(len(dataframe)), dataframe[label])
            ax.set_ylabel(value_units)
        else:
            plt.yticks(range(len(dataframe)), dataframe[label])
            ax.set_xlabel(value_units)
        plt.legend(loc='center left', bbox_to_anchor=(1.005, 0.5))


        plt.title(title)
        plt.tight_layout()

        return fig
