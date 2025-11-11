# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A chemistry teacher conducts a set of NumExperiments different experiments. Each
experiment i requires RedUsage[i] units of red liquid and BlueUsage[i] units of
blue liquid, and produces GreenGasProduction[i] units of green gas and
SmellyGasProduction[i] units of smelly gas. The total available red liquid is
TotalRed units and the total available blue liquid is TotalBlue units.
Additionally, the total smelly gas produced must not exceed MaxSmelly units. The
objective is to determine the number of each experiment to perform in order to
maximize the total GreenGasProduction.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/132/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumExperiments @Def: Number of different experiments @Shape: [] 
NumExperiments = data['NumExperiments']
# @Parameter RedUsage @Def: Amount of red liquid required for each experiment @Shape: ['NumExperiments'] 
RedUsage = data['RedUsage']
# @Parameter BlueUsage @Def: Amount of blue liquid required for each experiment @Shape: ['NumExperiments'] 
BlueUsage = data['BlueUsage']
# @Parameter GreenGasProduction @Def: Amount of green gas produced by each experiment @Shape: ['NumExperiments'] 
GreenGasProduction = data['GreenGasProduction']
# @Parameter SmellyGasProduction @Def: Amount of smelly gas produced by each experiment @Shape: ['NumExperiments'] 
SmellyGasProduction = data['SmellyGasProduction']
# @Parameter TotalRed @Def: Total units of red liquid available @Shape: [] 
TotalRed = data['TotalRed']
# @Parameter TotalBlue @Def: Total units of blue liquid available @Shape: [] 
TotalBlue = data['TotalBlue']
# @Parameter MaxSmelly @Def: Maximum units of smelly gas allowed @Shape: [] 
MaxSmelly = data['MaxSmelly']

# Variables 
# @Variable ExperimentPerformed @Def: Binary variable indicating whether each experiment is performed @Shape: ['NumExperiments'] 
ExperimentPerformed = model.addVars(NumExperiments, vtype=GRB.BINARY, name='ExperimentPerformed')

# Constraints 
# @Constraint Constr_1 @Def: The total red liquid used by all experiments does not exceed TotalRed units.
model.addConstr(quicksum(RedUsage[i] * ExperimentPerformed[i] for i in range(NumExperiments)) <= TotalRed)
# @Constraint Constr_2 @Def: The total blue liquid used by all experiments does not exceed TotalBlue units.
model.addConstr(quicksum(BlueUsage[i] * ExperimentPerformed[i] for i in range(NumExperiments)) <= TotalBlue)
# @Constraint Constr_3 @Def: The total smelly gas produced by all experiments does not exceed MaxSmelly units.
model.addConstr(quicksum(SmellyGasProduction[i] * ExperimentPerformed[i] for i in range(NumExperiments)) <= MaxSmelly)

# Objective 
# @Objective Objective @Def: Maximize the total GreenGasProduction by determining the number of each experiment to perform.
model.setObjective(quicksum(GreenGasProduction[i] * ExperimentPerformed[i] for i in range(NumExperiments)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ExperimentPerformed'] = [v.X for v in ExperimentPerformed.values()]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
