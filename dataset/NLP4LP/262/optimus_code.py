# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company uses camel caravans and desert trucks to transport goods to rural
cities. Each camel caravan can deliver CamelCaravanCapacity units of goods per
trip and takes CamelCaravanTime hours per trip. Each desert truck can deliver
DesertTruckCapacity units of goods per trip and takes DesertTruckTime hours per
trip. The company needs to deliver TotalGoodsToDeliver units of goods and
prefers to have more camel caravans than desert trucks. The objective is to
minimize the total number of hours required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/263/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CamelCaravanCapacity @Def: Amount of goods delivered per trip by a camel caravan @Shape: [] 
CamelCaravanCapacity = data['CamelCaravanCapacity']
# @Parameter CamelCaravanTime @Def: Time taken for one trip by a camel caravan @Shape: [] 
CamelCaravanTime = data['CamelCaravanTime']
# @Parameter DesertTruckCapacity @Def: Amount of goods delivered per trip by a desert truck @Shape: [] 
DesertTruckCapacity = data['DesertTruckCapacity']
# @Parameter DesertTruckTime @Def: Time taken for one trip by a desert truck @Shape: [] 
DesertTruckTime = data['DesertTruckTime']
# @Parameter TotalGoodsToDeliver @Def: Total amount of goods to be delivered @Shape: [] 
TotalGoodsToDeliver = data['TotalGoodsToDeliver']

# Variables 
# @Variable NumberCamelCaravans @Def: The number of camel caravans used @Shape: [] 
NumberCamelCaravans = model.addVar(vtype=GRB.INTEGER, name="NumberCamelCaravans")
# @Variable NumberDesertTrucks @Def: The number of desert trucks used @Shape: [] 
NumberDesertTrucks = model.addVar(vtype=GRB.INTEGER, name="NumberDesertTrucks")

# Constraints 
# @Constraint Constr_1 @Def: The combined delivery capacity of all camel caravans and desert trucks must be at least TotalGoodsToDeliver units.
model.addConstr(CamelCaravanCapacity * NumberCamelCaravans + DesertTruckCapacity * NumberDesertTrucks >= TotalGoodsToDeliver)

# Objective 
# @Objective Objective @Def: Minimize the total number of hours required, calculated as (Number of Camel Caravans × CamelCaravanTime) + (Number of Desert Trucks × DesertTruckTime), while preferring to use more camel caravans than desert trucks.
epsilon = 1e-5
model.setObjective(NumberCamelCaravans * CamelCaravanTime + NumberDesertTrucks * DesertTruckTime - epsilon * NumberCamelCaravans, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberCamelCaravans'] = NumberCamelCaravans.x
variables['NumberDesertTrucks'] = NumberDesertTrucks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
