import pyeapi
import pprint
import time
from graphviz import Digraph

nodes = []
edges = []
def create_topo(root, neigh_list):
    #nodes = []
    nodes_temp = [root]
    edges_temp = []
    #edges = []
    for neighbor in neigh_list:
         #print neighbor
    #    nodes.append(neighbor['neighborDevice'])
    #    #edges.append([root, neighbor['neighborDevice'], neighbor['neighborPort'] + "-" + neighbor['port'] ])
    #    edges.append([root, neighbor['neighborDevice']])
    #return [nodes, edges]
         #print neighbor
        #for key in neighbor :

    #    print ("******************************************************")
    #    print ("LLDP Neighbors for %s") % key
    #    print ("******************************************************")
            #for neighbordevices in neigh_list[key]:
            #print neighbors["Neighbor Device"]
         nodes_temp.append(neighbor["Neighbor Device"])
         edges_temp.append([root, neighbor["Neighbor Device"]])
    #print edges_temp
    nodes.append(nodes_temp)
    edges.append(edges_temp)
    #print nodes_temp
    #print nodes
    #print len(nodes)
    #print edges
    #print len(edges)
    return [nodes, edges]
    #return neigh_list

#my_topo = create_topo('Arista249', neighbors)


def make_topology(network_name, mytopo, sw_id):
    dot = Digraph(comment=network_name, format='png', engine='fdp')
    dot.graph_attr['splines'] = "ortho"
    #dot.attr(rankdir='LR')
    dot.attr('node', shape='box')
    #dot.attr('edge', dir='both')
    dot.attr('node', image="/Users/mdusija/Desktop/Python/Images/switch.png")
    #dot.attr('edge', arrowsize='2')
    dot.attr('edge', weight='10')
    dot.attr('edge', arrowhead='none')
    #dot.body.append(r'label = "\n\nMy Prettier Network Diagram"')
    dot.body.append('fontsize=20')
    for topo in mytopo[0]:
        for i in topo:
            dot.node(i)
            if i in sw_id :
                dot.attr(rank='min')
                #dot.node(i, pos='15,15')


    for topo in mytopo[1]:
        for i in topo:
        #dot.edge(i[0], i[1], i[2])
            dot.edge(i[0], i[1])
            #print i[0]
            #dot.attr(rank='min')

    return dot




def main():
    switches = ["yo410.sjc.aristanetworks.com", "yo653.sjc.aristanetworks.com"]
    value = []
    value1 = []
    switch_neighbor = {}
    #value_dict = {"Local Port" : "" , "Neighbor Device" : "", "Neighbor Port" : ""}


    for switch in switches :
        value =[]
        #switch = switch[0]
        node = pyeapi.connect(protocol="https", host=switch, username="mdusija", password="mdusija", port=None)
        neighbor = node.execute(["show lldp neighbors"])
        hostname = node.execute(["show hostname"])
        #print hostname


        for i in range(0,len(neighbor['result'][0]['lldpNeighbors'])) :

            value_temp = []
            value_dict={}
            value_dict["Local Port"] = str(neighbor['result'][0]['lldpNeighbors'][i]['port'])
            value_dict["Neighbor Device"] = str(neighbor['result'][0]['lldpNeighbors'][i]['neighborDevice'])
            value_dict["Neighbor Port"] = str(neighbor['result'][0]['lldpNeighbors'][i]['neighborPort'])

            if not value :
                value = [value, value_dict]
                #print value
            elif not value[0] :
                value = [value[1], value_dict]
                #print value
            else :
                value.append(value_dict)

        #print value
        switch_neighbor[switch] = value
            #print switch_neighbor[switch]
        my_topo = create_topo(switch, switch_neighbor[switch])
            #print len(my_topo)
            #print my_topo
            #for key in switch_neighbor :
            #  print ("******************************************************")
            #  print ("LLDP Neighbors for %s") % key
            #  print ("******************************************************")
            #  for neighbors in switch_neighbor[key]:
            #      print neighbors["Neighbor Device"]
    #print len(my_topo)
    #print my_topo
    dot = make_topology("My New Network", my_topo, switches)
    dot.view()
    dot.render(filename='Desktop/TopoDiag/NetworkDiag')



if __name__ == "__main__" :
    main()
