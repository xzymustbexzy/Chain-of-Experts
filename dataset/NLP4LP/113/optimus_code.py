# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A subject must determine the number of gummies and the number of pills to
consume in order to maximize the total zinc intake, which is calculated as
UnitsZincPerGummy multiplied by the number of gummies plus UnitsZincPerPill
multiplied by the number of pills. The consumption must satisfy the following
constraints: the total magnesium intake, calculated as UnitsMagnesiumPerGummy
multiplied by the number of gummies plus UnitsMagnesiumPerPill multiplied by the
number of pills, does not exceed MaximumUnitsOfMagnesium; the number of pills is
at least MinimumNumberOfPills; and the number of gummies is at least
MinimumGummiesToPillsRatio times the number of pills.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/114/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter UnitsMagnesiumPerGummy @Def: Units of magnesium per gummy @Shape: [] 
UnitsMagnesiumPerGummy = data['UnitsMagnesiumPerGummy']
# @Parameter UnitsZincPerGummy @Def: Units of zinc per gummy @Shape: [] 
UnitsZincPerGummy = data['UnitsZincPerGummy']
# @Parameter UnitsMagnesiumPerPill @Def: Units of magnesium per pill @Shape: [] 
UnitsMagnesiumPerPill = data['UnitsMagnesiumPerPill']
# @Parameter UnitsZincPerPill @Def: Units of zinc per pill @Shape: [] 
UnitsZincPerPill = data['UnitsZincPerPill']
# @Parameter MinimumNumberOfPills @Def: Minimum number of pills @Shape: [] 
MinimumNumberOfPills = data['MinimumNumberOfPills']
# @Parameter MinimumGummiesToPillsRatio @Def: Minimum gummies to pills ratio @Shape: [] 
MinimumGummiesToPillsRatio = data['MinimumGummiesToPillsRatio']
# @Parameter MaximumUnitsOfMagnesium @Def: Maximum units of magnesium consumption @Shape: [] 
MaximumUnitsOfMagnesium = data['MaximumUnitsOfMagnesium']

# Variables 
# @Variable NumberOfGummies @Def: The number of gummies @Shape: ['Continuous'] 
NumberOfGummies = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfGummies")
# @Variable NumberOfPills @Def: The number of pills @Shape: ['Continuous'] 
NumberOfPills = model.addVar(lb=MinimumNumberOfPills, vtype=GRB.CONTINUOUS, name="NumberOfPills")

# Constraints 
# @Constraint Constr_1 @Def: The total magnesium intake, calculated as UnitsMagnesiumPerGummy multiplied by the number of gummies plus UnitsMagnesiumPerPill multiplied by the number of pills, does not exceed MaximumUnitsOfMagnesium.
model.addConstr(UnitsMagnesiumPerGummy * NumberOfGummies + UnitsMagnesiumPerPill * NumberOfPills <= MaximumUnitsOfMagnesium)
# @Constraint Constr_2 @Def: The number of pills is at least MinimumNumberOfPills.
model.addConstr(NumberOfPills >= MinimumNumberOfPills)
# @Constraint Constr_3 @Def: The number of gummies is at least MinimumGummiesToPillsRatio times the number of pills.
model.addConstr(NumberOfGummies >= MinimumGummiesToPillsRatio * NumberOfPills)

# Objective 
# @Objective Objective @Def: The total zinc intake is the sum of UnitsZincPerGummy multiplied by the number of gummies plus UnitsZincPerPill multiplied by the number of pills. The objective is to maximize the total zinc intake.
model.setObjective(UnitsZincPerGummy * NumberOfGummies + UnitsZincPerPill * NumberOfPills, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfGummies'] = NumberOfGummies.x
variables['NumberOfPills'] = NumberOfPills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
