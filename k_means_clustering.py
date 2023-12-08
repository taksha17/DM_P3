import sys
import random
import matplotlib.pyplot as plt

# Initialize an empty list to store the errors
errors = []

# Interpreting system argument for the data file
try:
    data_file = sys.argv[1]
    random.seed(0)
except IndexError:
    print("Usage: python script.py <data_file>")
    sys.exit(1)

# Read input file
with open(data_file, 'r') as file_open:
    file_lines = file_open.readlines()

# Function to calculate Euclidean Distance
def euclidean_distance(point_1, point_2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(point_1, point_2)) ** 0.5

# Function to initialize clusters
def initialize_cluster(n_clusters, file_lines):
    cluster = [[] for _ in range(n_clusters)]
    input_list = []
    dimension = 0
    for line in file_lines:
        values = [float(val) for val in line.strip().split()]
        dimension = len(values) - 1  # Assuming last value is the label
        input_list.append(values[:dimension])
        cluster[random.randint(0, n_clusters - 1)].append(values[:dimension])
    return dimension, cluster, input_list

def calculate_centroids(cluster, input_list):
    centroids = []
    for points in cluster:
        if points:  # Check if there are points in the cluster
            centroids.append([sum(dim) / len(dim) for dim in zip(*points)])
        else:  # If the cluster is empty, reinitialize a random centroid
            centroids.append(random.choice(input_list))
    return centroids


# K-means clustering
def k_means_clustering(n_clusters, n_iterations, input_list):
    dimension, cluster, input_list = initialize_cluster(n_clusters, file_lines)
    # centroids = calculate_centroids(cluster)
    centroids = calculate_centroids(cluster, input_list)

    for _ in range(n_iterations):
        cluster = [[] for _ in range(n_clusters)]
        for point in input_list:
            distances = [euclidean_distance(point, centroid) for centroid in centroids]
            min_distance_index = distances.index(min(distances))
            cluster[min_distance_index].append(point)
        # centroids = calculate_centroids(cluster)
        centroids = calculate_centroids(cluster, input_list)
    # Calculate total error
    error = sum(min(euclidean_distance(point, centroid) for centroid in centroids) for point in input_list)
    return error

# Running the k-means clustering for K = 2 to 10 and collecting errors
for k in range(2, 11):
    error = k_means_clustering(k, 20, file_lines)
    errors.append(error)  # Append the error to the list
    print(f'For k = {k} After 20 iterations: Error = {error:.4f}')

    # Plot the Error vs K chart
plt.plot(range(2, 11), errors, marker='o')
plt.title('Error vs Number of Clusters (K)')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Error')
plt.xticks(range(2, 11))  # Set x-axis ticks to match the range of K values
plt.grid(True)
plt.show()
