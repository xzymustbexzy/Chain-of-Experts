# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A recycling company selects the number of SmallBins and LargeBins, where each
SmallBin requires WorkersPerSmallBin workers and holds CapacitySmallBin units of
recycling material, and each LargeBin requires WorkersPerLargeBin workers and
holds CapacityLargeBin units of recycling material. The total number of workers
used must not exceed TotalWorkers. The number of SmallBins must be
SmallBinToLargeBinRatio times the number of LargeBins. Additionally, the number
of SmallBins must be at least MinimumSmallBins and the number of LargeBins must
be at least MinimumLargeBins. The objective is to maximize the total recycling
material collected.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/164/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter WorkersPerSmallBin @Def: Number of workers required for a small bin @Shape: [] 
WorkersPerSmallBin = data['WorkersPerSmallBin']
# @Parameter WorkersPerLargeBin @Def: Number of workers required for a large bin @Shape: [] 
WorkersPerLargeBin = data['WorkersPerLargeBin']
# @Parameter CapacitySmallBin @Def: Capacity of a small bin in units of recycling material @Shape: [] 
CapacitySmallBin = data['CapacitySmallBin']
# @Parameter CapacityLargeBin @Def: Capacity of a large bin in units of recycling material @Shape: [] 
CapacityLargeBin = data['CapacityLargeBin']
# @Parameter TotalWorkers @Def: Total number of available workers @Shape: [] 
TotalWorkers = data['TotalWorkers']
# @Parameter SmallBinToLargeBinRatio @Def: Required ratio of small bins to large bins @Shape: [] 
SmallBinToLargeBinRatio = data['SmallBinToLargeBinRatio']
# @Parameter MinimumSmallBins @Def: Minimum number of small bins @Shape: [] 
MinimumSmallBins = data['MinimumSmallBins']
# @Parameter MinimumLargeBins @Def: Minimum number of large bins @Shape: [] 
MinimumLargeBins = data['MinimumLargeBins']

# Variables 
# @Variable NumberSmallBins @Def: The number of small bins used @Shape: ['Integer'] 
NumberSmallBins = model.addVar(vtype=GRB.INTEGER, name="NumberSmallBins")
# @Variable NumberLargeBins @Def: The number of large bins used @Shape: ['Integer'] 
NumberLargeBins = model.addVar(lb=MinimumLargeBins, vtype=GRB.INTEGER, name="NumberLargeBins")

# Constraints 
# @Constraint Constr_1 @Def: The total number of workers used must not exceed TotalWorkers. This is calculated as WorkersPerSmallBin multiplied by the number of SmallBins plus WorkersPerLargeBin multiplied by the number of LargeBins.
model.addConstr(WorkersPerSmallBin * NumberSmallBins + WorkersPerLargeBin * NumberLargeBins <= TotalWorkers)
# @Constraint Constr_2 @Def: The number of SmallBins must be equal to SmallBinToLargeBinRatio times the number of LargeBins.
model.addConstr(NumberSmallBins == SmallBinToLargeBinRatio * NumberLargeBins)
# @Constraint Constr_3 @Def: The number of SmallBins must be at least MinimumSmallBins.
model.addConstr(NumberSmallBins >= MinimumSmallBins)
# @Constraint Constr_4 @Def: The number of LargeBins must be at least MinimumLargeBins.
model.addConstr(NumberLargeBins >= MinimumLargeBins, name="MinLargeBins")

# Objective 
# @Objective Objective @Def: Total recycling material collected is calculated as CapacitySmallBin multiplied by the number of SmallBins plus CapacityLargeBin multiplied by the number of LargeBins. The objective is to maximize the total recycling material collected.
model.setObjective(CapacitySmallBin * NumberSmallBins + CapacityLargeBin * NumberLargeBins, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSmallBins'] = NumberSmallBins.x
variables['NumberLargeBins'] = NumberLargeBins.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
