# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A disease testing station conducts a temperature check and/or a blood test on
each patient. A temperature check takes TimeTemperatureCheck minutes while a
blood test takes TimeBloodTest minutes. The testing station must conduct at
least MinBloodTests blood tests. The temperature check is required to be
performed at least TempToBloodRatio times as many as the blood tests. If the
testing station has a total of TotalStaffMinutes staff minutes, how many of each
 test or check should be done to maximize the number of patients seen?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/214/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter TimeTemperatureCheck @Def: Time taken to perform a temperature check @Shape: [] 
TimeTemperatureCheck = data['TimeTemperatureCheck']
# @Parameter TimeBloodTest @Def: Time taken to perform a blood test @Shape: [] 
TimeBloodTest = data['TimeBloodTest']
# @Parameter MinBloodTests @Def: Minimum number of blood tests required @Shape: [] 
MinBloodTests = data['MinBloodTests']
# @Parameter TempToBloodRatio @Def: Minimum ratio of temperature checks to blood tests @Shape: [] 
TempToBloodRatio = data['TempToBloodRatio']
# @Parameter TotalStaffMinutes @Def: Total staff minutes available @Shape: [] 
TotalStaffMinutes = data['TotalStaffMinutes']

# Variables 
# @Variable TemperatureChecks @Def: The number of temperature checks @Shape: [] 
TemperatureChecks = model.addVar(vtype=GRB.CONTINUOUS, name="TemperatureChecks")
# @Variable BloodTests @Def: The number of blood tests @Shape: [] 
BloodTests = model.addVar(vtype=GRB.CONTINUOUS, name="BloodTests")
# @Variable PatientsSeen @Def: The number of patients seen @Shape: [] 
PatientsSeen = model.addVar(vtype=GRB.CONTINUOUS, name="PatientsSeen")

# Constraints 
# @Constraint Constr_1 @Def: The total time allocated for temperature checks and blood tests cannot exceed TotalStaffMinutes minutes.
model.addConstr(TimeTemperatureCheck * TemperatureChecks + TimeBloodTest * BloodTests <= TotalStaffMinutes)
# @Constraint Constr_2 @Def: At least MinBloodTests blood tests must be conducted.
model.addConstr(BloodTests >= MinBloodTests)
# @Constraint Constr_3 @Def: The number of temperature checks must be at least TempToBloodRatio times the number of blood tests.
model.addConstr(TemperatureChecks >= TempToBloodRatio * BloodTests)
# @Constraint Constr_4 @Def: The number of patients seen cannot exceed the total tests conducted.
model.addConstr(PatientsSeen <= TemperatureChecks + BloodTests)

# Objective 
# @Objective Objective @Def: Maximize the number of patients seen by conducting temperature checks and blood tests.
model.setObjective(PatientsSeen, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['TemperatureChecks'] = TemperatureChecks.x
variables['BloodTests'] = BloodTests.x
variables['PatientsSeen'] = PatientsSeen.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
