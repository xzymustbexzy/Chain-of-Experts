# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A chocolate shop produces two types of chocolate bars: milk and dark. Producing
one milk chocolate bar requires CocoaPerMilkBar units of cocoa and
MilkPerMilkBar units of milk. Producing one dark chocolate bar requires
CocoaPerDarkBar units of cocoa and MilkPerDarkBar units of milk. The shop has
TotalCocoa units of cocoa and TotalMilk units of milk available. At least
MinMilkToDarkRatio times as many milk chocolate bars as dark chocolate bars must
be produced. Producing one milk chocolate bar takes TimePerMilkBar minutes and
producing one dark chocolate bar takes TimePerDarkBar minutes. The objective is
to determine the number of each type of bar to produce in order to minimize the
total production time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/86/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CocoaPerMilkBar @Def: Amount of cocoa required to produce one milk chocolate bar @Shape: [] 
CocoaPerMilkBar = data['CocoaPerMilkBar']
# @Parameter MilkPerMilkBar @Def: Amount of milk required to produce one milk chocolate bar @Shape: [] 
MilkPerMilkBar = data['MilkPerMilkBar']
# @Parameter CocoaPerDarkBar @Def: Amount of cocoa required to produce one dark chocolate bar @Shape: [] 
CocoaPerDarkBar = data['CocoaPerDarkBar']
# @Parameter MilkPerDarkBar @Def: Amount of milk required to produce one dark chocolate bar @Shape: [] 
MilkPerDarkBar = data['MilkPerDarkBar']
# @Parameter TotalCocoa @Def: Total units of cocoa available @Shape: [] 
TotalCocoa = data['TotalCocoa']
# @Parameter TotalMilk @Def: Total units of milk available @Shape: [] 
TotalMilk = data['TotalMilk']
# @Parameter MinMilkToDarkRatio @Def: Minimum ratio of milk chocolate bars to dark chocolate bars @Shape: [] 
MinMilkToDarkRatio = data['MinMilkToDarkRatio']
# @Parameter TimePerMilkBar @Def: Time required to produce one milk chocolate bar in minutes @Shape: [] 
TimePerMilkBar = data['TimePerMilkBar']
# @Parameter TimePerDarkBar @Def: Time required to produce one dark chocolate bar in minutes @Shape: [] 
TimePerDarkBar = data['TimePerDarkBar']

# Variables 
# @Variable MilkBars @Def: The number of milk chocolate bars produced @Shape: [] 
MilkBars = model.addVar(vtype=GRB.INTEGER, name="MilkBars")
# @Variable DarkBars @Def: The number of dark chocolate bars produced @Shape: [] 
DarkBars = model.addVar(vtype=GRB.INTEGER, name="DarkBars")

# Constraints 
# @Constraint Constr_1 @Def: The total cocoa used to produce milk and dark chocolate bars does not exceed TotalCocoa units.
model.addConstr(CocoaPerMilkBar * MilkBars + CocoaPerDarkBar * DarkBars <= TotalCocoa)
# @Constraint Constr_2 @Def: The total milk used to produce milk and dark chocolate bars does not exceed TotalMilk units.
model.addConstr(MilkPerMilkBar * MilkBars + MilkPerDarkBar * DarkBars <= TotalMilk)
# @Constraint Constr_3 @Def: The number of milk chocolate bars produced is at least MinMilkToDarkRatio times the number of dark chocolate bars produced.
model.addConstr(MilkBars >= MinMilkToDarkRatio * DarkBars)

# Objective 
# @Objective Objective @Def: Minimize the total production time, which is the sum of the time required to produce the milk and dark chocolate bars.
model.setObjective(MilkBars * TimePerMilkBar + DarkBars * TimePerDarkBar, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['MilkBars'] = MilkBars.x
variables['DarkBars'] = DarkBars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
