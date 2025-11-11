# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A chemical company is transporting their hydrogen using NumTransportMethods
different transportation methods. Each method has a transport capacity per trip
given by TransportCapacity and a cost per trip given by TransportCost. The
company needs to transport at least MinimumHydrogen amount of hydrogen and has a
budget of Budget available. Additionally, the number of transports done by the
first transportation method must be less than the number of transports done by
the second transportation method. The company aims to determine the number of
each transportation method to minimize the total number of trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/179/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TransportCapacity @Def: Transport capacity per trip for each transportation method @Shape: ['NumTransportMethods'] 
TransportCapacity = data['TransportCapacity']
# @Parameter TransportCost @Def: Transport cost per trip for each transportation method @Shape: ['NumTransportMethods'] 
TransportCost = data['TransportCost']
# @Parameter MinimumHydrogen @Def: Minimum total hydrogen to transport @Shape: [] 
MinimumHydrogen = data['MinimumHydrogen']
# @Parameter Budget @Def: Available budget for transportation @Shape: [] 
Budget = data['Budget']
# @Parameter NumTransportMethods @Def: Number of transportation methods @Shape: [] 
NumTransportMethods = data['NumTransportMethods']

# Variables 
# @Variable NumTrips @Def: The number of trips for each transportation method @Shape: ['NumTransportMethods'] 
NumTrips = model.addVars(NumTransportMethods, vtype=GRB.INTEGER, name="NumTrips")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of hydrogen transported must be at least MinimumHydrogen.
model.addConstr(quicksum(TransportCapacity[i] * NumTrips[i] for i in range(NumTransportMethods)) >= MinimumHydrogen)
# @Constraint Constr_2 @Def: The total transportation cost must not exceed Budget.
model.addConstr(quicksum(TransportCost[i] * NumTrips[i] for i in range(NumTransportMethods)) <= Budget)
# @Constraint Constr_3 @Def: The number of transports done by the first transportation method must be less than the number of transports done by the second transportation method.
model.addConstr(NumTrips[0] <= NumTrips[1] - 1)

# Objective 
# @Objective Objective @Def: The total number of trips is the sum of the number of transports for each transportation method. The objective is to minimize the total number of trips.
model.setObjective(quicksum(NumTrips[i] for i in range(NumTransportMethods)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumTrips'] = model.getAttr("X", NumTrips)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
