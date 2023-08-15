from neuronautics.analysis.type.graph_analysis import GraphAnalysis
from neuronautics.analysis.helpers import to_timeseries
import numpy as np


class ActivityCorrelation(GraphAnalysis):
    def get_input_params(self):
        return [
            {'name': 'bin_window_ms', 'min': 1, 'max': 1_000, 'default': 100, 'type': 'int'},
            {'name': 'corr_thr', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'}
        ]

    def run(self, spikes, bin_window_ms, corr_thr, *args, **kwargs):
        print('running', bin_window_ms, corr_thr)
        spikes['class'] = spikes['class'].astype(int)
        spikes = spikes[spikes['class'] >= 0]  # remove noise
        spikes = spikes[['channel_id', 'ts_ms']].copy().reset_index(drop=True)

        bin_df = to_timeseries(spikes, group_lvl='channel_id', bin_ms=bin_window_ms)

        w_ij = np.zeros((len(bin_df), len(bin_df)))
        for i, (ch_id_i, bin_i, events_i) in bin_df.iterrows():
            max_i = events_i.sum()
            for j, (ch_id_j, bin_j, events_j) in bin_df.iterrows():
                max_j = events_j.sum()
                shift_0 = (events_i[:-1] * events_j[1:]).sum()
                shift_1 = (events_i[1:] * events_j[:-1]).sum()
                shift_2 = (events_i * events_j).sum()
                w_ij[i, j] = (shift_0 + shift_1 + shift_2) / (3 * max(max_i, max_j))
                w_ij[i, j] = 0 if i == j else w_ij[i, j]

        return w_ij > corr_thr
    
    def plot(self, *args, **kwargs):
        return super().plot('Activity Correlation', *args, **kwargs)
