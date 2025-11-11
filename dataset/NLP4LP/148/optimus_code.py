# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company utilizes NumVehicleTypes different vehicle types to transport patties.
Each vehicle type i has a Capacity[i] capacity for patties and incurs a
CostPerTrip[i] cost per trip. The number of vehicles of one type must not exceed
the number of vehicles of another type. The company must transport at least
MinPatties patties while staying within a Budget. The objective is to minimize
the total number of trips.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/149/parameters.json", "r") as f:
    data = json.load(f)
        
# @Def: definition of a target
# @Shape: shape of a target
            
# Parameters 
# @Parameter NumVehicleTypes @Def: Number of vehicle types @Shape: [] 
NumVehicleTypes = data['NumVehicleTypes']
# @Parameter Capacity @Def: Capacity of each vehicle type in number of patties @Shape: ['NumVehicleTypes'] 
Capacity = data['Capacity']
# @Parameter CostPerTrip @Def: Cost per trip for each vehicle type @Shape: ['NumVehicleTypes'] 
CostPerTrip = data['CostPerTrip']
# @Parameter MinPatties @Def: Minimum number of patties to be shipped @Shape: [] 
MinPatties = data['MinPatties']
# @Parameter Budget @Def: Budget for shipping @Shape: [] 
Budget = data['Budget']
    
# Variables 
# @Variable NumTrips @Def: The number of trips for each vehicle type @Shape: ['NumVehicleTypes'] 
NumTrips = model.addVars(NumVehicleTypes, vtype=GRB.INTEGER, name="NumTrips")
# @Variable NumVehicles @Def: The number of vehicles for each vehicle type @Shape: ['NumVehicleTypes'] 
NumVehicles = model.addVars(range(NumVehicleTypes), vtype=GRB.INTEGER, name="NumVehicles")
    
# Constraints 
# @Constraint Constr_1 @Def: At least MinPatties patties must be transported.
model.addConstr(quicksum(Capacity[i] * NumTrips[i] for i in range(NumVehicleTypes)) >= MinPatties)
# @Constraint Constr_2 @Def: The total cost of all trips must not exceed the Budget.
model.addConstr(quicksum(NumTrips[i] * CostPerTrip[i] for i in range(NumVehicleTypes)) <= Budget)
# @Constraint Constr_3 @Def: The number of vehicles of one vehicle type must not exceed the number of vehicles of another vehicle type.
for i in range(NumVehicleTypes):
    for j in range(NumVehicleTypes):
        if i != j:
            model.addConstr(NumVehicles[i] <= NumVehicles[j], name=f"Vehicles_Constraint_{i}_{j}")
    
# Objective 
# @Objective Objective @Def: Minimize the total number of trips required to transport the patties.
model.setObjective(quicksum(NumTrips[i] for i in range(NumVehicleTypes)), GRB.MINIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumTrips'] = {i: NumTrips[i].x for i in range(NumVehicleTypes)}
variables['NumVehicles'] = {i: NumVehicles[i].x for i in range(NumVehicleTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
