# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Minimize (SeniorWage × NumberOfSeniorCitizens + YoungAdultWage ×
NumberOfYoungAdults) subject to (SeniorWage × NumberOfSeniorCitizens +
YoungAdultWage × NumberOfYoungAdults ≤ MaxWeeklyWageBill),
(NumberOfSeniorCitizens + NumberOfYoungAdults ≥ MinWorkersPerDay),
(NumberOfYoungAdults ≥ MinYoungAdultsPerDay), and (NumberOfYoungAdults ≥
MinYoungToSeniorRatio × NumberOfSeniorCitizens).
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/5/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SeniorWage @Def: Weekly wage rate for senior citizens @Shape: [] 
SeniorWage = data['SeniorWage']
# @Parameter YoungAdultWage @Def: Weekly wage rate for young adults @Shape: [] 
YoungAdultWage = data['YoungAdultWage']
# @Parameter MaxWeeklyWageBill @Def: Maximum weekly wage bill @Shape: [] 
MaxWeeklyWageBill = data['MaxWeeklyWageBill']
# @Parameter MinWorkersPerDay @Def: Minimum number of workers required per day @Shape: [] 
MinWorkersPerDay = data['MinWorkersPerDay']
# @Parameter MinYoungAdultsPerDay @Def: Minimum number of young adults required per day @Shape: [] 
MinYoungAdultsPerDay = data['MinYoungAdultsPerDay']
# @Parameter MinYoungToSeniorRatio @Def: Minimum ratio of young adults to senior citizens @Shape: [] 
MinYoungToSeniorRatio = data['MinYoungToSeniorRatio']

# Variables 
# @Variable NumberOfSeniorCitizens @Def: The number of senior citizens @Shape: ['Integer'] 
NumberOfSeniorCitizens = model.addVar(vtype=GRB.INTEGER, name="NumberOfSeniorCitizens")
# @Variable NumberOfYoungAdults @Def: The number of young adults @Shape: ['Integer'] 
NumberOfYoungAdults = model.addVar(vtype=GRB.INTEGER, name="NumberOfYoungAdults")

# Constraints 
# @Constraint Constr_1 @Def: The total weekly wage bill (SeniorWage × NumberOfSeniorCitizens + YoungAdultWage × NumberOfYoungAdults) must not exceed the maximum weekly wage bill (MaxWeeklyWageBill).
model.addConstr(SeniorWage * NumberOfSeniorCitizens + YoungAdultWage * NumberOfYoungAdults <= MaxWeeklyWageBill)
# @Constraint Constr_2 @Def: The total number of employees (NumberOfSeniorCitizens + NumberOfYoungAdults) must be at least the minimum number of workers required per day (MinWorkersPerDay).
model.addConstr(NumberOfSeniorCitizens + NumberOfYoungAdults >= MinWorkersPerDay)
# @Constraint Constr_3 @Def: The number of young adults (NumberOfYoungAdults) must be at least the minimum number of young adults required per day (MinYoungAdultsPerDay).
model.addConstr(NumberOfYoungAdults >= MinYoungAdultsPerDay)
# @Constraint Constr_4 @Def: The number of young adults (NumberOfYoungAdults) must be at least the product of the minimum young to senior ratio (MinYoungToSeniorRatio) and the number of senior citizens (NumberOfSeniorCitizens).
model.addConstr(NumberOfYoungAdults >= MinYoungToSeniorRatio * NumberOfSeniorCitizens)

# Objective 
# @Objective Objective @Def: Minimize the total weekly wage expenses, calculated as (SeniorWage × NumberOfSeniorCitizens + YoungAdultWage × NumberOfYoungAdults).
model.setObjective(SeniorWage * NumberOfSeniorCitizens + YoungAdultWage * NumberOfYoungAdults, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSeniorCitizens'] = NumberOfSeniorCitizens.x
variables['NumberOfYoungAdults'] = NumberOfYoungAdults.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
