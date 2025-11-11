# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A water company sells glass and plastic bottles. Each glass bottle can hold
GlassBottleCapacity milliliters of water while each plastic bottle can hold
PlasticBottleCapacity milliliters of water. The number of plastic bottles must
be at least MinPlasticRatio times the number of glass bottles. There must be at
least MinGlassBottles glass bottles. The company has TotalWater milliliters of
water available. Determine the number of each type of bottle to maximize the
total number of bottles.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/78/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GlassBottleCapacity @Def: The capacity of a glass bottle in milliliters @Shape: [] 
GlassBottleCapacity = data['GlassBottleCapacity']
# @Parameter PlasticBottleCapacity @Def: The capacity of a plastic bottle in milliliters @Shape: [] 
PlasticBottleCapacity = data['PlasticBottleCapacity']
# @Parameter MinPlasticRatio @Def: The minimum ratio of plastic bottles to glass bottles @Shape: [] 
MinPlasticRatio = data['MinPlasticRatio']
# @Parameter MinGlassBottles @Def: The minimum number of glass bottles required @Shape: [] 
MinGlassBottles = data['MinGlassBottles']
# @Parameter TotalWater @Def: Total volume of water available in milliliters @Shape: [] 
TotalWater = data['TotalWater']

# Variables 
# @Variable PlasticBottles @Def: The number of plastic bottles @Shape: [] 
PlasticBottles = model.addVar(vtype=GRB.INTEGER, name="PlasticBottles")
# @Variable GlassBottles @Def: The number of glass bottles @Shape: [] 
GlassBottles = model.addVar(vtype=GRB.INTEGER, name="GlassBottles", lb=MinGlassBottles)

# Constraints 
# @Constraint Constr_1 @Def: The number of plastic bottles must be at least MinPlasticRatio times the number of glass bottles.
model.addConstr(PlasticBottles >= MinPlasticRatio * GlassBottles)
# @Constraint Constr_2 @Def: There must be at least MinGlassBottles glass bottles.
model.addConstr(GlassBottles >= MinGlassBottles)
# @Constraint Constr_3 @Def: The total volume of water used by the glass and plastic bottles must not exceed TotalWater milliliters.
model.addConstr(GlassBottles * GlassBottleCapacity + PlasticBottles * PlasticBottleCapacity <= TotalWater)

# Objective 
# @Objective Objective @Def: Maximize the total number of bottles, which is the sum of the number of glass bottles and plastic bottles.
model.setObjective(PlasticBottles + GlassBottles, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PlasticBottles'] = PlasticBottles.x
variables['GlassBottles'] = GlassBottles.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
