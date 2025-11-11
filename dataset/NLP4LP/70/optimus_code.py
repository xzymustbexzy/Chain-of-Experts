# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of motion activated machines and manual machines to
minimize the total number of machines, ensuring that the number of manual
machines does not exceed MaxManualPercentage of the total machines, at least
MinMotionActivatedMachines are motion activated, the combined drop rate is at
least MinTotalDrops, and the total energy consumption does not exceed
MaxTotalEnergy.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/71/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MotionActivatedDropRate @Def: Drop rate (drops per minute) of motion activated machine @Shape: [] 
MotionActivatedDropRate = data['MotionActivatedDropRate']
# @Parameter MotionActivatedEnergyConsumption @Def: Energy consumption (kWh) of motion activated machine @Shape: [] 
MotionActivatedEnergyConsumption = data['MotionActivatedEnergyConsumption']
# @Parameter ManualDropRate @Def: Drop rate (drops per minute) of manual machine @Shape: [] 
ManualDropRate = data['ManualDropRate']
# @Parameter ManualEnergyConsumption @Def: Energy consumption (kWh) of manual machine @Shape: [] 
ManualEnergyConsumption = data['ManualEnergyConsumption']
# @Parameter MaxManualPercentage @Def: Maximum percentage of machines that can be manual @Shape: [] 
MaxManualPercentage = data['MaxManualPercentage']
# @Parameter MinMotionActivatedMachines @Def: Minimum number of motion activated machines @Shape: [] 
MinMotionActivatedMachines = data['MinMotionActivatedMachines']
# @Parameter MinTotalDrops @Def: Minimum total drop delivery (drops per minute) @Shape: [] 
MinTotalDrops = data['MinTotalDrops']
# @Parameter MaxTotalEnergy @Def: Maximum total energy consumption (kWh per minute) @Shape: [] 
MaxTotalEnergy = data['MaxTotalEnergy']

# Variables 
# @Variable ManualMachines @Def: The number of manual machines @Shape: [] 
ManualMachines = model.addVar(vtype=GRB.INTEGER, name="ManualMachines")
# @Variable MotionActivatedMachines @Def: The number of motion activated machines @Shape: [] 
MotionActivatedMachines = model.addVar(vtype=GRB.INTEGER, name="MotionActivatedMachines")
# @Variable TotalMachines @Def: The total number of machines @Shape: [] 
TotalMachines = model.addVar(vtype=GRB.INTEGER, name="TotalMachines")

# Constraints 
# @Constraint Constr_1 @Def: The number of manual machines does not exceed MaxManualPercentage of the total machines.
model.addConstr((1 - MaxManualPercentage) * ManualMachines - MaxManualPercentage * MotionActivatedMachines <= 0)
# @Constraint Constr_2 @Def: At least MinMotionActivatedMachines are motion activated.
model.addConstr(MotionActivatedMachines >= MinMotionActivatedMachines)
# @Constraint Constr_3 @Def: The combined drop rate is at least MinTotalDrops.
model.addConstr(MotionActivatedDropRate * MotionActivatedMachines + ManualDropRate * ManualMachines >= MinTotalDrops)
# @Constraint Constr_4 @Def: The total energy consumption does not exceed MaxTotalEnergy.
model.addConstr(ManualMachines * ManualEnergyConsumption + MotionActivatedMachines * MotionActivatedEnergyConsumption <= MaxTotalEnergy)
# @Constraint Constr_5 @Def: The total number of machines is equal to the sum of manual and motion-activated machines.
model.addConstr(TotalMachines == ManualMachines + MotionActivatedMachines)

# Objective 
# @Objective Objective @Def: Minimize the total number of machines.
model.setObjective(TotalMachines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ManualMachines'] = ManualMachines.x
variables['MotionActivatedMachines'] = MotionActivatedMachines.x
variables['TotalMachines'] = TotalMachines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
