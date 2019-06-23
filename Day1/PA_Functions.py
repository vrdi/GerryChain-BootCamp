import csv
import os
from functools import partial
import json

import geopandas as gpd
import matplotlib.pyplot as plt

from gerrychain import (
    Election,
    Graph,
    MarkovChain,
    Partition,
    accept,
    constraints,
    updaters,
)
from gerrychain.metrics import efficiency_gap, mean_median
from gerrychain.proposals import recom
from gerrychain.updaters import cut_edges
from gerrychain.tree import recursive_tree_part

newdir = "./Outputs/"
os.makedirs(os.path.dirname(newdir + "init.txt"), exist_ok=True)
with open(newdir + "init.txt", "w") as f:
    f.write("Created Folder")


graph_path = "./Data/PA_VTDALL.json"  # "./Data/PA_BPOP_FINAL/VTD_FINAL.shp"
plot_path = "./Data/VTD_FINAL.shp"


df = gpd.read_file(plot_path)


def num_splits(partition):
    df["current"] = df[unique_label].map(dict(partition.assignment))
    splits = sum(df.groupby("COUNTYFP10")["current"].nunique() > 1)
    return splits


unique_label = "GEOID10"
pop_col = "TOT_POP"
district_col = "2011_PLA_1"
county_col = "COUNTYFP10"

num_elections = 3


election_names = [
    "PRES12",
    "PRES16",
    "SENW101216",
]
election_columns = [
    ["PRES12D", "PRES12R"],
    ["T16PRESD", "T16PRESR"],
    ["W101216D", "W101216R"],
]


graph = Graph.from_json(graph_path)


updaters = {
    "population": updaters.Tally("TOT_POP", alias="population"),
    "cut_edges": cut_edges,
}

elections = [
    Election(
        election_names[i],
        {"Democratic": election_columns[i][0], "Republican": election_columns[i][1]},
    )
    for i in range(num_elections)
]

election_updaters = {election.name: election for election in elections}

updaters.update(election_updaters)


partition_2011 = Partition(graph, "2011_PLA_1", updaters)
partition_GOV = Partition(graph, "GOV", updaters)
partition_TS = Partition(graph, "TS", updaters)
partition_REMEDIAL = Partition(graph, "REMEDIAL_P", updaters)
partition_CPCT = Partition(graph, "538CPCT__1", updaters)
partition_DEM = Partition(graph, "538DEM_PL", updaters)
partition_GOP = Partition(graph, "538GOP_PL", updaters)
partition_8th = Partition(graph, "8THGRADE_1", updaters)
tree_partitions = []
for i in range(10):
    cddict =  recursive_tree_part(graph,range(18),df["TOT_POP"].sum()/18,"TOT_POP", .01,1)
    tree_partitions.append(Partition(graph, cddict, updaters))

    
    
print("The 2011 plan has" , len(partition_2011["cut_edges"]), "cut edges.")
print("The GOV plan has" , len(partition_GOV["cut_edges"]), "cut edges.")
print("The TS plan has" , len(partition_TS["cut_edges"]), "cut edges.")
print("The REMEDIAL plan has" , len(partition_REMEDIAL["cut_edges"]), "cut edges.")
print("The 538 Compact plan has" , len(partition_CPCT["cut_edges"]), "cut edges.")
print("The 538 DEM plan has" , len(partition_DEM["cut_edges"]), "cut edges.")
print("The 538 GOP plan has" , len(partition_GOP["cut_edges"]), "cut edges.")
print("The 8th grade plan has" , len(partition_8th["cut_edges"]), "cut edges.")
for i in range(10):
    print(f"Tree plan #{i} has" , len(tree_partitions[i]["cut_edges"]), "cut edges.")


#NEW FUNCTIONs GO HERE

    
    
