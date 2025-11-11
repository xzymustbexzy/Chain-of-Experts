# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The government uses wide pipes and narrow pipes to transport water. Each wide
pipe can carry WidePipeCapacity units of water per minute, and each narrow pipe
can carry NarrowPipeCapacity units of water per minute. The number of wide pipes
is restricted to at most MaxWideToNarrowRatio times the number of narrow pipes.
The system must transport at least MinTransportRequired units of water every
minute, and at least MinWidePipes wide pipes must be utilized. The objective is
to minimize the total number of pipes required.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/215/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter WidePipeCapacity @Def: Water transport capacity of a wide pipe (units per minute) @Shape: [] 
WidePipeCapacity = data['WidePipeCapacity']
# @Parameter NarrowPipeCapacity @Def: Water transport capacity of a narrow pipe (units per minute) @Shape: [] 
NarrowPipeCapacity = data['NarrowPipeCapacity']
# @Parameter MaxWideToNarrowRatio @Def: Maximum ratio of wide pipes to narrow pipes @Shape: [] 
MaxWideToNarrowRatio = data['MaxWideToNarrowRatio']
# @Parameter MinTransportRequired @Def: Minimum required water transported per minute @Shape: [] 
MinTransportRequired = data['MinTransportRequired']
# @Parameter MinWidePipes @Def: Minimum number of wide pipes required @Shape: [] 
MinWidePipes = data['MinWidePipes']

# Variables 
# @Variable WidePipes @Def: The number of wide pipes @Shape: ['Integer'] 
WidePipes = model.addVar(vtype=GRB.INTEGER, name="WidePipes")
# @Variable NarrowPipes @Def: The number of narrow pipes @Shape: ['Integer'] 
NarrowPipes = model.addVar(vtype=GRB.INTEGER, name="NarrowPipes")

# Constraints 
# @Constraint Constr_1 @Def: WidePipeCapacity * WidePipes + NarrowPipeCapacity * NarrowPipes >= MinTransportRequired
model.addConstr(WidePipeCapacity * WidePipes + NarrowPipeCapacity * NarrowPipes >= MinTransportRequired)
# @Constraint Constr_2 @Def: WidePipes <= MaxWideToNarrowRatio * NarrowPipes
model.addConstr(WidePipes <= MaxWideToNarrowRatio * NarrowPipes)
# @Constraint Constr_3 @Def: WidePipes >= MinWidePipes
model.addConstr(WidePipes >= MinWidePipes)

# Objective 
# @Objective Objective @Def: Minimize the total number of pipes required, which is WidePipes plus NarrowPipes.
model.setObjective(WidePipes + NarrowPipes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['WidePipes'] = WidePipes.x
variables['NarrowPipes'] = NarrowPipes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
