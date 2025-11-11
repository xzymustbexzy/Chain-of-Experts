# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company delivers packages using camels and horses. Each camel can carry
CamelCapacity packages and requires CamelFood units of food each, while each
horse can carry HorseCapacity packages and requires HorseFood units of food
each. The company needs to deliver at least MinPackages packages and has
FoodAvailable units of food available. The number of horses cannot exceed the
number of camels. Determine the number of camels and horses to minimize the
total number of animals used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/159/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CamelCapacity @Def: Number of packages a camel can carry @Shape: [] 
CamelCapacity = data['CamelCapacity']
# @Parameter HorseCapacity @Def: Number of packages a horse can carry @Shape: [] 
HorseCapacity = data['HorseCapacity']
# @Parameter CamelFood @Def: Units of food a camel requires @Shape: [] 
CamelFood = data['CamelFood']
# @Parameter HorseFood @Def: Units of food a horse requires @Shape: [] 
HorseFood = data['HorseFood']
# @Parameter MinPackages @Def: Minimum number of packages to be delivered @Shape: [] 
MinPackages = data['MinPackages']
# @Parameter FoodAvailable @Def: Total units of food available @Shape: [] 
FoodAvailable = data['FoodAvailable']

# Variables 
# @Variable NumberOfCamels @Def: The number of camels used to deliver packages @Shape: ['Integer'] 
NumberOfCamels = model.addVar(vtype=GRB.INTEGER, name="NumberOfCamels")
# @Variable NumberOfHorses @Def: The number of horses used to deliver packages @Shape: ['Integer'] 
NumberOfHorses = model.addVar(vtype=GRB.INTEGER, name="NumberOfHorses")

# Constraints 
# @Constraint Constr_1 @Def: The total number of packages delivered by camels and horses must be at least MinPackages.
model.addConstr(NumberOfCamels * CamelCapacity + NumberOfHorses * HorseCapacity >= MinPackages)
# @Constraint Constr_2 @Def: The total food consumed by camels and horses must not exceed FoodAvailable units.
model.addConstr(CamelFood * NumberOfCamels + HorseFood * NumberOfHorses <= FoodAvailable)
# @Constraint Constr_3 @Def: The number of horses cannot exceed the number of camels.
model.addConstr(NumberOfHorses <= NumberOfCamels)

# Objective 
# @Objective Objective @Def: Minimize the total number of camels and horses used.
model.setObjective(NumberOfCamels + NumberOfHorses, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCamels'] = NumberOfCamels.x
variables['NumberOfHorses'] = NumberOfHorses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
