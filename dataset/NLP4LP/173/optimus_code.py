# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A factory transports rice using medium and large horse-drawn carts. Each medium
sized cart requires HorsesPerMediumCart horses and can carry CapacityMediumCart
kilograms of rice. Each large sized cart requires HorsesPerLargeCart horses and
can carry CapacityLargeCart kilograms of rice. The factory has
TotalHorsesAvailable horses available. The number of medium sized carts must be
MediumToLargeCartRatio times the number of large sized carts. Additionally,
there must be at least MinMediumCarts medium sized carts and at least
MinLargeCarts large sized carts. Determine the number of medium and large sized
carts to maximize the total amount of rice transported.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/174/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalHorsesAvailable @Def: Total number of horses available for transportation @Shape: [] 
TotalHorsesAvailable = data['TotalHorsesAvailable']
# @Parameter HorsesPerMediumCart @Def: Number of horses required to operate one medium sized cart @Shape: [] 
HorsesPerMediumCart = data['HorsesPerMediumCart']
# @Parameter HorsesPerLargeCart @Def: Number of horses required to operate one large sized cart @Shape: [] 
HorsesPerLargeCart = data['HorsesPerLargeCart']
# @Parameter CapacityMediumCart @Def: Rice carrying capacity of one medium sized cart in kilograms @Shape: [] 
CapacityMediumCart = data['CapacityMediumCart']
# @Parameter CapacityLargeCart @Def: Rice carrying capacity of one large sized cart in kilograms @Shape: [] 
CapacityLargeCart = data['CapacityLargeCart']
# @Parameter MediumToLargeCartRatio @Def: Required ratio of medium sized carts to large sized carts @Shape: [] 
MediumToLargeCartRatio = data['MediumToLargeCartRatio']
# @Parameter MinMediumCarts @Def: Minimum number of medium sized carts required @Shape: [] 
MinMediumCarts = data['MinMediumCarts']
# @Parameter MinLargeCarts @Def: Minimum number of large sized carts required @Shape: [] 
MinLargeCarts = data['MinLargeCarts']

# Variables 
# @Variable NumberMediumCarts @Def: The number of medium sized carts used @Shape: ['Integer'] 
NumberMediumCarts = model.addVar(vtype=GRB.INTEGER, name="NumberMediumCarts")
# @Variable NumberLargeCarts @Def: The number of large sized carts used @Shape: ['Integer'] 
NumberLargeCarts = model.addVar(vtype=GRB.INTEGER, lb=MinLargeCarts, name="NumberLargeCarts")

# Constraints 
# @Constraint Constr_1 @Def: The total number of horses used by medium and large sized carts does not exceed TotalHorsesAvailable.
model.addConstr(HorsesPerMediumCart * NumberMediumCarts + HorsesPerLargeCart * NumberLargeCarts <= TotalHorsesAvailable)
# @Constraint Constr_2 @Def: The number of medium sized carts must be MediumToLargeCartRatio times the number of large sized carts.
model.addConstr(NumberMediumCarts == MediumToLargeCartRatio * NumberLargeCarts)
# @Constraint Constr_3 @Def: There must be at least MinMediumCarts medium sized carts.
model.addConstr(NumberMediumCarts >= MinMediumCarts)
# @Constraint Constr_4 @Def: There must be at least MinLargeCarts large sized carts.
model.addConstr(NumberLargeCarts >= MinLargeCarts)

# Objective 
# @Objective Objective @Def: Maximize the total amount of rice transported by the medium and large sized carts.
model.setObjective(NumberMediumCarts * CapacityMediumCart + NumberLargeCarts * CapacityLargeCart, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberMediumCarts'] = NumberMediumCarts.x
variables['NumberLargeCarts'] = NumberLargeCarts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
