# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An accounting firm employs full time workers and part time workers. Each full
time worker works FullTimeHoursPerShift hours per shift and is paid
FullTimePayPerShift per shift, while each part time worker works
PartTimeHoursPerShift hours per shift and is paid PartTimePayPerShift per shift.
The firm has a project requiring LaborHoursRequired hours of labor and has a
budget of TotalBudget. The firm should schedule a number of full time and part
time workers to minimize the total number of workers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/80/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter FullTimeHoursPerShift @Def: The number of hours a full time worker works per shift @Shape: [] 
FullTimeHoursPerShift = data['FullTimeHoursPerShift']
# @Parameter PartTimeHoursPerShift @Def: The number of hours a part time worker works per shift @Shape: [] 
PartTimeHoursPerShift = data['PartTimeHoursPerShift']
# @Parameter FullTimePayPerShift @Def: The amount paid to a full time worker per shift @Shape: [] 
FullTimePayPerShift = data['FullTimePayPerShift']
# @Parameter PartTimePayPerShift @Def: The amount paid to a part time worker per shift @Shape: [] 
PartTimePayPerShift = data['PartTimePayPerShift']
# @Parameter LaborHoursRequired @Def: The total labor hours required for the project @Shape: [] 
LaborHoursRequired = data['LaborHoursRequired']
# @Parameter TotalBudget @Def: The total budget available for labor costs @Shape: [] 
TotalBudget = data['TotalBudget']

# Variables 
# @Variable NumFullTimeWorkers @Def: The number of full-time workers @Shape: [] 
NumFullTimeWorkers = model.addVar(vtype=GRB.INTEGER, name="NumFullTimeWorkers")
# @Variable NumPartTimeWorkers @Def: The number of part-time workers @Shape: [] 
NumPartTimeWorkers = model.addVar(vtype=GRB.INTEGER, name="NumPartTimeWorkers")

# Constraints 
# @Constraint Constr_1 @Def: The total labor hours provided by full-time workers and part-time workers must meet or exceed LaborHoursRequired.
model.addConstr(FullTimeHoursPerShift * NumFullTimeWorkers + PartTimeHoursPerShift * NumPartTimeWorkers >= LaborHoursRequired)
# @Constraint Constr_2 @Def: The total labor costs for full-time workers and part-time workers must not exceed TotalBudget.
model.addConstr(NumFullTimeWorkers * FullTimePayPerShift + NumPartTimeWorkers * PartTimePayPerShift <= TotalBudget)

# Objective 
# @Objective Objective @Def: Minimize the total number of workers, which is the sum of full-time and part-time workers.
model.setObjective(NumFullTimeWorkers + NumPartTimeWorkers, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumFullTimeWorkers'] = NumFullTimeWorkers.x
variables['NumPartTimeWorkers'] = NumPartTimeWorkers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
