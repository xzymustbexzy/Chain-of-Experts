# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A show performs NumDemonstrations different demonstrations. Each demonstration i
uses MintUsed[i] units of mint and ActiveIngredientUsed[i] units of active
ingredient to produce FoamProduced[i] units of minty foam and
BlackTarProduced[i] units of black tar. The show has TotalMintAvailable units of
mint and TotalActiveIngredientAvailable units of active ingredient available. At
most MaxBlackTarAllowed units of black tar can be produced. Determine the number
of each demonstration to maximize the total minty foam produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/102/parameters.json", "r") as f:
    data = json.load(f)
        
# @Def: definition of a target
# @Shape: shape of a target
            
# Parameters 
# @Parameter NumDemonstrations @Def: Number of demonstrations @Shape: [] 
NumDemonstrations = data['NumDemonstrations']
# @Parameter MintUsed @Def: Amount of mint used by each demonstration @Shape: ['NumDemonstrations'] 
MintUsed = data['MintUsed']
# @Parameter ActiveIngredientUsed @Def: Amount of active ingredient used by each demonstration @Shape: ['NumDemonstrations'] 
ActiveIngredientUsed = data['ActiveIngredientUsed']
# @Parameter FoamProduced @Def: Amount of minty foam produced by each demonstration @Shape: ['NumDemonstrations'] 
FoamProduced = data['FoamProduced']
# @Parameter BlackTarProduced @Def: Amount of black tar produced by each demonstration @Shape: ['NumDemonstrations'] 
BlackTarProduced = data['BlackTarProduced']
# @Parameter TotalMintAvailable @Def: Total units of mint available @Shape: [] 
TotalMintAvailable = data['TotalMintAvailable']
# @Parameter TotalActiveIngredientAvailable @Def: Total units of active ingredient available @Shape: [] 
TotalActiveIngredientAvailable = data['TotalActiveIngredientAvailable']
# @Parameter MaxBlackTarAllowed @Def: Maximum units of black tar allowed @Shape: [] 
MaxBlackTarAllowed = data['MaxBlackTarAllowed']

# Variables 
# @Variable DemonstrationUsed @Def: Number of times each demonstration is used @Shape: ['NumDemonstrations'] 
DemonstrationUsed = model.addVars(NumDemonstrations, vtype=GRB.CONTINUOUS, name="DemonstrationUsed")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of mint used by all demonstrations cannot exceed the total mint available.
model.addConstr(quicksum(MintUsed[i] * DemonstrationUsed[i] for i in range(NumDemonstrations)) <= TotalMintAvailable)
# @Constraint Constr_2 @Def: The total amount of active ingredient used by all demonstrations cannot exceed the total active ingredient available.
model.addConstr(quicksum(ActiveIngredientUsed[i] * DemonstrationUsed[i] for i in range(NumDemonstrations)) <= TotalActiveIngredientAvailable)
# @Constraint Constr_3 @Def: The total amount of black tar produced cannot exceed the maximum black tar allowed.
model.addConstr(quicksum(BlackTarProduced[j] * DemonstrationUsed[j] for j in range(NumDemonstrations)) <= MaxBlackTarAllowed)

# Objective 
# @Objective Objective @Def: Maximize the total minty foam produced by all demonstrations.
model.setObjective(quicksum(FoamProduced[d] * DemonstrationUsed[d] for d in range(NumDemonstrations)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['DemonstrationUsed'] = [DemonstrationUsed[i].x for i in range(NumDemonstrations)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
