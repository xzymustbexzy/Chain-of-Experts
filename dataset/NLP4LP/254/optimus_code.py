# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A venue needs to transport guests using two types of carts: golf carts and pull
carts. Each golf cart has a capacity of GolfCartCapacity guests, and each pull
cart has a capacity of PullCartCapacity guests. Due to space constraints, no
more than MaxGolfCartPercentage of the total carts can be golf carts. The venue
must transport at least MinGuests guests. The goal is to determine the number of
golf carts and pull carts to use in order to minimize the total number of carts
required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/255/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GolfCartCapacity @Def: Capacity of a golf cart @Shape: [] 
GolfCartCapacity = data['GolfCartCapacity']
# @Parameter PullCartCapacity @Def: Capacity of a pull cart @Shape: [] 
PullCartCapacity = data['PullCartCapacity']
# @Parameter MaxGolfCartPercentage @Def: Maximum percentage of carts that can be golf carts @Shape: [] 
MaxGolfCartPercentage = data['MaxGolfCartPercentage']
# @Parameter MinGuests @Def: Minimum number of guests to transport @Shape: [] 
MinGuests = data['MinGuests']

# Variables 
# @Variable NumGolfCarts @Def: The number of golf carts @Shape: ['Integer'] 
NumGolfCarts = model.addVar(vtype=GRB.INTEGER, name="NumGolfCarts")
# @Variable NumPullCarts @Def: The number of pull carts @Shape: ['Integer'] 
NumPullCarts = model.addVar(vtype=GRB.INTEGER, name="NumPullCarts")

# Constraints 
# @Constraint Constr_1 @Def: Each golf cart can transport GolfCartCapacity guests and each pull cart can transport PullCartCapacity guests. The total number of guests transported must be at least MinGuests.
model.addConstr(GolfCartCapacity * NumGolfCarts + PullCartCapacity * NumPullCarts >= MinGuests)
# @Constraint Constr_2 @Def: No more than MaxGolfCartPercentage of the total number of carts can be golf carts.
model.addConstr(NumGolfCarts <= MaxGolfCartPercentage * (NumGolfCarts + NumPullCarts))

# Objective 
# @Objective Objective @Def: Minimize the total number of carts required.
model.setObjective(NumGolfCarts + NumPullCarts, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumGolfCarts'] = NumGolfCarts.x
variables['NumPullCarts'] = NumPullCarts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
