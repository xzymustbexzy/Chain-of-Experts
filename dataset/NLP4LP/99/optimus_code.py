# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient can consume NumSyrups different syrups for treatment. For each syrup,
a serving delivers MedicineThroatPerServing units of medicine to the throat and
MedicineLungsPerServing units of medicine to the lungs. Each serving contains
SugarPerServing units of sugar. The patient must receive no more than
MaxMedicineThroat units of medicine for the throat and at least MinMedicineLungs
units of medicine for the lungs. The objective is to determine the number of
servings of each syrup to minimize total sugar intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/100/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumSyrups @Def: Number of available syrups @Shape: [] 
NumSyrups = data['NumSyrups']
# @Parameter MedicineThroatPerServing @Def: Amount of medicine delivered to the throat per serving of each syrup @Shape: ['NumSyrups'] 
MedicineThroatPerServing = data['MedicineThroatPerServing']
# @Parameter MedicineLungsPerServing @Def: Amount of medicine delivered to the lungs per serving of each syrup @Shape: ['NumSyrups'] 
MedicineLungsPerServing = data['MedicineLungsPerServing']
# @Parameter SugarPerServing @Def: Amount of sugar per serving of each syrup @Shape: ['NumSyrups'] 
SugarPerServing = data['SugarPerServing']
# @Parameter MaxMedicineThroat @Def: Maximum total medicine allowed for the throat @Shape: [] 
MaxMedicineThroat = data['MaxMedicineThroat']
# @Parameter MinMedicineLungs @Def: Minimum total medicine required for the lungs @Shape: [] 
MinMedicineLungs = data['MinMedicineLungs']

# Variables 
# @Variable Servings @Def: The number of servings for each syrup @Shape: ['NumSyrups'] 
Servings = model.addVars(NumSyrups, vtype=GRB.CONTINUOUS, name="Servings")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of medicine delivered to the throat by all syrups must not exceed MaxMedicineThroat units.
model.addConstr(quicksum(MedicineThroatPerServing[i] * Servings[i] for i in range(NumSyrups)) <= MaxMedicineThroat)
# @Constraint Constr_2 @Def: The total amount of medicine delivered to the lungs by all syrups must be at least MinMedicineLungs units.
model.addConstr(quicksum(Servings[i] * MedicineLungsPerServing[i] for i in range(NumSyrups)) >= MinMedicineLungs)

# Objective 
# @Objective Objective @Def: Minimize the total sugar intake, which is the sum of SugarPerServing units of sugar per serving multiplied by the number of servings of each syrup.
model.setObjective(quicksum(SugarPerServing[i] * Servings[i] for i in range(NumSyrups)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['Servings'] = {i: Servings[i].X for i in range(NumSyrups)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)