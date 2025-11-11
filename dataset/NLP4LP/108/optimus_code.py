# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A doctor's office takes the temperature of patients one by one using either an
electronic or regular thermometer. The electronic thermometer takes
TimeElectronicReading time per reading, while the regular thermometer takes
TimeRegularReading time per reading. At least MinRatioElectronicToRegular times
as many patients should have their temperature checked by the electronic
thermometer as by the regular thermometer. Additionally, at least
MinRegularPatients should have their temperature checked by the regular
thermometer. Given TotalAvailableTime, maximize the number of patients whose
temperature can be taken.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/109/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimeElectronicReading @Def: Time taken by electronic thermometer per reading @Shape: [] 
TimeElectronicReading = data['TimeElectronicReading']
# @Parameter TimeRegularReading @Def: Time taken by regular thermometer per reading @Shape: [] 
TimeRegularReading = data['TimeRegularReading']
# @Parameter MinRatioElectronicToRegular @Def: Minimum ratio of electronic thermometer uses to regular thermometer uses @Shape: [] 
MinRatioElectronicToRegular = data['MinRatioElectronicToRegular']
# @Parameter MinRegularPatients @Def: Minimum number of patients using regular thermometer @Shape: [] 
MinRegularPatients = data['MinRegularPatients']
# @Parameter TotalAvailableTime @Def: Total available time for temperature readings @Shape: [] 
TotalAvailableTime = data['TotalAvailableTime']

# Variables 
# @Variable ElectronicReadings @Def: The number of electronic thermometer readings @Shape: [] 
ElectronicReadings = model.addVar(vtype=GRB.INTEGER, name="ElectronicReadings")
# @Variable RegularReadings @Def: The number of regular thermometer readings @Shape: [] 
RegularReadings = model.addVar(vtype=GRB.INTEGER, name="RegularReadings")

# Constraints 
# @Constraint Constr_1 @Def: The total time taken by electronic and regular thermometer readings cannot exceed TotalAvailableTime.
model.addConstr(TimeElectronicReading * ElectronicReadings + TimeRegularReading * RegularReadings <= TotalAvailableTime)
# @Constraint Constr_2 @Def: At least MinRatioElectronicToRegular times as many patients should have their temperature checked by the electronic thermometer as by the regular thermometer.
model.addConstr(ElectronicReadings >= MinRatioElectronicToRegular * RegularReadings)
# @Constraint Constr_3 @Def: At least MinRegularPatients must have their temperature checked by the regular thermometer.
model.addConstr(RegularReadings >= MinRegularPatients)

# Objective 
# @Objective Objective @Def: The number of patients processed is the sum of patients checked by electronic and regular thermometers. The objective is to maximize this total number of patients within the available time and usage constraints.
model.setObjective(ElectronicReadings + RegularReadings, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ElectronicReadings'] = ElectronicReadings.x
variables['RegularReadings'] = RegularReadings.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
