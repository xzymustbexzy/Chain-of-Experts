# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A city employs seasonal and permanent snow removers. A seasonal snow remover
works HoursSeasonal hours per shift and gets paid PaymentSeasonal. A permanent
snow remover works HoursPermanent hours per shift and gets paid
PaymentPermanent. Currently the city needs RequiredLaborHours hours of snow
remover labor after a heavy snowfall. If the city has a budget of TotalBudget,
how many of each type of worker should be hired to minimize the total number of
snow removers?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/50/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HoursSeasonal @Def: Number of hours per shift for a seasonal snow remover @Shape: [] 
HoursSeasonal = data['HoursSeasonal']
# @Parameter PaymentSeasonal @Def: Payment per shift for a seasonal snow remover @Shape: [] 
PaymentSeasonal = data['PaymentSeasonal']
# @Parameter HoursPermanent @Def: Number of hours per shift for a permanent snow remover @Shape: [] 
HoursPermanent = data['HoursPermanent']
# @Parameter PaymentPermanent @Def: Payment per shift for a permanent snow remover @Shape: [] 
PaymentPermanent = data['PaymentPermanent']
# @Parameter RequiredLaborHours @Def: Total required labor hours after a heavy snowfall @Shape: [] 
RequiredLaborHours = data['RequiredLaborHours']
# @Parameter TotalBudget @Def: Total budget available for hiring snow removers @Shape: [] 
TotalBudget = data['TotalBudget']

# Variables 
# @Variable NumberSeasonal @Def: The number of seasonal snow removers hired @Shape: ['NonNegative Integer'] 
NumberSeasonal = model.addVar(vtype=GRB.INTEGER, name="NumberSeasonal")
# @Variable NumberPermanent @Def: The number of permanent snow removers hired @Shape: ['NonNegative Integer'] 
NumberPermanent = model.addVar(vtype=GRB.INTEGER, name="NumberPermanent")

# Constraints 
# @Constraint Constr_1 @Def: The total labor hours provided by seasonal and permanent snow removers must meet or exceed RequiredLaborHours.
model.addConstr(HoursSeasonal * NumberSeasonal + HoursPermanent * NumberPermanent >= RequiredLaborHours)
# @Constraint Constr_2 @Def: The total payment for seasonal and permanent snow removers must not exceed TotalBudget.
model.addConstr(NumberSeasonal * PaymentSeasonal + NumberPermanent * PaymentPermanent <= TotalBudget)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of snow removers, which is the sum of seasonal and permanent snow removers hired.
model.setObjective(quicksum([NumberSeasonal, NumberPermanent]), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSeasonal'] = NumberSeasonal.x
variables['NumberPermanent'] = NumberPermanent.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
