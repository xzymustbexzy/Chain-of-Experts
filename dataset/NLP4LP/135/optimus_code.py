# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Determine the number of blueberry packs and strawberry packs to minimize the
total sugar intake, where total sugar is the product of SugarPerBlueberryPack
and the number of blueberry packs plus the product of SugarPerStrawberryPack and
the number of strawberry packs. Ensure that the total anti-oxidants, calculated
as AntiOxidantsPerBlueberryPack multiplied by the number of blueberry packs plus
AntiOxidantsPerStrawberryPack multiplied by the number of strawberry packs, is
at least MinimumAntiOxidants. Similarly, the total minerals, calculated as
MineralsPerBlueberryPack multiplied by the number of blueberry packs plus
MineralsPerStrawberryPack multiplied by the number of strawberry packs, meets or
exceeds MinimumMinerals. Additionally, the number of strawberry packs must be at
least MinimumStrawberriesToBlueberriesRatio times the number of blueberry packs.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/136/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AntiOxidantsPerBlueberryPack @Def: Units of anti-oxidants per pack of blueberries @Shape: [] 
AntiOxidantsPerBlueberryPack = data['AntiOxidantsPerBlueberryPack']
# @Parameter AntiOxidantsPerStrawberryPack @Def: Units of anti-oxidants per pack of strawberries @Shape: [] 
AntiOxidantsPerStrawberryPack = data['AntiOxidantsPerStrawberryPack']
# @Parameter MineralsPerBlueberryPack @Def: Units of minerals per pack of blueberries @Shape: [] 
MineralsPerBlueberryPack = data['MineralsPerBlueberryPack']
# @Parameter MineralsPerStrawberryPack @Def: Units of minerals per pack of strawberries @Shape: [] 
MineralsPerStrawberryPack = data['MineralsPerStrawberryPack']
# @Parameter SugarPerBlueberryPack @Def: Grams of sugar per pack of blueberries @Shape: [] 
SugarPerBlueberryPack = data['SugarPerBlueberryPack']
# @Parameter SugarPerStrawberryPack @Def: Grams of sugar per pack of strawberries @Shape: [] 
SugarPerStrawberryPack = data['SugarPerStrawberryPack']
# @Parameter MinimumAntiOxidants @Def: Minimum required units of anti-oxidants @Shape: [] 
MinimumAntiOxidants = data['MinimumAntiOxidants']
# @Parameter MinimumMinerals @Def: Minimum required units of minerals @Shape: [] 
MinimumMinerals = data['MinimumMinerals']
# @Parameter MinimumStrawberriesToBlueberriesRatio @Def: Minimum ratio of strawberries packs to blueberry packs @Shape: [] 
MinimumStrawberriesToBlueberriesRatio = data['MinimumStrawberriesToBlueberriesRatio']

# Variables 
# @Variable NumberOfBlueberryPacks @Def: The number of blueberry packs @Shape: [] 
NumberOfBlueberryPacks = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfBlueberryPacks")
# @Variable NumberOfStrawberryPacks @Def: The number of strawberry packs @Shape: [] 
NumberOfStrawberryPacks = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfStrawberryPacks")

# Constraints 
# @Constraint Constr_1 @Def: The total anti-oxidants, calculated as AntiOxidantsPerBlueberryPack multiplied by the number of blueberry packs plus AntiOxidantsPerStrawberryPack multiplied by the number of strawberry packs, is at least MinimumAntiOxidants.
model.addConstr(AntiOxidantsPerBlueberryPack * NumberOfBlueberryPacks + AntiOxidantsPerStrawberryPack * NumberOfStrawberryPacks >= MinimumAntiOxidants)
# @Constraint Constr_2 @Def: The total minerals, calculated as MineralsPerBlueberryPack multiplied by the number of blueberry packs plus MineralsPerStrawberryPack multiplied by the number of strawberry packs, meets or exceeds MinimumMinerals.
model.addConstr(MineralsPerBlueberryPack * NumberOfBlueberryPacks + MineralsPerStrawberryPack * NumberOfStrawberryPacks >= MinimumMinerals)
# @Constraint Constr_3 @Def: The number of strawberry packs must be at least MinimumStrawberriesToBlueberriesRatio times the number of blueberry packs.
model.addConstr(NumberOfStrawberryPacks >= MinimumStrawberriesToBlueberriesRatio * NumberOfBlueberryPacks)

# Objective 
# @Objective Objective @Def: Total sugar intake is the product of SugarPerBlueberryPack and the number of blueberry packs plus the product of SugarPerStrawberryPack and the number of strawberry packs. The objective is to minimize the total sugar intake.
model.setObjective(SugarPerBlueberryPack * NumberOfBlueberryPacks + SugarPerStrawberryPack * NumberOfStrawberryPacks, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBlueberryPacks'] = NumberOfBlueberryPacks.x
variables['NumberOfStrawberryPacks'] = NumberOfStrawberryPacks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
