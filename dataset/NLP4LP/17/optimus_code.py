# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
An electronics store seeks to determine the optimal quantities of two types of
products to maintain in inventory to maximize profit. Each unit of the first
product yields ProfitPhone in profit, while each unit of the second product
yields ProfitLaptop in profit. The first product requires SpacePhone square feet
of floor space, and the second product requires SpaceLaptop square feet of floor
space. The store has a total of TotalSpace square feet of available floor space.
The inventory is limited to these two products only, with a corporate
requirement that at least MinLaptopPercentage of all stocked products must be
the second product. Additionally, each unit of the first product costs CostPhone
and each unit of the second product costs CostLaptop, with the total expenditure
not exceeding MaxBudget. Formulate a linear programming model to maximize the
store's profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/18/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitPhone @Def: Profit earned per phone @Shape: [] 
ProfitPhone = data['ProfitPhone']
# @Parameter ProfitLaptop @Def: Profit earned per laptop @Shape: [] 
ProfitLaptop = data['ProfitLaptop']
# @Parameter SpacePhone @Def: Floor space required per phone (sq ft) @Shape: [] 
SpacePhone = data['SpacePhone']
# @Parameter SpaceLaptop @Def: Floor space required per laptop (sq ft) @Shape: [] 
SpaceLaptop = data['SpaceLaptop']
# @Parameter TotalSpace @Def: Total available floor space (sq ft) @Shape: [] 
TotalSpace = data['TotalSpace']
# @Parameter MinLaptopPercentage @Def: Minimum percentage of laptops required in inventory @Shape: [] 
MinLaptopPercentage = data['MinLaptopPercentage']
# @Parameter CostPhone @Def: Cost per phone @Shape: [] 
CostPhone = data['CostPhone']
# @Parameter CostLaptop @Def: Cost per laptop @Shape: [] 
CostLaptop = data['CostLaptop']
# @Parameter MaxBudget @Def: Maximum total budget @Shape: [] 
MaxBudget = data['MaxBudget']

# Variables 
# @Variable NumberOfPhones @Def: The number of phones @Shape: ['NonNegative'] 
NumberOfPhones = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfPhones")
# @Variable NumberOfLaptops @Def: The number of laptops @Shape: ['NonNegative'] 
NumberOfLaptops = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfLaptops")

# Constraints 
# @Constraint Constr_1 @Def: The total floor space used by phones and laptops must not exceed TotalSpace square feet.
model.addConstr(NumberOfPhones * SpacePhone + NumberOfLaptops * SpaceLaptop <= TotalSpace)
# @Constraint Constr_2 @Def: The total cost of phones and laptops must not exceed MaxBudget.
model.addConstr(CostPhone * NumberOfPhones + CostLaptop * NumberOfLaptops <= MaxBudget)
# @Constraint Constr_3 @Def: The number of laptops must be at least MinLaptopPercentage of the total inventory of phones and laptops.
model.addConstr(NumberOfLaptops >= MinLaptopPercentage * (NumberOfPhones + NumberOfLaptops))

# Objective 
# @Objective Objective @Def: Maximize the total profit, which is calculated as (ProfitPhone multiplied by the number of phones) plus (ProfitLaptop multiplied by the number of laptops).
model.setObjective(ProfitPhone * NumberOfPhones + ProfitLaptop * NumberOfLaptops, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfPhones'] = NumberOfPhones.x
variables['NumberOfLaptops'] = NumberOfLaptops.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
