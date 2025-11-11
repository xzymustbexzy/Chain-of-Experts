# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Both subsoil and topsoil need to be added to a garden bed. The objective is to
minimize the total amount of water required to hydrate the garden bed, where
each bag of subsoil requires WaterSubsoil units of water per day and each bag of
topsoil requires WaterTopsoil units of water per day. The total number of bags
of subsoil and topsoil combined must not exceed MaxTotalBags. Additionally, at
least MinTopsoilBags bags of topsoil must be used, and the proportion of topsoil
bags must not exceed MaxTopsoilProportion of all bags.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/217/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter WaterSubsoil @Def: Amount of water required to hydrate one bag of subsoil per day @Shape: [] 
WaterSubsoil = data['WaterSubsoil']
# @Parameter WaterTopsoil @Def: Amount of water required to hydrate one bag of topsoil per day @Shape: [] 
WaterTopsoil = data['WaterTopsoil']
# @Parameter MaxTotalBags @Def: Maximum number of bags of topsoil and subsoil combined @Shape: [] 
MaxTotalBags = data['MaxTotalBags']
# @Parameter MinTopsoilBags @Def: Minimum number of topsoil bags to be used @Shape: [] 
MinTopsoilBags = data['MinTopsoilBags']
# @Parameter MaxTopsoilProportion @Def: Maximum proportion of bags that can be topsoil @Shape: [] 
MaxTopsoilProportion = data['MaxTopsoilProportion']

# Variables 
# @Variable SubsoilBags @Def: The number of subsoil bags @Shape: [] 
SubsoilBags = model.addVar(vtype=GRB.INTEGER, name="SubsoilBags")
# @Variable TopsoilBags @Def: The number of topsoil bags @Shape: [] 
TopsoilBags = model.addVar(vtype=GRB.INTEGER, name="TopsoilBags")

# Constraints 
# @Constraint Constr_1 @Def: The total number of subsoil and topsoil bags combined must not exceed MaxTotalBags.
model.addConstr(SubsoilBags + TopsoilBags <= MaxTotalBags)
# @Constraint Constr_2 @Def: At least MinTopsoilBags bags of topsoil must be used.
model.addConstr(TopsoilBags >= MinTopsoilBags)
# @Constraint Constr_3 @Def: The proportion of topsoil bags must not exceed MaxTopsoilProportion of all bags.
model.addConstr(TopsoilBags <= MaxTopsoilProportion * (TopsoilBags + SubsoilBags))

# Objective 
# @Objective Objective @Def: Total water required is the sum of (WaterSubsoil * number of subsoil bags) and (WaterTopsoil * number of topsoil bags). The objective is to minimize the total water required.
model.setObjective(WaterSubsoil * SubsoilBags + WaterTopsoil * TopsoilBags, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SubsoilBags'] = SubsoilBags.x
variables['TopsoilBags'] = TopsoilBags.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
