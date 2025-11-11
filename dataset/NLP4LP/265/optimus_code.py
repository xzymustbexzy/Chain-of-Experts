# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Maximize the total caloric intake by selecting the number of cups of spinach and
soybeans. This involves maximizing CaloriesSpinach multiplied by the number of
cups of spinach plus CaloriesSoybeans multiplied by the number of cups of
soybeans. The selection must satisfy the following constraints: FiberSpinach
multiplied by the number of cups of spinach plus FiberSoybeans multiplied by the
number of cups of soybeans is at least MinFiber, IronSpinach multiplied by the
number of cups of spinach plus IronSoybeans multiplied by the number of cups of
soybeans is at least MinIron, and the number of cups of spinach exceeds the
number of cups of soybeans.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/266/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FiberSpinach @Def: Number of units of fiber in one cup of spinach @Shape: [] 
FiberSpinach = data['FiberSpinach']
# @Parameter IronSpinach @Def: Amount of iron (mg) in one cup of spinach @Shape: [] 
IronSpinach = data['IronSpinach']
# @Parameter CaloriesSpinach @Def: Number of calories in one cup of spinach @Shape: [] 
CaloriesSpinach = data['CaloriesSpinach']
# @Parameter FiberSoybeans @Def: Number of units of fiber in one cup of soybeans @Shape: [] 
FiberSoybeans = data['FiberSoybeans']
# @Parameter IronSoybeans @Def: Amount of iron (mg) in one cup of soybeans @Shape: [] 
IronSoybeans = data['IronSoybeans']
# @Parameter CaloriesSoybeans @Def: Number of calories in one cup of soybeans @Shape: [] 
CaloriesSoybeans = data['CaloriesSoybeans']
# @Parameter MinFiber @Def: Minimum total units of fiber required @Shape: [] 
MinFiber = data['MinFiber']
# @Parameter MinIron @Def: Minimum total amount of iron required (mg) @Shape: [] 
MinIron = data['MinIron']

# Variables 
# @Variable CupsSpinach @Def: The number of cups of spinach @Shape: [] 
CupsSpinach = model.addVar(vtype=GRB.CONTINUOUS, name="CupsSpinach")
# @Variable CupsSoybeans @Def: The number of cups of soybeans @Shape: [] 
CupsSoybeans = model.addVar(vtype=GRB.CONTINUOUS, name="CupsSoybeans")

# Constraints 
# @Constraint Constr_1 @Def: FiberSpinach multiplied by the number of cups of spinach plus FiberSoybeans multiplied by the number of cups of soybeans is at least MinFiber.
model.addConstr(FiberSpinach * CupsSpinach + FiberSoybeans * CupsSoybeans >= MinFiber)
# @Constraint Constr_2 @Def: IronSpinach multiplied by the number of cups of spinach plus IronSoybeans multiplied by the number of cups of soybeans is at least MinIron.
model.addConstr(IronSpinach * CupsSpinach + IronSoybeans * CupsSoybeans >= MinIron)
# @Constraint Constr_3 @Def: The number of cups of spinach exceeds the number of cups of soybeans.
model.addConstr(CupsSpinach >= CupsSoybeans)

# Objective 
# @Objective Objective @Def: Total caloric intake is CaloriesSpinach multiplied by the number of cups of spinach plus CaloriesSoybeans multiplied by the number of cups of soybeans. The objective is to maximize the total caloric intake.
model.setObjective(CaloriesSpinach * CupsSpinach + CaloriesSoybeans * CupsSoybeans, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['CupsSpinach'] = CupsSpinach.x
variables['CupsSoybeans'] = CupsSoybeans.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
