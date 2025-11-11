# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A singer plans to hold pop and R&B concerts. Each pop concert attracts
AudiencePop audience members and requires PracticeDaysPop practice days. Each
R&B concert attracts AudienceRnB audience members and requires PracticeDaysRnB
practice days. The singer must attract at least MinAudience audience members and
has TotalPracticeDays available for practice. Additionally, no more than
MaxRnBProportion proportion of the total concerts can be R&B. The objective is
to determine the number of pop and R&B concerts that minimizes the total number
of concerts.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/227/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AudiencePop @Def: Audience members brought in by one pop concert @Shape: [] 
AudiencePop = data['AudiencePop']
# @Parameter AudienceRnB @Def: Audience members brought in by one R&B concert @Shape: [] 
AudienceRnB = data['AudienceRnB']
# @Parameter PracticeDaysPop @Def: Number of practice days required for one pop concert @Shape: [] 
PracticeDaysPop = data['PracticeDaysPop']
# @Parameter PracticeDaysRnB @Def: Number of practice days required for one R&B concert @Shape: [] 
PracticeDaysRnB = data['PracticeDaysRnB']
# @Parameter MinAudience @Def: Minimum required audience members @Shape: [] 
MinAudience = data['MinAudience']
# @Parameter TotalPracticeDays @Def: Total available practice days @Shape: [] 
TotalPracticeDays = data['TotalPracticeDays']
# @Parameter MaxRnBProportion @Def: Maximum proportion of concerts that can be R&B @Shape: [] 
MaxRnBProportion = data['MaxRnBProportion']

# Variables 
# @Variable NumPopConcerts @Def: The number of pop concerts @Shape: [] 
NumPopConcerts = model.addVar(vtype=GRB.INTEGER, name="NumPopConcerts")
# @Variable NumRnBConcerts @Def: The number of R&B concerts @Shape: [] 
NumRnBConcerts = model.addVar(vtype=GRB.INTEGER, name="NumRnBConcerts")

# Constraints 
# @Constraint Constr_1 @Def: The total audience attracted by pop and R&B concerts must be at least MinAudience.
model.addConstr(AudiencePop * NumPopConcerts + AudienceRnB * NumRnBConcerts >= MinAudience, "AudienceConstraint")
# @Constraint Constr_2 @Def: The total practice days required for pop and R&B concerts must not exceed TotalPracticeDays.
model.addConstr(NumPopConcerts * PracticeDaysPop + NumRnBConcerts * PracticeDaysRnB <= TotalPracticeDays)
# @Constraint Constr_3 @Def: R&B concerts must not exceed MaxRnBProportion of the total number of concerts.
model.addConstr(NumRnBConcerts <= MaxRnBProportion * (NumPopConcerts + NumRnBConcerts))

# Objective 
# @Objective Objective @Def: Minimize the total number of pop and R&B concerts.
model.setObjective(NumPopConcerts + NumRnBConcerts, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPopConcerts'] = NumPopConcerts.x
variables['NumRnBConcerts'] = NumRnBConcerts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
