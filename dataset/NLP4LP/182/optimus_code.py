# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Employees have the option of using Car or Bus for transportation. A Car can
carry CarCapacity employees and produces CarPollution units of pollution, while
a Bus can carry BusCapacity employees and produces BusPollution units of
pollution. At least MinEmployeesToTransport employees must be transported, and
no more than MaxBuses Buses can be used. The objective is to minimize the total
pollution produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/183/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CarCapacity @Def: The number of employees that a car can take @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter CarPollution @Def: The pollution produced by a car @Shape: [] 
CarPollution = data['CarPollution']
# @Parameter BusCapacity @Def: The number of employees that a bus can take @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter BusPollution @Def: The pollution produced by a bus @Shape: [] 
BusPollution = data['BusPollution']
# @Parameter MinEmployeesToTransport @Def: The minimum number of employees that need to be transported @Shape: [] 
MinEmployeesToTransport = data['MinEmployeesToTransport']
# @Parameter MaxBuses @Def: The maximum number of buses that can be used @Shape: [] 
MaxBuses = data['MaxBuses']

# Variables 
# @Variable xCars @Def: The number of cars used for transportation @Shape: ['Integer'] 
xCars = model.addVar(vtype=GRB.INTEGER, name="xCars")
# @Variable xBuses @Def: The number of buses used for transportation @Shape: ['Integer'] 
xBuses = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxBuses, name="xBuses")

# Constraints 
# @Constraint Constr_1 @Def: At least MinEmployeesToTransport employees must be transported.
model.addConstr(xCars * CarCapacity + xBuses * BusCapacity >= MinEmployeesToTransport)
# @Constraint Constr_2 @Def: No more than MaxBuses buses can be used.


# Objective 
# @Objective Objective @Def: Total pollution produced is the sum of pollution from cars and buses. The objective is to minimize the total pollution produced.
model.setObjective(xCars * CarPollution + xBuses * BusPollution, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['xCars'] = xCars.x
variables['xBuses'] = xBuses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
