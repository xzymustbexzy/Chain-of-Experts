# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A university research lab produces two types of diabetes medicine, medicine A
and medicine B. Each dose of medicine A requires ImportedMaterialPerDoseA units
of imported material and MRNAPerDoseA units of mRNA. Each dose of medicine B
requires ImportedMaterialPerDoseB units of imported material and MRNAPerDoseB
units of mRNA. The lab has a maximum of MaxImportedMaterial units of imported
material and MaxMRNA units of mRNA available. The production of medicine A is
limited to MaxDosesA doses, and the number of doses of medicine B must exceed
the number of doses of medicine A. The objective is to maximize the total number
of people treated, where each dose of medicine A treats TreatmentPerDoseA
individuals and each dose of medicine B treats TreatmentPerDoseB individuals.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/128/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ImportedMaterialPerDoseA @Def: Amount of imported material required to produce one dose of medicine A @Shape: [] 
ImportedMaterialPerDoseA = data['ImportedMaterialPerDoseA']
# @Parameter MRNAPerDoseA @Def: Amount of mRNA required to produce one dose of medicine A @Shape: [] 
MRNAPerDoseA = data['MRNAPerDoseA']
# @Parameter ImportedMaterialPerDoseB @Def: Amount of imported material required to produce one dose of medicine B @Shape: [] 
ImportedMaterialPerDoseB = data['ImportedMaterialPerDoseB']
# @Parameter MRNAPerDoseB @Def: Amount of mRNA required to produce one dose of medicine B @Shape: [] 
MRNAPerDoseB = data['MRNAPerDoseB']
# @Parameter MaxImportedMaterial @Def: Maximum available units of imported material @Shape: [] 
MaxImportedMaterial = data['MaxImportedMaterial']
# @Parameter MaxMRNA @Def: Maximum available units of mRNA @Shape: [] 
MaxMRNA = data['MaxMRNA']
# @Parameter MaxDosesA @Def: Maximum number of doses of medicine A that can be produced @Shape: [] 
MaxDosesA = data['MaxDosesA']
# @Parameter TreatmentPerDoseA @Def: Number of people treated by one dose of medicine A @Shape: [] 
TreatmentPerDoseA = data['TreatmentPerDoseA']
# @Parameter TreatmentPerDoseB @Def: Number of people treated by one dose of medicine B @Shape: [] 
TreatmentPerDoseB = data['TreatmentPerDoseB']

# Variables 
# @Variable DosesA @Def: The number of doses of medicine A produced @Shape: [] 
DosesA = model.addVar(vtype=GRB.CONTINUOUS, name="DosesA")
# @Variable DosesB @Def: The number of doses of medicine B produced @Shape: [] 
DosesB = model.addVar(vtype=GRB.CONTINUOUS, name="DosesB")

# Constraints 
# @Constraint Constr_1 @Def: The total imported material used by medicines A and B cannot exceed MaxImportedMaterial units.
model.addConstr(ImportedMaterialPerDoseA * DosesA + ImportedMaterialPerDoseB * DosesB <= MaxImportedMaterial)
# @Constraint Constr_2 @Def: The total mRNA used by medicines A and B cannot exceed MaxMRNA units.
model.addConstr(MRNAPerDoseA * DosesA + MRNAPerDoseB * DosesB <= MaxMRNA)
# @Constraint Constr_3 @Def: The number of doses of medicine A produced cannot exceed MaxDosesA.
model.addConstr(DosesA <= MaxDosesA)
# @Constraint Constr_4 @Def: The number of doses of medicine B produced must exceed the number of doses of medicine A.
model.addConstr(DosesB >= DosesA + 1)

# Objective 
# @Objective Objective @Def: Maximize the total number of people treated, which is the sum of TreatmentPerDoseA times the number of doses of medicine A and TreatmentPerDoseB times the number of doses of medicine B.
model.setObjective(TreatmentPerDoseA * DosesA + TreatmentPerDoseB * DosesB, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['DosesA'] = DosesA.x
variables['DosesB'] = DosesB.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
