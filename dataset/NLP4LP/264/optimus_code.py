# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the number of units of chemical A and chemical B to add to the mixer
to minimize the total time for the mixed bread to be ready. Each unit of
chemical A takes TimeChemicalA to become effective, and each unit of chemical B
takes TimeChemicalB to become effective. The number of units of chemical A must
be at least MinChemicalA, the total number of units of chemicals A and B must be
at least MinTotalChemicals, and the number of units of chemical A must not
exceed MaxRatioAtoB times the number of units of chemical B.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/265/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimeChemicalA @Def: Time for one unit of chemical A to become effective @Shape: [] 
TimeChemicalA = data['TimeChemicalA']
# @Parameter TimeChemicalB @Def: Time for one unit of chemical B to become effective @Shape: [] 
TimeChemicalB = data['TimeChemicalB']
# @Parameter MaxRatioAtoB @Def: Maximum ratio of chemical A to chemical B @Shape: [] 
MaxRatioAtoB = data['MaxRatioAtoB']
# @Parameter MinChemicalA @Def: Minimum units of chemical A required @Shape: [] 
MinChemicalA = data['MinChemicalA']
# @Parameter MinTotalChemicals @Def: Minimum total units of chemicals in the mixer @Shape: [] 
MinTotalChemicals = data['MinTotalChemicals']

# Variables 
# @Variable QuantityChemicalA @Def: The number of units of chemical A @Shape: [] 
QuantityChemicalA = model.addVar(vtype=GRB.CONTINUOUS, lb=MinChemicalA, name="QuantityChemicalA")
# @Variable QuantityChemicalB @Def: The number of units of chemical B @Shape: [] 
QuantityChemicalB = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityChemicalB")

# Constraints 
# @Constraint Constr_1 @Def: The number of units of chemical A must be at least MinChemicalA.
model.addConstr(QuantityChemicalA >= MinChemicalA)
# @Constraint Constr_2 @Def: The total number of units of chemicals A and B must be at least MinTotalChemicals.
model.addConstr(QuantityChemicalA + QuantityChemicalB >= MinTotalChemicals)
# @Constraint Constr_3 @Def: The number of units of chemical A must not exceed MaxRatioAtoB times the number of units of chemical B.
model.addConstr(QuantityChemicalA <= MaxRatioAtoB * QuantityChemicalB)

# Objective 
# @Objective Objective @Def: Minimize the total time for the mixed bread to be ready, calculated as (TimeChemicalA * Units of Chemical A) + (TimeChemicalB * Units of Chemical B).
model.setObjective(TimeChemicalA * QuantityChemicalA + TimeChemicalB * QuantityChemicalB, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityChemicalA'] = QuantityChemicalA.x
variables['QuantityChemicalB'] = QuantityChemicalB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
