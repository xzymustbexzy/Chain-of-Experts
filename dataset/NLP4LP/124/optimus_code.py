# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the quantities of sulfate and ginger to add to the shampoo such that
the number of sulfate units is at least MinSulfateUnits, the combined number of
sulfate and ginger units equals TotalUnits, the number of sulfate units does not
exceed MaxSulfateToGingerRatio multiplied by the number of ginger units, one
ingredient is added before the other, and the total effective time, based on
TimePerUnitSulfate and TimePerUnitGinger, is minimized.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/125/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimePerUnitSulfate @Def: Time taken for one unit of sulfate to be effective @Shape: [] 
TimePerUnitSulfate = data['TimePerUnitSulfate']
# @Parameter TimePerUnitGinger @Def: Time taken for one unit of ginger to be effective @Shape: [] 
TimePerUnitGinger = data['TimePerUnitGinger']
# @Parameter MinSulfateUnits @Def: Minimum required units of sulfate @Shape: [] 
MinSulfateUnits = data['MinSulfateUnits']
# @Parameter TotalUnits @Def: Total units of sulfate and ginger @Shape: [] 
TotalUnits = data['TotalUnits']
# @Parameter MaxSulfateToGingerRatio @Def: Maximum allowed ratio of sulfate to ginger @Shape: [] 
MaxSulfateToGingerRatio = data['MaxSulfateToGingerRatio']

# Variables 
# @Variable SulfateUnits @Def: The number of sulfate units @Shape: [] 
SulfateUnits = model.addVar(vtype=GRB.INTEGER, lb=MinSulfateUnits, name="SulfateUnits")
# @Variable GingerUnits @Def: The number of ginger units @Shape: [] 
GingerUnits = model.addVar(vtype=GRB.INTEGER, name="GingerUnits")
# @Variable SulfateAddedFirst @Def: Binary variable indicating whether Sulfate is added before Ginger @Shape: ['binary'] 
SulfateAddedFirst = model.addVar(vtype=GRB.BINARY, name="SulfateAddedFirst")

# Constraints 
# @Constraint Constr_1 @Def: The number of sulfate units is at least MinSulfateUnits.
model.addConstr(SulfateUnits >= MinSulfateUnits)
# @Constraint Constr_2 @Def: The combined number of sulfate and ginger units equals TotalUnits.
model.addConstr(SulfateUnits + GingerUnits == TotalUnits)
# @Constraint Constr_3 @Def: The number of sulfate units does not exceed MaxSulfateToGingerRatio multiplied by the number of ginger units.
model.addConstr(SulfateUnits <= MaxSulfateToGingerRatio * GingerUnits)
# @Constraint Constr_4 @Def: One ingredient is added before the other.
model.addConstr(SulfateAddedFirst == 1)

# Objective 
# @Objective Objective @Def: Minimize the total effective time, calculated as (TimePerUnitSulfate * number of sulfate units) + (TimePerUnitGinger * number of ginger units).
model.setObjective(TimePerUnitSulfate * SulfateUnits + TimePerUnitGinger * GingerUnits, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SulfateUnits'] = SulfateUnits.x
variables['GingerUnits'] = GingerUnits.x
variables['SulfateAddedFirst'] = SulfateAddedFirst.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
