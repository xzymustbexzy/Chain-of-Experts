# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A researcher must annotate at least MinTotalImages images by distributing the
work between a specialized company and a common company. The specialized company
annotates at a rate of SpecializedAnnotRate images per hour and charges
SpecializedCostPerHour per hour. The common company annotates at a rate of
CommonAnnotRate images per hour and charges CommonCostPerHour per hour. At least
MinSpecializedFraction of the work must be allocated to the specialized company.
The objective is to minimize the total annotation cost.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/254/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SpecializedAnnotRate @Def: Annotation rate of the specialized company (images per hour) @Shape: [] 
SpecializedAnnotRate = data['SpecializedAnnotRate']
# @Parameter CommonAnnotRate @Def: Annotation rate of the common company (images per hour) @Shape: [] 
CommonAnnotRate = data['CommonAnnotRate']
# @Parameter SpecializedCostPerHour @Def: Cost per hour of the specialized company @Shape: [] 
SpecializedCostPerHour = data['SpecializedCostPerHour']
# @Parameter CommonCostPerHour @Def: Cost per hour of the common company @Shape: [] 
CommonCostPerHour = data['CommonCostPerHour']
# @Parameter MinTotalImages @Def: Minimum number of images to annotate @Shape: [] 
MinTotalImages = data['MinTotalImages']
# @Parameter MinSpecializedFraction @Def: Minimum fraction of work allocated to the specialized company @Shape: [] 
MinSpecializedFraction = data['MinSpecializedFraction']

# Variables 
# @Variable SpecializedHours @Def: The number of hours the specialized company works @Shape: [] 
SpecializedHours = model.addVar(vtype=GRB.CONTINUOUS, name="SpecializedHours")
# @Variable CommonHours @Def: The number of hours the common company works @Shape: [] 
CommonHours = model.addVar(vtype=GRB.CONTINUOUS, name="CommonHours")

# Constraints 
# @Constraint Constr_1 @Def: The total number of images annotated by the specialized company and the common company must be at least MinTotalImages.
model.addConstr(SpecializedAnnotRate * SpecializedHours + CommonAnnotRate * CommonHours >= MinTotalImages)
# @Constraint Constr_2 @Def: The number of images annotated by the specialized company must be at least MinSpecializedFraction of the total number of annotated images.
model.addConstr(SpecializedAnnotRate * SpecializedHours >= MinSpecializedFraction * (SpecializedAnnotRate * SpecializedHours + CommonAnnotRate * CommonHours))

# Objective 
# @Objective Objective @Def: Minimize the total annotation cost, which is the sum of the costs of the specialized and common companies.
model.setObjective(SpecializedCostPerHour * SpecializedHours + CommonCostPerHour * CommonHours, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SpecializedHours'] = SpecializedHours.x
variables['CommonHours'] = CommonHours.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
