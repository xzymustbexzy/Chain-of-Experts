# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A fitness guru consumes NumFoodTypes different types of meals. Each bowl of the
i-th meal contains CaloriePerBowl[i] calories, ProteinPerBowl[i] grams of
protein, and SodiumPerBowl[i] mg of sodium. No more than MaxMealProportionEggs
proportion of the meals can be eggs. The fitness guru needs to consume at least
MinCalories total calories and at least MinProtein total grams of protein. The
objective is to determine the number of bowls of each meal type to minimize
total sodium intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/232/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
            
# Parameters 
# @Parameter NumFoodTypes @Def: Number of food types @Shape: [] 
NumFoodTypes = data['NumFoodTypes']
# @Parameter CaloriePerBowl @Def: Calorie content per bowl for each food type @Shape: ['NumFoodTypes'] 
CaloriePerBowl = data['CaloriePerBowl']
# @Parameter ProteinPerBowl @Def: Protein content per bowl for each food type @Shape: ['NumFoodTypes'] 
ProteinPerBowl = data['ProteinPerBowl']
# @Parameter SodiumPerBowl @Def: Sodium content per bowl for each food type @Shape: ['NumFoodTypes'] 
SodiumPerBowl = data['SodiumPerBowl']
# @Parameter MaxMealProportionEggs @Def: Maximum proportion of meals that can be eggs @Shape: [] 
MaxMealProportionEggs = data['MaxMealProportionEggs']
# @Parameter MinCalories @Def: Minimum total calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinProtein @Def: Minimum total protein required @Shape: [] 
MinProtein = data['MinProtein']

# Variables 
# @Variable NumMealsPerFoodType @Def: The number of meals for each food type @Shape: ['NumFoodTypes'] 
NumMealsPerFoodType = model.addVars(NumFoodTypes, vtype=GRB.INTEGER, name="NumMealsPerFoodType")

# Constraints 
# @Constraint Constr_1 @Def: No more than MaxMealProportionEggs proportion of the meals can be eggs.
model.addConstr(NumMealsPerFoodType[0] <= MaxMealProportionEggs * quicksum(NumMealsPerFoodType[i] for i in range(NumFoodTypes)))
# @Constraint Constr_2 @Def: The total caloric intake must be at least MinCalories.
model.addConstr(quicksum(NumMealsPerFoodType[i] * CaloriePerBowl[i] for i in range(NumFoodTypes)) >= MinCalories)
# @Constraint Constr_3 @Def: The total protein intake must be at least MinProtein.
model.addConstr(quicksum(ProteinPerBowl[i] * NumMealsPerFoodType[i] for i in range(NumFoodTypes)) >= MinProtein)

# Objective 
# @Objective Objective @Def: Minimize the total sodium intake.
model.setObjective(quicksum(SodiumPerBowl[i] * NumMealsPerFoodType[i] for i in range(NumFoodTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumMealsPerFoodType'] = {i: var.x for i, var in NumMealsPerFoodType.items()}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
