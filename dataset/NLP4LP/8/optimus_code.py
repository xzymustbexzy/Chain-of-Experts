# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
An artisan produces NumJarTypes different types of terracotta jars. Each jar
type requires ShapingTimePerType shaping time and BakingTimePerType baking time.
Each week, there is a total shaping time available of ShapingTimeAvailable and a
total baking time available of BakingTimeAvailable. The profit earned per unit
of each jar type is ProfitPerType. The artisan seeks to determine the number of
jars of each type to produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/9/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumJarTypes @Def: Number of different types of terracotta jars produced @Shape: [] 
NumJarTypes = data['NumJarTypes']
# @Parameter ShapingTimePerType @Def: Amount of shaping time required to produce one unit of each jar type @Shape: ['NumJarTypes'] 
ShapingTimePerType = data['ShapingTimePerType']
# @Parameter BakingTimePerType @Def: Amount of baking time required to produce one unit of each jar type @Shape: ['NumJarTypes'] 
BakingTimePerType = data['BakingTimePerType']
# @Parameter ProfitPerType @Def: Profit earned per unit of each jar type @Shape: ['NumJarTypes'] 
ProfitPerType = data['ProfitPerType']
# @Parameter ShapingTimeAvailable @Def: Total amount of shaping time available per week @Shape: [] 
ShapingTimeAvailable = data['ShapingTimeAvailable']
# @Parameter BakingTimeAvailable @Def: Total amount of baking time available per week @Shape: [] 
BakingTimeAvailable = data['BakingTimeAvailable']

# Variables 
# @Variable NumJars @Def: The number of jars produced for each type @Shape: ['NumJarTypes'] 
NumJars = model.addVars(NumJarTypes, vtype=GRB.CONTINUOUS, name='NumJars')

# Constraints 
# @Constraint Constr_1 @Def: The total shaping time required to produce the jars, calculated as the sum of ShapingTimePerType multiplied by the number of jars of each type produced, cannot exceed ShapingTimeAvailable.
model.addConstr(quicksum(ShapingTimePerType[i] * NumJars[i] for i in range(NumJarTypes)) <= ShapingTimeAvailable)
# @Constraint Constr_2 @Def: The total baking time required to produce the jars, calculated as the sum of BakingTimePerType multiplied by the number of jars of each type produced, cannot exceed BakingTimeAvailable.
model.addConstr(quicksum(BakingTimePerType[j] * NumJars[j] for j in range(NumJarTypes)) <= BakingTimeAvailable)

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profit per jar type multiplied by the number of jars of each type produced. The objective is to maximize the total profit.
model.setObjective(quicksum(ProfitPerType[i] * NumJars[i] for i in range(NumJarTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumJars'] = {i: NumJars[i].x for i in range(NumJarTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
