# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company produces chairs and dressers. Each chair yields a profit of
ProfitPerChair, while each dresser yields a profit of ProfitPerDresser. Each
week, AvailableStain gallons of stain and AvailableOak lengths of oak wood are
available. Each chair requires StainPerChair gallons of stain and OakPerChair
lengths of oak wood, while each dresser requires StainPerDresser gallons of
stain and OakPerDresser lengths of oak wood. Determine the maximum profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/7/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitPerChair @Def: Profit per chair @Shape: [] 
ProfitPerChair = data['ProfitPerChair']
# @Parameter ProfitPerDresser @Def: Profit per dresser @Shape: [] 
ProfitPerDresser = data['ProfitPerDresser']
# @Parameter AvailableStain @Def: Available gallons of stain per week @Shape: [] 
AvailableStain = data['AvailableStain']
# @Parameter AvailableOak @Def: Available lengths of oak wood per week @Shape: [] 
AvailableOak = data['AvailableOak']
# @Parameter StainPerChair @Def: Gallons of stain required to produce one chair @Shape: [] 
StainPerChair = data['StainPerChair']
# @Parameter StainPerDresser @Def: Gallons of stain required to produce one dresser @Shape: [] 
StainPerDresser = data['StainPerDresser']
# @Parameter OakPerChair @Def: Lengths of oak wood required to produce one chair @Shape: [] 
OakPerChair = data['OakPerChair']
# @Parameter OakPerDresser @Def: Lengths of oak wood required to produce one dresser @Shape: [] 
OakPerDresser = data['OakPerDresser']

# Variables 
# @Variable NumberOfChairs @Def: The number of chairs produced per week @Shape: [] 
NumberOfChairs = model.addVar(vtype=GRB.INTEGER, name="NumberOfChairs")
# @Variable NumberOfDressers @Def: The number of dressers produced per week @Shape: [] 
NumberOfDressers = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfDressers")

# Constraints 
# @Constraint Constr_1 @Def: The total gallons of stain used for producing chairs and dressers cannot exceed AvailableStain per week.
model.addConstr(StainPerChair * NumberOfChairs + StainPerDresser * NumberOfDressers <= AvailableStain)
# @Constraint Constr_2 @Def: The total lengths of oak wood used for producing chairs and dressers cannot exceed AvailableOak per week.
model.addConstr(NumberOfChairs * OakPerChair + NumberOfDressers * OakPerDresser <= AvailableOak)
# @Constraint Constr_3 @Def: The number of chairs produced must be a non-negative integer.
model.addConstr(NumberOfChairs >= 0)
# @Constraint Constr_4 @Def: The number of dressers produced must be a non-negative integer.
model.addConstr(NumberOfDressers >= 0)

# Objective 
# @Objective Objective @Def: Maximize the total profit, which is ProfitPerChair multiplied by the number of chairs produced plus ProfitPerDresser multiplied by the number of dressers produced.
model.setObjective(ProfitPerChair * NumberOfChairs + ProfitPerDresser * NumberOfDressers, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfChairs'] = NumberOfChairs.x
variables['NumberOfDressers'] = NumberOfDressers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
