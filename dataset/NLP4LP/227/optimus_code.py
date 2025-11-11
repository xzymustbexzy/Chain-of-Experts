# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A neighbourhood pizza restaurant produces large and medium pizzas. Each large
pizza requires DoughLarge units of dough and ToppingsLarge units of toppings and
takes BakingTimeLarge minutes to bake. Each medium pizza requires DoughMedium
units of dough and ToppingsMedium units of toppings and takes BakingTimeMedium
minutes to bake. The restaurant must use at least MinDough units of dough and
MinToppings units of toppings. At least MinMediumPizzas medium pizzas must be
made, and the number of large pizzas must be at least MinRatioLargeToMedium
times the number of medium pizzas. The objective is to minimize the total baking
time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/228/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter DoughLarge @Def: Units of dough required per large pizza @Shape: [] 
DoughLarge = data['DoughLarge']
# @Parameter DoughMedium @Def: Units of dough required per medium pizza @Shape: [] 
DoughMedium = data['DoughMedium']
# @Parameter ToppingsLarge @Def: Units of toppings required per large pizza @Shape: [] 
ToppingsLarge = data['ToppingsLarge']
# @Parameter ToppingsMedium @Def: Units of toppings required per medium pizza @Shape: [] 
ToppingsMedium = data['ToppingsMedium']
# @Parameter BakingTimeLarge @Def: Baking time per large pizza in minutes @Shape: [] 
BakingTimeLarge = data['BakingTimeLarge']
# @Parameter BakingTimeMedium @Def: Baking time per medium pizza in minutes @Shape: [] 
BakingTimeMedium = data['BakingTimeMedium']
# @Parameter MinDough @Def: Minimum units of dough required @Shape: [] 
MinDough = data['MinDough']
# @Parameter MinToppings @Def: Minimum units of toppings required @Shape: [] 
MinToppings = data['MinToppings']
# @Parameter MinMediumPizzas @Def: Minimum number of medium pizzas to be made @Shape: [] 
MinMediumPizzas = data['MinMediumPizzas']
# @Parameter MinRatioLargeToMedium @Def: Minimum ratio of large pizzas to medium pizzas @Shape: [] 
MinRatioLargeToMedium = data['MinRatioLargeToMedium']

# Variables 
# @Variable NumberLargePizzas @Def: The number of large pizzas to be made @Shape: ['Integer', 'NonNegative'] 
NumberLargePizzas = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberLargePizzas")
# @Variable NumberMediumPizzas @Def: The number of medium pizzas to be made @Shape: ['Integer', 'NonNegative'] 
NumberMediumPizzas = model.addVar(vtype=GRB.INTEGER, name="NumberMediumPizzas")

# Constraints 
# @Constraint Constr_1 @Def: Each large pizza requires DoughLarge units of dough and each medium pizza requires DoughMedium units of dough. The total dough used must be at least MinDough units.
model.addConstr(DoughLarge * NumberLargePizzas + DoughMedium * NumberMediumPizzas >= MinDough)
# @Constraint Constr_2 @Def: Each large pizza requires ToppingsLarge units of toppings and each medium pizza requires ToppingsMedium units of toppings. The total toppings used must be at least MinToppings units.
model.addConstr(ToppingsLarge * NumberLargePizzas + ToppingsMedium * NumberMediumPizzas >= MinToppings)
# @Constraint Constr_3 @Def: At least MinMediumPizzas medium pizzas must be made.
model.addConstr(NumberMediumPizzas >= MinMediumPizzas)
# @Constraint Constr_4 @Def: The number of large pizzas must be at least MinRatioLargeToMedium times the number of medium pizzas.
model.addConstr(NumberLargePizzas >= MinRatioLargeToMedium * NumberMediumPizzas)

# Objective 
# @Objective Objective @Def: Minimize the total baking time, which is the sum of the baking times for all large and medium pizzas.
model.setObjective(NumberLargePizzas * BakingTimeLarge + NumberMediumPizzas * BakingTimeMedium, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberLargePizzas'] = NumberLargePizzas.x
variables['NumberMediumPizzas'] = NumberMediumPizzas.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
