# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
At least MinLocals locals must be transported across a lake using kayaks and
motorboats. Kayaks can transport KayakCapacity people per trip and take
KayakTime minutes per trip, while motorboats can transport MotorboatCapacity
people per trip and take MotorboatTime minutes per trip. The number of motorboat
trips is limited to at most MaxMotorboatTrips, and at least
MinKayakTripPercentage of the total trips must be by kayak. The objective is to
minimize the total transportation time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/252/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinLocals @Def: Minimum number of locals to transport @Shape: [] 
MinLocals = data['MinLocals']
# @Parameter KayakCapacity @Def: Number of people a kayak can transport per trip @Shape: [] 
KayakCapacity = data['KayakCapacity']
# @Parameter MotorboatCapacity @Def: Number of people a motorboat can transport per trip @Shape: [] 
MotorboatCapacity = data['MotorboatCapacity']
# @Parameter KayakTime @Def: Time in minutes a kayak takes per trip @Shape: [] 
KayakTime = data['KayakTime']
# @Parameter MotorboatTime @Def: Time in minutes a motorboat takes per trip @Shape: [] 
MotorboatTime = data['MotorboatTime']
# @Parameter MaxMotorboatTrips @Def: Maximum number of motorboat trips allowed @Shape: [] 
MaxMotorboatTrips = data['MaxMotorboatTrips']
# @Parameter MinKayakTripPercentage @Def: Minimum percentage of trips that must be by kayak @Shape: [] 
MinKayakTripPercentage = data['MinKayakTripPercentage']

# Variables 
# @Variable KayakTrips @Def: The number of kayak trips @Shape: ['integer'] 
KayakTrips = model.addVar(vtype=GRB.INTEGER, name="KayakTrips")
# @Variable MotorboatTrips @Def: The number of motorboat trips @Shape: ['integer'] 
MotorboatTrips = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxMotorboatTrips, name="MotorboatTrips")

# Constraints 
# @Constraint Constr_1 @Def: Ensure that at least MinLocals individuals are transported across the lake using kayaks and motorboats.
model.addConstr(KayakCapacity * KayakTrips + MotorboatCapacity * MotorboatTrips >= MinLocals)
# @Constraint Constr_2 @Def: The number of motorboat trips must not exceed MaxMotorboatTrips.
model.addConstr(MotorboatTrips <= MaxMotorboatTrips)
# @Constraint Constr_3 @Def: At least MinKayakTripPercentage of the total trips must be conducted by kayak.
model.addConstr(KayakTrips >= MinKayakTripPercentage * (KayakTrips + MotorboatTrips))

# Objective 
# @Objective Objective @Def: Minimize the total transportation time, which is the sum of the time taken by all kayak trips and motorboat trips.
model.setObjective(KayakTime * KayakTrips + MotorboatTime * MotorboatTrips, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['KayakTrips'] = KayakTrips.x
variables['MotorboatTrips'] = MotorboatTrips.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
