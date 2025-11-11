# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company is building NumFactoryTypes different factory types. Each factory type
i produces ProductionRate[i] phones per day and requires ManagerRequirement[i]
managers. The company has AvailableManagers managers available and must produce
at least RequiredPhones phones per day. Determine the number of each factory
type to build to minimize the total number of factories.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/52/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumFactoryTypes @Def: Number of factory types @Shape: [] 
NumFactoryTypes = data['NumFactoryTypes']
# @Parameter ProductionRate @Def: Production rate of each factory type in phones per day @Shape: ['NumFactoryTypes'] 
ProductionRate = data['ProductionRate']
# @Parameter ManagerRequirement @Def: Number of managers required for each factory type @Shape: ['NumFactoryTypes'] 
ManagerRequirement = data['ManagerRequirement']
# @Parameter AvailableManagers @Def: Total number of managers available @Shape: [] 
AvailableManagers = data['AvailableManagers']
# @Parameter RequiredPhones @Def: Minimum number of phones required per day @Shape: [] 
RequiredPhones = data['RequiredPhones']
    
# Variables 
# @Variable FactoriesBuilt @Def: The number of factories built for each factory type @Shape: ['NumFactoryTypes'] 
FactoriesBuilt = model.addVars(NumFactoryTypes, vtype=GRB.INTEGER, name="FactoriesBuilt")
    
# Constraints 
# @Constraint Constr_1 @Def: The total number of managers required by all factory types built does not exceed AvailableManagers.
model.addConstr(quicksum(FactoriesBuilt[i] * ManagerRequirement[i] for i in range(NumFactoryTypes)) <= AvailableManagers)
# @Constraint Constr_2 @Def: The total phone production from all factory types built is at least RequiredPhones per day.
model.addConstr(quicksum(FactoriesBuilt[i] * ProductionRate[i] for i in range(NumFactoryTypes)) >= RequiredPhones)
    
# Objective 
# @Objective Objective @Def: Minimize the total number of factories built while meeting the production and manager constraints.
model.setObjective(quicksum(FactoriesBuilt[i] for i in range(NumFactoryTypes)), GRB.MINIMIZE)
    
# Solve 
model.optimize()
    
# Extract solution 
solution = {}
variables = {}
objective = []
variables['FactoriesBuilt'] = {i: FactoriesBuilt[i].x for i in range(NumFactoryTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)