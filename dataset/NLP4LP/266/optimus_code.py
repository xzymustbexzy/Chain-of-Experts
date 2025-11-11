# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A manufacturer produces two types of keyboards: mechanical and standard. The
number of mechanical keyboards should be MechanicalToStandardRatio times the
number of standard keyboards. Each mechanical keyboard requires
PlasticCostMechanical units of plastic and SolderCostMechanical units of solder,
while each standard keyboard requires PlasticCostStandard units of plastic and
SolderCostStandard units of solder. The total available plastic is
TotalPlasticAvailable units and the total available solder is
TotalSolderAvailable units. Additionally, the production of standard keyboards
must be at least MinimumStandardKeyboards units. The objective is to maximize
the total number of keyboards produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/267/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProductTypes @Def: Number of different product types @Shape: [] 
NumProductTypes = data['NumProductTypes']
# @Parameter PlasticCostMechanical @Def: Units of plastic required to produce one mechanical keyboard @Shape: [] 
PlasticCostMechanical = data['PlasticCostMechanical']
# @Parameter PlasticCostStandard @Def: Units of plastic required to produce one standard keyboard @Shape: [] 
PlasticCostStandard = data['PlasticCostStandard']
# @Parameter SolderCostMechanical @Def: Units of solder required to produce one mechanical keyboard @Shape: [] 
SolderCostMechanical = data['SolderCostMechanical']
# @Parameter SolderCostStandard @Def: Units of solder required to produce one standard keyboard @Shape: [] 
SolderCostStandard = data['SolderCostStandard']
# @Parameter MechanicalToStandardRatio @Def: Desired ratio of mechanical keyboards to standard keyboards @Shape: [] 
MechanicalToStandardRatio = data['MechanicalToStandardRatio']
# @Parameter MinimumStandardKeyboards @Def: Minimum number of standard keyboards to be produced @Shape: [] 
MinimumStandardKeyboards = data['MinimumStandardKeyboards']
# @Parameter TotalPlasticAvailable @Def: Total units of plastic available @Shape: [] 
TotalPlasticAvailable = data['TotalPlasticAvailable']
# @Parameter TotalSolderAvailable @Def: Total units of solder available @Shape: [] 
TotalSolderAvailable = data['TotalSolderAvailable']

# Variables 
# @Variable NumberMechanicalKeyboards @Def: The number of mechanical keyboards @Shape: [] 
NumberMechanicalKeyboards = model.addVar(vtype=GRB.CONTINUOUS, name="NumberMechanicalKeyboards")
# @Variable NumberStandardKeyboards @Def: The number of standard keyboards @Shape: [] 
NumberStandardKeyboards = model.addVar(vtype=GRB.CONTINUOUS, name="NumberStandardKeyboards")

# Constraints 
# @Constraint Constr_1 @Def: The number of mechanical keyboards is equal to MechanicalToStandardRatio times the number of standard keyboards.
model.addConstr(NumberMechanicalKeyboards == MechanicalToStandardRatio * NumberStandardKeyboards)
# @Constraint Constr_2 @Def: PlasticCostMechanical multiplied by the number of mechanical keyboards plus PlasticCostStandard multiplied by the number of standard keyboards does not exceed TotalPlasticAvailable units of plastic.
model.addConstr(PlasticCostMechanical * NumberMechanicalKeyboards + PlasticCostStandard * NumberStandardKeyboards <= TotalPlasticAvailable)
# @Constraint Constr_3 @Def: SolderCostMechanical multiplied by the number of mechanical keyboards plus SolderCostStandard multiplied by the number of standard keyboards does not exceed TotalSolderAvailable units of solder.
model.addConstr(SolderCostMechanical * NumberMechanicalKeyboards + SolderCostStandard * NumberStandardKeyboards <= TotalSolderAvailable)
# @Constraint Constr_4 @Def: The number of standard keyboards produced is at least MinimumStandardKeyboards.
model.addConstr(NumberStandardKeyboards >= MinimumStandardKeyboards)

# Objective 
# @Objective Objective @Def: Maximize the total number of keyboards produced.
model.setObjective(NumberMechanicalKeyboards + NumberStandardKeyboards, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberMechanicalKeyboards'] = NumberMechanicalKeyboards.x
variables['NumberStandardKeyboards'] = NumberStandardKeyboards.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
