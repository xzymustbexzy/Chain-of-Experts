# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A research group is producing NumProducts different products using NumMethods
production methods. Each method has a ProductionRate for each product and
consumes SpecialElementConsumption units of a special element per hour. The
research group has TotalSpecialElement units of the special element available
and must produce at least MinRequired units for each product. The objective is
to minimize the total time needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/250/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumMethods @Def: The number of production methods available @Shape: [] 
NumMethods = data['NumMethods']
# @Parameter NumProducts @Def: The number of different products being produced @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter ProductionRate @Def: Units of each product produced per hour by each method @Shape: ['NumProducts', 'NumMethods'] 
ProductionRate = data['ProductionRate']
# @Parameter SpecialElementConsumption @Def: Units of the special element required per hour by each method @Shape: ['NumMethods'] 
SpecialElementConsumption = data['SpecialElementConsumption']
# @Parameter TotalSpecialElement @Def: Total units of the special element available @Shape: [] 
TotalSpecialElement = data['TotalSpecialElement']
# @Parameter MinRequired @Def: Minimum number of units required for each product @Shape: ['NumProducts'] 
MinRequired = data['MinRequired']

# Variables 
# @Variable OperationTime @Def: The number of hours each production method is operated @Shape: ['NumMethods'] 
OperationTime = model.addVars(NumMethods, vtype=GRB.CONTINUOUS, name="OperationTime")
# @Variable TotalTime @Def: The total time to produce all required products @Shape: [] 
TotalTime = model.addVar(vtype=GRB.CONTINUOUS, name="TotalTime")

# Constraints 
# @Constraint Constr_1 @Def: The total consumption of the special element by all production methods cannot exceed TotalSpecialElement units.
model.addConstr(quicksum(SpecialElementConsumption[m] * OperationTime[m] for m in range(NumMethods)) <= TotalSpecialElement)
# @Constraint Constr_2 @Def: For each product, the total number of units produced by all production methods must be at least MinRequired units.
model.addConstrs((quicksum(ProductionRate[p][m] * OperationTime[m] for m in range(NumMethods)) >= MinRequired[p] for p in range(NumProducts)), name="MinRequiredProduction")

# Objective 
# @Objective Objective @Def: The objective is to minimize the total time needed to produce all required products while satisfying the resource and production constraints.
model.setObjective(TotalTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['OperationTime'] = {m: OperationTime[m].x for m in range(NumMethods)}
variables['TotalTime'] = TotalTime.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
