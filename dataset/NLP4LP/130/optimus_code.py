# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bodybuilder purchases two types of meals: MealA and MealB. Each MealA contains
ProteinTurkey amount of protein, CarbsTurkey amount of carbohydrates, and
FatTurkey amount of fat. Each MealB contains ProteinTuna amount of protein,
CarbsTuna amount of carbohydrates, and FatTuna amount of fat. The bodybuilder
aims to obtain at least MinProtein total protein and at least MinCarbs total
carbohydrates. Additionally, no more than MaxTurkeyFraction fraction of the
total meals can be MealA. The objective is to minimize the total fat intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/131/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProteinTurkey @Def: Amount of protein in one turkey dinner @Shape: [] 
ProteinTurkey = data['ProteinTurkey']
# @Parameter CarbsTurkey @Def: Amount of carbohydrates in one turkey dinner @Shape: [] 
CarbsTurkey = data['CarbsTurkey']
# @Parameter FatTurkey @Def: Amount of fat in one turkey dinner @Shape: [] 
FatTurkey = data['FatTurkey']
# @Parameter ProteinTuna @Def: Amount of protein in one tuna salad sandwich @Shape: [] 
ProteinTuna = data['ProteinTuna']
# @Parameter CarbsTuna @Def: Amount of carbohydrates in one tuna salad sandwich @Shape: [] 
CarbsTuna = data['CarbsTuna']
# @Parameter FatTuna @Def: Amount of fat in one tuna salad sandwich @Shape: [] 
FatTuna = data['FatTuna']
# @Parameter MinProtein @Def: Minimum required total protein @Shape: [] 
MinProtein = data['MinProtein']
# @Parameter MinCarbs @Def: Minimum required total carbohydrates @Shape: [] 
MinCarbs = data['MinCarbs']
# @Parameter MaxTurkeyFraction @Def: Maximum fraction of meals that can be turkey dinners @Shape: [] 
MaxTurkeyFraction = data['MaxTurkeyFraction']

# Variables 
# @Variable QuantityTurkey @Def: The number of turkey dinners @Shape: [] 
QuantityTurkey = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityTurkey")
# @Variable QuantityTuna @Def: The number of tuna salad sandwiches @Shape: [] 
QuantityTuna = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityTuna")

# Constraints 
# @Constraint Constr_1 @Def: The total protein from MealA and MealB must be at least MinProtein.
model.addConstr(ProteinTurkey * QuantityTurkey + ProteinTuna * QuantityTuna >= MinProtein)
# @Constraint Constr_2 @Def: The total carbohydrates from MealA and MealB must be at least MinCarbs.
model.addConstr(CarbsTurkey * QuantityTurkey + CarbsTuna * QuantityTuna >= MinCarbs)
# @Constraint Constr_3 @Def: No more than MaxTurkeyFraction fraction of the total meals can be MealA.
model.addConstr(QuantityTurkey <= MaxTurkeyFraction * (QuantityTurkey + QuantityTuna))

# Objective 
# @Objective Objective @Def: Minimize the total fat intake.
model.setObjective(FatTurkey * QuantityTurkey + FatTuna * QuantityTuna, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityTurkey'] = QuantityTurkey.x
variables['QuantityTuna'] = QuantityTuna.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
