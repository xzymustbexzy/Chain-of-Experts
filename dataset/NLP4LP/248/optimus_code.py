# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The airport can install escalators and elevators. Each escalator transports
TransportRateEscalator people per minute and requires SpaceEscalator units of
space. Each elevator transports TransportRateElevator people per minute and
requires SpaceElevator units of space. The airport must have a total transport
capacity of at least MinPeopleTransport people per minute. Additionally, the
number of escalators must be at least RatioEscalatorsToElevators times the
number of elevators, and at least MinElevators elevators must be installed. The
objective is to minimize the total space used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/249/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TransportRateEscalator @Def: Transport rate of an escalator in people per minute @Shape: [] 
TransportRateEscalator = data['TransportRateEscalator']
# @Parameter TransportRateElevator @Def: Transport rate of an elevator in people per minute @Shape: [] 
TransportRateElevator = data['TransportRateElevator']
# @Parameter SpaceEscalator @Def: Space taken by an escalator in units @Shape: [] 
SpaceEscalator = data['SpaceEscalator']
# @Parameter SpaceElevator @Def: Space taken by an elevator in units @Shape: [] 
SpaceElevator = data['SpaceElevator']
# @Parameter MinPeopleTransport @Def: Minimum number of people to transport per minute @Shape: [] 
MinPeopleTransport = data['MinPeopleTransport']
# @Parameter RatioEscalatorsToElevators @Def: Minimum ratio of escalators to elevators @Shape: [] 
RatioEscalatorsToElevators = data['RatioEscalatorsToElevators']
# @Parameter MinElevators @Def: Minimum number of elevators to be installed @Shape: [] 
MinElevators = data['MinElevators']

# Variables 
# @Variable NumberEscalators @Def: The number of escalators to install @Shape: ['Integer'] 
NumberEscalators = model.addVar(vtype=GRB.INTEGER, name="NumberEscalators")
# @Variable NumberElevators @Def: The number of elevators to install @Shape: ['Integer'] 
NumberElevators = model.addVar(vtype=GRB.INTEGER, name="NumberElevators", lb=MinElevators)

# Constraints 
# @Constraint Constr_1 @Def: The total transport capacity from escalators and elevators must be at least MinPeopleTransport people per minute.
model.addConstr(TransportRateEscalator * NumberEscalators + TransportRateElevator * NumberElevators >= MinPeopleTransport)
# @Constraint Constr_2 @Def: The number of escalators must be at least RatioEscalatorsToElevators times the number of elevators.
model.addConstr(NumberEscalators >= RatioEscalatorsToElevators * NumberElevators)
# @Constraint Constr_3 @Def: At least MinElevators elevators must be installed.
model.addConstr(NumberElevators >= MinElevators)

# Objective 
# @Objective Objective @Def: The total space used is the sum of the spaces required for all escalators and elevators. The objective is to minimize the total space used.
model.setObjective(NumberEscalators * SpaceEscalator + NumberElevators * SpaceElevator, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberEscalators'] = NumberEscalators.x
variables['NumberElevators'] = NumberElevators.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
