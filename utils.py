import pandas as pd
import networkx as nx

def create_graph(df):
    # Names of the plants -> nodes
    # Edges -> colour-coded, green for help and red for avoid
    G = nx.DiGraph()
    num_node = 0

    for index, row in df.iterrows():
        plant1 = row['Source Node']
        plant2 = row['Destination Node']
        relationship = row['Link']

        if relationship == 'helps' or relationship == 'helped_by':
            color = 'green'
        elif relationship == 'avoid':
            color = 'red'
        else:
            color = 'gray'  # For any other relationships

        name = nx.get_node_attributes(G, "data")
        name_list = list(name.values())

        if plant1 in name_list:
            plant1_node = name_list.index(plant1)
        else:
            G.add_node(num_node, data=plant1)
            plant1_node = num_node
            num_node += 1    
        if plant2 in name_list:
            plant2_node = name_list.index(plant2)
        else:
            G.add_node(num_node, data=plant2)
            plant2_node = num_node
            num_node += 1

        if relationship == 'helps':
            G.add_edge(plant2_node, plant1_node, color=color)
        elif relationship == 'helped_by':
            G.add_edge(plant1_node, plant2_node, color=color)
        else:    
            G.add_edge(plant1_node, plant2_node, color=color)

    return G

def recommend_plants(G, plant_name):
    # Get the node index for the given plant name
    name = nx.get_node_attributes(G, "data")
    name_list = list(name.values())
    
    if plant_name not in name_list:
        return []
    
    plant_node = name_list.index(plant_name)
    
    # Get all neighboring nodes in both directions and keep only green relationships.
    neighboring_nodes = set(G.successors(plant_node)) | set(G.predecessors(plant_node))
    recommended_nodes = []
    for node in neighboring_nodes:
        edge_colors = []
        if G.has_edge(plant_node, node):
            edge_colors.append(G[plant_node][node]['color'])
        if G.has_edge(node, plant_node):
            edge_colors.append(G[node][plant_node]['color'])

        if 'green' in edge_colors:
            recommended_nodes.append(node)
    
    # Get the names of the recommended plants
    recommended_plants = [name[n] for n in recommended_nodes]
    
    return recommended_plants

def avoid_plants(G, plant_name):
    # Get the node index for the given plant name
    name = nx.get_node_attributes(G, "data")
    name_list = list(name.values())
    
    if plant_name not in name_list:
        return []
    
    plant_node = name_list.index(plant_name)
    
    # Get all neighboring nodes in both directions and keep only red relationships.
    neighboring_nodes = set(G.successors(plant_node)) | set(G.predecessors(plant_node))
    avoid_nodes = []
    for node in neighboring_nodes:
        edge_colors = []
        if G.has_edge(plant_node, node):
            edge_colors.append(G[plant_node][node]['color'])
        if G.has_edge(node, plant_node):
            edge_colors.append(G[node][plant_node]['color'])

        if 'red' in edge_colors:
            avoid_nodes.append(node)
    
    # Get the names of the plants to avoid
    avoid_plants = [name[n] for n in avoid_nodes]
    
    return avoid_plants