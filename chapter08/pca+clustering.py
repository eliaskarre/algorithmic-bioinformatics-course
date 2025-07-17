import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict

from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
data_pca2 = pca.fit_transform(data)

kmeans = KMeans(n_clusters=5, tol=1e-4)
labels = kmeans.fit_predict(data_pca2)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(data_pca2[:, 0], data_pca2[:, 1], c=labels, cmap="tab10", s=10)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title(f"PCA then k-Means Clustering (k={k})")
plt.colorbar(scatter, ticks=range(k), label="Cluster ID")
plt.tight_layout()
plt.savefig('PCA_clustering.png')
