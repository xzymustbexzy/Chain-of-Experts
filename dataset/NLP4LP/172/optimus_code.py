# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A tourist spot provides two transportation options: hot-air balloons and gondola
lifts. Each hot-air balloon carries VisitorsPerBalloon visitors and generates
PollutionPerBalloon pollution units per ride, while each gondola lift carries
VisitorsPerGondola visitors and generates PollutionPerGondola pollution units
per ride. The number of hot-air balloon rides is limited to MaxBalloonRides, and
a minimum of MinVisitors visitors must be transported. The objective is to
minimize the total pollution produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/173/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VisitorsPerBalloon @Def: Number of visitors that can be carried by one hot-air balloon @Shape: [] 
VisitorsPerBalloon = data['VisitorsPerBalloon']
# @Parameter VisitorsPerGondola @Def: Number of visitors that can be carried by one gondola lift @Shape: [] 
VisitorsPerGondola = data['VisitorsPerGondola']
# @Parameter PollutionPerBalloon @Def: Units of pollution produced by one hot-air balloon ride @Shape: [] 
PollutionPerBalloon = data['PollutionPerBalloon']
# @Parameter PollutionPerGondola @Def: Units of pollution produced by one gondola lift ride @Shape: [] 
PollutionPerGondola = data['PollutionPerGondola']
# @Parameter MaxBalloonRides @Def: Maximum number of hot-air balloon rides allowed @Shape: [] 
MaxBalloonRides = data['MaxBalloonRides']
# @Parameter MinVisitors @Def: Minimum number of visitors that need to be transported @Shape: [] 
MinVisitors = data['MinVisitors']

# Variables 
# @Variable BalloonRides @Def: The number of hot-air balloon rides @Shape: ['Integer'] 
BalloonRides = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxBalloonRides, name="BalloonRides")
# @Variable GondolaLifts @Def: The number of gondola lift rides @Shape: ['Integer'] 
GondolaLifts = model.addVar(vtype=GRB.INTEGER, name="GondolaLifts")

# Constraints 
# @Constraint Constr_1 @Def: The number of hot-air balloon rides cannot exceed MaxBalloonRides.
model.addConstr(BalloonRides <= MaxBalloonRides)
# @Constraint Constr_2 @Def: A minimum of MinVisitors visitors must be transported using hot-air balloons and gondola lifts.
model.addConstr(VisitorsPerBalloon * BalloonRides + VisitorsPerGondola * GondolaLifts >= MinVisitors)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total pollution produced by the transportation options.
model.setObjective(PollutionPerBalloon * BalloonRides + PollutionPerGondola * GondolaLifts, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BalloonRides'] = BalloonRides.x
variables['GondolaLifts'] = GondolaLifts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
