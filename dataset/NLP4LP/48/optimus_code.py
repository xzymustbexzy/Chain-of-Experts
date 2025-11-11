# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bubble tea shop produces two types of bubble teas: mango and lychee. Each
mango bubble tea requires MangoJuicePerMangoTea units of mango juice and
TeaPerMangoTea units of tea. Each lychee bubble tea requires
LycheeJuicePerLycheeTea units of lychee juice and TeaPerLycheeTea units of tea.
The shop has a total of TotalMangoJuice units of mango juice and
TotalLycheeJuice units of lychee juice available. At least MinLycheePercentage
of the total bubble teas produced must be lychee flavored. Additionally, the
number of mango bubble teas produced must be greater than the number of lychee
bubble teas. The objective is to determine the number of mango and lychee bubble
teas to produce in order to minimize the total amount of tea used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/49/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MangoJuicePerMangoTea @Def: Units of mango juice required to make one mango bubble tea @Shape: [] 
MangoJuicePerMangoTea = data['MangoJuicePerMangoTea']
# @Parameter LycheeJuicePerLycheeTea @Def: Units of lychee juice required to make one lychee bubble tea @Shape: [] 
LycheeJuicePerLycheeTea = data['LycheeJuicePerLycheeTea']
# @Parameter TeaPerMangoTea @Def: Units of tea required to make one mango bubble tea @Shape: [] 
TeaPerMangoTea = data['TeaPerMangoTea']
# @Parameter TeaPerLycheeTea @Def: Units of tea required to make one lychee bubble tea @Shape: [] 
TeaPerLycheeTea = data['TeaPerLycheeTea']
# @Parameter TotalMangoJuice @Def: Total units of mango juice available @Shape: [] 
TotalMangoJuice = data['TotalMangoJuice']
# @Parameter TotalLycheeJuice @Def: Total units of lychee juice available @Shape: [] 
TotalLycheeJuice = data['TotalLycheeJuice']
# @Parameter MinLycheePercentage @Def: Minimum percentage of total bubble teas that must be lychee flavored @Shape: [] 
MinLycheePercentage = data['MinLycheePercentage']

# Variables 
# @Variable NumberOfMangoBubbleTeas @Def: The number of mango bubble teas produced @Shape: ['Non-negative'] 
NumberOfMangoBubbleTeas = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="NumberOfMangoBubbleTeas")
# @Variable NumberOfLycheeBubbleTeas @Def: The number of lychee bubble teas produced @Shape: ['Non-negative'] 
NumberOfLycheeBubbleTeas = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfLycheeBubbleTeas")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of mango juice used for mango bubble teas cannot exceed TotalMangoJuice units. This is calculated as MangoJuicePerMangoTea multiplied by the number of mango bubble teas produced.
model.addConstr(MangoJuicePerMangoTea * NumberOfMangoBubbleTeas <= TotalMangoJuice)
# @Constraint Constr_2 @Def: The total amount of lychee juice used for lychee bubble teas cannot exceed TotalLycheeJuice units. This is calculated as LycheeJuicePerLycheeTea multiplied by the number of lychee bubble teas produced.
model.addConstr(LycheeJuicePerLycheeTea * NumberOfLycheeBubbleTeas <= TotalLycheeJuice)
# @Constraint Constr_3 @Def: At least MinLycheePercentage of the total bubble teas produced must be lychee flavored. This means that the number of lychee bubble teas divided by the total number of bubble teas (mango and lychee) must be greater than or equal to MinLycheePercentage.
model.addConstr((1 - MinLycheePercentage) * NumberOfLycheeBubbleTeas >= MinLycheePercentage * NumberOfMangoBubbleTeas)
# @Constraint Constr_4 @Def: The number of mango bubble teas produced must be greater than the number of lychee bubble teas produced.
model.addConstr(NumberOfMangoBubbleTeas >= NumberOfLycheeBubbleTeas)

# Objective 
# @Objective Objective @Def: Minimize the total amount of tea used, which is the sum of TeaPerMangoTea units for each mango bubble tea produced and TeaPerLycheeTea units for each lychee bubble tea produced.
model.setObjective(TeaPerMangoTea * NumberOfMangoBubbleTeas + TeaPerLycheeTea * NumberOfLycheeBubbleTeas, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfMangoBubbleTeas'] = NumberOfMangoBubbleTeas.x
variables['NumberOfLycheeBubbleTeas'] = NumberOfLycheeBubbleTeas.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
