import os
import numpy as np
from jakteristics import compute_features

# Thresholds
threshold_zstart = 2
threshold_wrong_branch = 0.5
threshold_verticality = 0.3

# Specify the directory containing the point cloud files
directory = "path/to/your/point-cloud-files/"

# Create the 'lower' and 'upper' directories if they don't exist
lower_dir = os.path.join(directory, "lower")
upper_dir = os.path.join(directory, "upper")
os.makedirs(lower_dir, exist_ok=True)
os.makedirs(upper_dir, exist_ok=True)

# Get a list of all files with the .xyz extension in the directory
file_list = [f for f in os.listdir(directory) if f.endswith('.xyz')]

def calculate_verticality_jakteristics(point_cloud, search_radius=0.2):
    """
    Calculate verticality for each point in the point cloud using jakteristics.

    Parameters:
        point_cloud (ndarray): Nx3 array of points with columns [x, y, z].
        search_radius (float): Radius for neighbourhood search.

    Returns:
        ndarray: Verticality values for each point.
    """
    xyz = point_cloud[:, :3]  # Extract only x, y, z coordinates
    features = compute_features(xyz, search_radius=search_radius, feature_names=['verticality'])
    return features[:, 0]  # 'verticality' is the first feature in the output

# Process each file in the directory
for file_name in file_list:
    # Load the point cloud from the current file
    file_path = os.path.join(directory, file_name)
    point_cloud = np.loadtxt(file_path)
    
    # Preprocess: Calculate verticality using jakteristics
    verticality = calculate_verticality_jakteristics(point_cloud)
    point_cloud = np.hstack((point_cloud, verticality[:, np.newaxis]))
    
    # Sort the point cloud based on the z-values in ascending order
    sorted_point_cloud = point_cloud[np.argsort(point_cloud[:, 2])]
    
    # Find the minimum and maximum z-values
    min_z = sorted_point_cloud[:, 2].min()
    max_z = sorted_point_cloud[:, 2].max()
    
    if max_z - min_z > 20:
        threshold_zstart = 0.3 * (max_z - min_z)
    
    # Initialize variables to store the z-values and differences
    z_values = []
    differences = []
    occurrence_counter = 0
    
    # Iterate over the sorted point cloud
    for j in range(sorted_point_cloud.shape[0] - 1):
        z1, z2 = sorted_point_cloud[j, 2], sorted_point_cloud[j + 1, 2]
        v1, v2 = sorted_point_cloud[j, 3], sorted_point_cloud[j + 1, 3]
        
        # Check if the z-value is above (min_z + threshold_zstart)
        if z2 - min_z > threshold_zstart:
            # Check if the difference in verticality values is greater than the threshold
            if abs(v2 - v1) > threshold_verticality:
                occurrence_counter += 1
                z_values.append(z2)
                differences.append(abs(v2 - v1))
                
                # Check for consecutive occurrences
                if occurrence_counter >= 2:
                    diff_z = abs(z_values[-1] - z_values[-2])
                    if diff_z >= threshold_wrong_branch:
                        z_values.clear()
                        differences.clear()
                        occurrence_counter = 0
                        continue
                
                if occurrence_counter == 4:
                    break
    
    # Segment the point cloud into upper and lower portions
    if z_values:
        segment_threshold = z_values[0] - 2
        upper_point_cloud = point_cloud[point_cloud[:, 2] >= segment_threshold]
        lower_point_cloud = point_cloud[point_cloud[:, 2] < segment_threshold]
    else:
        upper_point_cloud = point_cloud
        lower_point_cloud = np.empty((0, point_cloud.shape[1]))
    
    # Save the upper and lower point clouds to separate files
    lower_file_path = os.path.join(lower_dir, file_name)
    upper_file_path = os.path.join(upper_dir, file_name)
    np.savetxt(lower_file_path, lower_point_cloud, fmt="%.6f")
    np.savetxt(upper_file_path, upper_point_cloud, fmt="%.6f")

