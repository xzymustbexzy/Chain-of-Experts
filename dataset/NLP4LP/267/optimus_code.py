# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A tourism company can purchase sedans and buses. Each sedan seats SedanCapacity
tourists per day and produces SedanPollution units of pollution per day. Each
bus seats BusCapacity tourists per day and produces BusPollution units of
pollution per day. The company is limited to a maximum of MaxPollution units of
pollution per day. To be profitable, the company must serve at least
MinCustomers customers per day. The goal is to determine the number of sedans
and buses to purchase in order to minimize the total number of vehicles needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/268/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SedanCapacity @Def: Number of tourists that a sedan can seat per day @Shape: [] 
SedanCapacity = data['SedanCapacity']
# @Parameter SedanPollution @Def: Units of pollution resulting from one sedan per day @Shape: [] 
SedanPollution = data['SedanPollution']
# @Parameter BusCapacity @Def: Number of tourists that a bus can seat per day @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter BusPollution @Def: Units of pollution resulting from one bus per day @Shape: [] 
BusPollution = data['BusPollution']
# @Parameter MaxPollution @Def: Maximum units of pollution allowed per day @Shape: [] 
MaxPollution = data['MaxPollution']
# @Parameter MinCustomers @Def: Minimum number of customers required per day @Shape: [] 
MinCustomers = data['MinCustomers']

# Variables 
# @Variable NumberOfSedans @Def: The number of sedans used per day @Shape: [] 
NumberOfSedans = model.addVar(vtype=GRB.INTEGER, name="NumberOfSedans")
# @Variable NumberOfBuses @Def: The number of buses used per day @Shape: [] 
NumberOfBuses = model.addVar(vtype=GRB.INTEGER, name="NumberOfBuses")

# Constraints 
# @Constraint Constr_1 @Def: The total pollution produced by the vehicles cannot exceed MaxPollution units per day. This is calculated as SedanPollution multiplied by the number of sedans plus BusPollution multiplied by the number of buses.
model.addConstr(SedanPollution * NumberOfSedans + BusPollution * NumberOfBuses <= MaxPollution)
# @Constraint Constr_2 @Def: The company must serve at least MinCustomers customers per day. This is achieved by ensuring that SedanCapacity multiplied by the number of sedans plus BusCapacity multiplied by the number of buses is at least MinCustomers.
model.addConstr(SedanCapacity * NumberOfSedans + BusCapacity * NumberOfBuses >= MinCustomers)

# Objective 
# @Objective Objective @Def: Minimize the total number of vehicles needed, which is the sum of the number of sedans and the number of buses purchased.
model.setObjective(NumberOfSedans + NumberOfBuses, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSedans'] = NumberOfSedans.x
variables['NumberOfBuses'] = NumberOfBuses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
