
# A Linear DAG with H states from 0 to H-1
# is defined by two dictionaries: (t,n)
# transition array t
# 0 is the first unit of the trunk, H-1 are the leaves
# to key i corresponds the list of its targets j in the DAG

# duplication array n:
# Number of tree duplications for a transition in the DAG:
# to each node i, and each target node j (in the same order as in t)
# n[i][j] defines the number of times branch (i,j) in the DAG is duplicated
# in the tree

# Geometry primitives
m1 = "F"
langle= "+(30)"
rangle = "-(30)"
id = "+(0)"

phi2 = "/(180)^(-30)"

phi31 = "/(60)^(-30)"
phi32 = "/(180)^(-30)"
phi33 = "/(300)^(-30)"

# print "Passing in module dags"

# DAG definitions
t1 = {
0: [1,2], 
1: [2,3],
2: [3,4],
3: [4,5],
4: [5,6],
5: [6,7],
6: [7,8],
7: [8,9],
8: [9],
9: []
}

n1 = {
0:[1,1],
1:[1,1],
2:[1,1],
3:[1,1],
4:[1,1],
5:[1,1],
6:[1,1],
7:[1,1],
8:[1],
9:[]
}

# Structure of the geometry dict:
# array containing a string corresponding to the model of node i and an array of edge geometries
# the array of edge geometries contains as many elements as the array t1[i] (and n1[i])
# (= nb of edges exiting from node i to different nodes k)
# its kth element is an array containing n1[i][k] strings corresponding to the string defining
# the relative orientation of each duplicated element specified by this edge

# t1 is a monopodial tree:
# at each bifurcation, the main branch has no change in geometric direction wrt parent branch (= Identity (id))
# the other branch makes an angle phi2 with the parent branch direction

g1 = {
0:[m1,[ [id],[phi2] ] ],
1:[m1,[ [id],[phi2] ] ],
2:[m1,[ [id],[phi2] ] ],
3:[m1,[ [id],[phi2] ] ],
4:[m1,[ [id],[phi2] ] ],
5:[m1,[ [id],[phi2] ] ],
6:[m1,[ [id],[phi2] ] ],
7:[m1,[ [id],[phi2] ] ],
8:[m1,[ [id],[phi2] ] ],
9:[m1]
}

# Dichotomic DAG 
t2 = {
0: [1], 
1: [2],
2: [3],
3: [4],
4: [5],
5: [6],
6: [7],
7: [8],
8: [9],
9: []
}

n2 = {
0:[2], 
1:[2],
2:[2],
3:[2],
4:[2],
5:[2],
6:[2],
7:[2],
8:[2],
9:[]
}

g2 = {
0:[m1,[[langle,rangle]]],
1:[m1,[[langle,rangle]]],
2:[m1,[[langle,rangle]]],
3:[m1,[[langle,rangle]]],
4:[m1,[[langle,rangle]]],
5:[m1,[[langle,rangle]]],
6:[m1,[[langle,rangle]]],
7:[m1,[[langle,rangle]]],
8:[m1,[[langle,rangle]]],
9:[m1]
}

# Trichotomic DAG 
t3 = {
0: [1], 
1: [2],
2: [3],
3: [4],
4: [5],
5: [6],
6: [7],
7: [8],
8: [9],
9: []
}

n3 = {
0:[3], 
1:[3],
2:[3],
3:[3],
4:[3],
5:[3],
6:[3],
7:[3],
8:[3],
9:[]
}



g3 = {
0:[m1,[[phi31,phi32,phi33]]],
1:[m1,[[phi31,phi32,phi33]]],
2:[m1,[[phi31,phi32,phi33]]],
3:[m1,[[phi31,phi32,phi33]]],
4:[m1,[[phi31,phi32,phi33]]],
5:[m1,[[phi31,phi32,phi33]]],
6:[m1,[[phi31,phi32,phi33]]],
7:[m1,[[phi31,phi32,phi33]]],
8:[m1,[[phi31,phi32,phi33]]],
9:[m1]
}

# Trichotomic DAG with higher depth
t3_14 = {
0: [1],
1: [2],
2: [3],
3: [4],
4: [5],
5: [6],
6: [7],
7: [8],
8: [9],
#9: [10],
#10: [11],
#11: [12],
#12: [13],
#13: []
9 : []
}

n3_14 = {
0:[3],
1:[3],
2:[3],
3:[3],
4:[3],
5:[3],
6:[3],
7:[3],
8:[3],
#9:[3],
#10:[3],
#11:[3],
#12:[3],
#13:[]
9 : []
}

g3_14 = {
0:[m1,[[phi31,phi32,phi33]]],
1:[m1,[[phi31,phi32,phi33]]],
2:[m1,[[phi31,phi32,phi33]]],
3:[m1,[[phi31,phi32,phi33]]],
4:[m1,[[phi31,phi32,phi33]]],
5:[m1,[[phi31,phi32,phi33]]],
6:[m1,[[phi31,phi32,phi33]]],
7:[m1,[[phi31,phi32,phi33]]],
8:[m1,[[phi31,phi32,phi33]]],
#9:[m1,[[phi31,phi32,phi33]]],
#10:[m1,[[phi31,phi32,phi33]]],
#11:[m1,[[phi31,phi32,phi33]]],
#12:[m1,[[phi31,phi32,phi33]]],
#13:[m1]
9:[m1]
}



# Simulation of lateral resistance on each segment based on t1
t4 = {
0: [1,2,9],
1: [2,3,9],
2: [3,4,9],
3: [4,5,9],
4: [5,6,9],
5: [6,7,9],
6: [7,8,9],
7: [8,9,9],
8: [9],
9: []
}

n4 = {
0:[1,1,1],
1:[1,1,1],
2:[1,1,1],
3:[1,1,1],
4:[1,1,1],
5:[1,1,1],
6:[1,1,1],
7:[1,1,1],
8:[1],
9:[]
}

# Simulation of lateral resistance on each segment based on t1
# now lateral resistances are decreasing with height
t5 = {
0: [1,2,9],
1: [2,3,9],
2: [3,4,9],
3: [4,5,9],
4: [5,6,9],
5: [6,7,9],
6: [7,8,9],
7: [8,9,9],
8: [9],
9: []
}

n5 = {
0:[1,1,4],
1:[1,1,4],
2:[1,1,3],
3:[1,1,3],
4:[1,1,2],
5:[1,1,2],
6:[1,1,1],
7:[1,1,1],
8:[1],
9:[]
}

# Resistances of segments corresponding to a DAG are defined by an array:
# resistance of module at height h
# indexes refer to h values (as explained above)

# Note:
# si les resistances s'annullent a partir d'une certaine hauteur :
#  r = [0.,0.,0.,0.,0.,1.,1.,1.,1.,1.]
# les conductivites suivent la suite de Fibonacci !!!
# (dans le cas d'une arborescence avec un automate
# ayant un saut de h vers h+1 et h+2 seulement)
# car C(h) = C(h+1) + C(h+2)

# RESISTANCES
# exact values for fibonacci for:

r1 = [0., 0., 0., 0., 0., 0., 0., 0., 0., 1.]
r2 = [0.,0.,0.,0.,0.,1.,1.,1.,1.,1.]
r21 = [0.,0.,0.,0.,0.,0.1,0.1,0.1,0.1,1.]
r22 = [0.,0.,0.,0.,0.,1,1,1,1,10.]
r3 = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
r4 = [0.001,0.005,0.01,0.05,0.1,0.5,1.,1.,1.,1.]
r5 = [0.5,0.05,0.01,0.05,0.1,0.1,0.5,1.,1.,1.]

#r4.reverse

from dag import DAG

dag1 = DAG(t1, n1, g1)
dag2 = DAG(t2, n2, g2)
dag3 = DAG(t3, n3, g3)
