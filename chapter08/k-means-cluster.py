import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict


def cluster_by_centroids(data, centroids_rows):
    closest_centroid = [] # Tupel: (<distance>, <centroid id>)

    for x in range(len(data)):  #For each Row (Sample) in input Dataframe
        sample = data[x]                  
        distances_to_centroids = [] #List of distances to each of the k centroids

        for idx, centroid_row in enumerate(centroids_rows): #Compare distance to each centroid
            dist_sq = 0
            for y in range(len(sample)): #For each Column (Feature) of Row (Sample) of Input Dataframe
                #Sum Euclidian Distance
                diff = sample[y] - centroid_row[y] 
                dist_sq += diff * diff              
            distances_to_centroids.append((dist_sq**0.5, idx))  #Tupel: (<distance>, <centroid id>)
                                                                #Square root of sum is euclidian distance

        closest_centroid.append(min(distances_to_centroids, key=lambda t: t[0])) #chose the lowest distance centroid to be the closest
                                                                                 #each element of this list has the same index as the Rows of the Input Dataframe
    
    #Create Clustering Dictionary
    clusters = defaultdict(list)
    for idx, sample in enumerate(closest_centroid):
        cluster_id = sample[1]
        clusters[cluster_id].append(idx)
    
    return clusters

def calculate_new_centroids(data, clusters, k):
    new_centroids = np.zeros((k, data.shape[1]))

    for cluster_id, indices in clusters.items():
        if len(indices) > 0:
            new_centroids[cluster_id] = data[indices].mean(axis=0)
        else:
            new_centroids[cluster_id] = np.zeros(data.shape[1])
    
    return new_centroids

def k_means_cluster(data, k, tol):
     
    centroids_idx = random.sample(range(len(data)), k) #Find k random and distinct rows (as index) from input data 
    centroids_rows = data[centroids_idx]

    #Initial clustering

    clusters = cluster_by_centroids(data, centroids_rows)
    previous_centroids = centroids_rows.copy()
    #Calculate new Centroids and Cluster again

    converged = False

    while not converged:

        new_centroids = calculate_new_centroids(data, clusters, k)
        
        print("Previous:")
        print(previous_centroids)
        print("New:")
        print(new_centroids)

        shifts = np.linalg.norm(new_centroids - previous_centroids, axis=1)
        max_shift = shifts.max()
        print("Max Shift: ", max_shift)
        
        if max_shift < tol:
           converged = True

        clusters = cluster_by_centroids(data, new_centroids)

        previous_centroids = new_centroids.copy()

    return clusters, new_centroids

data = np.log1p(np.loadtxt("data.csv", delimiter=","))

clusters, centroids = k_means_cluster(data, 5, 0.0001)

print(clusters)
