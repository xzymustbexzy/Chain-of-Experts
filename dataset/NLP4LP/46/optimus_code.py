# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An amusement park is installing cash-based machines and card-only machines. A
cash-based machine can process CashMachineProcessingRate people per hour, while
a card-only machine can process CardMachineProcessingRate people per hour. The
cash-based machine needs CashMachinePaperRolls rolls of paper per hour, while
the card-only machine requires CardMachinePaperRolls rolls of paper per hour.
The amusement park needs to be able to process at least MinPeopleProcessed
people per hour but can use at most MaxPaperRolls paper rolls per hour.
Additionally, the number of card-only machines must not exceed the number of
cash-based machines. The objective is to minimize the total number of machines
in the park.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/47/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CashMachineProcessingRate @Def: Processing rate of a cash-based machine in people per hour @Shape: [] 
CashMachineProcessingRate = data['CashMachineProcessingRate']
# @Parameter CardMachineProcessingRate @Def: Processing rate of a card-only machine in people per hour @Shape: [] 
CardMachineProcessingRate = data['CardMachineProcessingRate']
# @Parameter CashMachinePaperRolls @Def: Number of paper rolls used per hour by a cash-based machine @Shape: [] 
CashMachinePaperRolls = data['CashMachinePaperRolls']
# @Parameter CardMachinePaperRolls @Def: Number of paper rolls used per hour by a card-only machine @Shape: [] 
CardMachinePaperRolls = data['CardMachinePaperRolls']
# @Parameter MinPeopleProcessed @Def: Minimum number of people that must be processed per hour @Shape: [] 
MinPeopleProcessed = data['MinPeopleProcessed']
# @Parameter MaxPaperRolls @Def: Maximum number of paper rolls that can be used per hour @Shape: [] 
MaxPaperRolls = data['MaxPaperRolls']

# Variables 
# @Variable NumCashMachines @Def: The number of cash-based machines @Shape: [] 
NumCashMachines = model.addVar(vtype=GRB.INTEGER, name="NumCashMachines")
# @Variable NumCardMachines @Def: The number of card-only machines @Shape: [] 
NumCardMachines = model.addVar(vtype=GRB.INTEGER, name="NumCardMachines")

# Constraints 
# @Constraint Constr_1 @Def: The total number of people processed per hour by cash-based and card-only machines must be at least MinPeopleProcessed.
model.addConstr(CashMachineProcessingRate * NumCashMachines + CardMachineProcessingRate * NumCardMachines >= MinPeopleProcessed)
# @Constraint Constr_2 @Def: The total number of paper rolls used per hour by cash-based and card-only machines must not exceed MaxPaperRolls.
model.addConstr(NumCashMachines * CashMachinePaperRolls + NumCardMachines * CardMachinePaperRolls <= MaxPaperRolls)
# @Constraint Constr_3 @Def: The number of card-only machines must not exceed the number of cash-based machines.
model.addConstr(NumCardMachines <= NumCashMachines)

# Objective 
# @Objective Objective @Def: Minimize the total number of machines in the park.
model.setObjective(NumCashMachines + NumCardMachines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumCashMachines'] = NumCashMachines.x
variables['NumCardMachines'] = NumCardMachines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
