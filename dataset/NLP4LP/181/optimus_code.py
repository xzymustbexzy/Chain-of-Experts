# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
There has been an accident and patients need to be transported to the hospital
by either helicopter or bus. A helicopter can transport HelicopterCapacity
patients per trip and takes HelicopterTripTime time. On the other hand, a bus
can transport BusCapacity patients per trip and takes BusTripTime time. At least
MinPatients patients need to be transported and at least
MinHelicopterTripPercentage of the trips should be by helicopter. In addition,
there can be at most MaxBusTrips bus trips. The objective is to minimize the
total transportation time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/182/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HelicopterCapacity @Def: Number of patients that can be transported by helicopter in one trip @Shape: [] 
HelicopterCapacity = data['HelicopterCapacity']
# @Parameter HelicopterTripTime @Def: Time taken for one helicopter trip @Shape: [] 
HelicopterTripTime = data['HelicopterTripTime']
# @Parameter BusCapacity @Def: Number of patients that can be transported by bus in one trip @Shape: [] 
BusCapacity = data['BusCapacity']
# @Parameter BusTripTime @Def: Time taken for one bus trip @Shape: [] 
BusTripTime = data['BusTripTime']
# @Parameter MinPatients @Def: Minimum number of patients that need to be transported @Shape: [] 
MinPatients = data['MinPatients']
# @Parameter MinHelicopterTripPercentage @Def: Minimum percentage of trips that should be by helicopter @Shape: [] 
MinHelicopterTripPercentage = data['MinHelicopterTripPercentage']
# @Parameter MaxBusTrips @Def: Maximum number of bus trips allowed @Shape: [] 
MaxBusTrips = data['MaxBusTrips']

# Variables 
# @Variable HelicopterTrips @Def: The number of helicopter trips @Shape: [] 
HelicopterTrips = model.addVar(vtype=GRB.INTEGER, name="HelicopterTrips")
# @Variable BusTrips @Def: The number of bus trips @Shape: [] 
BusTrips = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxBusTrips, name="BusTrips")
# @Variable PatientsHelicopter @Def: The number of patients transported by helicopter @Shape: [] 
PatientsHelicopter = model.addVar(vtype=GRB.INTEGER, name="PatientsHelicopter")
# @Variable PatientsBus @Def: The number of patients transported by bus @Shape: [] 
PatientsBus = model.addVar(vtype=GRB.INTEGER, name="PatientsBus")

# Constraints 
# @Constraint Constr_1 @Def: At least MinPatients patients need to be transported.
model.addConstr(HelicopterTrips * HelicopterCapacity + BusTrips * BusCapacity >= MinPatients)
# @Constraint Constr_2 @Def: At least MinHelicopterTripPercentage of the trips should be by helicopter.
model.addConstr(HelicopterTrips >= MinHelicopterTripPercentage * (HelicopterTrips + BusTrips))
# @Constraint Constr_3 @Def: At most MaxBusTrips bus trips are allowed.
model.addConstr(BusTrips <= MaxBusTrips)
# @Constraint Constr_4 @Def: Each helicopter trip can transport up to HelicopterCapacity patients.
model.addConstr(PatientsHelicopter <= HelicopterCapacity * HelicopterTrips)
# @Constraint Constr_5 @Def: Each bus trip can transport up to BusCapacity patients.
model.addConstr(PatientsBus <= BusCapacity * BusTrips)

# Objective 
# @Objective Objective @Def: Minimize the total transportation time.
model.setObjective(HelicopterTrips * HelicopterTripTime + BusTrips * BusTripTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['HelicopterTrips'] = HelicopterTrips.x
variables['BusTrips'] = BusTrips.x
variables['PatientsHelicopter'] = PatientsHelicopter.x
variables['PatientsBus'] = PatientsBus.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
