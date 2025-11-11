# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A farmer wants to mix FeedA and FeedB such that the mixture contains at least
MinProtein units of protein and at least MinFat units of fat. FeedA costs
CostFeedA per kilogram and provides ProteinFeedA units of protein and FatFeedA
units of fat per kilogram. FeedB costs CostFeedB per kilogram and provides
ProteinFeedB units of protein and FatFeedB units of fat per kilogram. The
objective is to determine the amounts of FeedA and FeedB to minimize the total
cost of the mixture.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/8/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostFeedA @Def: Cost per kilogram of Feed A @Shape: [] 
CostFeedA = data['CostFeedA']
# @Parameter CostFeedB @Def: Cost per kilogram of Feed B @Shape: [] 
CostFeedB = data['CostFeedB']
# @Parameter ProteinFeedA @Def: Protein units per kilogram of Feed A @Shape: [] 
ProteinFeedA = data['ProteinFeedA']
# @Parameter ProteinFeedB @Def: Protein units per kilogram of Feed B @Shape: [] 
ProteinFeedB = data['ProteinFeedB']
# @Parameter FatFeedA @Def: Fat units per kilogram of Feed A @Shape: [] 
FatFeedA = data['FatFeedA']
# @Parameter FatFeedB @Def: Fat units per kilogram of Feed B @Shape: [] 
FatFeedB = data['FatFeedB']
# @Parameter MinProtein @Def: Minimum required units of protein in the mixture @Shape: [] 
MinProtein = data['MinProtein']
# @Parameter MinFat @Def: Minimum required units of fat in the mixture @Shape: [] 
MinFat = data['MinFat']

# Variables 
# @Variable QuantityFeedA @Def: The quantity of Feed A used in the mixture (in kilograms) @Shape: [] 
QuantityFeedA = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityFeedA")
# @Variable QuantityFeedB @Def: The quantity of Feed B used in the mixture (in kilograms) @Shape: [] 
QuantityFeedB = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityFeedB")

# Constraints 
# @Constraint Constr_1 @Def: Each kilogram of FeedA provides ProteinFeedA units of protein and each kilogram of FeedB provides ProteinFeedB units of protein. The mixture must contain at least MinProtein units of protein.
model.addConstr(ProteinFeedA * QuantityFeedA + ProteinFeedB * QuantityFeedB >= MinProtein)
# @Constraint Constr_2 @Def: Each kilogram of FeedA provides FatFeedA units of fat and each kilogram of FeedB provides FatFeedB units of fat. The mixture must contain at least MinFat units of fat.
model.addConstr(FatFeedA * QuantityFeedA + FatFeedB * QuantityFeedB >= MinFat)

# Objective 
# @Objective Objective @Def: The total cost of the mixture is CostFeedA multiplied by the amount of FeedA plus CostFeedB multiplied by the amount of FeedB. The objective is to minimize the total cost.
model.setObjective(CostFeedA * QuantityFeedA + CostFeedB * QuantityFeedB, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityFeedA'] = QuantityFeedA.x
variables['QuantityFeedB'] = QuantityFeedB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
