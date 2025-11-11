# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A snack exporter must determine the number of small and large suitcases to send
in order to maximize the total number of snacks delivered. Each small suitcase
has a capacity of SmallSuitcaseCapacity snacks, and each large suitcase has a
capacity of LargeSuitcaseCapacity snacks. The number of small suitcases used
must be at least MinSmallToLargeRatio times the number of large suitcases. The
exporter is limited by MaxSmallSuitcases available small suitcases and
MaxLargeSuitcases available large suitcases. Additionally, the exporter must
send at least MinLargeSuitcases large suitcases and ensure that the total number
of suitcases sent does not exceed MaxTotalSuitcases.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/160/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallSuitcaseCapacity @Def: Capacity of a small suitcase in snacks @Shape: [] 
SmallSuitcaseCapacity = data['SmallSuitcaseCapacity']
# @Parameter LargeSuitcaseCapacity @Def: Capacity of a large suitcase in snacks @Shape: [] 
LargeSuitcaseCapacity = data['LargeSuitcaseCapacity']
# @Parameter MinSmallToLargeRatio @Def: Minimum ratio factor indicating that the number of small suitcases must be at least twice the number of large suitcases @Shape: [] 
MinSmallToLargeRatio = data['MinSmallToLargeRatio']
# @Parameter MaxSmallSuitcases @Def: Maximum number of small suitcases available @Shape: [] 
MaxSmallSuitcases = data['MaxSmallSuitcases']
# @Parameter MaxLargeSuitcases @Def: Maximum number of large suitcases available @Shape: [] 
MaxLargeSuitcases = data['MaxLargeSuitcases']
# @Parameter MinLargeSuitcases @Def: Minimum number of large suitcases to send @Shape: [] 
MinLargeSuitcases = data['MinLargeSuitcases']
# @Parameter MaxTotalSuitcases @Def: Maximum total number of suitcases to send @Shape: [] 
MaxTotalSuitcases = data['MaxTotalSuitcases']

# Variables 
# @Variable SmallSuitcasesUsed @Def: The number of small suitcases used @Shape: [] 
SmallSuitcasesUsed = model.addVar(ub=MaxSmallSuitcases, vtype=GRB.INTEGER, name="SmallSuitcasesUsed")
# @Variable LargeSuitcasesUsed @Def: The number of large suitcases used @Shape: [] 
LargeSuitcasesUsed = model.addVar(lb=MinLargeSuitcases, ub=MaxLargeSuitcases, vtype=GRB.INTEGER, name="LargeSuitcasesUsed")

# Constraints 
# @Constraint Constr_1 @Def: The number of small suitcases used must be at least MinSmallToLargeRatio times the number of large suitcases.
model.addConstr(SmallSuitcasesUsed >= MinSmallToLargeRatio * LargeSuitcasesUsed)
# @Constraint Constr_2 @Def: The number of small suitcases sent cannot exceed MaxSmallSuitcases.
model.addConstr(SmallSuitcasesUsed <= MaxSmallSuitcases)
# @Constraint Constr_3 @Def: The number of large suitcases sent cannot exceed MaxLargeSuitcases.
model.addConstr(LargeSuitcasesUsed <= MaxLargeSuitcases)
# @Constraint Constr_4 @Def: At least MinLargeSuitcases large suitcases must be sent.
# The constraint 'LargeSuitcasesUsed >= MinLargeSuitcases' is already enforced by setting the variable's lower bound.
# No additional constraint is needed.
# @Constraint Constr_5 @Def: The total number of suitcases sent cannot exceed MaxTotalSuitcases.
model.addConstr(SmallSuitcasesUsed + LargeSuitcasesUsed <= MaxTotalSuitcases)

# Objective 
# @Objective Objective @Def: Maximize the total number of snacks delivered, calculated as (Number of Small Suitcases × SmallSuitcaseCapacity) plus (Number of Large Suitcases × LargeSuitcaseCapacity).
model.setObjective(SmallSuitcasesUsed * SmallSuitcaseCapacity + LargeSuitcasesUsed * LargeSuitcaseCapacity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallSuitcasesUsed'] = SmallSuitcasesUsed.x
variables['LargeSuitcasesUsed'] = LargeSuitcasesUsed.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
