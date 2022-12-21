"""
The task is to implement a modified Octree algorithm. The algorithm should construct a standard Octree two times. Meaning at first it should divide the X, Y, Z field into 8 cubes and then again divide
those cubes into even smaller 8 cubes. Meaning 64 small cubes in the end. A sphere should be embedded into each of those 64 cubes. All the points that are outside of the sphere should be discarded. 
The final result should be visualized.

The program opens .las format file with coordinates of the points. Then it calculates the nearest and the furthest points from the starting point of the coordinates and from that moment it takes in
the consideration only this field, as there could be a situation where the points are quite far from the starting point and further manipulations could give no or insignificant results. 
Then the program divides the new field into 8 cuboids (yes, cuboids, not cubes as the length of the axis could differ by a lot, and again we would not get a significant result). This step is done to save 
time as for computer, it would take less time to check the results divided into 8 smaller databases than a single big one.
Then those 8 cuboids are divided into 8 smaller cuboids. After that, the program checks what points from the initial .las file are inside the spheres and what are not and writes the result in newly 
generated "output.las" file. Visualization of the result could be generated using "Octree_algorithm_visualization.ipynb" file that is also attached.
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
# If you want a .las format file to open, you have to write the name of the file below.
las = laspy.read('XXX.las')
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
def minXYZ():
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
minXYZ()
print("The shortest axis of the future Octree cuboid was found and is equal to", round(min, 2))

start_time4 = time.time()

# Creating new list where the program will write the coordinates of the centers of big cuboids / spheres. 
centerB = []

# The coordinates of the first center of the cuboid / sphere, which is the closest one to the starting point coordinates.
center_x = minX + distX / 4
center_y = minY + distY / 4
center_z = minZ + distZ / 4

# Finding center coordinates of each big octree cuboid / sphere.
def finding_centers():
    global center_x
    global center_y
    global center_z
    while center_x < maxX:
        if center_y < maxY:
            if center_z < maxZ:
                centerB.append((center_x, center_y, center_z))
                center_z = center_z + (distZ / 2)
            elif center_y < maxY:
                center_z = minZ + (distZ / 4)
                center_y = center_y + (distY / 2)
        elif center_x < maxX:
            center_z = minZ + (distZ / 4)
            center_y = minY + (distY / 4)
            center_x = center_x + (distX / 2)
    else:
        return centerB
finding_centers()

print("Centers of the big Octree cuboids were found. The total number of cuboids:", len(centerB), " Time taken for the operation:", " %s seconds " % round(time.time() - start_time4, 3))

start_time4_1 = time.time()

# Creating new list where the program will write the coordinates of the centers of small cuboids / spheres. 
centerS = []

center_x = minX + distX / 8
center_y = minY + distY / 8
center_z = minZ + distZ / 8

# Finding center coordinates of each small octree cuboid / sphere.
def finding_centers():
    global center_x
    global center_y
    global center_z
    while center_x < maxX:
        if center_y < maxY:
            if center_z < maxZ:
                centerS.append((center_x, center_y, center_z))
                center_z = center_z + (distZ / 4)
            elif center_y < maxY:
                center_z = minZ + (distZ / 8)
                center_y = center_y + (distY / 4)
        elif center_x < maxX:
            center_z = minZ + (distZ / 8)
            center_y = minY + (distY / 8)
            center_x = center_x + (distX / 4)
    else:
        return centerS
finding_centers()

print("Centers of the small Octree cuboids were found. The total number of cuboids:", len(centerS), " Time taken for the operation:", " %s seconds " % round(time.time() - start_time4_1, 3), "\n")

# Creating new empty lists where coordinates of the points would be stored divided into octree cuboids.
octreeB = [[] for _ in range(len(centerB))]
# Creating new empty list where center coordinates of the big octree cuboids will be stored. 
octreeCentersB = [[] for _ in range(len(centerB))]
# Creating new empty list where all of the points coordinates will be stored divided into big cuboids.
octree = [[] for _ in range(len(centerB))]

start_time5 = time.time()

print("Starting the operation dividing bigger cuboids into smaller ones and saving center coordinates of the smaller cuboids.")
# Calculating distance from center of the cuboid to the border of the cuboid. 
rx = distX / 4
ry = distY / 4
rz = distZ / 4

def octree_cuboids_CentersB():
    i = 0
    a = 0
    while a in range (len(centerB)):
            print("Checking the small cuboid centers in the big cuboid No.", a+1)
            while i in range(len(centerS)):
                if centerS[i][0] >= (centerB[a][0]-rx) and centerS[i][0] <= (centerB[a][0]+rx) and centerS[i][1] >= (centerB[a][1]-ry) and centerS[i][1] <= (centerB[a][1]+ry) and centerS[i][2] >= (centerB[a][2]-rz) and centerS[i][2] <= (centerB[a][2]+rz):
                    octreeCentersB[a].append(((centerS[i][0], centerS[i][1], centerS[i][2])))
                    i += 1
                else: 
                    i += 1
            else:
                i = 0
                a += 1
    return octreeCentersB
octree_cuboids_CentersB()

# Checking the total number of centers in all of the cuboids combined, to be sure that we haven't lost any in the process.
def numbc():
    global numb
    numb = 0
    g = 0
    while g in range(len(octreeCentersB)):
        numb = numb + len(octreeCentersB[g])
        g += 1
    return numb
numbc()
print("Checking the total number of centers in all cuboids combined:", numb)
print("The operation finished in", " %s seconds " % round(time.time() - start_time5, 3), "\n")

start_time5_1 = time.time()

print("Starting the operation for positioning points coordinates of big cuboids to the list.")
# Calculating distance from center of the cuboid to the border of the cuboid. 
rx = distX / 4
ry = distY / 4
rz = distZ / 4

# Function that divides the points by coordinates from the list to n amount of bigger octree cuboids.
def octree_cuboids_B():
    i = 0
    a = 0
    while a in range (len(centerB)):
            print("Checking the points in big cuboid No.", a+1)
            while i in range(len(output_X)):
                if output_X[i] >= (centerB[a][0]-rx) and output_X[i] <= (centerB[a][0]+rx) and output_Y[i] >= (centerB[a][1]-ry) and output_Y[i] <= (centerB[a][1]+ry) and output_Z[i] >= (centerB[a][2]-rz) and output_Z[i] <= (centerB[a][2]+rz):
                    octreeB[a].append(((output_X[i], output_Y[i], output_Z[i])))
                    i += 1
                else: 
                    i += 1
            else:
                i = 0
                a += 1
    return octreeB
octree_cuboids_B()

# Checking the total number of points in all of the cuboids combined, to be sure that we haven't lost any in the process.
def numbb():
    global numb
    numb = 0
    g = 0
    while g in range(len(octreeB)):
        numb = numb + len(octreeB[g])
        g += 1
    return numb
numbb()  
print("Checking the total number of points in all cuboids combined:", numb)
print("The operation finished in", " %s seconds " % round(time.time() - start_time5_1, 3), "\n")

start_time5_2 = time.time()

print("Starting the operation for division into smaller cuboids.")
# Calculating distance from center of the cuboid to the border of the cuboid. 
rx = distX / 8
ry = distY / 8
rz = distZ / 8

# Function that devides the coordinates from the list to n amount of smaller octree cuboids.
def octree_cuboids():
    i = 0
    a = 0
    b = 0
    c = 0
    while a in range(len(centerB)): 
        while b in range (len(octreeB)): 
            print("Checking the points in small cuboid No.", c+1)
            while i in range(len(octreeB[a])):
                if (octreeCentersB[a][b][0]-rx) <= octreeB[a][i][0] and (octreeCentersB[a][b][0]+rx) >= octreeB[a][i][0] and (octreeCentersB[a][b][1]-ry) <= octreeB[a][i][1] and (octreeCentersB[a][b][1]+ry) >= octreeB[a][i][1] and (octreeCentersB[a][b][2]-rz) <= octreeB[a][i][2] and (octreeCentersB[a][b][2]+rz) >= octreeB[a][i][2]:
                    octree[a].append(((octreeB[a][i][0], octreeB[a][i][1], octreeB[a][i][2])))
                    i += 1
                else:
                    i += 1
            else:
                i = 0
                b += 1
                c += 1
        else:
            i = 0
            b = 0
            a += 1   

# Checking the total number of points in all of the cuboids combined, to be sure that we haven't lost any in the process.
    def numbb():
        global numb
        numb = 0
        g = 0
        while g in range(len(octree)):
            numb = numb + len(octree[g])
            g += 1
        return numb
    numbb()
            
    print("Total number of points in all octree cuboids:", numb, "\n")
    print("Difference in point numbers:", len(output_X) - numb, "\n")
    print("The operation finished in", " %s seconds " % round(time.time() - start_time5_2, 3), "\n")

    print("Starting the operation which will find what points belong to spheres.")
    start_time6 = time.time()

# This part of the funcion checks if coordinates in small octree cuboid belongs to the sphere that is inside the cuboid.
    global results_x
    global results_y
    global results_z
    results_x = []
    results_y = []
    results_z = []
    i = 0
    j = 0
    a = 0
    c = 0
    while a in range (len(octree)):
            while j in range(len(octreeCentersB[a])):
                print("Checking the points in sphere No.", c+1)
                while i in range(len(octree[a])):
                    if (((octree[a][i][0]-octreeCentersB[a][j][0])**2 + (octree[a][i][1]-octreeCentersB[a][j][1])**2 + (octree[a][i][2]-octreeCentersB[a][j][2])**2) <= ((min/8)**2)): 
                        results_x.append(octree[a][i][0])
                        results_y.append(octree[a][i][1])
                        results_z.append(octree[a][i][2])
                        i += 1
                    else: 
                        i += 1
                else:
                    i = 0
                    j += 1
                    c += 1
            else:
                i = 0
                j = 0
                a += 1
    print("The operation finished in", " %s seconds " % round(time.time() - start_time6, 3))
    return results_x, results_y, results_z
octree_cuboids()

print("The total amount of the points that belongs to the Spheres: ", len(results_x), "\n")

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
print("If you want to see visualization of the results please run Octree_algorithm_visualization.ipynb file")
input("Press enter to exit!")