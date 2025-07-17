non_log_data = np.loadtxt("data.csv", delimiter=",")

inertias, silhouettes = [], []
for k in range(2, 11):
    km = KMeans(n_clusters=k).fit(non_log_data) # I used the function from a library, because it was a little faster to test with it
                                        # Rather then with my Implementation
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(non_log_data, km.labels_))
print("Inertias: ", inertias)
print("Silhouettes: ", silhouettes)

# Elbow Method
plt.figure()
plt.plot(range(2, 11), inertias, marker='o')
plt.xlabel('Number of Cluster k')
plt.ylabel('Inertia (WCSS)')
plt.title('Elbow-Methode: Inertia vs k')
plt.savefig('inertia.png')

# Silhouette-Score
plt.figure()
plt.plot(range(2, 11), silhouettes, marker='o')
plt.xlabel('Number of Cluster k')
plt.ylabel('Silhouette-Score')
plt.title('Silhouette-Analysis: Score vs k')
plt.savefig('silhouette.png')
