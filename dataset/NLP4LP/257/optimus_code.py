# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A researcher needs to perform two types of experiments: in-vivo and ex-vivo.
Each in-vivo experiment requires PrepTimeInVivo for preparation and
ExecTimeInVivo for execution, and yields RadiationInVivo radiation. Each ex-vivo
experiment requires PrepTimeExVivo for preparation and ExecTimeExVivo for
execution, and yields RadiationExVivo radiation. The total preparation time must
not exceed MaxPrepTime, and the total execution time must not exceed
MaxExecTime. The researcher aims to determine the number of in-vivo and ex-vivo
experiments to schedule in order to minimize the total radiation received.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/258/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PrepTimeInVivo @Def: Preparation time required for in-vivo experiments @Shape: [] 
PrepTimeInVivo = data['PrepTimeInVivo']
# @Parameter ExecTimeInVivo @Def: Execution time required for in-vivo experiments @Shape: [] 
ExecTimeInVivo = data['ExecTimeInVivo']
# @Parameter RadiationInVivo @Def: Radiation units received from in-vivo experiments @Shape: [] 
RadiationInVivo = data['RadiationInVivo']
# @Parameter PrepTimeExVivo @Def: Preparation time required for ex-vivo experiments @Shape: [] 
PrepTimeExVivo = data['PrepTimeExVivo']
# @Parameter ExecTimeExVivo @Def: Execution time required for ex-vivo experiments @Shape: [] 
ExecTimeExVivo = data['ExecTimeExVivo']
# @Parameter RadiationExVivo @Def: Radiation units received from ex-vivo experiments @Shape: [] 
RadiationExVivo = data['RadiationExVivo']
# @Parameter MaxPrepTime @Def: Maximum available preparation time @Shape: [] 
MaxPrepTime = data['MaxPrepTime']
# @Parameter MaxExecTime @Def: Maximum available execution time @Shape: [] 
MaxExecTime = data['MaxExecTime']

# Variables 
# @Variable NumberOfInVivoExperiments @Def: The number of in-vivo experiments @Shape: [] 
NumberOfInVivoExperiments = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfInVivoExperiments")
# @Variable NumberOfExVivoExperiments @Def: The number of ex-vivo experiments @Shape: [] 
NumberOfExVivoExperiments = model.addVar(vtype=GRB.INTEGER, name='NumberOfExVivoExperiments')

# Constraints 
# @Constraint Constr_1 @Def: The total preparation time for in-vivo and ex-vivo experiments must not exceed MaxPrepTime.
model.addConstr(PrepTimeInVivo * NumberOfInVivoExperiments + PrepTimeExVivo * NumberOfExVivoExperiments <= MaxPrepTime)
# @Constraint Constr_2 @Def: The total execution time for in-vivo and ex-vivo experiments must not exceed MaxExecTime.
model.addConstr(ExecTimeInVivo * NumberOfInVivoExperiments + ExecTimeExVivo * NumberOfExVivoExperiments <= MaxExecTime)

# Objective 
# @Objective Objective @Def: Minimize the total radiation received, which is the sum of RadiationInVivo multiplied by the number of in-vivo experiments and RadiationExVivo multiplied by the number of ex-vivo experiments.
model.setObjective(RadiationInVivo * NumberOfInVivoExperiments + RadiationExVivo * NumberOfExVivoExperiments, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfInVivoExperiments'] = NumberOfInVivoExperiments.x
variables['NumberOfExVivoExperiments'] = NumberOfExVivoExperiments.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
