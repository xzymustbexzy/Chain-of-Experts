# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A railway company is planning the infrastructure for the city and is considering
two types of transportation, trains and trams. Each train can transport
TrainCapacity people per hour comfortably and each tram can transport
TramCapacity people per hour comfortably. Since trains take longer to build, the
number of trams must be at least MinTramsToTrainsRatio times the number of
trains. If the railway company wants to transport at least MinPeoplePerHour
people per hour, minimize the total number of transportation units required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/246/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TrainCapacity @Def: Number of people transported per train per hour @Shape: [] 
TrainCapacity = data['TrainCapacity']
# @Parameter TramCapacity @Def: Number of people transported per tram per hour @Shape: [] 
TramCapacity = data['TramCapacity']
# @Parameter MinTramsToTrainsRatio @Def: Minimum ratio of trams to trains @Shape: [] 
MinTramsToTrainsRatio = data['MinTramsToTrainsRatio']
# @Parameter MinPeoplePerHour @Def: Minimum number of people to transport per hour @Shape: [] 
MinPeoplePerHour = data['MinPeoplePerHour']

# Variables 
# @Variable NumberOfTrams @Def: The number of trams @Shape: ['Integer'] 
NumberOfTrams = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrams")
# @Variable NumberOfTrains @Def: The number of trains @Shape: ['Integer'] 
NumberOfTrains = model.addVar(vtype=GRB.INTEGER, name="NumberOfTrains")

# Constraints 
# @Constraint Constr_1 @Def: The number of trams must be at least MinTramsToTrainsRatio times the number of trains.
model.addConstr(NumberOfTrams >= MinTramsToTrainsRatio * NumberOfTrains)
# @Constraint Constr_2 @Def: The total number of people transported per hour by trains and trams must be at least MinPeoplePerHour.
model.addConstr(NumberOfTrains * TrainCapacity + NumberOfTrams * TramCapacity >= MinPeoplePerHour)

# Objective 
# @Objective Objective @Def: Minimize the total number of transportation units required.
model.setObjective(NumberOfTrams + NumberOfTrains, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfTrams'] = NumberOfTrams.x
variables['NumberOfTrains'] = NumberOfTrains.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
