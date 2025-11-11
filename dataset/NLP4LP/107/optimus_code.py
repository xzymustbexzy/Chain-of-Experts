# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A clinic produces two products: vitamin shots and vitamin pills. Each batch of
vitamin shots requires VitaminCShots units of vitamin C and VitaminDShots units
of vitamin D. Each batch of vitamin pills requires VitaminCPills units of
vitamin C and VitaminDPills units of vitamin D. The number of batches of vitamin
pills must be greater than the number of batches of vitamin shots by at least
MinBatchDifference. The clinic can produce at most MaxBatchesShots batches of
vitamin shots. The clinic has AvailableVitaminC units of vitamin C and
AvailableVitaminD units of vitamin D available. Each batch of vitamin shots can
supply SupplyShots people and each batch of vitamin pills can supply SupplyPills
people. The objective is to determine the number of batches of each product to
maximize the number of people that can be supplied.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/108/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VitaminCShots @Def: Amount of vitamin C required per batch of vitamin shots @Shape: [] 
VitaminCShots = data['VitaminCShots']
# @Parameter VitaminDShots @Def: Amount of vitamin D required per batch of vitamin shots @Shape: [] 
VitaminDShots = data['VitaminDShots']
# @Parameter VitaminCPills @Def: Amount of vitamin C required per batch of vitamin pills @Shape: [] 
VitaminCPills = data['VitaminCPills']
# @Parameter VitaminDPills @Def: Amount of vitamin D required per batch of vitamin pills @Shape: [] 
VitaminDPills = data['VitaminDPills']
# @Parameter MaxBatchesShots @Def: The maximum number of batches of vitamin shots that can be produced @Shape: [] 
MaxBatchesShots = data['MaxBatchesShots']
# @Parameter AvailableVitaminC @Def: Total available units of vitamin C @Shape: [] 
AvailableVitaminC = data['AvailableVitaminC']
# @Parameter AvailableVitaminD @Def: Total available units of vitamin D @Shape: [] 
AvailableVitaminD = data['AvailableVitaminD']
# @Parameter SupplyShots @Def: Number of people supplied per batch of vitamin shots @Shape: [] 
SupplyShots = data['SupplyShots']
# @Parameter SupplyPills @Def: Number of people supplied per batch of vitamin pills @Shape: [] 
SupplyPills = data['SupplyPills']
# @Parameter MinBatchDifference @Def: Minimum number of additional batches of vitamin pills compared to vitamin shots @Shape: [] 
MinBatchDifference = data['MinBatchDifference']

# Variables 
# @Variable BatchesShots @Def: The number of batches of vitamin shots produced @Shape: ['integer'] 
BatchesShots = model.addVar(vtype=GRB.INTEGER, name="BatchesShots", lb=0, ub=MaxBatchesShots)
# @Variable BatchesPills @Def: The number of batches of vitamin pills produced @Shape: ['integer'] 
BatchesPills = model.addVar(vtype=GRB.INTEGER, name="BatchesPills")

# Constraints 
# @Constraint Constr_1 @Def: Each batch of vitamin shots requires VitaminCShots units of vitamin C and each batch of vitamin pills requires VitaminCPills units of vitamin C. The total vitamin C used cannot exceed AvailableVitaminC.
model.addConstr(VitaminCShots * BatchesShots + VitaminCPills * BatchesPills <= AvailableVitaminC)
# @Constraint Constr_2 @Def: Each batch of vitamin shots requires VitaminDShots units of vitamin D and each batch of vitamin pills requires VitaminDPills units of vitamin D. The total vitamin D used cannot exceed AvailableVitaminD.
model.addConstr(VitaminDShots * BatchesShots + VitaminDPills * BatchesPills <= AvailableVitaminD)
# @Constraint Constr_3 @Def: The number of batches of vitamin pills must exceed the number of batches of vitamin shots by at least MinBatchDifference.
model.addConstr(BatchesPills - BatchesShots >= MinBatchDifference)
# @Constraint Constr_4 @Def: The number of batches of vitamin shots produced cannot exceed MaxBatchesShots.
model.addConstr(BatchesShots <= MaxBatchesShots)

# Objective 
# @Objective Objective @Def: The total number of people supplied is the sum of the people supplied by vitamin shots and vitamin pills. The objective is to maximize this total number of people supplied.
model.setObjective(SupplyShots * BatchesShots + SupplyPills * BatchesPills, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BatchesShots'] = BatchesShots.x
variables['BatchesPills'] = BatchesPills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
