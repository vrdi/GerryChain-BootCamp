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

num_elections = 14


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


initial_partition = Partition(graph, "2011_PLA_1", updaters)

#Other possible starting plans are: 
#"2011_PLA_1": Congressional district ID in 2011 enacted congressional map
#"GOV": Congressional district ID in Governor’s counter-proposed plan
#"TS": Congressional district ID in Turzai-Scarnati Plan
#"REMEDIAL_P": Congressional district ID in 2018 enacted remedial plan
#"538CPCT__1": Congressional district ID in 538’s compactness favoring plan
#"538DEM_PL": Congressional district ID in 538’s Democratic favoring plan
#"538GOP_PL": Congressional district ID in 538’s Republican favoring plan
#"8THGRADE_1": Congressional district ID in Jon Kimmel’s eighth grade class’s second redistricting plan

#FUNCTION GO HERE

    
    
