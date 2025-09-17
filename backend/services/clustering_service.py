import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

class ClusteringService:
    def __init__(self, data: pd.DataFrame):
        self.data = data.select_dtypes(include=["float64", "int64"])

    def kmeans(self, n_clusters: int = 3):
        if self.data.empty:
            return []
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.data)
        model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = model.fit_predict(scaled_data)
        # Split dataset into clusters
        clusters = []
        for i in range(n_clusters):
            clusters.append(self.data.iloc[labels == i].to_dict(orient="records"))
        return clusters

    def agglomerative(self, n_clusters: int = 3):
        if self.data.empty:
            return []
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.data)
        model = AgglomerativeClustering(n_clusters=n_clusters)
        labels = model.fit_predict(scaled_data)
        clusters = []
        for i in range(n_clusters):
            clusters.append(self.data.iloc[labels == i].to_dict(orient="records"))
        return clusters
