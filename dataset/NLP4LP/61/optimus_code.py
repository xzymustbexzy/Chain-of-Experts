# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A bank can build small and large branches to serve their customers. A small
branch can serve CustomersSmall customers per day and requires TellersSmall bank
tellers. A large branch can serve CustomersLarge customers per day and requires
TellersLarge bank tellers. The bank has available TotalTellers bank tellers and
needs to be able to serve at least MinCustomers customers per day. They aim to
minimize the total number of branches built.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/62/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CustomersSmall @Def: Number of customers a small branch can serve per day @Shape: [] 
CustomersSmall = data['CustomersSmall']
# @Parameter TellersSmall @Def: Number of tellers required by a small branch @Shape: [] 
TellersSmall = data['TellersSmall']
# @Parameter CustomersLarge @Def: Number of customers a large branch can serve per day @Shape: [] 
CustomersLarge = data['CustomersLarge']
# @Parameter TellersLarge @Def: Number of tellers required by a large branch @Shape: [] 
TellersLarge = data['TellersLarge']
# @Parameter TotalTellers @Def: Total number of available bank tellers @Shape: [] 
TotalTellers = data['TotalTellers']
# @Parameter MinCustomers @Def: Minimum number of customers that need to be served per day @Shape: [] 
MinCustomers = data['MinCustomers']

# Variables 
# @Variable SmallBranches @Def: The number of small branches @Shape: [] 
SmallBranches = model.addVar(vtype=GRB.INTEGER, name="SmallBranches")
# @Variable LargeBranches @Def: The number of large branches @Shape: [] 
LargeBranches = model.addVar(vtype=GRB.INTEGER, name="LargeBranches")

# Constraints 
# @Constraint Constr_1 @Def: The total number of tellers required by small and large branches cannot exceed the available tellers (SmallBranches * TellersSmall + LargeBranches * TellersLarge ≤ TotalTellers).
model.addConstr(SmallBranches * TellersSmall + LargeBranches * TellersLarge <= TotalTellers)
# @Constraint Constr_2 @Def: The total number of customers served by small and large branches must be at least the minimum required (SmallBranches * CustomersSmall + LargeBranches * CustomersLarge ≥ MinCustomers).
model.addConstr(SmallBranches * CustomersSmall + LargeBranches * CustomersLarge >= MinCustomers)

# Objective 
# @Objective Objective @Def: Minimize the total number of branches built (SmallBranches + LargeBranches).
model.setObjective(SmallBranches + LargeBranches, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallBranches'] = SmallBranches.x
variables['LargeBranches'] = LargeBranches.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
