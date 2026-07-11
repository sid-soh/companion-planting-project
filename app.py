import os
import tempfile
from pathlib import Path

import pandas as pd
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from utils import create_graph, recommend_plants, avoid_plants


def drawGraph(plant_graph, selected_plant):
    name_to_node = {name: node_id for node_id, name in nx.get_node_attributes(plant_graph, "data").items()}
    selected_node = name_to_node.get(selected_plant)

    if selected_node is None:
        return

    neighborhood_nodes = {selected_node}
    neighborhood_nodes.update(plant_graph.successors(selected_node))
    neighborhood_nodes.update(plant_graph.predecessors(selected_node))

    neighborhood_graph = plant_graph.subgraph(neighborhood_nodes).copy()

    network = Network(height="600px", width="100%", directed=True, bgcolor="#ffffff", font_color="#1f2937")
    network.from_nx(neighborhood_graph)

    network.toggle_physics(False)
    network.set_options(
        """
        {
            "interaction": {
                "dragNodes": true,
                "dragView": true,
                "zoomView": true,
                "selectable": true,
                "hover": true
            },
            "physics": {
                "enabled": false
            }
        }
        """
    )

    for node in network.nodes:
        node_id = node["id"]
        plant_name = neighborhood_graph.nodes[node_id].get("data", str(node_id))
        node["label"] = plant_name
        node["title"] = plant_name
        node["color"] = "#2563eb" if node_id == selected_node else "#94a3b8"
        node["borderWidth"] = 3 if node_id == selected_node else 1

    for edge in network.edges:
        edge["title"] = edge.get("color", "relationship")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        network.write_html(str(temp_path), open_browser=False)
        components.html(temp_path.read_text(encoding="utf-8"), height=650, scrolling=True)
    finally:
        if temp_path.exists():
            os.unlink(temp_path)

st.write(
    """
    # Companion Plants App
    Select a plant to get recommendations and see which plants to avoid.
    """
)

file = "data/cleaned_data.csv"
plant_data = pd.read_csv(file)
plant_graph = create_graph(plant_data)

available_plants = list(nx.get_node_attributes(plant_graph, "data").values())

selected_plant = st.selectbox("Choose plant...", available_plants)

recc_col, avoid_col = st.columns(2)
with recc_col:
    st.write(f"### Recommendations:")
    recc_plants = recommend_plants(plant_graph, selected_plant)
    if recc_plants is not None and len(recc_plants) > 0:
        for plant in recc_plants:
            st.write(f"- {plant}")
    else:
        st.write("No recommendations available.")
with avoid_col:
    st.write(f"## Plants to avoid:")
    avoid_plants_list = avoid_plants(plant_graph, selected_plant)
    if avoid_plants_list is not None and len(avoid_plants_list) > 0:
        for plant in avoid_plants_list:
            st.write(f"- {plant}")
    else:
        st.write("No plants to avoid.")

st.write("## Companion Plant Graph")
drawGraph(plant_graph, selected_plant)

# Garden bed planner
st.write(
    """
    # Garden Bed Planner
    Select the number of rows and columns for your garden bed.
    """
)
row_picker, col_picker = st.columns(2)
with row_picker:
    row_num = st.number_input("Number of rows:", min_value=0, max_value=8, value=2, step=1)
with col_picker:
    col_num = st.number_input("Number of columns:", min_value=0, max_value=8, value=2, step=1)

st.write("""
        ## Garden Bed Layout
         """)
for i in range(row_num):
    cols = st.columns(col_num)
    for j in range(col_num):
        with cols[j]:
            plant_choice = st.selectbox(f"Row {i+1}, Column {j+1}", available_plants, key=f"{i}_{j}")
    