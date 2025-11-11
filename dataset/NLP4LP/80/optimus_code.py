# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A factory has two types of machines, A and B. Each day, machine A can produce
ProductionA items and consumes EnergyA kWh. Machine B can produce ProductionB
items and consumes EnergyB kWh per day. The factory must produce at least
MinProduction items per day and has MaxEnergy kWh of electricity available per
day. Due to limited workers, at most MaxPercentB of the machines can be of type
B. Additionally, at least MinA machines of type A must be used. The objective is
to determine the number of each machine to minimize the total number of
machines.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/81/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProductionA @Def: Production rate of Machine A in items per day @Shape: [] 
ProductionA = data['ProductionA']
# @Parameter ProductionB @Def: Production rate of Machine B in items per day @Shape: [] 
ProductionB = data['ProductionB']
# @Parameter EnergyA @Def: Energy consumption of Machine A in kWh per day @Shape: [] 
EnergyA = data['EnergyA']
# @Parameter EnergyB @Def: Energy consumption of Machine B in kWh per day @Shape: [] 
EnergyB = data['EnergyB']
# @Parameter MinProduction @Def: Minimum required production in items per day @Shape: [] 
MinProduction = data['MinProduction']
# @Parameter MaxEnergy @Def: Maximum available energy in kWh per day @Shape: [] 
MaxEnergy = data['MaxEnergy']
# @Parameter MaxPercentB @Def: Maximum percentage of machines that can be of type B @Shape: [] 
MaxPercentB = data['MaxPercentB']
# @Parameter MinA @Def: Minimum number of machines of type A @Shape: [] 
MinA = data['MinA']

# Variables 
# @Variable NumberA @Def: The number of machines of type A @Shape: ['Integer'] 
NumberA = model.addVar(vtype=GRB.INTEGER, lb=MinA, name="NumberA")
# @Variable NumberB @Def: The number of machines of type B @Shape: ['Integer'] 
NumberB = model.addVar(vtype=GRB.INTEGER, name="NumberB")

# Constraints 
# @Constraint Constr_1 @Def: The total production by machines of type A and B must be at least MinProduction items per day.
model.addConstr(ProductionA * NumberA + ProductionB * NumberB >= MinProduction)
# @Constraint Constr_2 @Def: The total energy consumption by machines of type A and B must not exceed MaxEnergy kWh per day.
model.addConstr(EnergyA * NumberA + EnergyB * NumberB <= MaxEnergy)
# @Constraint Constr_3 @Def: At most MaxPercentB percentage of the machines can be of type B.
model.addConstr((1 - MaxPercentB) * NumberB <= MaxPercentB * NumberA)
# @Constraint Constr_4 @Def: At least MinA machines of type A must be used.
model.addConstr(NumberA >= MinA)

# Objective 
# @Objective Objective @Def: Minimize the total number of machines of type A and B used in the factory.
model.setObjective(NumberA + NumberB, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberA'] = NumberA.x
variables['NumberB'] = NumberB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
