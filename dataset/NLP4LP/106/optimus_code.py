# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Let B represent the number of burgers and P represent the number of pizza
slices. The objective is to minimize CholesterolPerBurger multiplied by B plus
CholesterolPerPizzaSlice multiplied by P. This is subject to the constraints
that FatPerBurger multiplied by B plus FatPerPizzaSlice multiplied by P is at
least MinFat, CaloriesPerBurger multiplied by B plus CaloriesPerPizzaSlice
multiplied by P is at least MinCalories, and P is at least MinPizzaToBurgerRatio
multiplied by B.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/107/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FatPerBurger @Def: Units of fat per burger @Shape: [] 
FatPerBurger = data['FatPerBurger']
# @Parameter FatPerPizzaSlice @Def: Units of fat per slice of pizza @Shape: [] 
FatPerPizzaSlice = data['FatPerPizzaSlice']
# @Parameter CaloriesPerBurger @Def: Calories per burger @Shape: [] 
CaloriesPerBurger = data['CaloriesPerBurger']
# @Parameter CaloriesPerPizzaSlice @Def: Calories per slice of pizza @Shape: [] 
CaloriesPerPizzaSlice = data['CaloriesPerPizzaSlice']
# @Parameter CholesterolPerBurger @Def: Units of cholesterol per burger @Shape: [] 
CholesterolPerBurger = data['CholesterolPerBurger']
# @Parameter CholesterolPerPizzaSlice @Def: Units of cholesterol per slice of pizza @Shape: [] 
CholesterolPerPizzaSlice = data['CholesterolPerPizzaSlice']
# @Parameter MinFat @Def: Minimum total units of fat required @Shape: [] 
MinFat = data['MinFat']
# @Parameter MinCalories @Def: Minimum total calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinPizzaToBurgerRatio @Def: Minimum ratio of slices of pizza to burgers @Shape: [] 
MinPizzaToBurgerRatio = data['MinPizzaToBurgerRatio']

# Variables 
# @Variable Burgers @Def: The number of burgers @Shape: [] 
Burgers = model.addVar(vtype=GRB.INTEGER, name="Burgers")
# @Variable PizzaSlices @Def: The number of slices of pizza @Shape: [] 
PizzaSlices = model.addVar(vtype=GRB.CONTINUOUS, name="PizzaSlices")

# Constraints 
# @Constraint Constr_1 @Def: FatPerBurger multiplied by B plus FatPerPizzaSlice multiplied by P is at least MinFat
model.addConstr(FatPerBurger * Burgers + FatPerPizzaSlice * PizzaSlices >= MinFat)
# @Constraint Constr_2 @Def: CaloriesPerBurger multiplied by B plus CaloriesPerPizzaSlice multiplied by P is at least MinCalories
model.addConstr(CaloriesPerBurger * Burgers + CaloriesPerPizzaSlice * PizzaSlices >= MinCalories)
# @Constraint Constr_3 @Def: P is at least MinPizzaToBurgerRatio multiplied by B
model.addConstr(PizzaSlices >= MinPizzaToBurgerRatio * Burgers)

# Objective 
# @Objective Objective @Def: Minimize CholesterolPerBurger multiplied by B plus CholesterolPerPizzaSlice multiplied by P
model.setObjective(CholesterolPerBurger * Burgers + CholesterolPerPizzaSlice * PizzaSlices, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Burgers'] = Burgers.x
variables['PizzaSlices'] = PizzaSlices.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
