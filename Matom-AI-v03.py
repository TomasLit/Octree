"""
Your task is to implement a modified Octree algorithm. The algorithm should construct a standard Octree, but we want you to embed a sphere in each of the Octree cubes. 
All the points within a sphere should further be subdivided into eight cubes (with spheres inside). All the points that are outside of the sphere can be discarded. Visualize the results.
"""

import numpy as np
import laspy
import laspy.header
import laspy.file
import time

start_time = time.time()
print("The program has started!")

# Reading a .las file.
print("Starting to read the .las file")
las = laspy.read('2743_1234.las')
coordinates = np.stack((las.x, las.y, las.z)).transpose()
print("Finished reading .las file in", " %s seconds " % round(time.time() - start_time, 3))
start_time2 = time.time()

# Reading coordindates of each point in X, Y, Z axis. 
coordinates_X = np.array(las.x)
coordinates_Y = np.array(las.y)
coordinates_Z = np.array(las.z)
print("Numpy arrays for X, Y, Z axis were created in", " %s seconds " % round(time.time() - start_time2, 3))
start_time3 = time.time()

# Converting information about points from numpy arrays into lists.
output_X = coordinates_X.tolist()
output_Y = coordinates_Y.tolist()
output_Z = coordinates_Z.tolist()
print("Numpy arrays were converted to lists in", " %s seconds " % round(time.time() - start_time3, 3))
print("The total amount of points in the .len file : ", len(output_X))

# Finding the most distant points in each axis. 
minX = min(output_X)
minY = min(output_Y)
minZ = min(output_Z)
print("The least distant points in the axis X, Y and Z were found.")

# Finding the most distant points in each axis. 
maxX = max(output_X)
maxY = max(output_Y)
maxZ = max(output_Z)
print("The most distant points in the axis X, Y and Z were found.")

# Distance between the most and least distant points to the coordinates starting point.
distX = maxX - minX
distY = maxY - minY
distZ = maxZ - minZ
print("The distances between most and least distant points to the starting point of the coordinates were found (X, Y, Z):", round(distX, 2), ",", round(distY, 2), ",", round(distZ, 2))

# To create a sphere inside Octree cuboid we need to know the shortest axis. Calculating the shortest axis.
def minXYZa():
    global min
    if distX <= distY:
        if distX <= distZ:
            min = distX
            return min
        else: 
            min = distZ
            return min
    elif distY <= distZ:
        min = distY
        return min
    else:
        min = distZ
        return min
minXYZa()
print("The shortest axis of the future Octree cuboid was found and is equal to", round(min, 2))

# Creating new list where the program will write the coordinates of the centers of cuboids / spheres. 
center = []

# The coordinates of the first center of the cuboid / sphere, which is the closest one to the starting point coordinates.
center_x = minX + (distX / 8)
center_y = minY + (distY / 8)
center_z = minZ + (distZ / 8)

start_time4 = time.time()

# Finding center coordinates of each octree cuboid / sphere.
def finding_centers():
    global center_x
    global center_y
    global center_z
    while center_x < maxX:
        if center_y < maxY:
            if center_z < maxZ:
                center.append((center_x, center_y, center_z))
                center_z = center_z + (distZ / 4)
            elif center_y < maxY:
                center_z = minZ + (distZ / 8)
                center_y = center_y + (distY / 4)
        elif center_x < maxX:
            center_z = minZ + (distZ / 8)
            center_y = minY + (distY / 8)
            center_x = center_x + (distX / 4)
    else:
        return center
finding_centers()

print("Centers of the Octree cuboids were found. The total number of cuboids:", len(center), " Time taken for the operation:", " %s seconds " % round(time.time() - start_time4, 3), "\n")

# Creating new empty list were coordinates of the points would be stored divided into octree cuboids.
octree = [[] for _ in range(len(center))]

print("Starting the operation for division into smaller cuboids.")
start_time5 = time.time()

# Calculating distance from center of the cuboid to the border of the cuboid. 
rx = distX / 8
ry = distY / 8
rz = distZ / 8

# Function that devides the coordinates from the list to n amount of smaller octree cuboids.
def octree_cuboids():
    i = 0
    a = 0
    while a in range (len(center)):
            print("Checking the points in cuboid No.", a+1)
            while i in range(len(output_X)):
                if output_X[i] >= (center[a][0]-rx) and output_X[i] <= (center[a][0]+rx) and output_Y[i] >= (center[a][1]-ry) and output_Y[i] <= (center[a][1]+ry) and output_Z[i] >= (center[a][2]-rz) and output_Z[i] <= (center[a][2]+rz):
                    octree[a].append(((output_X[i], output_Y[i], output_Z[i])))
                    i += 1
                else: 
                    i += 1
            else:
                i = 0
                a += 1
    print("The operation finished in", " %s seconds " % round(time.time() - start_time5, 3), "\n")
    print("Starting the operation which will find what points belong to spheres.")
    start_time6 = time.time()

    # Second part of the funcion - that checks if coordinates in small octree cuboid belongs to the sphere that is inside the cuboid.
    global results_x
    global results_y
    global results_z
    results_x = []
    results_y = []
    results_z = []
    i = 0
    a = 0
    while a in range (len(octree)):
            print("Checking the points in sphere No.", a+1)
            while i in range(len(octree[a])):
                if (((octree[a][i][0]-center[a][0])**2 + (octree[a][i][1]-center[a][1])**2 + (octree[a][i][2]-center[a][2])**2) <= ((min/8)**2)): 
                    results_x.append(octree[a][i][0])
                    results_y.append(octree[a][i][1])
                    results_z.append(octree[a][i][2])
                    i += 1
                else: 
                    i += 1
            else:
                i = 0
                a += 1
    print("The operation finished in", " %s seconds " % round(time.time() - start_time6, 3), "\n")
    return results_x, results_y, results_z
octree_cuboids()

print("The total amount of the points that belongs to the Spheres: ", len(results_x))
start_time7 = time.time()

# Converting the results from list to numpy array
results_array_x = np.array(results_x)
results_array_y = np.array(results_y)
results_array_z = np.array(results_z)
print("Converting results to numpy array in", " %s seconds " % round(time.time() - start_time7, 3))

start_time8 = time.time()

# Creating new .las file 
my_data_xx = np.array(results_array_x)
my_data_yy = np.array(results_array_y)
my_data_zz = np.array(results_array_z)
my_data = np.hstack((my_data_xx.reshape((-1, 1)), my_data_yy.reshape((-1, 1)), my_data_zz.reshape((-1, 1))))

# Creating a new header for .las file
header = laspy.LasHeader(point_format=3, version="1.2")
header.add_extra_dim(laspy.ExtraBytesParams(name="random", type=np.int32))
header.offsets = np.min(my_data, axis=0)
header.scales = np.array([0.01, 0.01, 0.01])

# Creating a Las
las = laspy.LasData(header)

las.x = my_data[:, 0]
las.y = my_data[:, 1]
las.z = my_data[:, 2]

las.write("output.las")

print("New .las file created in", " %s seconds " % round(time.time() - start_time8, 3))
print("The whole program has finished in", " %s seconds " % round(time.time() - start_time, 3))
print("If you want to see visualization of the results please run Matom-AI_visualization.ipynb file")
input("Press enter to exit!")
