import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


class SpikeSorter:

    def __init__(self, data):
        self.data = data
        self.output = None

    def pca(self, num_components):
        pca = PCA(n_components=num_components)
        self.data = pca.fit_transform(self.data)
        return self

    def kmeans(self, num_clusters):
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
        labels = kmeans.fit_predict(self.data)
        self.output = [int(lab) + 1 for lab in labels]
        return self

    def run(self):
        return self.output
