# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A sandwich company can open NumStoreTypes types of stores. Each store type
produces SandwichesPerStoreType sandwiches per day and requires
EmployeesPerStoreType employees to operate. The company must produce at least
MinimumSandwiches sandwiches per day and has at most MaximumEmployees employees
available. Determine the number of each type of store to minimize the total
number of stores.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/42/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumStoreTypes @Def: Number of types of stores available @Shape: [] 
NumStoreTypes = data['NumStoreTypes']
# @Parameter SandwichesPerStoreType @Def: Number of sandwiches produced per store type per day @Shape: ['NumStoreTypes'] 
SandwichesPerStoreType = data['SandwichesPerStoreType']
# @Parameter EmployeesPerStoreType @Def: Number of employees required per store type @Shape: ['NumStoreTypes'] 
EmployeesPerStoreType = data['EmployeesPerStoreType']
# @Parameter MinimumSandwiches @Def: Minimum number of sandwiches to be produced per day @Shape: [] 
MinimumSandwiches = data['MinimumSandwiches']
# @Parameter MaximumEmployees @Def: Maximum number of employees available @Shape: [] 
MaximumEmployees = data['MaximumEmployees']

# Variables 
# @Variable NumberStore @Def: The number of stores for each store type @Shape: ['NumStoreTypes'] 
NumberStore = model.addVars(NumStoreTypes, vtype=GRB.INTEGER, name="NumberStore")

# Constraints 
# @Constraint Constr_1 @Def: The total number of sandwiches produced per day must be at least MinimumSandwiches. This is calculated by summing SandwichesPerStoreType multiplied by the number of each store type.
model.addConstr(quicksum(SandwichesPerStoreType[i] * NumberStore[i] for i in range(NumStoreTypes)) >= MinimumSandwiches)
# @Constraint Constr_2 @Def: The total number of employees required must not exceed MaximumEmployees. This is calculated by summing EmployeesPerStoreType multiplied by the number of each store type.
model.addConstr(quicksum(EmployeesPerStoreType[i] * NumberStore[i] for i in range(NumStoreTypes)) <= MaximumEmployees)

# Objective 
# @Objective Objective @Def: Minimize the total number of stores, which is the sum of the number of each type of store.
model.setObjective(quicksum(NumberStore[t] for t in range(NumStoreTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberStore'] = {i: NumberStore[i].x for i in range(NumStoreTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)