# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A chemical plant can purchase two types of generators, Generator A and Generator
B, which use different processes to generate hydrogen. Generator A produces
HydrogenProductionA amount of hydrogen and PollutantOutputA units of pollutants
per day. Generator B produces HydrogenProductionB amount of hydrogen and
PollutantOutputB units of pollutants per day. The plant must produce at least
MinHydrogenRequired amount of hydrogen per day and can produce at most
MaxPollutantAllowed units of pollutants per day. The objective is to minimize
the total number of generators purchased.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/83/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HydrogenProductionA @Def: Amount of hydrogen produced per day by generator A @Shape: [] 
HydrogenProductionA = data['HydrogenProductionA']
# @Parameter PollutantOutputA @Def: Amount of pollutants produced per day by generator A @Shape: [] 
PollutantOutputA = data['PollutantOutputA']
# @Parameter HydrogenProductionB @Def: Amount of hydrogen produced per day by generator B @Shape: [] 
HydrogenProductionB = data['HydrogenProductionB']
# @Parameter PollutantOutputB @Def: Amount of pollutants produced per day by generator B @Shape: [] 
PollutantOutputB = data['PollutantOutputB']
# @Parameter MinHydrogenRequired @Def: Minimum hydrogen required per day @Shape: [] 
MinHydrogenRequired = data['MinHydrogenRequired']
# @Parameter MaxPollutantAllowed @Def: Maximum pollutants allowed per day @Shape: [] 
MaxPollutantAllowed = data['MaxPollutantAllowed']

# Variables 
# @Variable NumberOfGeneratorA @Def: The number of Generator A used per day @Shape: [] 
NumberOfGeneratorA = model.addVar(vtype=GRB.INTEGER, name="NumberOfGeneratorA")
# @Variable NumberOfGeneratorB @Def: The number of Generator B used per day @Shape: [] 
NumberOfGeneratorB = model.addVar(vtype=GRB.INTEGER, name="NumberOfGeneratorB")

# Constraints 
# @Constraint Constr_1 @Def: The total hydrogen produced by Generator A and Generator B must be at least MinHydrogenRequired per day.
model.addConstr(HydrogenProductionA * NumberOfGeneratorA + HydrogenProductionB * NumberOfGeneratorB >= MinHydrogenRequired)
# @Constraint Constr_2 @Def: The total pollutant output from Generator A and Generator B must be at most MaxPollutantAllowed units per day.
model.addConstr(NumberOfGeneratorA * PollutantOutputA + NumberOfGeneratorB * PollutantOutputB <= MaxPollutantAllowed)

# Objective 
# @Objective Objective @Def: Minimize the total number of generators purchased.
model.setObjective(NumberOfGeneratorA + NumberOfGeneratorB, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfGeneratorA'] = NumberOfGeneratorA.x
variables['NumberOfGeneratorB'] = NumberOfGeneratorB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
