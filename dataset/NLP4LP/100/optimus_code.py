# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the quantities of crab cakes and lobster rolls that minimize the total
unsaturated fat, where total unsaturated fat is calculated as
UnsaturatedFatPerCrabCake multiplied by the number of crab cakes plus
UnsaturatedFatPerLobsterRoll multiplied by the number of lobster rolls. Ensure
that the total vitamin A intake is at least MinimumVitaminA, the total vitamin C
intake is at least MinimumVitaminC, and the proportion of lobster rolls does not
exceed MaximumLobsterFraction of the total meals.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/101/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinimumVitaminA @Def: Minimum required units of vitamin A @Shape: [] 
MinimumVitaminA = data['MinimumVitaminA']
# @Parameter MinimumVitaminC @Def: Minimum required units of vitamin C @Shape: [] 
MinimumVitaminC = data['MinimumVitaminC']
# @Parameter VitaminAPerCrabCake @Def: Units of vitamin A per crab cake @Shape: [] 
VitaminAPerCrabCake = data['VitaminAPerCrabCake']
# @Parameter VitaminCPerCrabCake @Def: Units of vitamin C per crab cake @Shape: [] 
VitaminCPerCrabCake = data['VitaminCPerCrabCake']
# @Parameter VitaminAPerLobsterRoll @Def: Units of vitamin A per lobster roll @Shape: [] 
VitaminAPerLobsterRoll = data['VitaminAPerLobsterRoll']
# @Parameter VitaminCPerLobsterRoll @Def: Units of vitamin C per lobster roll @Shape: [] 
VitaminCPerLobsterRoll = data['VitaminCPerLobsterRoll']
# @Parameter UnsaturatedFatPerCrabCake @Def: Units of unsaturated fat per crab cake @Shape: [] 
UnsaturatedFatPerCrabCake = data['UnsaturatedFatPerCrabCake']
# @Parameter UnsaturatedFatPerLobsterRoll @Def: Units of unsaturated fat per lobster roll @Shape: [] 
UnsaturatedFatPerLobsterRoll = data['UnsaturatedFatPerLobsterRoll']
# @Parameter MaximumLobsterFraction @Def: Maximum fraction of meals that can be lobster rolls @Shape: [] 
MaximumLobsterFraction = data['MaximumLobsterFraction']

# Variables 
# @Variable QuantityCrabCake @Def: The number of crab cakes @Shape: [] 
QuantityCrabCake = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityCrabCake")
# @Variable QuantityLobsterRoll @Def: The number of lobster rolls @Shape: [] 
QuantityLobsterRoll = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityLobsterRoll")

# Constraints 
# @Constraint Constr_1 @Def: The total vitamin A intake from crab cakes and lobster rolls must be at least MinimumVitaminA.
model.addConstr(VitaminAPerCrabCake * QuantityCrabCake + VitaminAPerLobsterRoll * QuantityLobsterRoll >= MinimumVitaminA)
# @Constraint Constr_2 @Def: The total vitamin C intake from crab cakes and lobster rolls must be at least MinimumVitaminC.
model.addConstr(VitaminCPerCrabCake * QuantityCrabCake + VitaminCPerLobsterRoll * QuantityLobsterRoll >= MinimumVitaminC)
# @Constraint Constr_3 @Def: The proportion of lobster rolls in the total meals must not exceed MaximumLobsterFraction.
model.addConstr(QuantityLobsterRoll <= MaximumLobsterFraction * (QuantityCrabCake + QuantityLobsterRoll))

# Objective 
# @Objective Objective @Def: Total unsaturated fat is calculated as UnsaturatedFatPerCrabCake multiplied by the number of crab cakes plus UnsaturatedFatPerLobsterRoll multiplied by the number of lobster rolls. The objective is to minimize the total unsaturated fat.
model.setObjective(UnsaturatedFatPerCrabCake * QuantityCrabCake + UnsaturatedFatPerLobsterRoll * QuantityLobsterRoll, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityCrabCake'] = QuantityCrabCake.x
variables['QuantityLobsterRoll'] = QuantityLobsterRoll.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
