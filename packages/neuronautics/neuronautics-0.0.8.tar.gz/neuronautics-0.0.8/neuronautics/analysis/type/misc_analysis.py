from abc import ABC

from neuronautics.analysis.type.abstract_analysis import AbstractAnalysis, AnalysisType


class MiscAnalysis(AbstractAnalysis, ABC):

    def type(self):
        return AnalysisType.OTHER
