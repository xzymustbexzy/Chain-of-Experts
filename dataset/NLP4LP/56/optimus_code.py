# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of GasGrills and ElectricGrills to minimize the total
number of grills, such that GasPattiesPerMinute multiplied by GasGrills plus
ElectricPattiesPerMinute multiplied by ElectricGrills is at least
MinPattiesPerMinute, GasOilPerMinute multiplied by GasGrills plus
ElectricOilPerMinute multiplied by ElectricGrills does not exceed
MaxOilPerMinute, and the number of ElectricGrills is less than the number of
GasGrills.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/57/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GasPattiesPerMinute @Def: The number of patties a single gas grill can cook per minute @Shape: [] 
GasPattiesPerMinute = data['GasPattiesPerMinute']
# @Parameter ElectricPattiesPerMinute @Def: The number of patties a single electric grill can cook per minute @Shape: [] 
ElectricPattiesPerMinute = data['ElectricPattiesPerMinute']
# @Parameter GasOilPerMinute @Def: The units of cooking oil a single gas grill uses per minute @Shape: [] 
GasOilPerMinute = data['GasOilPerMinute']
# @Parameter ElectricOilPerMinute @Def: The units of cooking oil a single electric grill uses per minute @Shape: [] 
ElectricOilPerMinute = data['ElectricOilPerMinute']
# @Parameter MinPattiesPerMinute @Def: The minimum number of patties the chain wants to make per minute @Shape: [] 
MinPattiesPerMinute = data['MinPattiesPerMinute']
# @Parameter MaxOilPerMinute @Def: The maximum units of cooking oil the chain wants to use per minute @Shape: [] 
MaxOilPerMinute = data['MaxOilPerMinute']

# Variables 
# @Variable GasGrills @Def: The number of gas grills used @Shape: ['Integer'] 
GasGrills = model.addVar(vtype=GRB.INTEGER, name="GasGrills")
# @Variable ElectricGrills @Def: The number of electric grills used @Shape: ['Integer'] 
ElectricGrills = model.addVar(vtype=GRB.INTEGER, name="ElectricGrills")

# Constraints 
# @Constraint Constr_1 @Def: GasPattiesPerMinute multiplied by GasGrills plus ElectricPattiesPerMinute multiplied by ElectricGrills is at least MinPattiesPerMinute
model.addConstr(GasPattiesPerMinute * GasGrills + ElectricPattiesPerMinute * ElectricGrills >= MinPattiesPerMinute)
# @Constraint Constr_2 @Def: GasOilPerMinute multiplied by GasGrills plus ElectricOilPerMinute multiplied by ElectricGrills does not exceed MaxOilPerMinute
model.addConstr(GasOilPerMinute * GasGrills + ElectricOilPerMinute * ElectricGrills <= MaxOilPerMinute)
# @Constraint Constr_3 @Def: The number of ElectricGrills is less than the number of GasGrills
model.addConstr(ElectricGrills <= GasGrills - 1)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of grills, which is the sum of GasGrills and ElectricGrills.
model.setObjective(GasGrills + ElectricGrills, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['GasGrills'] = GasGrills.x
variables['ElectricGrills'] = ElectricGrills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
