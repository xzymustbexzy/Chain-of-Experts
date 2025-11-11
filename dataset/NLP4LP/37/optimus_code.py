# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A teddy bear company produces NumColors different colored bears using
NumFactories different factories. Running factory k for one hour costs
FactoryRunningCost[k]. Factory k produces ProductionRate[k][c] teddy bears of
color c per hour. To meet demand, the company must produce at least Demand[c]
teddy bears of each color daily. The objective is to minimize the total
production cost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/38/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumFactories @Def: The number of different factories available for production @Shape: [] 
NumFactories = data['NumFactories']
# @Parameter NumColors @Def: The number of different colored teddy bears produced @Shape: [] 
NumColors = data['NumColors']
# @Parameter FactoryRunningCost @Def: The cost to run each factory for one hour @Shape: ['NumFactories'] 
FactoryRunningCost = data['FactoryRunningCost']
# @Parameter ProductionRate @Def: The number of teddy bears of each color produced per hour by each factory @Shape: ['NumFactories', 'NumColors'] 
ProductionRate = data['ProductionRate']
# @Parameter Demand @Def: The minimum number of teddy bears of each color required per day @Shape: ['NumColors'] 
Demand = data['Demand']

# Variables 
# @Variable RunningTime @Def: The running time of each factory @Shape: ['NumFactories'] 
RunningTime = model.addVars(NumFactories, vtype=GRB.CONTINUOUS, name="RunningTime")

# Constraints 
# @Constraint Constr_1 @Def: For each color c, the total production across all factories must be at least Demand[c]. This means that the sum of ProductionRate[k][c] multiplied by the running time of factory k for all factories k must be greater than or equal to Demand[c].
model.addConstrs(
    (quicksum(ProductionRate[k][c] * RunningTime[k] for k in range(NumFactories)) >= Demand[c] 
     for c in range(NumColors)),
    name="DemandConstraint"
)
# @Constraint Constr_2 @Def: Factory running times must be non-negative.
model.addConstrs(RunningTime[i] >= 0 for i in range(NumFactories))

# Objective 
# @Objective Objective @Def: Minimize the total production cost, which is the sum of the running costs of all factories multiplied by their respective running times.
model.setObjective(quicksum(FactoryRunningCost[i] * RunningTime[i] for i in range(NumFactories)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RunningTime'] = {k: RunningTime[k].X for k in range(NumFactories)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)