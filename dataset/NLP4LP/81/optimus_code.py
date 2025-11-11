# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company can build NumFactoryTypes different factory types. Each factory type i
has a production rate of ProductionRate[i] toys per day and requires
OperatorRequirement[i] operators. The company must produce at least
TotalProductionRequirement toys per day and has a total of
TotalAvailableOperators operators available. Determine the number of each
factory type to build to minimize the total number of factories.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/82/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumFactoryTypes @Def: Number of factory types @Shape: [] 
NumFactoryTypes = data['NumFactoryTypes']
# @Parameter ProductionRate @Def: Production rate of each factory type (toys per day) @Shape: ['NumFactoryTypes'] 
ProductionRate = data['ProductionRate']
# @Parameter OperatorRequirement @Def: Number of operators required for each factory type @Shape: ['NumFactoryTypes'] 
OperatorRequirement = data['OperatorRequirement']
# @Parameter TotalProductionRequirement @Def: Minimum number of toys required per day @Shape: [] 
TotalProductionRequirement = data['TotalProductionRequirement']
# @Parameter TotalAvailableOperators @Def: Total number of available operators @Shape: [] 
TotalAvailableOperators = data['TotalAvailableOperators']

# Variables 
# @Variable NumberOfFactories @Def: The number of factories of each type @Shape: ['NumFactoryTypes'] 
NumberOfFactories = model.addVars(NumFactoryTypes, vtype=GRB.INTEGER, name="NumberOfFactories")

# Constraints 
# @Constraint Constr_1 @Def: The total production must be at least TotalProductionRequirement toys per day. This is achieved by ensuring that the sum of ProductionRate[i] multiplied by the number of factories of each type i is greater than or equal to TotalProductionRequirement.
model.addConstr(quicksum(ProductionRate[i] * NumberOfFactories[i] for i in range(NumFactoryTypes)) >= TotalProductionRequirement)
# @Constraint Constr_2 @Def: The total number of operators used must not exceed TotalAvailableOperators. This is ensured by making sure that the sum of OperatorRequirement[i] multiplied by the number of factories of each type i is less than or equal to TotalAvailableOperators.
model.addConstr(quicksum(OperatorRequirement[i] * NumberOfFactories[i] for i in range(NumFactoryTypes)) <= TotalAvailableOperators)

# Objective 
# @Objective Objective @Def: Minimize the total number of factories built. This is done by minimizing the sum of the number of factories of each type.
model.setObjective(quicksum(NumberOfFactories[i] for i in range(NumFactoryTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfFactories'] = {i: NumberOfFactories[i].x for i in range(NumFactoryTypes)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)