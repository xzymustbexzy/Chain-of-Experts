# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of large bags (L) and tiny bags (T) such that
LargeBagEnergy * L + TinyBagEnergy * T ≤ TotalEnergy, L = RatioLargeToTiny * T,
and T ≥ MinTinyBags. The goal is to maximize the total grain weight, which is
LargeBagCapacity * L + TinyBagCapacity * T.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/244/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter LargeBagCapacity @Def: The capacity of a large bag in kilograms @Shape: [] 
LargeBagCapacity = data['LargeBagCapacity']
# @Parameter LargeBagEnergy @Def: The energy required to transport a large bag @Shape: [] 
LargeBagEnergy = data['LargeBagEnergy']
# @Parameter TinyBagCapacity @Def: The capacity of a tiny bag in kilograms @Shape: [] 
TinyBagCapacity = data['TinyBagCapacity']
# @Parameter TinyBagEnergy @Def: The energy required to transport a tiny bag @Shape: [] 
TinyBagEnergy = data['TinyBagEnergy']
# @Parameter TotalEnergy @Def: Total available energy for distribution @Shape: [] 
TotalEnergy = data['TotalEnergy']
# @Parameter RatioLargeToTiny @Def: The ratio of large bags to tiny bags @Shape: [] 
RatioLargeToTiny = data['RatioLargeToTiny']
# @Parameter MinTinyBags @Def: Minimum number of tiny bags required @Shape: [] 
MinTinyBags = data['MinTinyBags']

# Variables 
# @Variable LargeBags @Def: The number of large bags to transport @Shape: [] 
LargeBags = model.addVar(vtype=GRB.INTEGER, name="LargeBags")
# @Variable TinyBags @Def: The number of tiny bags to transport @Shape: [] 
TinyBags = model.addVar(vtype=GRB.INTEGER, name="TinyBags")

# Constraints 
# @Constraint Constr_1 @Def: LargeBagEnergy * L + TinyBagEnergy * T must be less than or equal to TotalEnergy.
model.addConstr(LargeBagEnergy * LargeBags + TinyBagEnergy * TinyBags <= TotalEnergy)
# @Constraint Constr_2 @Def: L must be equal to RatioLargeToTiny multiplied by T.
model.addConstr(LargeBags == RatioLargeToTiny * TinyBags)
# @Constraint Constr_3 @Def: T must be greater than or equal to MinTinyBags.
model.addConstr(TinyBags >= MinTinyBags)

# Objective 
# @Objective Objective @Def: Maximize the total grain weight, which is LargeBagCapacity * L + TinyBagCapacity * T.
model.setObjective(LargeBagCapacity * LargeBags + TinyBagCapacity * TinyBags, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LargeBags'] = LargeBags.x
variables['TinyBags'] = TinyBags.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
