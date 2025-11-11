# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A village delivers mail to nearby villages either by runners or canoeers.
Runners can carry RunnerCapacity bags of mail each trip and take RunnerTime
hours. Canoeers can carry CanoeCapacity bags of mail each trip and take
CanoeTime hours. At most MaxCanoePercentage of deliveries can be made by canoe.
Additionally, the village can spare at most MaxTotalHours total hours for
deliveries and must use at least MinRunners runners. The objective is to
determine the number of trips by runners and canoeers to maximize the total
amount of mail delivered.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/259/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter RunnerCapacity @Def: Number of bags a runner can carry each trip @Shape: [] 
RunnerCapacity = data['RunnerCapacity']
# @Parameter RunnerTime @Def: Time a runner takes per trip (in hours) @Shape: [] 
RunnerTime = data['RunnerTime']
# @Parameter CanoeCapacity @Def: Number of bags a canoeer can carry each trip @Shape: [] 
CanoeCapacity = data['CanoeCapacity']
# @Parameter CanoeTime @Def: Time a canoeer takes per trip (in hours) @Shape: [] 
CanoeTime = data['CanoeTime']
# @Parameter MaxCanoePercentage @Def: Maximum fraction of total deliveries that can be made by canoe @Shape: [] 
MaxCanoePercentage = data['MaxCanoePercentage']
# @Parameter MaxTotalHours @Def: Maximum total hours the village can spare for deliveries @Shape: [] 
MaxTotalHours = data['MaxTotalHours']
# @Parameter MinRunners @Def: Minimum number of runners that must be used @Shape: [] 
MinRunners = data['MinRunners']

# Variables 
# @Variable NumRunnerTrips @Def: Number of trips made by runners @Shape: ['Integer'] 
NumRunnerTrips = model.addVar(vtype=GRB.INTEGER, name="NumRunnerTrips")
# @Variable NumCanoeTrips @Def: Number of trips made by canoeers @Shape: ['Integer'] 
NumCanoeTrips = model.addVar(vtype=GRB.INTEGER, name="NumCanoeTrips")
# @Variable NumberOfRunners @Def: The number of runners used for deliveries @Shape: ['Integer'] 
NumberOfRunners = model.addVar(vtype=GRB.INTEGER, lb=MinRunners, name="NumberOfRunners")

# Constraints 
# @Constraint Constr_1 @Def: The total hours spent on deliveries by runners and canoeers must not exceed MaxTotalHours.
model.addConstr(RunnerTime * NumRunnerTrips + CanoeTime * NumCanoeTrips <= MaxTotalHours)
# @Constraint Constr_2 @Def: No more than MaxCanoePercentage of the total mail delivered can be delivered by canoeers.
model.addConstr(NumCanoeTrips * CanoeCapacity <= MaxCanoePercentage * (NumRunnerTrips * RunnerCapacity + NumCanoeTrips * CanoeCapacity))
# @Constraint Constr_3 @Def: At least MinRunners runners must be used for deliveries.
model.addConstr(NumberOfRunners >= MinRunners)

# Objective 
# @Objective Objective @Def: Maximize the total amount of mail delivered by runners and canoeers within the given time, capacity, and usage constraints.
model.setObjective(NumRunnerTrips * RunnerCapacity + NumCanoeTrips * CanoeCapacity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumRunnerTrips'] = NumRunnerTrips.x
variables['NumCanoeTrips'] = NumCanoeTrips.x
variables['NumberOfRunners'] = NumberOfRunners.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
