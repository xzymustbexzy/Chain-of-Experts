# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A magic school sends letters to students using carrier pigeons and owls. Each
carrier pigeon can carry PigeonLetterCapacity letters per trip and requires
PigeonTreatCost treats for service. Each owl can carry OwlLetterCapacity letters
per trip and requires OwlTreatCost treats for service. At most MaxOwlProportion
of the total birds can be owls. The school has TotalTreats treats available. At
least MinPigeons carrier pigeons must be used. The goal is to determine the
number of carrier pigeons and owls to maximize the total number of letters sent.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/185/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PigeonLetterCapacity @Def: The number of letters a carrier pigeon can carry at a time @Shape: [] 
PigeonLetterCapacity = data['PigeonLetterCapacity']
# @Parameter PigeonTreatCost @Def: The number of treats required for a carrier pigeon's service @Shape: [] 
PigeonTreatCost = data['PigeonTreatCost']
# @Parameter OwlLetterCapacity @Def: The number of letters an owl can carry at a time @Shape: [] 
OwlLetterCapacity = data['OwlLetterCapacity']
# @Parameter OwlTreatCost @Def: The number of treats required for an owl's service @Shape: [] 
OwlTreatCost = data['OwlTreatCost']
# @Parameter MaxOwlProportion @Def: The maximum proportion of birds that can be owls @Shape: [] 
MaxOwlProportion = data['MaxOwlProportion']
# @Parameter TotalTreats @Def: The total number of treats available @Shape: [] 
TotalTreats = data['TotalTreats']
# @Parameter MinPigeons @Def: The minimum number of carrier pigeons that must be used @Shape: [] 
MinPigeons = data['MinPigeons']

# Variables 
# @Variable NumPigeons @Def: The number of carrier pigeons used @Shape: [] 
NumPigeons = model.addVar(vtype=GRB.INTEGER, name="NumPigeons")
# @Variable NumOwls @Def: The number of owls used @Shape: [] 
NumOwls = model.addVar(vtype=GRB.INTEGER, name="NumOwls")

# Constraints 
# @Constraint Constr_1 @Def: The total number of treats required for carrier pigeons and owls must not exceed TotalTreats.
model.addConstr(PigeonTreatCost * NumPigeons + OwlTreatCost * NumOwls <= TotalTreats, "TotalTreats")
# @Constraint Constr_2 @Def: The number of owls used must be at most MaxOwlProportion of the total number of birds.
model.addConstr(NumOwls <= MaxOwlProportion * (NumOwls + NumPigeons))
# @Constraint Constr_3 @Def: At least MinPigeons carrier pigeons must be used.
model.addConstr(NumPigeons >= MinPigeons)

# Objective 
# @Objective Objective @Def: Maximize the total number of letters sent, which is the sum of letters carried by carrier pigeons and owls.
model.setObjective(NumPigeons * PigeonLetterCapacity + NumOwls * OwlLetterCapacity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPigeons'] = NumPigeons.x
variables['NumOwls'] = NumOwls.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
