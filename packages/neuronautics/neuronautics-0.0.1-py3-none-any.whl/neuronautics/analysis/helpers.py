import numpy as np


def to_timeseries(data, group_lvl, bin_ms=100):
    """
    helper function for binarizing a timeseries of events
    """
    data['bin'] = (data['ts_ms'] // bin_ms).astype(int)
    end_time = data['bin'].max()

    bin_df = data.groupby(group_lvl)['bin'].agg(list).reset_index()
    def _to_timeseries(events):
        bin = np.zeros(end_time + 1)
        bin[events] = 1
        return bin

    bin_df['events'] = bin_df.bin.map(_to_timeseries)
    return bin_df