# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A pharmaceutical company produces regular and premium batches. Each regular
batch requires MedicinalIngredientPerRegularBatch units of medicinal ingredients
and RehydrationProductPerRegularBatch units of rehydration product. Each premium
batch requires MedicinalIngredientPerPremiumBatch units of medicinal ingredients
and RehydrationProductPerPremiumBatch units of rehydration product. The company
has TotalMedicinalIngredients units of medicinal ingredients and
TotalRehydrationProduct units of rehydration product available. The number of
regular batches produced must be at least MinRegularBatches and less than the
number of premium batches. Each regular batch can treat
PeopleTreatedPerRegularBatch people and each premium batch can treat
PeopleTreatedPerPremiumBatch people. The objective is to determine the number of
regular and premium batches to produce in order to maximize the total number of
people treated.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/98/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MedicinalIngredientPerRegularBatch @Def: Units of medicinal ingredients required to produce one regular batch @Shape: [] 
MedicinalIngredientPerRegularBatch = data['MedicinalIngredientPerRegularBatch']
# @Parameter RehydrationProductPerRegularBatch @Def: Units of rehydration product required to produce one regular batch @Shape: [] 
RehydrationProductPerRegularBatch = data['RehydrationProductPerRegularBatch']
# @Parameter MedicinalIngredientPerPremiumBatch @Def: Units of medicinal ingredients required to produce one premium batch @Shape: [] 
MedicinalIngredientPerPremiumBatch = data['MedicinalIngredientPerPremiumBatch']
# @Parameter RehydrationProductPerPremiumBatch @Def: Units of rehydration product required to produce one premium batch @Shape: [] 
RehydrationProductPerPremiumBatch = data['RehydrationProductPerPremiumBatch']
# @Parameter TotalMedicinalIngredients @Def: Total available units of medicinal ingredients @Shape: [] 
TotalMedicinalIngredients = data['TotalMedicinalIngredients']
# @Parameter TotalRehydrationProduct @Def: Total available units of rehydration product @Shape: [] 
TotalRehydrationProduct = data['TotalRehydrationProduct']
# @Parameter MinRegularBatches @Def: Minimum number of regular batches to produce @Shape: [] 
MinRegularBatches = data['MinRegularBatches']
# @Parameter PeopleTreatedPerRegularBatch @Def: Number of people treated by one regular batch @Shape: [] 
PeopleTreatedPerRegularBatch = data['PeopleTreatedPerRegularBatch']
# @Parameter PeopleTreatedPerPremiumBatch @Def: Number of people treated by one premium batch @Shape: [] 
PeopleTreatedPerPremiumBatch = data['PeopleTreatedPerPremiumBatch']

# Variables 
# @Variable RegularBatches @Def: The number of regular batches produced @Shape: [] 
RegularBatches = model.addVar(vtype=GRB.INTEGER, name="RegularBatches")
# @Variable PremiumBatches @Def: The number of premium batches produced @Shape: [] 
PremiumBatches = model.addVar(vtype=GRB.INTEGER, name="PremiumBatches")

# Constraints 
# @Constraint Constr_1 @Def: The total units of medicinal ingredients used by regular and premium batches cannot exceed TotalMedicinalIngredients.
model.addConstr(RegularBatches * MedicinalIngredientPerRegularBatch + PremiumBatches * MedicinalIngredientPerPremiumBatch <= TotalMedicinalIngredients)
# @Constraint Constr_2 @Def: The total units of rehydration product used by regular and premium batches cannot exceed TotalRehydrationProduct.
model.addConstr(RehydrationProductPerRegularBatch * RegularBatches + RehydrationProductPerPremiumBatch * PremiumBatches <= TotalRehydrationProduct)
# @Constraint Constr_3 @Def: The number of regular batches produced must be at least MinRegularBatches.
model.addConstr(RegularBatches >= MinRegularBatches)
# @Constraint Constr_4 @Def: The number of regular batches produced must be less than the number of premium batches.
model.addConstr(RegularBatches <= PremiumBatches - 1)

# Objective 
# @Objective Objective @Def: The total number of people treated is the sum of (PeopleTreatedPerRegularBatch multiplied by the number of regular batches) and (PeopleTreatedPerPremiumBatch multiplied by the number of premium batches). The objective is to maximize the total number of people treated.
model.setObjective(PeopleTreatedPerRegularBatch * RegularBatches + PeopleTreatedPerPremiumBatch * PremiumBatches, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RegularBatches'] = RegularBatches.x
variables['PremiumBatches'] = PremiumBatches.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
