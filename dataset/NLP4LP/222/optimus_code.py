# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company must determine the number of HighVolumePipes and LowVolumePipes to
ensure that the combined daily capacity meets or exceeds the DailyGasDemand. The
total number of technicians required to monitor these pipes must not exceed the
TotalTechnicians available. Additionally, the proportion of HighVolumePipes used
should not surpass the MaxHighVolumeProportion of all pipes, and there must be
at least MinLowVolumePipes LowVolumePipes. The objective is to minimize the
total number of pipes employed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/223/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HighVolumeCapacity @Def: The daily capacity of a high-volume pipe in US gallons @Shape: [] 
HighVolumeCapacity = data['HighVolumeCapacity']
# @Parameter LowVolumeCapacity @Def: The daily capacity of a low-volume pipe in US gallons @Shape: [] 
LowVolumeCapacity = data['LowVolumeCapacity']
# @Parameter TechniciansPerHighVolumePipe @Def: Number of technicians required to monitor each high-volume pipe daily @Shape: [] 
TechniciansPerHighVolumePipe = data['TechniciansPerHighVolumePipe']
# @Parameter TechniciansPerLowVolumePipe @Def: Number of technicians required to monitor each low-volume pipe daily @Shape: [] 
TechniciansPerLowVolumePipe = data['TechniciansPerLowVolumePipe']
# @Parameter DailyGasDemand @Def: Minimum daily US gallons of gas that need to be met @Shape: [] 
DailyGasDemand = data['DailyGasDemand']
# @Parameter TotalTechnicians @Def: Total number of technicians available daily @Shape: [] 
TotalTechnicians = data['TotalTechnicians']
# @Parameter MaxHighVolumeProportion @Def: Maximum allowed proportion of high-volume pipes @Shape: [] 
MaxHighVolumeProportion = data['MaxHighVolumeProportion']
# @Parameter MinLowVolumePipes @Def: Minimum number of low-volume pipes required @Shape: [] 
MinLowVolumePipes = data['MinLowVolumePipes']

# Variables 
# @Variable HighVolumePipes @Def: The number of high-volume pipes @Shape: [] 
HighVolumePipes = model.addVar(vtype=GRB.INTEGER, name="HighVolumePipes")
# @Variable LowVolumePipes @Def: The number of low-volume pipes @Shape: [] 
LowVolumePipes = model.addVar(vtype=GRB.INTEGER, name="LowVolumePipes")

# Constraints 
# @Constraint Constr_1 @Def: The combined daily capacity of HighVolumePipes and LowVolumePipes must be at least DailyGasDemand.
model.addConstr(HighVolumeCapacity * HighVolumePipes + LowVolumeCapacity * LowVolumePipes >= DailyGasDemand)
# @Constraint Constr_2 @Def: The total number of technicians required to monitor HighVolumePipes and LowVolumePipes must not exceed TotalTechnicians available.
model.addConstr(TechniciansPerHighVolumePipe * HighVolumePipes + TechniciansPerLowVolumePipe * LowVolumePipes <= TotalTechnicians)
# @Constraint Constr_3 @Def: The proportion of HighVolumePipes relative to the total number of pipes must not exceed MaxHighVolumeProportion.
model.addConstr(HighVolumePipes <= MaxHighVolumeProportion * (HighVolumePipes + LowVolumePipes))
# @Constraint Constr_4 @Def: At least MinLowVolumePipes LowVolumePipes must be employed.
model.addConstr(LowVolumePipes >= MinLowVolumePipes)

# Objective 
# @Objective Objective @Def: Minimize the total number of pipes employed.
model.setObjective(HighVolumePipes + LowVolumePipes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['HighVolumePipes'] = HighVolumePipes.x
variables['LowVolumePipes'] = LowVolumePipes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
