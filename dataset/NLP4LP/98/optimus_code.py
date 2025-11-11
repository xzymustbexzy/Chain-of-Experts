# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A clinic processes patients using an automatic machine and a manual machine. Let
A represent the number of patients processed by the automatic machine and M
represent the number of patients processed by the manual machine. The total
processing time, calculated as AutomaticMachineTimePerPatient multiplied by A
plus ManualMachineTimePerPatient multiplied by M, must not exceed
TotalAvailableTime. Additionally, the number of patients processed by the manual
machine must be at least ManualPatientMinRatio times A, and the automatic
machine must process at least AutomaticMachineMinimumPatients. The objective is
to maximize the total number of patients, which is the sum of A and M.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/99/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AutomaticMachineTimePerPatient @Def: Time taken by the automatic machine to process one patient. @Shape: [] 
AutomaticMachineTimePerPatient = data['AutomaticMachineTimePerPatient']
# @Parameter ManualMachineTimePerPatient @Def: Time taken by the manual machine to process one patient. @Shape: [] 
ManualMachineTimePerPatient = data['ManualMachineTimePerPatient']
# @Parameter ManualPatientMinRatio @Def: Minimum ratio of manual machine patients to automatic machine patients. @Shape: [] 
ManualPatientMinRatio = data['ManualPatientMinRatio']
# @Parameter AutomaticMachineMinimumPatients @Def: Minimum number of patients that must be processed by the automatic machine. @Shape: [] 
AutomaticMachineMinimumPatients = data['AutomaticMachineMinimumPatients']
# @Parameter TotalAvailableTime @Def: Total available time for the clinic in minutes. @Shape: [] 
TotalAvailableTime = data['TotalAvailableTime']

# Variables 
# @Variable AutomaticPatients @Def: The number of patients processed by the automatic machine @Shape: [] 
AutomaticPatients = model.addVar(vtype=GRB.INTEGER, name="AutomaticPatients")
# @Variable ManualPatients @Def: The number of patients processed by the manual machine @Shape: [] 
ManualPatients = model.addVar(vtype=GRB.INTEGER, name="ManualPatients")

# Constraints 
# @Constraint Constr_1 @Def: AutomaticMachineTimePerPatient multiplied by A plus ManualMachineTimePerPatient multiplied by M does not exceed TotalAvailableTime.
model.addConstr(AutomaticMachineTimePerPatient * AutomaticPatients + ManualMachineTimePerPatient * ManualPatients <= TotalAvailableTime)
# @Constraint Constr_2 @Def: The number of patients processed by the manual machine must be at least ManualPatientMinRatio times A.
model.addConstr(ManualPatients >= ManualPatientMinRatio * AutomaticPatients)
# @Constraint Constr_3 @Def: A must be at least AutomaticMachineMinimumPatients.
model.addConstr(AutomaticPatients >= AutomaticMachineMinimumPatients)

# Objective 
# @Objective Objective @Def: Maximize the total number of patients, which is the sum of A and M.
model.setObjective(AutomaticPatients + ManualPatients, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AutomaticPatients'] = AutomaticPatients.x
variables['ManualPatients'] = ManualPatients.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
