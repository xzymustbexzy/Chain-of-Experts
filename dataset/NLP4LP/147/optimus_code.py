# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A school hires small buses and large buses with capacities SmallBusCapacity and
LargeBusCapacity respectively to transport at least MinimumStudents students. No
more than MaxLargeBusPercentage of the total buses can be large buses. The
objective is to minimize the total number of buses hired.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/148/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallBusCapacity @Def: Capacity of a small bus @Shape: [] 
SmallBusCapacity = data['SmallBusCapacity']
# @Parameter LargeBusCapacity @Def: Capacity of a large bus @Shape: [] 
LargeBusCapacity = data['LargeBusCapacity']
# @Parameter MinimumStudents @Def: Minimum number of students to transport @Shape: [] 
MinimumStudents = data['MinimumStudents']
# @Parameter MaxLargeBusPercentage @Def: Maximum percentage of buses that can be large buses @Shape: [] 
MaxLargeBusPercentage = data['MaxLargeBusPercentage']

# Variables 
# @Variable NumberSmallBuses @Def: The number of small buses @Shape: ['Integer'] 
NumberSmallBuses = model.addVar(vtype=GRB.INTEGER, name="NumberSmallBuses")
# @Variable NumberLargeBuses @Def: The number of large buses @Shape: ['Integer'] 
NumberLargeBuses = model.addVar(vtype=GRB.INTEGER, name="NumberLargeBuses")

# Constraints 
# @Constraint Constr_1 @Def: A small bus transports SmallBusCapacity students and a large bus transports LargeBusCapacity students. The total number of students transported must be at least MinimumStudents.
model.addConstr(SmallBusCapacity * NumberSmallBuses + LargeBusCapacity * NumberLargeBuses >= MinimumStudents)
# @Constraint Constr_2 @Def: No more than MaxLargeBusPercentage of the total buses can be large buses.
model.addConstr((1 - MaxLargeBusPercentage) * NumberLargeBuses <= MaxLargeBusPercentage * NumberSmallBuses)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of buses hired.
model.setObjective(NumberSmallBuses + NumberLargeBuses, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSmallBuses'] = NumberSmallBuses.x
variables['NumberLargeBuses'] = NumberLargeBuses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
