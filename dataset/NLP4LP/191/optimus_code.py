# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company manufactures desks and drawers. Each desk requires AssemblyTimeDesk
minutes of assembly and SandingTimeDesk minutes of sanding. Each drawer requires
AssemblyTimeDrawer minutes of assembly and SandingTimeDrawer minutes of sanding.
The company has TotalAssemblyTime minutes available for assembly and
TotalSandingTime minutes available for sanding. The profit per desk is
ProfitPerDesk and the profit per drawer is ProfitPerDrawer. Determine the number
of desks and drawers to produce to maximize profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/192/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AssemblyTimeDesk @Def: Minutes required for assembly per desk @Shape: [] 
AssemblyTimeDesk = data['AssemblyTimeDesk']
# @Parameter SandingTimeDesk @Def: Minutes required for sanding per desk @Shape: [] 
SandingTimeDesk = data['SandingTimeDesk']
# @Parameter AssemblyTimeDrawer @Def: Minutes required for assembly per drawer @Shape: [] 
AssemblyTimeDrawer = data['AssemblyTimeDrawer']
# @Parameter SandingTimeDrawer @Def: Minutes required for sanding per drawer @Shape: [] 
SandingTimeDrawer = data['SandingTimeDrawer']
# @Parameter TotalAssemblyTime @Def: Total available assembly minutes @Shape: [] 
TotalAssemblyTime = data['TotalAssemblyTime']
# @Parameter TotalSandingTime @Def: Total available sanding minutes @Shape: [] 
TotalSandingTime = data['TotalSandingTime']
# @Parameter ProfitPerDesk @Def: Profit per desk @Shape: [] 
ProfitPerDesk = data['ProfitPerDesk']
# @Parameter ProfitPerDrawer @Def: Profit per drawer @Shape: [] 
ProfitPerDrawer = data['ProfitPerDrawer']

# Variables 
# @Variable NumberOfDesks @Def: The number of desks to be produced @Shape: [] 
NumberOfDesks = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfDesks")
# @Variable NumberOfDrawers @Def: The number of drawers to be produced @Shape: [] 
NumberOfDrawers = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfDrawers")

# Constraints 
# @Constraint Constr_1 @Def: AssemblyTimeDesk multiplied by the number of desks plus AssemblyTimeDrawer multiplied by the number of drawers must not exceed TotalAssemblyTime.
model.addConstr(AssemblyTimeDesk * NumberOfDesks + AssemblyTimeDrawer * NumberOfDrawers <= TotalAssemblyTime)
# @Constraint Constr_2 @Def: SandingTimeDesk multiplied by the number of desks plus SandingTimeDrawer multiplied by the number of drawers must not exceed TotalSandingTime.
model.addConstr(SandingTimeDesk * NumberOfDesks + SandingTimeDrawer * NumberOfDrawers <= TotalSandingTime)

# Objective 
# @Objective Objective @Def: Maximize the total profit, which is ProfitPerDesk multiplied by the number of desks plus ProfitPerDrawer multiplied by the number of drawers.
model.setObjective(ProfitPerDesk * NumberOfDesks + ProfitPerDrawer * NumberOfDrawers, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfDesks'] = NumberOfDesks.x
variables['NumberOfDrawers'] = NumberOfDrawers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
