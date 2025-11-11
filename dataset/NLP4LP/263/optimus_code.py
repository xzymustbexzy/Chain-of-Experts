# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A biotechnology company has TotalAntibiotics units of antibiotics available,
which are essential for producing first-dose and second-dose vaccines. The
first-dose vaccine requires AntibioticsFirstDose units of antibiotics and
GelatineFirstDose mg of gelatine per unit, while the second-dose vaccine
requires AntibioticsSecondDose units of antibiotics and GelatineSecondDose mg of
gelatine per unit. The production of first-dose vaccines must exceed the
production of second-dose vaccines, and at least MinimumSecondDose second-dose
vaccines must be produced. The objective is to determine the number of first-
dose and second-dose vaccines to manufacture in order to minimize the total
gelatine usage.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/264/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalAntibiotics @Def: Total number of antibiotics available @Shape: [] 
TotalAntibiotics = data['TotalAntibiotics']
# @Parameter AntibioticsFirstDose @Def: Antibiotics required for one first-dose vaccine @Shape: [] 
AntibioticsFirstDose = data['AntibioticsFirstDose']
# @Parameter GelatineFirstDose @Def: Gelatine required for one first-dose vaccine @Shape: [] 
GelatineFirstDose = data['GelatineFirstDose']
# @Parameter AntibioticsSecondDose @Def: Antibiotics required for one second-dose vaccine @Shape: [] 
AntibioticsSecondDose = data['AntibioticsSecondDose']
# @Parameter GelatineSecondDose @Def: Gelatine required for one second-dose vaccine @Shape: [] 
GelatineSecondDose = data['GelatineSecondDose']
# @Parameter MinimumSecondDose @Def: Minimum number of second-dose vaccines required @Shape: [] 
MinimumSecondDose = data['MinimumSecondDose']

# Variables 
# @Variable FirstDoseVaccines @Def: The number of first-dose vaccines administered @Shape: [] 
FirstDoseVaccines = model.addVar(vtype=GRB.CONTINUOUS, name="FirstDoseVaccines")
# @Variable SecondDoseVaccines @Def: The number of second-dose vaccines administered @Shape: [] 
SecondDoseVaccines = model.addVar(vtype=GRB.CONTINUOUS, name="SecondDoseVaccines")

# Constraints 
# @Constraint Constr_1 @Def: The total antibiotics used for first-dose and second-dose vaccines must not exceed TotalAntibiotics units.
model.addConstr(AntibioticsFirstDose * FirstDoseVaccines + AntibioticsSecondDose * SecondDoseVaccines <= TotalAntibiotics)
# @Constraint Constr_2 @Def: The number of first-dose vaccines produced must be greater than the number of second-dose vaccines produced.
model.addConstr(FirstDoseVaccines >= SecondDoseVaccines)
# @Constraint Constr_3 @Def: At least MinimumSecondDose second-dose vaccines must be produced.
model.addConstr(SecondDoseVaccines >= MinimumSecondDose)

# Objective 
# @Objective Objective @Def: Minimize the total gelatine usage, which is the sum of GelatineFirstDose multiplied by the number of first-dose vaccines and GelatineSecondDose multiplied by the number of second-dose vaccines.
model.setObjective(GelatineFirstDose * FirstDoseVaccines + GelatineSecondDose * SecondDoseVaccines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['FirstDoseVaccines'] = FirstDoseVaccines.x
variables['SecondDoseVaccines'] = SecondDoseVaccines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
