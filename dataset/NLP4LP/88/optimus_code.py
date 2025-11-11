# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
The company produces two types of candy packs: peach and cherry. Each pack of
peach candy requires PeachFlavoringPerPack units of peach flavoring and
SpecialSyrupPerPackPeach units of special syrup. Each pack of cherry candy
requires CherryFlavoringPerPack units of cherry flavoring and
SpecialSyrupPerPackCherry units of special syrup. The company has
AvailablePeachFlavoring units of peach flavoring and AvailableCherryFlavoring
units of cherry flavoring available. The number of peach candy packs produced
must be greater than the number of cherry candy packs, and at least
MinimumCherryPercentage fraction of the total packs must be cherry flavored. The
objective is to determine the number of each type of pack to minimize the total
amount of special syrup used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/89/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AvailablePeachFlavoring @Def: Units of peach flavoring available @Shape: [] 
AvailablePeachFlavoring = data['AvailablePeachFlavoring']
# @Parameter AvailableCherryFlavoring @Def: Units of cherry flavoring available @Shape: [] 
AvailableCherryFlavoring = data['AvailableCherryFlavoring']
# @Parameter PeachFlavoringPerPack @Def: Units of peach flavoring required per pack of peach candy @Shape: [] 
PeachFlavoringPerPack = data['PeachFlavoringPerPack']
# @Parameter CherryFlavoringPerPack @Def: Units of cherry flavoring required per pack of cherry candy @Shape: [] 
CherryFlavoringPerPack = data['CherryFlavoringPerPack']
# @Parameter SpecialSyrupPerPackPeach @Def: Units of special syrup required per pack of peach candy @Shape: [] 
SpecialSyrupPerPackPeach = data['SpecialSyrupPerPackPeach']
# @Parameter SpecialSyrupPerPackCherry @Def: Units of special syrup required per pack of cherry candy @Shape: [] 
SpecialSyrupPerPackCherry = data['SpecialSyrupPerPackCherry']
# @Parameter MinimumCherryPercentage @Def: Minimum fraction of packs that must be cherry flavored @Shape: [] 
MinimumCherryPercentage = data['MinimumCherryPercentage']

# Variables 
# @Variable NumberOfPeachPacks @Def: The number of peach packs to produce @Shape: [] 
NumberOfPeachPacks = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfPeachPacks")
# @Variable NumberOfCherryPacks @Def: The number of cherry packs to produce @Shape: [] 
NumberOfCherryPacks = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfCherryPacks")

# Constraints 
# @Constraint Constr_1 @Def: The total peach flavoring used (PeachFlavoringPerPack * number of peach packs) must not exceed AvailablePeachFlavoring.
model.addConstr(PeachFlavoringPerPack * NumberOfPeachPacks <= AvailablePeachFlavoring)
# @Constraint Constr_2 @Def: The total cherry flavoring used (CherryFlavoringPerPack * number of cherry packs) must not exceed AvailableCherryFlavoring.
model.addConstr(CherryFlavoringPerPack * NumberOfCherryPacks <= AvailableCherryFlavoring)
# @Constraint Constr_3 @Def: The number of peach candy packs produced must be greater than the number of cherry candy packs produced.
model.addConstr(NumberOfPeachPacks >= NumberOfCherryPacks)
# @Constraint Constr_4 @Def: At least MinimumCherryPercentage fraction of the total candy packs produced must be cherry flavored.
model.addConstr(NumberOfCherryPacks >= MinimumCherryPercentage * (NumberOfCherryPacks + NumberOfPeachPacks))

# Objective 
# @Objective Objective @Def: Minimize the total amount of special syrup used, which is calculated as (SpecialSyrupPerPackPeach * number of peach packs) + (SpecialSyrupPerPackCherry * number of cherry packs).
model.setObjective(SpecialSyrupPerPackPeach * NumberOfPeachPacks + SpecialSyrupPerPackCherry * NumberOfCherryPacks, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfPeachPacks'] = NumberOfPeachPacks.x
variables['NumberOfCherryPacks'] = NumberOfCherryPacks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
