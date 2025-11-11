# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A popup clinic administers two types of virus tests: spit tests and swab tests.
Administering a spit test takes TimeSpitTest minutes and administering a swab
test takes TimeSwabTest minutes. At least MinRatioSpitToSwab times as many spit
tests as swab tests must be administered, and at least MinSwabTests swab tests
must be administered. The clinic operates for TotalOperatingTime minutes. The
objective is to maximize the total number of tests administered.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/129/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimeSpitTest @Def: Time to administer a spit test @Shape: [] 
TimeSpitTest = data['TimeSpitTest']
# @Parameter TimeSwabTest @Def: Time to administer a swab test @Shape: [] 
TimeSwabTest = data['TimeSwabTest']
# @Parameter MinRatioSpitToSwab @Def: Minimum ratio of spit tests to swab tests @Shape: [] 
MinRatioSpitToSwab = data['MinRatioSpitToSwab']
# @Parameter MinSwabTests @Def: Minimum number of swab tests to administer @Shape: [] 
MinSwabTests = data['MinSwabTests']
# @Parameter TotalOperatingTime @Def: Total operating time in minutes @Shape: [] 
TotalOperatingTime = data['TotalOperatingTime']

# Variables 
# @Variable NumberOfSpitTests @Def: The number of spit tests to administer @Shape: [] 
NumberOfSpitTests = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfSpitTests")
# @Variable NumberOfSwabTests @Def: The number of swab tests to administer @Shape: [] 
NumberOfSwabTests = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfSwabTests")

# Constraints 
# @Constraint Constr_1 @Def: Administering a spit test takes TimeSpitTest minutes and administering a swab test takes TimeSwabTest minutes. The total operating time cannot exceed TotalOperatingTime minutes.
model.addConstr(TimeSpitTest * NumberOfSpitTests + TimeSwabTest * NumberOfSwabTests <= TotalOperatingTime)
# @Constraint Constr_2 @Def: At least MinRatioSpitToSwab times as many spit tests as swab tests must be administered.
model.addConstr(NumberOfSpitTests >= MinRatioSpitToSwab * NumberOfSwabTests)
# @Constraint Constr_3 @Def: At least MinSwabTests swab tests must be administered.
model.addConstr(NumberOfSwabTests >= MinSwabTests)

# Objective 
# @Objective Objective @Def: The total number of tests administered is the sum of spit tests and swab tests. The objective is to maximize the total number of tests administered.
model.setObjective(NumberOfSpitTests + NumberOfSwabTests, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSpitTests'] = NumberOfSpitTests.x
variables['NumberOfSwabTests'] = NumberOfSwabTests.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
