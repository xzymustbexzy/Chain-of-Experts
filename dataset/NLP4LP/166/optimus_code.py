# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A farmer sends corn to the city by either tractor or car. A tractor can carry
TractorCapacity kilograms of corn while a car can carry CarCapacity kilograms of
corn. Since tractors are very slow, the number of cars used must be at least
MinimumCarMultiplier times the number of tractors used. If at least
MinimumCornToSend kilograms of corn need to be sent to the city, minimize the
total number of tractors and cars needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/167/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TractorCapacity @Def: Capacity of one tractor in kilograms @Shape: [] 
TractorCapacity = data['TractorCapacity']
# @Parameter CarCapacity @Def: Capacity of one car in kilograms @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter MinimumCarMultiplier @Def: Minimum multiplier for the number of cars relative to tractors @Shape: [] 
MinimumCarMultiplier = data['MinimumCarMultiplier']
# @Parameter MinimumCornToSend @Def: Minimum total amount of corn to send in kilograms @Shape: [] 
MinimumCornToSend = data['MinimumCornToSend']

# Variables 
# @Variable NumberOfCarsUsed @Def: The number of cars used @Shape: ['NonNegative', 'Integer'] 
NumberOfCarsUsed = model.addVar(vtype=GRB.INTEGER, name="NumberOfCarsUsed")
# @Variable NumberOfTractorsUsed @Def: The number of tractors used @Shape: ['NonNegative', 'Integer'] 
NumberOfTractorsUsed = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfTractorsUsed")
# @Variable CornTractor @Def: The amount of corn carried by tractors in kilograms @Shape: ['NonNegative'] 
CornTractor = model.addVar(vtype=GRB.CONTINUOUS, name="CornTractor")
# @Variable CornCar @Def: The amount of corn carried by cars in kilograms @Shape: ['NonNegative'] 
CornCar = model.addVar(vtype=GRB.CONTINUOUS, name="CornCar")

# Constraints 
# @Constraint Constr_1 @Def: The number of cars used must be at least MinimumCarMultiplier times the number of tractors used.
model.addConstr(NumberOfCarsUsed >= MinimumCarMultiplier * NumberOfTractorsUsed)
# @Constraint Constr_2 @Def: Each tractor can carry TractorCapacity kilograms of corn.
model.addConstr(CornTractor <= NumberOfTractorsUsed * TractorCapacity)
# @Constraint Constr_3 @Def: Each car can carry CarCapacity kilograms of corn.
model.addConstr(CornCar <= CarCapacity * NumberOfCarsUsed)
# @Constraint Constr_4 @Def: At least MinimumCornToSend kilograms of corn must be sent to the city.
model.addConstr(CornTractor + CornCar >= MinimumCornToSend)

# Objective 
# @Objective Objective @Def: Minimize the total number of tractors and cars needed.
model.setObjective(NumberOfCarsUsed + NumberOfTractorsUsed, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCarsUsed'] = NumberOfCarsUsed.x
variables['NumberOfTractorsUsed'] = NumberOfTractorsUsed.x
variables['CornTractor'] = CornTractor.x
variables['CornCar'] = CornCar.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
