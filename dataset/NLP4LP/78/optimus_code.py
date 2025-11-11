# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A restaurant produces two types of curry: goat curry and chicken curry. Each
bowl of goat curry requires GoatMeatPerGoatCurry units of goat meat and
CurryBasePerGoatCurry units of curry base. Each bowl of chicken curry requires
ChickenMeatPerChickenCurry units of chicken meat and CurryBasePerChickenCurry
units of curry base. The restaurant has TotalGoatMeatAvailable units of goat
meat and TotalChickenMeatAvailable units of chicken meat available. At least
MinChickenCurryPercentage of the total curry bowls produced must be chicken
curry. Additionally, the number of goat curry bowls produced must be greater
than the number of chicken curry bowls. The objective is to determine the number
of bowls of each type of curry to produce in order to minimize the total units
of curry base used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/79/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GoatMeatPerGoatCurry @Def: Units of goat meat required to produce one bowl of goat curry @Shape: [] 
GoatMeatPerGoatCurry = data['GoatMeatPerGoatCurry']
# @Parameter ChickenMeatPerChickenCurry @Def: Units of chicken meat required to produce one bowl of chicken curry @Shape: [] 
ChickenMeatPerChickenCurry = data['ChickenMeatPerChickenCurry']
# @Parameter CurryBasePerGoatCurry @Def: Units of curry base required to produce one bowl of goat curry @Shape: [] 
CurryBasePerGoatCurry = data['CurryBasePerGoatCurry']
# @Parameter CurryBasePerChickenCurry @Def: Units of curry base required to produce one bowl of chicken curry @Shape: [] 
CurryBasePerChickenCurry = data['CurryBasePerChickenCurry']
# @Parameter TotalGoatMeatAvailable @Def: Total available units of goat meat @Shape: [] 
TotalGoatMeatAvailable = data['TotalGoatMeatAvailable']
# @Parameter TotalChickenMeatAvailable @Def: Total available units of chicken meat @Shape: [] 
TotalChickenMeatAvailable = data['TotalChickenMeatAvailable']
# @Parameter MinChickenCurryPercentage @Def: Minimum percentage of curry bowls that must be chicken curry @Shape: [] 
MinChickenCurryPercentage = data['MinChickenCurryPercentage']

# Variables 
# @Variable NumGoatCurry @Def: The number of bowls of goat curry @Shape: ['integer'] 
NumGoatCurry = model.addVar(vtype=GRB.INTEGER, name="NumGoatCurry")
# @Variable NumChickenCurry @Def: The number of bowls of chicken curry @Shape: ['integer'] 
NumChickenCurry = model.addVar(vtype=GRB.INTEGER, name="NumChickenCurry")

# Constraints 
# @Constraint Constr_1 @Def: Each bowl of goat curry requires GoatMeatPerGoatCurry units of goat meat, and the total goat meat used cannot exceed TotalGoatMeatAvailable units.
model.addConstr(GoatMeatPerGoatCurry * NumGoatCurry <= TotalGoatMeatAvailable)
# @Constraint Constr_2 @Def: Each bowl of chicken curry requires ChickenMeatPerChickenCurry units of chicken meat, and the total chicken meat used cannot exceed TotalChickenMeatAvailable units.
model.addConstr(ChickenMeatPerChickenCurry * NumChickenCurry <= TotalChickenMeatAvailable)
# @Constraint Constr_3 @Def: At least MinChickenCurryPercentage of the total curry bowls produced must be chicken curry.
model.addConstr(NumChickenCurry >= MinChickenCurryPercentage * (NumChickenCurry + NumGoatCurry))
# @Constraint Constr_4 @Def: The number of goat curry bowls produced must be greater than the number of chicken curry bowls.
model.addConstr(NumGoatCurry >= NumChickenCurry + 1)

# Objective 
# @Objective Objective @Def: Minimize the total units of curry base used, calculated as (CurryBasePerGoatCurry * number of goat curry bowls) + (CurryBasePerChickenCurry * number of chicken curry bowls).
model.setObjective(CurryBasePerGoatCurry * NumGoatCurry + CurryBasePerChickenCurry * NumChickenCurry, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumGoatCurry'] = NumGoatCurry.x
variables['NumChickenCurry'] = NumChickenCurry.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
