# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The clinic must perform a number of throat swabs and nasal swabs. Each throat
swab requires TimeThroatSwab minutes and each nasal swab requires TimeNasalSwab
minutes. At least MinimumNasalSwabs nasal swabs must be administered. The number
of throat swabs must be at least ThroatToNasalRatio times the number of nasal
swabs. The clinic operates for a total of TotalOperationalTime minutes. The
objective is to maximize the total number of patients seen.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/119/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimeThroatSwab @Def: Time required to perform one throat swab in minutes @Shape: [] 
TimeThroatSwab = data['TimeThroatSwab']
# @Parameter TimeNasalSwab @Def: Time required to perform one nasal swab in minutes @Shape: [] 
TimeNasalSwab = data['TimeNasalSwab']
# @Parameter MinimumNasalSwabs @Def: Minimum number of nasal swabs to be performed @Shape: [] 
MinimumNasalSwabs = data['MinimumNasalSwabs']
# @Parameter ThroatToNasalRatio @Def: Minimum ratio of throat swabs to nasal swabs @Shape: [] 
ThroatToNasalRatio = data['ThroatToNasalRatio']
# @Parameter TotalOperationalTime @Def: Total operational time available in minutes @Shape: [] 
TotalOperationalTime = data['TotalOperationalTime']

# Variables 
# @Variable NumThroatSwab @Def: The number of throat swabs to be performed @Shape: [] 
NumThroatSwab = model.addVar(vtype=GRB.INTEGER, name="NumThroatSwab")
# @Variable NumNasalSwab @Def: The number of nasal swabs to be performed @Shape: [] 
NumNasalSwab = model.addVar(lb=MinimumNasalSwabs, vtype=GRB.INTEGER, name='NumNasalSwab')

# Constraints 
# @Constraint Constr_1 @Def: Each throat swab requires TimeThroatSwab minutes and each nasal swab requires TimeNasalSwab minutes. The total operational time cannot exceed TotalOperationalTime minutes.
model.addConstr(TimeThroatSwab * NumThroatSwab + TimeNasalSwab * NumNasalSwab <= TotalOperationalTime, 'OperationalTime')
# @Constraint Constr_2 @Def: At least MinimumNasalSwabs nasal swabs must be administered.
model.addConstr(NumNasalSwab >= MinimumNasalSwabs)
# @Constraint Constr_3 @Def: The number of throat swabs must be at least ThroatToNasalRatio times the number of nasal swabs.
model.addConstr(NumThroatSwab >= ThroatToNasalRatio * NumNasalSwab)

# Objective 
# @Objective Objective @Def: The objective is to maximize the total number of patients seen.
model.setObjective(NumThroatSwab + NumNasalSwab, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumThroatSwab'] = NumThroatSwab.x
variables['NumNasalSwab'] = NumNasalSwab.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
