# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A florist transports small and large bouquets, where each small bouquet contains
FlowersPerSmallBouquet flowers and each large bouquet contains
FlowersPerLargeBouquet flowers. The florist can transport at most
MaxSmallBouquets small bouquets and MaxLargeBouquets large bouquets. In total,
the florist can transport at most MaxTotalBouquets bouquets. The florist must
transport at least MinLargeBouquets large bouquets. Additionally, the number of
small bouquets transported must be at least MinSmallToLargeRatio times the
number of large bouquets transported. The objective is to determine the number
of small and large bouquets to transport in order to maximize the total number
of flowers delivered to the stores.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/150/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FlowersPerSmallBouquet @Def: Number of flowers in a small bouquet @Shape: [] 
FlowersPerSmallBouquet = data['FlowersPerSmallBouquet']
# @Parameter FlowersPerLargeBouquet @Def: Number of flowers in a large bouquet @Shape: [] 
FlowersPerLargeBouquet = data['FlowersPerLargeBouquet']
# @Parameter MaxSmallBouquets @Def: Maximum number of small bouquets that can be transported @Shape: [] 
MaxSmallBouquets = data['MaxSmallBouquets']
# @Parameter MaxLargeBouquets @Def: Maximum number of large bouquets that can be transported @Shape: [] 
MaxLargeBouquets = data['MaxLargeBouquets']
# @Parameter MaxTotalBouquets @Def: Maximum total number of bouquets that can be transported @Shape: [] 
MaxTotalBouquets = data['MaxTotalBouquets']
# @Parameter MinLargeBouquets @Def: Minimum number of large bouquets that must be transported @Shape: [] 
MinLargeBouquets = data['MinLargeBouquets']
# @Parameter MinSmallToLargeRatio @Def: Minimum ratio of small bouquets to large bouquets @Shape: [] 
MinSmallToLargeRatio = data['MinSmallToLargeRatio']

# Variables 
# @Variable SmallBouquets @Def: The number of small bouquets transported @Shape: [] 
SmallBouquets = model.addVar(vtype=GRB.INTEGER, ub=MaxSmallBouquets, name="SmallBouquets")
# @Variable LargeBouquets @Def: The number of large bouquets transported @Shape: [] 
LargeBouquets = model.addVar(lb=MinLargeBouquets, ub=MaxLargeBouquets, vtype=GRB.INTEGER, name="LargeBouquets")

# Constraints 
# @Constraint Constr_1 @Def: The number of small bouquets transported cannot exceed MaxSmallBouquets.
model.addConstr(SmallBouquets <= MaxSmallBouquets)
# @Constraint Constr_2 @Def: The number of large bouquets transported cannot exceed MaxLargeBouquets.
model.addConstr(LargeBouquets <= MaxLargeBouquets)
# @Constraint Constr_3 @Def: The total number of bouquets transported cannot exceed MaxTotalBouquets.
model.addConstr(SmallBouquets + LargeBouquets <= MaxTotalBouquets)
# @Constraint Constr_4 @Def: At least MinLargeBouquets large bouquets must be transported.
model.addConstr(LargeBouquets >= MinLargeBouquets)
# @Constraint Constr_5 @Def: The number of small bouquets transported must be at least MinSmallToLargeRatio times the number of large bouquets transported.
model.addConstr(SmallBouquets >= MinSmallToLargeRatio * LargeBouquets)

# Objective 
# @Objective Objective @Def: The total number of flowers delivered is the sum of FlowersPerSmallBouquet multiplied by the number of small bouquets and FlowersPerLargeBouquet multiplied by the number of large bouquets. The objective is to maximize the total number of flowers delivered to the stores.
model.setObjective(FlowersPerSmallBouquet * SmallBouquets + FlowersPerLargeBouquet * LargeBouquets, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallBouquets'] = SmallBouquets.x
variables['LargeBouquets'] = LargeBouquets.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
