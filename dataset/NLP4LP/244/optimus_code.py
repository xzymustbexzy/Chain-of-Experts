# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An autobody shop needs to purchase AutoElectricJacks and GasPoweredJacks. Each
AutoElectricJack can process AutoElectricProcessingRate cars per hour and uses
AutoElectricElectricityUsage units of electricity per hour. Each GasPoweredJack
can process GasPoweredProcessingRate cars per hour and uses GasPoweredGasUsage
units of gas per hour. The shop must use fewer than MaxAutoElectricJacks
AutoElectricJacks. Additionally, the shop can use at most MaxElectricityUnits
units of electricity and MaxGasUnits units of gas. The objective is to maximize
the number of cars processed every hour.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/245/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AutoElectricProcessingRate @Def: The number of cars processed per hour by one automatic electric jack. @Shape: [] 
AutoElectricProcessingRate = data['AutoElectricProcessingRate']
# @Parameter AutoElectricElectricityUsage @Def: Units of electricity used per hour by one automatic electric jack. @Shape: [] 
AutoElectricElectricityUsage = data['AutoElectricElectricityUsage']
# @Parameter GasPoweredProcessingRate @Def: The number of cars processed per hour by one gas-powered jack. @Shape: [] 
GasPoweredProcessingRate = data['GasPoweredProcessingRate']
# @Parameter GasPoweredGasUsage @Def: Units of gas used per hour by one gas-powered jack. @Shape: [] 
GasPoweredGasUsage = data['GasPoweredGasUsage']
# @Parameter MaxAutoElectricJacks @Def: The maximum number of automatic electric jacks that can be used. @Shape: [] 
MaxAutoElectricJacks = data['MaxAutoElectricJacks']
# @Parameter MaxElectricityUnits @Def: The maximum units of electricity available. @Shape: [] 
MaxElectricityUnits = data['MaxElectricityUnits']
# @Parameter MaxGasUnits @Def: The maximum units of gas available. @Shape: [] 
MaxGasUnits = data['MaxGasUnits']

# Variables 
# @Variable AutoElectricJacksUsed @Def: The number of automatic electric jacks used @Shape: [] 
AutoElectricJacksUsed = model.addVar(vtype=GRB.INTEGER, name="AutoElectricJacksUsed", ub=MaxAutoElectricJacks)
# @Variable GasPoweredJacksUsed @Def: The number of gas-powered jacks used @Shape: [] 
GasPoweredJacksUsed = model.addVar(vtype=GRB.INTEGER, name="GasPoweredJacksUsed")

# Constraints 
# @Constraint Constr_1 @Def: The number of AutoElectricJacks used must be fewer than MaxAutoElectricJacks.
model.addConstr(AutoElectricJacksUsed <= MaxAutoElectricJacks - 1)
# @Constraint Constr_2 @Def: The total electricity usage by AutoElectricJacks must not exceed MaxElectricityUnits.
model.addConstr(AutoElectricElectricityUsage * AutoElectricJacksUsed <= MaxElectricityUnits)
# @Constraint Constr_3 @Def: The total gas usage by GasPoweredJacks must not exceed MaxGasUnits.
model.addConstr(GasPoweredGasUsage * GasPoweredJacksUsed <= MaxGasUnits)

# Objective 
# @Objective Objective @Def: Maximize the number of cars processed every hour.
model.setObjective(AutoElectricJacksUsed * AutoElectricProcessingRate + GasPoweredJacksUsed * GasPoweredProcessingRate, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AutoElectricJacksUsed'] = AutoElectricJacksUsed.x
variables['GasPoweredJacksUsed'] = GasPoweredJacksUsed.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
