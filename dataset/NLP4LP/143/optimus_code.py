# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A lawn mowing service utilizes SmallTeams and LargeTeams. Each SmallTeam
requires EmployeesPerSmallTeam employees and can mow AreaMowedSmallTeam of lawn.
Each LargeTeam requires EmployeesPerLargeTeam employees and can mow
AreaMowedLargeTeam of lawn. The service has TotalEmployees available employees.
The number of SmallTeams must be at least RatioSmallToLargeTeams times the
number of LargeTeams. Additionally, there must be a minimum of MinLargeTeams
LargeTeams and at least MinSmallTeams SmallTeams. The objective is to determine
the optimal number of SmallTeams and LargeTeams to maximize the total area
mowed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/144/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter EmployeesPerSmallTeam @Def: Number of employees required per small team @Shape: [] 
EmployeesPerSmallTeam = data['EmployeesPerSmallTeam']
# @Parameter AreaMowedSmallTeam @Def: Area mowed by a small team @Shape: [] 
AreaMowedSmallTeam = data['AreaMowedSmallTeam']
# @Parameter EmployeesPerLargeTeam @Def: Number of employees required per large team @Shape: [] 
EmployeesPerLargeTeam = data['EmployeesPerLargeTeam']
# @Parameter AreaMowedLargeTeam @Def: Area mowed by a large team @Shape: [] 
AreaMowedLargeTeam = data['AreaMowedLargeTeam']
# @Parameter TotalEmployees @Def: Total number of employees available @Shape: [] 
TotalEmployees = data['TotalEmployees']
# @Parameter RatioSmallToLargeTeams @Def: Minimum ratio of small teams to large teams @Shape: [] 
RatioSmallToLargeTeams = data['RatioSmallToLargeTeams']
# @Parameter MinLargeTeams @Def: Minimum number of large teams @Shape: [] 
MinLargeTeams = data['MinLargeTeams']
# @Parameter MinSmallTeams @Def: Minimum number of small teams @Shape: [] 
MinSmallTeams = data['MinSmallTeams']

# Variables 
# @Variable SmallTeams @Def: The number of small teams @Shape: ['Integer'] 
SmallTeams = model.addVar(vtype=GRB.INTEGER, name="SmallTeams")
# @Variable LargeTeams @Def: The number of large teams @Shape: ['Integer'] 
LargeTeams = model.addVar(vtype=GRB.INTEGER, name="LargeTeams")

# Constraints 
# @Constraint Constr_1 @Def: The total number of employees required by SmallTeams and LargeTeams cannot exceed TotalEmployees.
model.addConstr(EmployeesPerSmallTeam * SmallTeams + EmployeesPerLargeTeam * LargeTeams <= TotalEmployees)
# @Constraint Constr_2 @Def: The number of SmallTeams must be at least RatioSmallToLargeTeams times the number of LargeTeams.
model.addConstr(SmallTeams >= RatioSmallToLargeTeams * LargeTeams)
# @Constraint Constr_3 @Def: There must be at least MinLargeTeams LargeTeams.
model.addConstr(LargeTeams >= MinLargeTeams)
# @Constraint Constr_4 @Def: There must be at least MinSmallTeams SmallTeams.
model.addConstr(SmallTeams >= MinSmallTeams)

# Objective 
# @Objective Objective @Def: Total area mowed is the sum of the areas mowed by SmallTeams and LargeTeams. The objective is to maximize the total area mowed.
model.setObjective(AreaMowedSmallTeam * SmallTeams + AreaMowedLargeTeam * LargeTeams, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallTeams'] = SmallTeams.x
variables['LargeTeams'] = LargeTeams.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
