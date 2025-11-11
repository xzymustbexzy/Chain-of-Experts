# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A market owner wants to start a jam business. He can either sell sets of small
packets or jugs. Each set of small packets has a capacity of SmallPacketCapacity
milliliters and each jug has a capacity of JugCapacity milliliters. At least
MinJugRatio times as many jugs must be used as sets of small packets. At least
MinSmallPackets sets of small packets must be filled. The market owner has
TotalJam milliliters of jam. The owner aims to maximize the total number of
units sold to customers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/237/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallPacketCapacity @Def: Capacity of one set of small packets in milliliters @Shape: [] 
SmallPacketCapacity = data['SmallPacketCapacity']
# @Parameter JugCapacity @Def: Capacity of one jug in milliliters @Shape: [] 
JugCapacity = data['JugCapacity']
# @Parameter MinJugRatio @Def: Minimum ratio of jugs to sets of small packets @Shape: [] 
MinJugRatio = data['MinJugRatio']
# @Parameter MinSmallPackets @Def: Minimum number of sets of small packets to be filled @Shape: [] 
MinSmallPackets = data['MinSmallPackets']
# @Parameter TotalJam @Def: Total available milliliters of jam @Shape: [] 
TotalJam = data['TotalJam']

# Variables 
# @Variable NumberOfSmallPacketSets @Def: The number of sets of small packets @Shape: [] 
NumberOfSmallPacketSets = model.addVar(vtype=GRB.INTEGER, name="NumberOfSmallPacketSets")
# @Variable NumberOfJugs @Def: The number of jugs @Shape: [] 
NumberOfJugs = model.addVar(vtype=GRB.INTEGER, name="NumberOfJugs")
# @Variable TotalJamUsedSmall @Def: The total milliliters of jam used by small packet sets @Shape: [] 
TotalJamUsedSmall = model.addVar(vtype=GRB.CONTINUOUS, name="TotalJamUsedSmall")
# @Variable TotalJamUsedJugs @Def: The total milliliters of jam used by jugs @Shape: [] 
TotalJamUsedJugs = model.addVar(vtype=GRB.CONTINUOUS, name="TotalJamUsedJugs")

# Constraints 
# @Constraint Constr_1 @Def: The total jam used for small packets and jugs cannot exceed the total available jam (TotalJam).
model.addConstr(NumberOfSmallPacketSets * SmallPacketCapacity + NumberOfJugs * JugCapacity <= TotalJam)
# @Constraint Constr_2 @Def: Each set of small packets sold uses SmallPacketCapacity milliliters of jam.
model.addConstr(TotalJamUsedSmall == NumberOfSmallPacketSets * SmallPacketCapacity)
# @Constraint Constr_3 @Def: Each jug sold uses JugCapacity milliliters of jam.
model.addConstr(TotalJamUsedJugs == JugCapacity * NumberOfJugs)
# @Constraint Constr_4 @Def: The number of jugs sold must be at least MinJugRatio times the number of sets of small packets sold.
model.addConstr(NumberOfJugs >= MinJugRatio * NumberOfSmallPacketSets)
# @Constraint Constr_5 @Def: At least MinSmallPackets sets of small packets must be filled.
model.addConstr(NumberOfSmallPacketSets >= MinSmallPackets)

# Objective 
# @Objective Objective @Def: The objective is to maximize the total number of units sold to customers, where total units sold are the sum of sets of small packets and jugs sold.
model.setObjective(NumberOfSmallPacketSets + NumberOfJugs, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSmallPacketSets'] = NumberOfSmallPacketSets.x
variables['NumberOfJugs'] = NumberOfJugs.x
variables['TotalJamUsedSmall'] = TotalJamUsedSmall.x
variables['TotalJamUsedJugs'] = TotalJamUsedJugs.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
