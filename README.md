# Octree

# Implementation of Octree algorithm to process data (points with X, Y, Z coordinates) in .las format file.  

# The task of the program is to implement a modified Octree algorithm. The algorithm should construct a standard Octree two times. Meaning at first it should divide the X, Y, Z field into 8 cubes and then again divide
those cubes into even smaller 8 cubes. Meaning 64 small cubes in the end. A sphere should be embedded into each of those 64 cubes. All the points that are outside of the sphere should be discarded. 
The final result should be visualized.

The program opens .las format file with coordinates of the points. Then it calculates the nearest and the furthest points from the starting point of the coordinates and from that moment it takes in
the consideration only this field, as there could be a situation where the points are quite far from the starting point and further manipulations could give no or insignificant results. 
Then the program divides the new field into 8 cuboids (yes, cuboids, not cubes as the length of the axis could differ by a lot, and again we would not get a significant result). This step is done to save 
time as for computer, it would take less time to check the results divided into 8 smaller databases than a single big one.
Then those 8 cuboids are divided into 8 smaller cuboids. After that, the program checks what points from the initial .las file are inside the spheres and what are not and writes the result in newly 
generated "output.las" file. Visualization of the result could be generated using "Octree_algorithm_visualization.ipynb" file that is also attached.
