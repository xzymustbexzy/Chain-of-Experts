# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A woman has TotalMoney to gamble on NumBets different sports bets. Each sport
bet has a loss probability given by LossProbabilities and a payout per dollar
given by Payouts. She limits her average chance of losing her money to at most
MaxAverageLossProbability. Determine the allocation of money to each sport bet
to maximize her average payout.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/204/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalMoney @Def: Total amount of money available to gamble @Shape: [] 
TotalMoney = data['TotalMoney']
# @Parameter NumBets @Def: Number of different sports bets @Shape: [] 
NumBets = data['NumBets']
# @Parameter LossProbabilities @Def: Chance of losing money for each sport bet @Shape: ['NumBets'] 
LossProbabilities = data['LossProbabilities']
# @Parameter Payouts @Def: Payout per dollar for each sport bet @Shape: ['NumBets'] 
Payouts = data['Payouts']
# @Parameter MaxAverageLossProbability @Def: Maximum average chance of losing money @Shape: [] 
MaxAverageLossProbability = data['MaxAverageLossProbability']

# Variables 
# @Variable Allocation @Def: The amount of money allocated to each sports bet @Shape: ['NumBets'] 
Allocation = model.addVars(NumBets, vtype=GRB.CONTINUOUS, name="Allocation")

# Constraints 
# @Constraint Constr_1 @Def: The sum of allocations to all sports bets must equal TotalMoney.
model.addConstr(quicksum(Allocation[i] for i in range(NumBets)) == TotalMoney)
# @Constraint Constr_2 @Def: The weighted average of LossProbabilities, based on the allocation, must not exceed MaxAverageLossProbability.
model.addConstr(quicksum(Allocation[i] * LossProbabilities[i] for i in range(NumBets)) <= TotalMoney * MaxAverageLossProbability)

# Objective 
# @Objective Objective @Def: Maximize the total expected payout from all sports bets.
model.setObjective(quicksum(Allocation[i] * Payouts[i] * (1 - LossProbabilities[i]) for i in range(NumBets)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Allocation'] = {i: Allocation[i].x for i in range(NumBets)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)