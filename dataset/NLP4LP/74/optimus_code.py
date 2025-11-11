# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A man fishes in a lake of TotalLakeArea acres and can catch fish either using a
net or fishing line. For each acre of the lake, using a net will catch
FishPerAcreNet fish and requires BaitPerAcreNet units of bait but also causes
PainPerAcreNet units of pain for the fisherman. For each acre of the lake, using
a fishing line will catch FishPerAcreLine fish and requires BaitPerAcreLine
units of bait but also causes PainPerAcreLine units of pain for the fisherman.
The fisherman has available TotalAvailableBait units of bait and can tolerate at
most MaxTotalPain units of pain. Determine the number of acres to allocate to
each fishing method to maximize the number of fish caught.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/75/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalLakeArea @Def: Total area of the lake in acres @Shape: [] 
TotalLakeArea = data['TotalLakeArea']
# @Parameter FishPerAcreNet @Def: Number of fish caught per acre using a net @Shape: [] 
FishPerAcreNet = data['FishPerAcreNet']
# @Parameter BaitPerAcreNet @Def: Units of bait required per acre using a net @Shape: [] 
BaitPerAcreNet = data['BaitPerAcreNet']
# @Parameter PainPerAcreNet @Def: Units of pain caused per acre using a net @Shape: [] 
PainPerAcreNet = data['PainPerAcreNet']
# @Parameter FishPerAcreLine @Def: Number of fish caught per acre using a fishing line @Shape: [] 
FishPerAcreLine = data['FishPerAcreLine']
# @Parameter BaitPerAcreLine @Def: Units of bait required per acre using a fishing line @Shape: [] 
BaitPerAcreLine = data['BaitPerAcreLine']
# @Parameter PainPerAcreLine @Def: Units of pain caused per acre using a fishing line @Shape: [] 
PainPerAcreLine = data['PainPerAcreLine']
# @Parameter TotalAvailableBait @Def: Total available units of bait @Shape: [] 
TotalAvailableBait = data['TotalAvailableBait']
# @Parameter MaxTotalPain @Def: Maximum tolerable units of pain @Shape: [] 
MaxTotalPain = data['MaxTotalPain']

# Variables 
# @Variable AcresNet @Def: Number of acres allocated to net @Shape: ['Continuous'] 
AcresNet = model.addVar(vtype=GRB.CONTINUOUS, name="AcresNet")
# @Variable AcresLine @Def: Number of acres allocated to fishing line @Shape: ['Continuous'] 
AcresLine = model.addVar(vtype=GRB.CONTINUOUS, name="AcresLine")

# Constraints 
# @Constraint Constr_1 @Def: The total number of acres allocated to net and fishing line must equal TotalLakeArea.
model.addConstr(AcresNet + AcresLine == TotalLakeArea)
# @Constraint Constr_2 @Def: The total bait used by net and fishing line cannot exceed TotalAvailableBait units.
model.addConstr(BaitPerAcreNet * AcresNet + BaitPerAcreLine * AcresLine <= TotalAvailableBait)
# @Constraint Constr_3 @Def: The total pain caused by net and fishing line cannot exceed MaxTotalPain units.
model.addConstr(PainPerAcreNet * AcresNet + PainPerAcreLine * AcresLine <= MaxTotalPain)

# Objective 
# @Objective Objective @Def: The total number of fish caught is the sum of the fish caught using net and fishing line. The objective is to maximize the total number of fish caught while adhering to constraints on bait usage and pain tolerance.
model.setObjective(FishPerAcreNet * AcresNet + FishPerAcreLine * AcresLine, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AcresNet'] = AcresNet.x
variables['AcresLine'] = AcresLine.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
