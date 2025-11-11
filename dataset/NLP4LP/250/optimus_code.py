# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A taxi company selects quantities of NumVehicleTypes different vehicle types to
maximize the total Earnings per shift, subject to the total Pollution being
below PollutionCap, the total TransportCapacity being at least
MinTransportCapacity, and each vehicle type not exceeding its
MaxVehiclePercentage of the total number of vehicles.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/251/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumVehicleTypes @Def: Number of different vehicle types. @Shape: [] 
NumVehicleTypes = data['NumVehicleTypes']
# @Parameter TransportCapacity @Def: The number of people each vehicle type can transport per shift. @Shape: ['NumVehicleTypes'] 
TransportCapacity = data['TransportCapacity']
# @Parameter Pollution @Def: The units of pollution each vehicle type produces per shift. @Shape: ['NumVehicleTypes'] 
Pollution = data['Pollution']
# @Parameter Earnings @Def: The earnings the company makes per shift from each vehicle type. @Shape: ['NumVehicleTypes'] 
Earnings = data['Earnings']
# @Parameter MaxVehiclePercentage @Def: The maximum proportion of the total number of vehicles that can be of each vehicle type. @Shape: ['NumVehicleTypes'] 
MaxVehiclePercentage = data['MaxVehiclePercentage']
# @Parameter PollutionCap @Def: The maximum total units of pollution allowed per shift. @Shape: [] 
PollutionCap = data['PollutionCap']
# @Parameter MinTransportCapacity @Def: The minimum number of people that need to be transported per shift. @Shape: [] 
MinTransportCapacity = data['MinTransportCapacity']

# Variables 
# @Variable NumVehicles @Def: The number of vehicles of each type used per shift @Shape: ['NumVehicleTypes'] 
NumVehicles = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumVehicles")

# Constraints 
# @Constraint Constr_1 @Def: The total Pollution is below PollutionCap.
model.addConstr(quicksum(Pollution[i] * NumVehicles[i] for i in range(NumVehicleTypes)) <= PollutionCap)
# @Constraint Constr_2 @Def: The total TransportCapacity is at least MinTransportCapacity.
model.addConstr(quicksum(NumVehicles[i] * TransportCapacity[i] for i in range(NumVehicleTypes)) >= MinTransportCapacity)
# @Constraint Constr_3 @Def: Each vehicle type does not exceed its MaxVehiclePercentage of the total number of vehicles.
model.addConstrs(NumVehicles[i] <= MaxVehiclePercentage[i] * quicksum(NumVehicles[j] for j in range(NumVehicleTypes)) for i in range(NumVehicleTypes))

# Objective 
# @Objective Objective @Def: Maximize the total Earnings per shift.
model.setObjective(quicksum(Earnings[t] * NumVehicles[t] for t in range(NumVehicleTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumVehicles'] = model.getAttr("X", NumVehicles)
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
