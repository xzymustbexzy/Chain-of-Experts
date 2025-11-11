# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A farmer has TotalFarmArea acres to plant NumCrops different crops. The total
watering budget is TotalWateringBudget dollars and the total available labor is
TotalAvailableLabor days. Each crop requires LaborPerAcre[i] days of labor and
WateringCostPerAcre[i] dollars per acre for watering. The profit per acre for
each crop is ProfitPerAcre[i] dollars. The objective is to maximize the total
profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/35/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter TotalFarmArea @Def: Total area of the farm in acres @Shape: [] 
TotalFarmArea = data['TotalFarmArea']
# @Parameter TotalWateringBudget @Def: Total budget available for watering in dollars @Shape: [] 
TotalWateringBudget = data['TotalWateringBudget']
# @Parameter TotalAvailableLabor @Def: Total available labor in days @Shape: [] 
TotalAvailableLabor = data['TotalAvailableLabor']
# @Parameter NumCrops @Def: Number of different crops to be planted @Shape: [] 
NumCrops = data['NumCrops']
# @Parameter LaborPerAcre @Def: Amount of labor required per acre for each crop in days @Shape: ['NumCrops'] 
LaborPerAcre = data['LaborPerAcre']
# @Parameter WateringCostPerAcre @Def: Watering cost per acre for each crop in dollars @Shape: ['NumCrops'] 
WateringCostPerAcre = data['WateringCostPerAcre']
# @Parameter ProfitPerAcre @Def: Profit per acre for each crop in dollars @Shape: ['NumCrops'] 
ProfitPerAcre = data['ProfitPerAcre']
    
# Variables 
# @Variable Acreage @Def: The acreage allocated to each crop @Shape: ['NumCrops'] 
Acreage = model.addVars(NumCrops, vtype=GRB.CONTINUOUS, name="Acreage")
    
# Constraints 
# @Constraint Constr_1 @Def: The total acreage allocated to all crops must not exceed TotalFarmArea.
model.addConstr(quicksum(Acreage[i] for i in range(NumCrops)) <= TotalFarmArea)
# @Constraint Constr_2 @Def: The total watering cost, calculated as the sum of WateringCostPerAcre[i] multiplied by the acreage of each crop, must not exceed TotalWateringBudget.
model.addConstr(quicksum(WateringCostPerAcre[i] * Acreage[i] for i in range(NumCrops)) <= TotalWateringBudget)
# @Constraint Constr_3 @Def: The total labor required, calculated as the sum of LaborPerAcre[i] multiplied by the acreage of each crop, must not exceed TotalAvailableLabor.
model.addConstr(quicksum(LaborPerAcre[i] * Acreage[i] for i in range(NumCrops)) <= TotalAvailableLabor)
    
# Objective 
# @Objective Objective @Def: Maximize the total profit, which is the sum of ProfitPerAcre[i] multiplied by the acreage of each crop.
model.setObjective(quicksum(ProfitPerAcre[i] * Acreage[i] for i in range(NumCrops)), GRB.MAXIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['Acreage'] = [Acreage[i].x for i in range(NumCrops)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)