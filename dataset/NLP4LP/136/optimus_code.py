# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of beam bridges and truss bridges to maximize the total
mass supported, given that the total number of Popsicle sticks used for beam
bridges and truss bridges does not exceed TotalPopsicleSticks, the total units
of glue used for beam bridges and truss bridges does not exceed TotalGlue, the
number of truss bridges does not exceed MaxTrussBridges, and the number of beam
bridges is greater than the number of truss bridges.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/137/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalPopsicleSticks @Def: Total number of Popsicle sticks available @Shape: [] 
TotalPopsicleSticks = data['TotalPopsicleSticks']
# @Parameter PopsicleSticksPerBeamBridge @Def: Number of Popsicle sticks required to build one beam bridge @Shape: [] 
PopsicleSticksPerBeamBridge = data['PopsicleSticksPerBeamBridge']
# @Parameter PopsicleSticksPerTrussBridge @Def: Number of Popsicle sticks required to build one truss bridge @Shape: [] 
PopsicleSticksPerTrussBridge = data['PopsicleSticksPerTrussBridge']
# @Parameter TotalGlue @Def: Total units of glue available @Shape: [] 
TotalGlue = data['TotalGlue']
# @Parameter GluePerBeamBridge @Def: Units of glue required to build one beam bridge @Shape: [] 
GluePerBeamBridge = data['GluePerBeamBridge']
# @Parameter GluePerTrussBridge @Def: Units of glue required to build one truss bridge @Shape: [] 
GluePerTrussBridge = data['GluePerTrussBridge']
# @Parameter MaxTrussBridges @Def: Maximum number of truss bridges that can be built @Shape: [] 
MaxTrussBridges = data['MaxTrussBridges']
# @Parameter MassPerBeamBridge @Def: Mass that one beam bridge can hold @Shape: [] 
MassPerBeamBridge = data['MassPerBeamBridge']
# @Parameter MassPerTrussBridge @Def: Mass that one truss bridge can hold @Shape: [] 
MassPerTrussBridge = data['MassPerTrussBridge']

# Variables 
# @Variable BeamBridges @Def: The number of beam bridges to build @Shape: [] 
BeamBridges = model.addVar(vtype=GRB.INTEGER, name="BeamBridges")
# @Variable TrussBridges @Def: The number of truss bridges to build @Shape: [] 
TrussBridges = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxTrussBridges, name="TrussBridges")

# Constraints 
# @Constraint Constr_1 @Def: The total number of Popsicle sticks used for beam bridges and truss bridges does not exceed TotalPopsicleSticks.
model.addConstr(PopsicleSticksPerBeamBridge * BeamBridges + PopsicleSticksPerTrussBridge * TrussBridges <= TotalPopsicleSticks)
# @Constraint Constr_2 @Def: The total units of glue used for beam bridges and truss bridges does not exceed TotalGlue.
model.addConstr(GluePerBeamBridge * BeamBridges + GluePerTrussBridge * TrussBridges <= TotalGlue)
# @Constraint Constr_3 @Def: The number of truss bridges does not exceed MaxTrussBridges.
model.addConstr(TrussBridges <= MaxTrussBridges)
# @Constraint Constr_4 @Def: The number of beam bridges is greater than the number of truss bridges.
model.addConstr(BeamBridges >= TrussBridges + 1)

# Objective 
# @Objective Objective @Def: Maximize the total mass supported, which is the sum of the mass supported by beam bridges and truss bridges.
model.setObjective(MassPerBeamBridge * BeamBridges + MassPerTrussBridge * TrussBridges, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BeamBridges'] = BeamBridges.x
variables['TrussBridges'] = TrussBridges.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
