# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient can be connected to two machines, Machine1 and Machine2, for certain
durations. Machine1 delivers Machine1HeartDeliveryRate units of medicine to the
heart per minute and Machine1BrainDeliveryRate units to the brain per minute,
while producing Machine1WasteRate units of waste per minute. Machine2 delivers
Machine2HeartDeliveryRate units of medicine to the heart per minute and
Machine2BrainDeliveryRate units to the brain per minute, while producing
Machine2WasteRate units of waste per minute. The total medicine delivered to the
heart must not exceed HeartMedicineMax units, and the total medicine delivered
to the brain must be at least BrainMedicineMin units. Determine the operating
time for each machine to minimize the total waste produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/110/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter Machine1HeartDeliveryRate @Def: Units of medicine delivered to the heart per minute by machine 1 @Shape: [] 
Machine1HeartDeliveryRate = data['Machine1HeartDeliveryRate']
# @Parameter Machine1BrainDeliveryRate @Def: Units of medicine delivered to the brain per minute by machine 1 @Shape: [] 
Machine1BrainDeliveryRate = data['Machine1BrainDeliveryRate']
# @Parameter Machine1WasteRate @Def: Units of waste produced per minute by machine 1 @Shape: [] 
Machine1WasteRate = data['Machine1WasteRate']
# @Parameter Machine2HeartDeliveryRate @Def: Units of medicine delivered to the heart per minute by machine 2 @Shape: [] 
Machine2HeartDeliveryRate = data['Machine2HeartDeliveryRate']
# @Parameter Machine2BrainDeliveryRate @Def: Units of medicine delivered to the brain per minute by machine 2 @Shape: [] 
Machine2BrainDeliveryRate = data['Machine2BrainDeliveryRate']
# @Parameter Machine2WasteRate @Def: Units of waste produced per minute by machine 2 @Shape: [] 
Machine2WasteRate = data['Machine2WasteRate']
# @Parameter HeartMedicineMax @Def: Maximum units of medicine that can be received by the heart @Shape: [] 
HeartMedicineMax = data['HeartMedicineMax']
# @Parameter BrainMedicineMin @Def: Minimum units of medicine that should be received by the brain @Shape: [] 
BrainMedicineMin = data['BrainMedicineMin']

# Variables 
# @Variable Machine1OperatingTime @Def: The operating time of Machine 1 in minutes @Shape: [] 
Machine1OperatingTime = model.addVar(vtype=GRB.CONTINUOUS, name="Machine1OperatingTime")
# @Variable Machine2OperatingTime @Def: The operating time of Machine 2 in minutes @Shape: [] 
Machine2OperatingTime = model.addVar(vtype=GRB.CONTINUOUS, name="Machine2OperatingTime")

# Constraints 
# @Constraint Constr_1 @Def: The total medicine delivered to the heart by Machine1 and Machine2 must not exceed HeartMedicineMax units.
model.addConstr(Machine1HeartDeliveryRate * Machine1OperatingTime + Machine2HeartDeliveryRate * Machine2OperatingTime <= HeartMedicineMax)
# @Constraint Constr_2 @Def: The total medicine delivered to the brain by Machine1 and Machine2 must be at least BrainMedicineMin units.
model.addConstr(Machine1BrainDeliveryRate * Machine1OperatingTime + Machine2BrainDeliveryRate * Machine2OperatingTime >= BrainMedicineMin)

# Objective 
# @Objective Objective @Def: The total waste produced is the sum of waste produced by Machine1 and Machine2. The objective is to minimize the total waste produced.
model.setObjective(Machine1WasteRate * Machine1OperatingTime + Machine2WasteRate * Machine2OperatingTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Machine1OperatingTime'] = Machine1OperatingTime.x
variables['Machine2OperatingTime'] = Machine2OperatingTime.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
