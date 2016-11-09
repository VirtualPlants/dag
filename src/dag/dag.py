# Definition of electric dags intances


class DAG:
    def __init__(self, childrenlationship, childrenlationshipnb, geomcommands, root = 0, **nodeproperties):
        self.tt = childrenlationship
        self.nn = dict([(nid, dict(zip(self.tt[nid], w))) for nid, w in childrenlationshipnb.items() ])
        self.geomcommands = dict([(nid, (g[0], dict(zip(self.tt[nid], g[1]))  if len(g) > 1 else None ) ) for nid, g in geomcommands.items() ])
        self.root = root
        self._node_properties = nodeproperties
        self._parents = self._parentrelationship()

    def _parentrelationship(self):
        parents = dict([(vid, []) for vid in self.tt.keys()])
        for vid, children in self.tt.items():
            for c in children:
                parents[c].append(vid)
        return parents

    def nodes(self):
        return self.tt.keys()

    def parentrelationship(self):
        return self._parents

    def childrenlationship(sekf):
        return self.tt    

    def node_properties(self): 
        return self._node_properties

    def node_property(self,name):
        if not name in self._node_properties :
            self._node_properties[name] = {}
        return self._node_properties[name]

    def set_node_property(self,name, values = {}):
        self._node_properties[name] = values

    def preorder_egde_traversal(self):
        cnode = self.root
        toprocess = [(cnode, None)]
        alreadyprocessed = set()
        while len(toprocess) > 0:
            cnode, cparent = toprocess.pop(0)
            if cnode != self.root:
                yield cparent, cnode
            if not cnode in alreadyprocessed:
                if self.nb_children(cnode) > 0:
                    for cchild in self.children(cnode):
                        toprocess.append((cchild, cnode))
            alreadyprocessed.add(cnode)

    def postorder_edge_traversal(self):
        res = []
        for record in self.preorder_egde_traversal():
            res.append(record)
        for cparent, cnode in reversed(res):
            yield cparent, cnode

    def preorder_node_traversal(self):
        cnode = self.root
        toprocess = [cnode]
        parents = self.parentrelationship()
        alreadyprocessed = set()
        while len(toprocess) > 0:
            i = 0
            while not set(parents[toprocess[i]]).issubset(alreadyprocessed):
                i += 1
            cnode = toprocess.pop(i)
            alreadyprocessed.add(cnode)
            yield cnode
            if self.nb_children(cnode) > 0:
                for cchild in self.children(cnode):
                    if not cchild in toprocess:
                        toprocess.append(cchild)

    def postorder_node_traversal(self):
        res = []
        for record in self.preorder_node_traversal():
            res.append(record)
        for cnode in reversed(res):
            yield cnode

    def geom(self, nodeid):
        return self.geomcommands[nodeid][0]

    def children(self, nodeid):
        return self.tt[nodeid]

    def nb_children(self, nodeid):
        return len(self.tt[nodeid])

    def parents(self, nodeid):
        return self._parents[nodeid]

    def edge_weigth(self, parent, child):
        return self.nn[parent][child]

    def edge_geomcmd(self, parent, child):
        return self.geomcommands[parent][1][child]

    def interpret(self, instanciation = True, colorproperty = None, bounds = None, colormap = 'jet'):
        import openalea.lpy as lpy
        from openalea.plantgl.all import PglTurtle, Scene, Group, Shape
        print 'Instanciation :', instanciation

        def smb_interpret(cmd, turtle):
            ls = lpy.Lstring(cmd)
            lpy.turtle_interpretation(ls, turtle)

        def transf_interpret(cmd, smb, turtle):
            ls = lpy.Lstring(cmd)
            #print 'interpret', ls, cmd

            turtle.push()
            sc = lpy.turtle_partial_interpretation(ls, turtle)
            turtle.customGeometry(smb)
            turtle.pop()

        def sc2group(sc):
            if len(sc) == 1: return sc[0].geometry
            return Group([sh.geometry for sh in sc])

        def color_scene(sc, color):
            from openalea.plantgl.all import Discretizer, Scene
            d = Discretizer()
            for sh in sc:
                sh.geometry.apply(d)
                tr = d.result
                tr.colorList = [color for i in xrange(len(tr.indexList))]
                tr.colorPerVertex = False
                sh.geometry = tr

        geommap = dict()
        invorderednodes = []
        if colorproperty:
            from openalea.plantgl.scenegraph.colormap import PglColorMap
            if type(colorproperty) == str:
                cproperty = self.node_property(colorproperty)
            else:
                cproperty = colorproperty
            if bounds:
                cmap = PglColorMap(bounds[0],bounds[1],colormap)
            else:
                cmap = PglColorMap(min(cproperty.values()),max(cproperty.values()),colormap)
        for node in self.postorder_node_traversal():
            t = PglTurtle()
            #print node
            smb_interpret(self.geom(node), t)
            if colorproperty:
                color_scene(t.getScene(), cmap(cproperty[node]))

            if self.nb_children(node) > 0:
                for cchild, edgecmds in self.geomcommands[node][1].items():
                    for edgecmd in edgecmds:
                        transf_interpret(edgecmd, geommap[cchild] if instanciation else geommap[cchild].deepcopy(), t)
            smb = sc2group(t.getScene())
            smb.name = 'Shape_'+str(node)
            geommap[node] = smb

        t = PglTurtle()
        if colorproperty:
            return Scene([Shape(geommap[self.root],t.getColorList()[1])])+cmap.pglrepr() 
        else:
            return Scene([Shape(geommap[self.root],t.getColorList()[1])])


    def nb_elements(self):
        nb_elements = {}
        for ni in self.nodes():
          nb_elements[ni] = 1
        for ni, nj in self.postorder_edge_traversal():
          w = self.edge_weigth(ni,nj)
          nb_elements[ni] += nb_elements[nj] * w
        
        return nb_elements[self.root]            

    def get_tree(self):

        class TreeConstructor:
            def __init__(self, dag):
                self.ntopo = {}
                self.nweigth = {}
                self.ngeom = {}
                self.nproperties = dict([(name, {}) for name in dag._node_properties.keys()])

                self.idmap = {}
                self.idgen = 0
                self.dag = dag

            def process(self, current):
                cnewid = self.idgen
                self.idgen += 1
                self.idmap[cnewid] = current
                self.ntopo[cnewid] = []
                self.nweigth[cnewid] = []
                edge_geom_prop = []
                self.ngeom[cnewid] = [self.dag.geom(current),edge_geom_prop]
                for name, values in self.dag._node_properties.items():
                    self.nproperties[name][cnewid] = values[current]

                for child in self.dag.children(current):
                    ncid = self.process(child)
                    self.ntopo[cnewid].append(ncid)
                    self.nweigth[cnewid].append(self.dag.edge_weigth(current, child))
                    edge_geom_prop.append(self.dag.edge_geomcmd(current,child))
                return cnewid

            def generate(self):
                self.process(self.dag.root)
                return DAG(self.ntopo, self.nweigth, self.ngeom, self.idmap[self.dag.root], idmap=self.idmap, **self.nproperties)

        return TreeConstructor(self).generate()

    def is_strictlylinear(self):
        for vid, p in self._parents.items():
            if len(p) >= 2: 
                print vid, p
                return False
        return True

    @staticmethod
    def generate(depth = 9, w = 4):
        from math import log
        if w > 1:
            print 'nb elements :', (1 - w ** (depth+1))/(1-w)
        else:
            print 'nb elements :', depth


        topo = {}
        for i in xrange(0,depth):
          topo[i] = [i+1] 

        topo[depth] = [] 


        weight = {}
        for i in xrange(0,depth):
          weight[i] = [w] 

        weight[depth] = [] 

        minradius = 0.05
        maxradius = 2

        if w > 1:
            p = (depth * log(w)) / (log(maxradius) -log(minradius))
            radius = lambda d : pow(pow(w, depth-d), 1/p) * minradius
        else:
            deltaradius = maxradius - minradius
            radius = lambda d : minradius + deltaradius * ((depth-d) / float(depth))

        suma   = 250
        astart = 50
        adec   = 2 * (astart * depth - suma)/float((depth - 1) * depth)
        
        branchingangle = lambda d : astart - (adec * d)

        if w == 2:            
            phis = lambda d : ['/('+str(180/w + 360*v/w)+')^(-'+str(branchingangle(d))+')' for v in xrange(w)]
        else:
            phis = lambda d : ['']+['/('+str(180/w + 360*v/(w-1))+')^(-'+str(branchingangle(d))+')' for v in xrange(w-1)]

        geom = {}
        for i in xrange(0,depth):
          geom[i] = ['_('+str(radius(i))+')F('+str(10-(9*i/float(depth)))+')',[phis(i)]] 

        geom[depth] = ['_('+str(minradius)+')F(1)'] 

        return DAG(topo, weight, geom)
         

    @staticmethod
    def generate_random(depth = 9, nbchildren= (1,4), w = (1,2), maxjump = None):
        from math import log
        from random import randint

        assert nbchildren[0] >= 1
        assert w[0] >= 1

        if maxjump is None: 
            maxjump = depth

        # Trichotomic DAG with higher depth
        topo = dict([(i,[]) for i in xrange(0,depth)])
        for i in xrange(1,depth+1):
          candidate = randint(0,i-1)
          while len(topo[candidate]) >= nbchildren[1]:
              candidate = randint(0,i-1)
          topo[candidate].append(i) 

        for i in xrange(depth):
            n = randint(nbchildren[0],min(depth-i,nbchildren[1]))
            while len(topo[i]) < n:
                candidate = randint(i+1, min(depth, i+maxjump))
                if not candidate in topo[i]:
                    topo[i].append(candidate)

        topo[depth] = [] 

        for i in xrange(depth):
            topo[i].sort()


        weight = {}
        for i, children in topo.items():
          weight[i] = [randint(w[0],w[1]) for c in children] 

        weight[depth] = [] 

        minradius = 0.05
        maxradius = 2

        deltaradius = maxradius - minradius
        radius = lambda d : minradius + deltaradius * ((depth-d) / float(depth))

        suma   = 250
        astart = 50
        adec   = 2 * (astart * depth - suma)/float((depth - 1) * depth)
        
        branchingangle = lambda d : astart - (adec * d)

        phis = lambda d, prevtotw, w, totw : ['/('+str((prevtotw+v)*360/totw)+')^(-'+(str(branchingangle(d)) if w > 1 else str(0))+')' for v in xrange(w)]

        geom = {}
        for i in xrange(0,depth):
          geom[i] = ['_('+str(radius(i))+')F('+str(10-(9*i/float(depth)))+')',[phis(i, sum(weight[i][:j]), w , sum(weight[i])) for j,w in enumerate(weight[i])]] 

        geom[depth] = ['_('+str(minradius)+')F(1)'] 

        return DAG(topo, weight, geom)    

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

dag1 = DAG(t1, n1, g1)
dag2 = DAG(t2, n2, g2)
dag3 = DAG(t3, n3, g3)

def test_tree():
   d = DAG.generate_random(4,(1,3))
   print d.tt
   print d.parentrelationship()
   d2 = d.get_tree()
   print d2.tt
   print d2.parentrelationship()

