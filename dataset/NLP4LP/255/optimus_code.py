# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A smoothie shop produces AcaiSmoothies and BananaSmoothies. Each AcaiSmoothie
requires AcaiBerriesPerAcaiSmoothie units of acai berries and
WaterPerAcaiSmoothie units of water. Each BananaSmoothie requires
BananaChocolatePerBananaSmoothie units of banana chocolate and
WaterPerBananaSmoothie units of water. The number of BananaSmoothies produced
must be greater than the number of AcaiSmoothies produced. At least
MinAcaiProportion proportion of the total smoothies made must be AcaiSmoothies.
The shop has AcaiBerriesAvailable units of acai berries and
BananaChocolateAvailable units of banana chocolate available. The objective is
to minimize the total amount of water used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/256/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AcaiBerriesAvailable @Def: Total units of acai berries available @Shape: [] 
AcaiBerriesAvailable = data['AcaiBerriesAvailable']
# @Parameter BananaChocolateAvailable @Def: Total units of banana chocolate available @Shape: [] 
BananaChocolateAvailable = data['BananaChocolateAvailable']
# @Parameter AcaiBerriesPerAcaiSmoothie @Def: Units of acai berries required per acai berry smoothie @Shape: [] 
AcaiBerriesPerAcaiSmoothie = data['AcaiBerriesPerAcaiSmoothie']
# @Parameter WaterPerAcaiSmoothie @Def: Units of water required per acai berry smoothie @Shape: [] 
WaterPerAcaiSmoothie = data['WaterPerAcaiSmoothie']
# @Parameter BananaChocolatePerBananaSmoothie @Def: Units of banana chocolate required per banana chocolate smoothie @Shape: [] 
BananaChocolatePerBananaSmoothie = data['BananaChocolatePerBananaSmoothie']
# @Parameter WaterPerBananaSmoothie @Def: Units of water required per banana chocolate smoothie @Shape: [] 
WaterPerBananaSmoothie = data['WaterPerBananaSmoothie']
# @Parameter MinAcaiProportion @Def: Minimum proportion of smoothies that must be acai berry smoothies @Shape: [] 
MinAcaiProportion = data['MinAcaiProportion']

# Variables 
# @Variable AcaiSmoothies @Def: The number of AcaiSmoothies produced @Shape: [] 
AcaiSmoothies = model.addVar(vtype=GRB.CONTINUOUS, name="AcaiSmoothies")
# @Variable BananaSmoothies @Def: The number of BananaSmoothies produced @Shape: [] 
BananaSmoothies = model.addVar(vtype=GRB.CONTINUOUS, name="BananaSmoothies")

# Constraints 
# @Constraint Constr_1 @Def: The total units of acai berries used for AcaiSmoothies cannot exceed AcaiBerriesAvailable.
model.addConstr(AcaiBerriesPerAcaiSmoothie * AcaiSmoothies <= AcaiBerriesAvailable)
# @Constraint Constr_2 @Def: The total units of banana chocolate used for BananaSmoothies cannot exceed BananaChocolateAvailable.
model.addConstr(BananaChocolatePerBananaSmoothie * BananaSmoothies <= BananaChocolateAvailable)
# @Constraint Constr_3 @Def: The number of BananaSmoothies produced must be greater than the number of AcaiSmoothies produced.
model.addConstr(BananaSmoothies - AcaiSmoothies >= 0)
# @Constraint Constr_4 @Def: At least MinAcaiProportion proportion of the total smoothies made must be AcaiSmoothies.
model.addConstr(AcaiSmoothies >= MinAcaiProportion * (AcaiSmoothies + BananaSmoothies))

# Objective 
# @Objective Objective @Def: Minimize the total amount of water used, which is the sum of the water used by AcaiSmoothies and BananaSmoothies.
model.setObjective(WaterPerAcaiSmoothie * AcaiSmoothies + WaterPerBananaSmoothie * BananaSmoothies, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AcaiSmoothies'] = AcaiSmoothies.x
variables['BananaSmoothies'] = BananaSmoothies.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
