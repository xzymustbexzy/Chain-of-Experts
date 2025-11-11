# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
There are two processes, Process A and Process B. Executing Process A once
requires GoldRequiredProcessA units of gold and WireRequiredProcessA wires, and
plates CoinsPlatedProcessA coins. Executing Process B once requires
GoldRequiredProcessB units of gold and WireRequiredProcessB wires, and plates
CoinsPlatedProcessB coins. A total of TotalGoldAvailable units of gold and
TotalWiresAvailable wires are available. Determine the number of executions of
Process A and Process B to maximize the total number of coins plated.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/43/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GoldRequiredProcessA @Def: Amount of gold required to run Process A once @Shape: [] 
GoldRequiredProcessA = data['GoldRequiredProcessA']
# @Parameter WireRequiredProcessA @Def: Number of wires required to run Process A once @Shape: [] 
WireRequiredProcessA = data['WireRequiredProcessA']
# @Parameter CoinsPlatedProcessA @Def: Number of coins plated per execution of Process A @Shape: [] 
CoinsPlatedProcessA = data['CoinsPlatedProcessA']
# @Parameter GoldRequiredProcessB @Def: Amount of gold required to run Process B once @Shape: [] 
GoldRequiredProcessB = data['GoldRequiredProcessB']
# @Parameter WireRequiredProcessB @Def: Number of wires required to run Process B once @Shape: [] 
WireRequiredProcessB = data['WireRequiredProcessB']
# @Parameter CoinsPlatedProcessB @Def: Number of coins plated per execution of Process B @Shape: [] 
CoinsPlatedProcessB = data['CoinsPlatedProcessB']
# @Parameter TotalGoldAvailable @Def: Total amount of gold available @Shape: [] 
TotalGoldAvailable = data['TotalGoldAvailable']
# @Parameter TotalWiresAvailable @Def: Total number of wires available @Shape: [] 
TotalWiresAvailable = data['TotalWiresAvailable']

# Variables 
# @Variable ExecuteProcessA @Def: The number of times Process A is executed @Shape: [] 
ExecuteProcessA = model.addVar(vtype=GRB.INTEGER, name="ExecuteProcessA")
# @Variable ExecuteProcessB @Def: The number of times Process B is executed @Shape: [] 
ExecuteProcessB = model.addVar(vtype=GRB.INTEGER, name="ExecuteProcessB")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of gold required for executing Process A and Process B does not exceed TotalGoldAvailable units of gold.
model.addConstr(GoldRequiredProcessA * ExecuteProcessA + GoldRequiredProcessB * ExecuteProcessB <= TotalGoldAvailable)
# @Constraint Constr_2 @Def: The total number of wires required for executing Process A and Process B does not exceed TotalWiresAvailable wires.
model.addConstr(WireRequiredProcessA * ExecuteProcessA + WireRequiredProcessB * ExecuteProcessB <= TotalWiresAvailable)

# Objective 
# @Objective Objective @Def: The total number of coins plated is the sum of CoinsPlatedProcessA multiplied by the number of executions of Process A and CoinsPlatedProcessB multiplied by the number of executions of Process B. The objective is to maximize the total number of coins plated.
model.setObjective(CoinsPlatedProcessA * ExecuteProcessA + CoinsPlatedProcessB * ExecuteProcessB, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ExecuteProcessA'] = ExecuteProcessA.x
variables['ExecuteProcessB'] = ExecuteProcessB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
