# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A dentist must determine the number of molars and canines to fill, ensuring that
ResinPerMolar multiplied by the number of molars plus ResinPerCanine multiplied
by the number of canines does not exceed TotalResin. Additionally, the number of
canines must be at least MinPercentageCanines times the total number of cavities
filled, and the number of molars must be at least MinNumMolars. The objective is
to minimize the total pain killer used, which is PainKillerPerMolar multiplied
by the number of molars plus PainKillerPerCanine multiplied by the number of
canines.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/225/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalResin @Def: Total amount of resin available for filling cavities @Shape: [] 
TotalResin = data['TotalResin']
# @Parameter ResinPerMolar @Def: Units of resin required to fill one molar @Shape: [] 
ResinPerMolar = data['ResinPerMolar']
# @Parameter ResinPerCanine @Def: Units of resin required to fill one canine @Shape: [] 
ResinPerCanine = data['ResinPerCanine']
# @Parameter PainKillerPerMolar @Def: Units of pain killer required to fill one molar @Shape: [] 
PainKillerPerMolar = data['PainKillerPerMolar']
# @Parameter PainKillerPerCanine @Def: Units of pain killer required to fill one canine @Shape: [] 
PainKillerPerCanine = data['PainKillerPerCanine']
# @Parameter MinPercentageCanines @Def: Minimum fraction of cavities filled that must be canines @Shape: [] 
MinPercentageCanines = data['MinPercentageCanines']
# @Parameter MinNumMolars @Def: Minimum number of molars that must be filled @Shape: [] 
MinNumMolars = data['MinNumMolars']

# Variables 
# @Variable NumberMolars @Def: The number of molars to be filled @Shape: [] 
NumberMolars = model.addVar(vtype=GRB.INTEGER, name="NumberMolars")
# @Variable NumberCanines @Def: The number of canines to be filled @Shape: [] 
NumberCanines = model.addVar(vtype=GRB.INTEGER, name="NumberCanines")

# Constraints 
# @Constraint Constr_1 @Def: The total resin used for filling molars and canines must not exceed the total available resin. This is represented by ResinPerMolar multiplied by the number of molars plus ResinPerCanine multiplied by the number of canines being less than or equal to TotalResin.
model.addConstr(ResinPerMolar * NumberMolars + ResinPerCanine * NumberCanines <= TotalResin)
# @Constraint Constr_2 @Def: The number of canines filled must be at least MinPercentageCanines times the total number of cavities filled. This means that the number of canines is at least MinPercentageCanines multiplied by the sum of the number of molars and canines.
model.addConstr(NumberCanines >= MinPercentageCanines * (NumberCanines + NumberMolars))
# @Constraint Constr_3 @Def: The number of molars filled must be at least MinNumMolars.
model.addConstr(NumberMolars >= MinNumMolars)

# Objective 
# @Objective Objective @Def: Minimize the total pain killer used, which is PainKillerPerMolar multiplied by the number of molars plus PainKillerPerCanine multiplied by the number of canines.
model.setObjective(PainKillerPerMolar * NumberMolars + PainKillerPerCanine * NumberCanines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberMolars'] = NumberMolars.x
variables['NumberCanines'] = NumberCanines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
