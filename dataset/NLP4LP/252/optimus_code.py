# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A drop-in clinic is performing tests either through the ear or blood. Each blood
test takes TimePerBloodTest minutes to perform while each ear test takes
TimePerEarTest minutes. Since the blood test is more accurate, at least
BloodToEarTestRatio times as many blood tests should be performed as ear tests.
However, at least MinEarTests ear tests must be administered. If the drop-in
clinic operates for TotalOperatingTime minutes, maximize the number of tests
that can be performed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/253/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimePerBloodTest @Def: Time required to perform a blood test in minutes @Shape: [] 
TimePerBloodTest = data['TimePerBloodTest']
# @Parameter TimePerEarTest @Def: Time required to perform an ear test in minutes @Shape: [] 
TimePerEarTest = data['TimePerEarTest']
# @Parameter BloodToEarTestRatio @Def: Minimum ratio of blood tests to ear tests @Shape: [] 
BloodToEarTestRatio = data['BloodToEarTestRatio']
# @Parameter MinEarTests @Def: Minimum number of ear tests to be administered @Shape: [] 
MinEarTests = data['MinEarTests']
# @Parameter TotalOperatingTime @Def: Total operating time of the clinic in minutes @Shape: [] 
TotalOperatingTime = data['TotalOperatingTime']

# Variables 
# @Variable NumberOfBloodTests @Def: The number of blood tests to be administered @Shape: [] 
NumberOfBloodTests = model.addVar(vtype=GRB.INTEGER, name="NumberOfBloodTests")
# @Variable NumberOfEarTests @Def: The number of ear tests to be administered @Shape: [] 
NumberOfEarTests = model.addVar(vtype=GRB.INTEGER, name="NumberOfEarTests")

# Constraints 
# @Constraint Constr_1 @Def: The total time required for blood tests plus ear tests does not exceed TotalOperatingTime minutes.
model.addConstr(TimePerBloodTest * NumberOfBloodTests + TimePerEarTest * NumberOfEarTests <= TotalOperatingTime)
# @Constraint Constr_2 @Def: The number of blood tests is at least BloodToEarTestRatio times the number of ear tests.
model.addConstr(NumberOfBloodTests >= BloodToEarTestRatio * NumberOfEarTests)
# @Constraint Constr_3 @Def: At least MinEarTests ear tests must be administered.
model.addConstr(NumberOfEarTests >= MinEarTests)

# Objective 
# @Objective Objective @Def: Maximize the total number of tests performed (blood tests plus ear tests).
model.setObjective(NumberOfBloodTests + NumberOfEarTests, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBloodTests'] = NumberOfBloodTests.x
variables['NumberOfEarTests'] = NumberOfEarTests.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
