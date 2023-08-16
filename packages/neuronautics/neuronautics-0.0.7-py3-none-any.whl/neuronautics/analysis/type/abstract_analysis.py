import abc
from enum import Enum


class AnalysisType(Enum):
    LINE = 'line'
    GRAPH = 'graph'
    BAR = 'bar'
    IMAGE = 'image'
    OTHER = 'misc'


class AbstractAnalysis(abc.ABC):

    @abc.abstractmethod
    def get_input_params(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def type(self):
        # line, bar, graph, image
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def plot(self, *args, **kwargs):
        raise NotImplementedError()

    def input_params_check(self, **kwargs):
        pass