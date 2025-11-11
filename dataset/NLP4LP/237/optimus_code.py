# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A navy ship is preparing salads and fruit bowls for their staff. Each salad
provides VitaminsPerSalad units of vitamins, FiberPerSalad units of fiber, and
PotassiumPerSalad units of potassium. Each fruit bowl provides
VitaminsPerFruitBowl units of vitamins, FiberPerFruitBowl units of fiber, and
PotassiumPerFruitBowl units of potassium. The nutritionist must ensure that each
staff member receives at least MinVitamins units of vitamins and at least
MinFiber units of fiber. Additionally, at most MaxFruitBowlFraction fraction of
the meals can be fruit bowls. The objective is to determine the number of salads
and fruit bowls to maximize potassium intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/238/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinVitamins @Def: Minimum required units of vitamins per staff @Shape: [] 
MinVitamins = data['MinVitamins']
# @Parameter MinFiber @Def: Minimum required units of fiber per staff @Shape: [] 
MinFiber = data['MinFiber']
# @Parameter VitaminsPerSalad @Def: Units of vitamins per salad @Shape: [] 
VitaminsPerSalad = data['VitaminsPerSalad']
# @Parameter VitaminsPerFruitBowl @Def: Units of vitamins per fruit bowl @Shape: [] 
VitaminsPerFruitBowl = data['VitaminsPerFruitBowl']
# @Parameter FiberPerSalad @Def: Units of fiber per salad @Shape: [] 
FiberPerSalad = data['FiberPerSalad']
# @Parameter FiberPerFruitBowl @Def: Units of fiber per fruit bowl @Shape: [] 
FiberPerFruitBowl = data['FiberPerFruitBowl']
# @Parameter PotassiumPerSalad @Def: Units of potassium per salad @Shape: [] 
PotassiumPerSalad = data['PotassiumPerSalad']
# @Parameter PotassiumPerFruitBowl @Def: Units of potassium per fruit bowl @Shape: [] 
PotassiumPerFruitBowl = data['PotassiumPerFruitBowl']
# @Parameter MaxFruitBowlFraction @Def: Maximum fraction of meals that can be fruit bowls @Shape: [] 
MaxFruitBowlFraction = data['MaxFruitBowlFraction']

# Variables 
# @Variable QuantitySalads @Def: The quantity of salads @Shape: [] 
QuantitySalads = model.addVar(vtype=GRB.CONTINUOUS, name="QuantitySalads")
# @Variable QuantityFruitBowls @Def: The quantity of fruit bowls @Shape: [] 
QuantityFruitBowls = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityFruitBowls")

# Constraints 
# @Constraint Constr_1 @Def: The total vitamins provided by the salads and fruit bowls must be at least MinVitamins units.
model.addConstr(VitaminsPerSalad * QuantitySalads + VitaminsPerFruitBowl * QuantityFruitBowls >= MinVitamins)
# @Constraint Constr_2 @Def: The total fiber provided by the salads and fruit bowls must be at least MinFiber units.
model.addConstr(FiberPerSalad * QuantitySalads + FiberPerFruitBowl * QuantityFruitBowls >= MinFiber)
# @Constraint Constr_3 @Def: At most MaxFruitBowlFraction fraction of the meals can be fruit bowls.
model.addConstr(QuantityFruitBowls <= MaxFruitBowlFraction * (QuantitySalads + QuantityFruitBowls))

# Objective 
# @Objective Objective @Def: Maximize the total potassium intake, calculated as PotassiumPerSalad multiplied by the number of salads plus PotassiumPerFruitBowl multiplied by the number of fruit bowls.
model.setObjective(PotassiumPerSalad * QuantitySalads + PotassiumPerFruitBowl * QuantityFruitBowls, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantitySalads'] = QuantitySalads.x
variables['QuantityFruitBowls'] = QuantityFruitBowls.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
