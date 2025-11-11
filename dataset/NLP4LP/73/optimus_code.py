# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A scientist is conducting NumExperiments different experiments to produce
electricity. Each experiment i produces ElectricityProduced[i] units of
electricity and requires specific amounts of NumResources types of resources as
defined by ResourceRequired[j][i]. The laboratory has ResourceAvailable[j] units
of each resource available. The scientist aims to determine the number of each
experiment to conduct in order to maximize the total electricity produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/74/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumExperiments @Def: Number of experiments @Shape: [] 
NumExperiments = data['NumExperiments']
# @Parameter NumResources @Def: Number of resource types @Shape: [] 
NumResources = data['NumResources']
# @Parameter ResourceAvailable @Def: Amount of resource j available @Shape: ['NumResources'] 
ResourceAvailable = data['ResourceAvailable']
# @Parameter ResourceRequired @Def: Amount of resource j required for experiment i @Shape: ['NumResources', 'NumExperiments'] 
ResourceRequired = data['ResourceRequired']
# @Parameter ElectricityProduced @Def: Amount of electricity produced by experiment i @Shape: ['NumExperiments'] 
ElectricityProduced = data['ElectricityProduced']

# Variables 
# @Variable ConductExperiment @Def: The number of times each experiment is conducted @Shape: ['NumExperiments'] 
ConductExperiment = model.addVars(NumExperiments, vtype=GRB.CONTINUOUS, name="ConductExperiment")

# Constraints 
# @Constraint Constr_1 @Def: The total metal required for all experiments does not exceed the available metal.
model.addConstr(quicksum(ResourceRequired[0][i] * ConductExperiment[i] for i in range(NumExperiments)) <= ResourceAvailable[0])
# @Constraint Constr_2 @Def: The total acid required for all experiments does not exceed the available acid.
model.addConstr(quicksum(ResourceRequired[1][i] * ConductExperiment[i] for i in range(NumExperiments)) <= ResourceAvailable[1])

# Objective 
# @Objective Objective @Def: Maximize the total electricity produced by conducting the experiments.
model.setObjective(quicksum(ConductExperiment[i] * ElectricityProduced[i] for i in range(NumExperiments)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ConductExperiment'] = {i: ConductExperiment[i].X for i in range(NumExperiments)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
