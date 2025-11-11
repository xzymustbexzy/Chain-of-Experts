# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Ayse produces a plant growth compound by mixing NumFertilizers different types
of fertilizer. The compound must contain at least RequiredNitrousOxide units of
nitrous oxide and at least RequiredVitaminMix units of vitamin mix. Each
fertilizer has a cost per kilogram given by CostFertilizer, contains
NitrousOxidePerFertilizer units of nitrous oxide per kilogram, and
VitaminMixPerFertilizer units of vitamin mix per kilogram. Determine the minimum
cost of Ayse's compound.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/24/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumFertilizers @Def: Number of different fertilizers used in the compound @Shape: [] 
NumFertilizers = data['NumFertilizers']
# @Parameter CostFertilizer @Def: Cost per kilogram of each fertilizer @Shape: ['NumFertilizers'] 
CostFertilizer = data['CostFertilizer']
# @Parameter NitrousOxidePerFertilizer @Def: Units of nitrous oxide per kilogram of each fertilizer @Shape: ['NumFertilizers'] 
NitrousOxidePerFertilizer = data['NitrousOxidePerFertilizer']
# @Parameter VitaminMixPerFertilizer @Def: Units of vitamin mix per kilogram of each fertilizer @Shape: ['NumFertilizers'] 
VitaminMixPerFertilizer = data['VitaminMixPerFertilizer']
# @Parameter RequiredNitrousOxide @Def: Minimum required units of nitrous oxide in the compound @Shape: [] 
RequiredNitrousOxide = data['RequiredNitrousOxide']
# @Parameter RequiredVitaminMix @Def: Minimum required units of vitamin mix in the compound @Shape: [] 
RequiredVitaminMix = data['RequiredVitaminMix']

# Variables 
# @Variable FertilizerQuantity @Def: The quantity of each fertilizer used in the compound @Shape: ['NumFertilizers'] 
FertilizerQuantity = model.addVars(NumFertilizers, vtype=GRB.CONTINUOUS, name="FertilizerQuantity")

# Constraints 
# @Constraint Constr_1 @Def: The compound must contain at least RequiredNitrousOxide units of nitrous oxide.
model.addConstr(quicksum(NitrousOxidePerFertilizer[i] * FertilizerQuantity[i] for i in range(NumFertilizers)) >= RequiredNitrousOxide)
# @Constraint Constr_2 @Def: The compound must contain at least RequiredVitaminMix units of vitamin mix.
model.addConstr(quicksum(VitaminMixPerFertilizer[i] * FertilizerQuantity[i] for i in range(NumFertilizers)) >= RequiredVitaminMix)
# @Constraint Constr_3 @Def: The amount of each fertilizer used must be non-negative.
model.addConstrs((FertilizerQuantity[k] >= 0 for k in range(NumFertilizers)), name="NonNegativeFertilizerQuantity")

# Objective 
# @Objective Objective @Def: The total cost of the compound is the sum of the cost per kilogram of each fertilizer multiplied by the amount used. The objective is to minimize the total cost of the compound.
model.setObjective(quicksum(CostFertilizer[i] * FertilizerQuantity[i] for i in range(NumFertilizers)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FertilizerQuantity'] = [FertilizerQuantity[i].X for i in range(NumFertilizers)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
