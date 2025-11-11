# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient can take doses of NumPainKillers different pain killers. Each dose of
each pain killer delivers MedicinePerDose units of medicine to each of
NumTargets targets. The total amount of sleep medicine delivered must not exceed
MaxSleepMedicine units. The total amount of medicine delivered to the legs must
be at least MinLegsMedicine units. The objective is to determine the number of
doses of each pain killer to maximize the total amount of medicine delivered to
the back.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/120/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumPainKillers @Def: Number of different pain killers available @Shape: [] 
NumPainKillers = data['NumPainKillers']
# @Parameter NumTargets @Def: Number of different medicine targets @Shape: [] 
NumTargets = data['NumTargets']
# @Parameter MedicinePerDose @Def: Amount of medicine delivered to each target per dose for each pain killer @Shape: ['NumPainKillers', 'NumTargets'] 
MedicinePerDose = data['MedicinePerDose']
# @Parameter MaxSleepMedicine @Def: Maximum units of sleeping medicine that can be delivered @Shape: [] 
MaxSleepMedicine = data['MaxSleepMedicine']
# @Parameter MinLegsMedicine @Def: Minimum units of medicine required for legs @Shape: [] 
MinLegsMedicine = data['MinLegsMedicine']

# Define target indices
# Assuming target order is ['Sleep', 'legs', 'back']
target_indices = {"Sleep": 0, "legs": 1, "back": 2}

# Variables 
# @Variable NumDoses @Def: The number of doses for each painkiller @Shape: ['NumPainKillers'] 
NumDoses = model.addVars(NumPainKillers, vtype=GRB.CONTINUOUS, name="NumDoses")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of sleep medicine delivered must not exceed MaxSleepMedicine units.
model.addConstr(quicksum(MedicinePerDose[p][target_indices['Sleep']] * NumDoses[p] for p in range(NumPainKillers)) <= MaxSleepMedicine)
# @Constraint Constr_2 @Def: The total amount of medicine delivered to the legs must be at least MinLegsMedicine units.
model.addConstr(quicksum(MedicinePerDose[i][target_indices['legs']] * NumDoses[i] for i in range(NumPainKillers)) >= MinLegsMedicine)

# Objective 
# @Objective Objective @Def: The objective is to maximize the total amount of medicine delivered to the back.
model.setObjective(quicksum(NumDoses[i] * MedicinePerDose[i][target_indices['back']] for i in range(NumPainKillers)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumDoses'] = {p: NumDoses[p].X for p in range(NumPainKillers)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)