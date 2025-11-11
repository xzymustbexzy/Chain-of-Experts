# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
To minimize the total number of machines, the ice cream store must decide how
many counter-top sized machines and fridge sized machines to purchase. Each
counter-top machine produces ProductionCounterTop ice creams per day and outputs
HeatCounterTop units of heat, while each fridge machine produces
ProductionFridge ice creams per day and outputs HeatFridge units of heat. The
total heat output must not exceed MaxHeat, and the total ice cream production
must be at least MinProduction.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/53/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProductionCounterTop @Def: Ice cream production per day by a counter-top sized machine @Shape: [] 
ProductionCounterTop = data['ProductionCounterTop']
# @Parameter ProductionFridge @Def: Ice cream production per day by a fridge sized machine @Shape: [] 
ProductionFridge = data['ProductionFridge']
# @Parameter HeatCounterTop @Def: Heat output per day by a counter-top sized machine @Shape: [] 
HeatCounterTop = data['HeatCounterTop']
# @Parameter HeatFridge @Def: Heat output per day by a fridge sized machine @Shape: [] 
HeatFridge = data['HeatFridge']
# @Parameter MaxHeat @Def: Maximum heat output per day @Shape: [] 
MaxHeat = data['MaxHeat']
# @Parameter MinProduction @Def: Minimum ice cream production per day @Shape: [] 
MinProduction = data['MinProduction']

# Variables 
# @Variable MachinesCounterTop @Def: The number of counter-top sized machines @Shape: [] 
MachinesCounterTop = model.addVar(vtype=GRB.INTEGER, name="MachinesCounterTop")
# @Variable MachinesFridge @Def: The number of fridge-sized machines @Shape: [] 
MachinesFridge = model.addVar(vtype=GRB.INTEGER, name="MachinesFridge")

# Constraints 
# @Constraint Constr_1 @Def: The total heat output from all counter-top and fridge-sized machines must not exceed MaxHeat.
model.addConstr(HeatCounterTop * MachinesCounterTop + HeatFridge * MachinesFridge <= MaxHeat)
# @Constraint Constr_2 @Def: The total ice cream production from all counter-top and fridge-sized machines must be at least MinProduction.
model.addConstr(ProductionCounterTop * MachinesCounterTop + ProductionFridge * MachinesFridge >= MinProduction)

# Objective 
# @Objective Objective @Def: Minimize the total number of machines, which is the sum of the number of counter-top and fridge-sized machines.
model.setObjective(MachinesCounterTop + MachinesFridge, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['MachinesCounterTop'] = MachinesCounterTop.x
variables['MachinesFridge'] = MachinesFridge.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
