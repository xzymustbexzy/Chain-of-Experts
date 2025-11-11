# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A patient can take NumPillTypes different pills. Each pill type provides
PainMedicationPerPill units of pain medication and AnxietyMedicationPerPill
units of anxiety medication. Additionally, each pill type causes
DischargePerPill units of discharge. The total amount of pain medication
provided must not exceed MaxPainMedication, and the total amount of anxiety
medication provided must be at least MinAnxietyMedication. The goal is to
determine the number of pills of each type to minimize the total discharge.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/90/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumPillTypes @Def: Number of pill types @Shape: [] 
NumPillTypes = data['NumPillTypes']
# @Parameter PainMedicationPerPill @Def: Amount of pain medication provided by one unit of each pill type @Shape: ['NumPillTypes'] 
PainMedicationPerPill = data['PainMedicationPerPill']
# @Parameter AnxietyMedicationPerPill @Def: Amount of anxiety medication provided by one unit of each pill type @Shape: ['NumPillTypes'] 
AnxietyMedicationPerPill = data['AnxietyMedicationPerPill']
# @Parameter DischargePerPill @Def: Amount of discharge caused by one unit of each pill type @Shape: ['NumPillTypes'] 
DischargePerPill = data['DischargePerPill']
# @Parameter MaxPainMedication @Def: Maximum units of pain medication allowed @Shape: [] 
MaxPainMedication = data['MaxPainMedication']
# @Parameter MinAnxietyMedication @Def: Minimum units of anxiety medication required @Shape: [] 
MinAnxietyMedication = data['MinAnxietyMedication']

# Variables 
# @Variable NumberOfPills @Def: The number of pills of each type @Shape: ['NumPillTypes'] 
NumberOfPills = model.addVars(NumPillTypes, vtype=GRB.INTEGER, name="NumberOfPills")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of pain medication provided, calculated as the sum of PainMedicationPerPill multiplied by the number of pills of each type, must not exceed MaxPainMedication.
model.addConstr(quicksum(PainMedicationPerPill[j] * NumberOfPills[j] for j in range(NumPillTypes)) <= MaxPainMedication)
# @Constraint Constr_2 @Def: The total amount of anxiety medication provided, calculated as the sum of AnxietyMedicationPerPill multiplied by the number of pills of each type, must be at least MinAnxietyMedication.
model.addConstr(quicksum(AnxietyMedicationPerPill[j] * NumberOfPills[j] for j in range(NumPillTypes)) >= MinAnxietyMedication)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total discharge, which is calculated as the sum of DischargePerPill multiplied by the number of pills of each type.
model.setObjective(quicksum(DischargePerPill[i] * NumberOfPills[i] for i in range(NumPillTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
# variables['NumberOfPills'] = NumberOfPills.x
variables['NumberOfPills'] = {j: NumberOfPills[j].x for j in range(NumPillTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
