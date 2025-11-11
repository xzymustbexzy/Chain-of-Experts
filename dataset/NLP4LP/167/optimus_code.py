# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A village needs to transport at least NumberOfPeople individuals using bikes and
cars. Each bike has a capacity of BikeCapacity people, and each car has a
capacity of CarCapacity people. At most MaxCarPercentage of the total vehicles
can be cars. Determine the number of bikes and cars required to minimize the
total number of bikes needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/168/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BikeCapacity @Def: Number of people each bike can transport @Shape: [] 
BikeCapacity = data['BikeCapacity']
# @Parameter CarCapacity @Def: Number of people each car can transport @Shape: [] 
CarCapacity = data['CarCapacity']
# @Parameter MaxCarPercentage @Def: Maximum percentage of vehicles that can be cars @Shape: [] 
MaxCarPercentage = data['MaxCarPercentage']
# @Parameter NumberOfPeople @Def: Total number of people to transport @Shape: [] 
NumberOfPeople = data['NumberOfPeople']

# Variables 
# @Variable NumberOfBikes @Def: The number of bikes used for transportation @Shape: [] 
NumberOfBikes = model.addVar(vtype=GRB.INTEGER, name="NumberOfBikes")
# @Variable NumberOfCars @Def: The number of cars used for transportation @Shape: [] 
NumberOfCars = model.addVar(vtype=GRB.INTEGER, name="NumberOfCars")

# Constraints 
# @Constraint Constr_1 @Def: The total number of people transported by bikes and cars must be at least NumberOfPeople.
model.addConstr(NumberOfBikes * BikeCapacity + NumberOfCars * CarCapacity >= NumberOfPeople)
# @Constraint Constr_2 @Def: The number of cars used cannot exceed MaxCarPercentage of the total number of vehicles.
model.addConstr(NumberOfCars <= MaxCarPercentage * (NumberOfCars + NumberOfBikes))

# Objective 
# @Objective Objective @Def: Minimize the total number of bikes needed.
model.setObjective(NumberOfBikes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBikes'] = NumberOfBikes.x
variables['NumberOfCars'] = NumberOfCars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
