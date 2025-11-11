# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A concert organizer must determine the optimal number of carts and trolleys to
minimize the total number of workers. Each cart transports equipment at a rate
of CartTransportRate kilograms per minute and requires CartWorkersRequired
workers. Each trolley transports equipment at a rate of TrolleyTransportRate
kilograms per minute and requires TrolleyWorkersRequired workers. The total
transportation must meet or exceed the DeliveryRate kilograms per minute.
Additionally, the number of trolleys used must be at least MinTrolleys, and the
transportation rate using trolleys must not exceed MaxTrolleyTransportPercentage
of the total transportation rate.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/216/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CartTransportRate @Def: Equipment transport rate of carts in kilograms per minute @Shape: [] 
CartTransportRate = data['CartTransportRate']
# @Parameter CartWorkersRequired @Def: Number of workers required per cart @Shape: [] 
CartWorkersRequired = data['CartWorkersRequired']
# @Parameter TrolleyTransportRate @Def: Equipment transport rate of trolleys in kilograms per minute @Shape: [] 
TrolleyTransportRate = data['TrolleyTransportRate']
# @Parameter TrolleyWorkersRequired @Def: Number of workers required per trolley @Shape: [] 
TrolleyWorkersRequired = data['TrolleyWorkersRequired']
# @Parameter MinTrolleys @Def: Minimum number of trolleys to be used @Shape: [] 
MinTrolleys = data['MinTrolleys']
# @Parameter MaxTrolleyTransportPercentage @Def: Maximum percentage of transportation that can use trolleys @Shape: [] 
MaxTrolleyTransportPercentage = data['MaxTrolleyTransportPercentage']
# @Parameter DeliveryRate @Def: Delivery rate of equipment in kilograms per minute @Shape: [] 
DeliveryRate = data['DeliveryRate']

# Variables 
# @Variable NumberOfCarts @Def: The number of carts used @Shape: [] 
NumberOfCarts = model.addVar(vtype=GRB.INTEGER, name="NumberOfCarts")
# @Variable NumberOfTrolleys @Def: The number of trolleys used @Shape: [] 
NumberOfTrolleys = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrolleys")

# Constraints 
# @Constraint Constr_1 @Def: The total transportation rate must be at least DeliveryRate kilograms per minute.
model.addConstr(NumberOfCarts * CartTransportRate + NumberOfTrolleys * TrolleyTransportRate >= DeliveryRate)
# @Constraint Constr_2 @Def: The number of trolleys used must be at least MinTrolleys.
model.addConstr(NumberOfTrolleys >= MinTrolleys)
# @Constraint Constr_3 @Def: The transportation rate using trolleys must not exceed MaxTrolleyTransportPercentage of the total transportation rate.
model.addConstr(NumberOfTrolleys * TrolleyTransportRate <= MaxTrolleyTransportPercentage * (NumberOfCarts * CartTransportRate + NumberOfTrolleys * TrolleyTransportRate))

# Objective 
# @Objective Objective @Def: Minimize the total number of workers, which is the sum of CartWorkersRequired workers for each cart and TrolleyWorkersRequired workers for each trolley.
model.setObjective(CartWorkersRequired * NumberOfCarts + TrolleyWorkersRequired * NumberOfTrolleys, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCarts'] = NumberOfCarts.x
variables['NumberOfTrolleys'] = NumberOfTrolleys.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
