# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A delivery person can schedule shifts on either bike or scooter. Each bike shift
delivers OrdersPerBikeShift orders, consumes EnergyPerBikeShift units of energy,
and receives TipsPerBikeShift in tips. Each scooter shift delivers
OrdersPerScooterShift orders, consumes EnergyPerScooterShift units of energy,
and receives TipsPerScooterShift in tips. The delivery person has TotalShifts
available per month, TotalEnergy units of energy, must deliver at least
MinOrders orders, and must schedule at least MinShiftsScooter shifts on a
scooter. The goal is to maximize the total tips received.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/226/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalShifts @Def: Total number of shifts available per month @Shape: [] 
TotalShifts = data['TotalShifts']
# @Parameter TotalEnergy @Def: Total units of energy available per month @Shape: [] 
TotalEnergy = data['TotalEnergy']
# @Parameter MinOrders @Def: Minimum number of orders to deliver @Shape: [] 
MinOrders = data['MinOrders']
# @Parameter MinShiftsScooter @Def: Minimum number of shifts on a scooter @Shape: [] 
MinShiftsScooter = data['MinShiftsScooter']
# @Parameter OrdersPerBikeShift @Def: Number of orders delivered per bike shift @Shape: [] 
OrdersPerBikeShift = data['OrdersPerBikeShift']
# @Parameter EnergyPerBikeShift @Def: Units of energy consumed per bike shift @Shape: [] 
EnergyPerBikeShift = data['EnergyPerBikeShift']
# @Parameter TipsPerBikeShift @Def: Tips received per bike shift @Shape: [] 
TipsPerBikeShift = data['TipsPerBikeShift']
# @Parameter OrdersPerScooterShift @Def: Number of orders delivered per scooter shift @Shape: [] 
OrdersPerScooterShift = data['OrdersPerScooterShift']
# @Parameter EnergyPerScooterShift @Def: Units of energy consumed per scooter shift @Shape: [] 
EnergyPerScooterShift = data['EnergyPerScooterShift']
# @Parameter TipsPerScooterShift @Def: Tips received per scooter shift @Shape: [] 
TipsPerScooterShift = data['TipsPerScooterShift']

# Variables 
# @Variable BikeShifts @Def: The number of bike shifts scheduled @Shape: [] 
BikeShifts = model.addVar(vtype=GRB.INTEGER, name="BikeShifts")
# @Variable ScooterShifts @Def: The number of scooter shifts scheduled @Shape: [] 
ScooterShifts = model.addVar(vtype=GRB.INTEGER, name="ScooterShifts")

# Constraints 
# @Constraint Constr_1 @Def: The total number of bike and scooter shifts scheduled cannot exceed the TotalShifts available per month.
model.addConstr(BikeShifts + ScooterShifts <= TotalShifts)
# @Constraint Constr_2 @Def: The total energy consumed by all shifts cannot exceed TotalEnergy units.
model.addConstr(EnergyPerBikeShift * BikeShifts + EnergyPerScooterShift * ScooterShifts <= TotalEnergy)
# @Constraint Constr_3 @Def: The total number of orders delivered must be at least MinOrders.
model.addConstr(BikeShifts * OrdersPerBikeShift + ScooterShifts * OrdersPerScooterShift >= MinOrders)
# @Constraint Constr_4 @Def: At least MinShiftsScooter shifts must be scheduled on a scooter.
model.addConstr(ScooterShifts >= MinShiftsScooter)

# Objective 
# @Objective Objective @Def: The total tips received is the sum of the tips from all bike and scooter shifts. The objective is to maximize the total tips received.
model.setObjective(TipsPerBikeShift * BikeShifts + TipsPerScooterShift * ScooterShifts, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BikeShifts'] = BikeShifts.x
variables['ScooterShifts'] = ScooterShifts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
