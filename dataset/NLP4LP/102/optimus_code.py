# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A lab has TotalMRNAAvailable amount of mRNA anti-viral available to make
children's and adult vaccines. Each children's vaccine contains
MRNAPerChildVaccine mRNA and FeverSuppressantPerChildVaccine fever suppressant.
Each adult vaccine contains MRNAPerAdultVaccine mRNA and
FeverSuppressantPerAdultVaccine fever suppressant. At least
MinPercentageAdultVaccines percent of vaccines should be adult vaccines. At
least MinChildVaccines children's vaccines should be made. Determine the number
of each vaccine to minimize the amount of fever suppressant used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/103/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalMRNAAvailable @Def: Total amount of mRNA anti-viral available @Shape: [] 
TotalMRNAAvailable = data['TotalMRNAAvailable']
# @Parameter MRNAPerChildVaccine @Def: Amount of mRNA per children vaccine @Shape: [] 
MRNAPerChildVaccine = data['MRNAPerChildVaccine']
# @Parameter MRNAPerAdultVaccine @Def: Amount of mRNA per adult vaccine @Shape: [] 
MRNAPerAdultVaccine = data['MRNAPerAdultVaccine']
# @Parameter FeverSuppressantPerChildVaccine @Def: Amount of fever suppressant per children vaccine @Shape: [] 
FeverSuppressantPerChildVaccine = data['FeverSuppressantPerChildVaccine']
# @Parameter FeverSuppressantPerAdultVaccine @Def: Amount of fever suppressant per adult vaccine @Shape: [] 
FeverSuppressantPerAdultVaccine = data['FeverSuppressantPerAdultVaccine']
# @Parameter MinPercentageAdultVaccines @Def: Minimum percentage of vaccines that should be adult vaccines @Shape: [] 
MinPercentageAdultVaccines = data['MinPercentageAdultVaccines']
# @Parameter MinChildVaccines @Def: Minimum number of children's vaccines to be made @Shape: [] 
MinChildVaccines = data['MinChildVaccines']

# Variables 
# @Variable NumChildVaccines @Def: The number of children's vaccines to produce @Shape: ['Continuous'] 
NumChildVaccines = model.addVar(vtype=GRB.CONTINUOUS, name="NumChildVaccines")
# @Variable NumAdultVaccines @Def: The number of adult vaccines to produce @Shape: ['Continuous'] 
NumAdultVaccines = model.addVar(vtype=GRB.CONTINUOUS, name="NumAdultVaccines")

# Constraints 
# @Constraint Constr_1 @Def: The total mRNA used for children's and adult vaccines cannot exceed TotalMRNAAvailable.
model.addConstr(MRNAPerChildVaccine * NumChildVaccines + MRNAPerAdultVaccine * NumAdultVaccines <= TotalMRNAAvailable)
# @Constraint Constr_2 @Def: At least MinPercentageAdultVaccines percent of the total vaccines must be adult vaccines.
model.addConstr(NumAdultVaccines >= MinPercentageAdultVaccines * (NumAdultVaccines + NumChildVaccines))
# @Constraint Constr_3 @Def: At least MinChildVaccines children's vaccines must be produced.
model.addConstr(NumChildVaccines >= MinChildVaccines)

# Objective 
# @Objective Objective @Def: Minimize the total amount of fever suppressant used, which is calculated as (FeverSuppressantPerChildVaccine * NumberOfChildrenVaccines) + (FeverSuppressantPerAdultVaccine * NumberOfAdultVaccines).
model.setObjective(FeverSuppressantPerChildVaccine * NumChildVaccines + FeverSuppressantPerAdultVaccine * NumAdultVaccines, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumChildVaccines'] = NumChildVaccines.x
variables['NumAdultVaccines'] = NumAdultVaccines.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
