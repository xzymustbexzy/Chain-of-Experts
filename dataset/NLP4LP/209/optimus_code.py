# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the quantities of FullWeighted and SemiWeighted keyboards to
manufacture in order to maximize total revenue, where total revenue is
calculated as PriceFullWeighted multiplied by the quantity of FullWeighted
keyboards plus PriceSemiWeighted multiplied by the quantity of SemiWeighted
keyboards. The production must satisfy two constraints: the total oscillator
chips used, calculated as ChipsPerFullWeighted multiplied by the quantity of
FullWeighted keyboards plus ChipsPerSemiWeighted multiplied by the quantity of
SemiWeighted keyboards, must not exceed TotalChipsAvailable, and the total
production time, calculated as ProductionTimePerKeyboard multiplied by the sum
of the quantities of FullWeighted and SemiWeighted keyboards, must not exceed
TotalProductionHours.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/210/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PriceFullWeighted @Def: Price of the full-weighted keyboard @Shape: [] 
PriceFullWeighted = data['PriceFullWeighted']
# @Parameter PriceSemiWeighted @Def: Price of the semi-weighted keyboard @Shape: [] 
PriceSemiWeighted = data['PriceSemiWeighted']
# @Parameter TotalChipsAvailable @Def: Total oscillator chips available per day @Shape: [] 
TotalChipsAvailable = data['TotalChipsAvailable']
# @Parameter ChipsPerFullWeighted @Def: Number of oscillator chips required per full-weighted keyboard @Shape: [] 
ChipsPerFullWeighted = data['ChipsPerFullWeighted']
# @Parameter ChipsPerSemiWeighted @Def: Number of oscillator chips required per semi-weighted keyboard @Shape: [] 
ChipsPerSemiWeighted = data['ChipsPerSemiWeighted']
# @Parameter TotalProductionHours @Def: Total production hours available per day @Shape: [] 
TotalProductionHours = data['TotalProductionHours']
# @Parameter ProductionTimePerKeyboard @Def: Production time required to manufacture one keyboard @Shape: [] 
ProductionTimePerKeyboard = data['ProductionTimePerKeyboard']

# Variables 
# @Variable QuantityFullWeighted @Def: The quantity of FullWeighted keyboards @Shape: [] 
QuantityFullWeighted = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityFullWeighted")
# @Variable QuantitySemiWeighted @Def: The quantity of SemiWeighted keyboards @Shape: [] 
QuantitySemiWeighted = model.addVar(vtype=GRB.CONTINUOUS, name="QuantitySemiWeighted")

# Constraints 
# @Constraint Constr_1 @Def: The total oscillator chips used, calculated as ChipsPerFullWeighted multiplied by the quantity of FullWeighted keyboards plus ChipsPerSemiWeighted multiplied by the quantity of SemiWeighted keyboards, must not exceed TotalChipsAvailable.
model.addConstr(ChipsPerFullWeighted * QuantityFullWeighted + ChipsPerSemiWeighted * QuantitySemiWeighted <= TotalChipsAvailable)
# @Constraint Constr_2 @Def: The total production time, calculated as ProductionTimePerKeyboard multiplied by the sum of the quantities of FullWeighted and SemiWeighted keyboards, must not exceed TotalProductionHours.
model.addConstr(ProductionTimePerKeyboard * (QuantityFullWeighted + QuantitySemiWeighted) <= TotalProductionHours)

# Objective 
# @Objective Objective @Def: Total revenue is calculated as PriceFullWeighted multiplied by the quantity of FullWeighted keyboards plus PriceSemiWeighted multiplied by the quantity of SemiWeighted keyboards. The objective is to maximize total revenue.
model.setObjective(PriceFullWeighted * QuantityFullWeighted + PriceSemiWeighted * QuantitySemiWeighted, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityFullWeighted'] = QuantityFullWeighted.x
variables['QuantitySemiWeighted'] = QuantitySemiWeighted.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
