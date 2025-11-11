# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A dessert shop produces NumDessertTypes different desserts using NumIngredients
different ingredients. The ResourceUsage matrix specifies the amount of each
ingredient required per dessert. The shop must produce more of one dessert type
than another and ensure that at least a proportion MinMatchaProportion of the
total desserts are of a specific type. The total usage of each ingredient must
not exceed AvailableIngredients. The objective is to minimize the total amount
of flavouring required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/269/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumDessertTypes @Def: Number of different dessert types @Shape: [] 
NumDessertTypes = data['NumDessertTypes']
# @Parameter NumIngredients @Def: Number of different ingredients @Shape: [] 
NumIngredients = data['NumIngredients']
# @Parameter ResourceUsage @Def: Amount of each ingredient required to produce one unit of each dessert @Shape: ['NumIngredients', 'NumDessertTypes'] 
ResourceUsage = data['ResourceUsage']
# @Parameter AvailableIngredients @Def: Total available units of each ingredient @Shape: ['NumIngredients'] 
AvailableIngredients = data['AvailableIngredients']
# @Parameter MinMatchaProportion @Def: Minimum proportion of desserts that must be matcha ice cream @Shape: [] 
MinMatchaProportion = data['MinMatchaProportion']

# Variables 
# @Variable MatchaIceCream @Def: The number of matcha ice cream desserts produced @Shape: [] 
MatchaIceCream = model.addVar(vtype=GRB.CONTINUOUS, name="MatchaIceCream")
# @Variable OrangeSorbet @Def: The number of orange sorbet desserts produced @Shape: [] 
OrangeSorbet = model.addVar(vtype=GRB.CONTINUOUS, name="OrangeSorbet")

# Constraints 
# @Constraint Constr_1 @Def: The number of matcha ice cream desserts produced must be greater than the number of orange sorbet desserts produced.
model.addConstr(MatchaIceCream >= OrangeSorbet)
# @Constraint Constr_2 @Def: At least a proportion MinMatchaProportion of the total desserts must be matcha ice cream.
model.addConstr(MatchaIceCream >= MinMatchaProportion * (MatchaIceCream + OrangeSorbet))
# @Constraint Constr_3 @Def: The total usage of each ingredient must not exceed AvailableIngredients.
for i in range(NumIngredients):
    model.addConstr(ResourceUsage[i][0] * MatchaIceCream + ResourceUsage[i][1] * OrangeSorbet <= AvailableIngredients[i])

# Objective 
# @Objective Objective @Def: The objective is to minimize the total amount of flavouring required.
model.setObjective(quicksum(ResourceUsage[i][0] * MatchaIceCream + ResourceUsage[i][1] * OrangeSorbet for i in range(NumIngredients)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['MatchaIceCream'] = MatchaIceCream.x
variables['OrangeSorbet'] = OrangeSorbet.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
