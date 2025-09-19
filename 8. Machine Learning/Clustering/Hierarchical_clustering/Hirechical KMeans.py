import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Users\shali\Desktop\DS_Road_Map\8. Machine Learning\Clustering\Hierarchical_DBCSAN\Mall_Customers.csv")
x = dataset.iloc[:,[3,4]].values

import scipy.cluster.hierarchy as sch
dendogram = sch.dendrogram(sch.linkage(x,method ="ward"))

plt.title("Dendogram")
plt.xlabel("Cluster")
plt.ylabel("Eucliden Ditances")
plt.show()

# Fitting Agglomerative Clustering
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters=5, linkage='ward')
y_hc = hc.fit_predict(x)

# Plotting Clusters
plt.figure(figsize=(8, 5))
plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s=100, c='green', label='Cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s=100, c='cyan', label='Cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s=100, c='magenta', label='Cluster 5')
plt.title('Hierarchical Clusters of Customers')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1–100)')
plt.legend()
plt.show()
