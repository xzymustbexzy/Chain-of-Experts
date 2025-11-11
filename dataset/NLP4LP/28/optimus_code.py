# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Maximize the total profit, which is ProfitChocolate multiplied by the number of
gallons of chocolate ice cream produced plus ProfitVanilla multiplied by the
number of gallons of vanilla ice cream produced, subject to the following
constraints: the number of gallons of chocolate ice cream produced is at least
MinGallonsChocolate and at most MaxGallonsChocolate; the number of gallons of
vanilla ice cream produced is at least MinGallonsVanilla and at most
MaxGallonsVanilla; the total production time, calculated as
ProductionTimeChocolate multiplied by the number of gallons of chocolate ice
cream produced plus ProductionTimeVanilla multiplied by the number of gallons of
vanilla ice cream produced, does not exceed TotalProductionHours;
WorkersNeededChocolate multiplied by the number of chocolate production
operations plus WorkersNeededVanilla multiplied by the number of vanilla
production operations does not exceed the total number of workers available, and
the total number of workers is at least MinTotalWorkers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/29/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinGallonsChocolate @Def: Minimum gallons of chocolate ice cream to produce per week @Shape: [] 
MinGallonsChocolate = data['MinGallonsChocolate']
# @Parameter MinGallonsVanilla @Def: Minimum gallons of vanilla ice cream to produce per week @Shape: [] 
MinGallonsVanilla = data['MinGallonsVanilla']
# @Parameter MaxGallonsChocolate @Def: Maximum gallons of chocolate ice cream to produce per week @Shape: [] 
MaxGallonsChocolate = data['MaxGallonsChocolate']
# @Parameter MaxGallonsVanilla @Def: Maximum gallons of vanilla ice cream to produce per week @Shape: [] 
MaxGallonsVanilla = data['MaxGallonsVanilla']
# @Parameter ProductionTimeChocolate @Def: Production time in hours to produce one gallon of chocolate ice cream @Shape: [] 
ProductionTimeChocolate = data['ProductionTimeChocolate']
# @Parameter ProductionTimeVanilla @Def: Production time in hours to produce one gallon of vanilla ice cream @Shape: [] 
ProductionTimeVanilla = data['ProductionTimeVanilla']
# @Parameter TotalProductionHours @Def: Total production hours available per week @Shape: [] 
TotalProductionHours = data['TotalProductionHours']
# @Parameter WorkersNeededChocolate @Def: Number of workers required to operate production of chocolate ice cream @Shape: [] 
WorkersNeededChocolate = data['WorkersNeededChocolate']
# @Parameter WorkersNeededVanilla @Def: Number of workers required to operate production of vanilla ice cream @Shape: [] 
WorkersNeededVanilla = data['WorkersNeededVanilla']
# @Parameter MinTotalWorkers @Def: Minimum total number of workers required @Shape: [] 
MinTotalWorkers = data['MinTotalWorkers']
# @Parameter ProfitChocolate @Def: Profit per gallon of chocolate ice cream @Shape: [] 
ProfitChocolate = data['ProfitChocolate']
# @Parameter ProfitVanilla @Def: Profit per gallon of vanilla ice cream @Shape: [] 
ProfitVanilla = data['ProfitVanilla']

# Variables 
# @Variable GallonsChocolateProduced @Def: The number of gallons of chocolate ice cream produced per week @Shape: ['Continuous'] 
GallonsChocolateProduced = model.addVar(lb=MinGallonsChocolate, ub=MaxGallonsChocolate, vtype=GRB.CONTINUOUS, name="GallonsChocolateProduced")
# @Variable GallonsVanillaProduced @Def: The number of gallons of vanilla ice cream produced per week @Shape: ['Continuous'] 
GallonsVanillaProduced = model.addVar(vtype=GRB.CONTINUOUS, lb=MinGallonsVanilla, ub=MaxGallonsVanilla, name="GallonsVanillaProduced")

# Constraints 
# @Constraint Constr_1 @Def: The number of gallons of chocolate ice cream produced is at least MinGallonsChocolate and at most MaxGallonsChocolate.
model.addConstr(GallonsChocolateProduced >= MinGallonsChocolate)
model.addConstr(GallonsChocolateProduced <= MaxGallonsChocolate)
# @Constraint Constr_2 @Def: The number of gallons of vanilla ice cream produced is at least MinGallonsVanilla and at most MaxGallonsVanilla.

# @Constraint Constr_3 @Def: The total production time, calculated as ProductionTimeChocolate multiplied by the number of gallons of chocolate ice cream produced plus ProductionTimeVanilla multiplied by the number of gallons of vanilla ice cream produced, does not exceed TotalProductionHours.
model.addConstr(ProductionTimeChocolate * GallonsChocolateProduced + ProductionTimeVanilla * GallonsVanillaProduced <= TotalProductionHours)
# @Constraint Constr_4 @Def: WorkersNeededChocolate multiplied by the number of gallons of chocolate ice cream produced plus WorkersNeededVanilla multiplied by the number of gallons of vanilla ice cream produced is at least MinTotalWorkers.
model.addConstr(WorkersNeededChocolate * GallonsChocolateProduced + WorkersNeededVanilla * GallonsVanillaProduced >= MinTotalWorkers)

# Objective 
# @Objective Objective @Def: Maximize the total profit, which is ProfitChocolate multiplied by the number of gallons of chocolate ice cream produced plus ProfitVanilla multiplied by the number of gallons of vanilla ice cream produced.
model.setObjective(ProfitChocolate * GallonsChocolateProduced + ProfitVanilla * GallonsVanillaProduced, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['GallonsChocolateProduced'] = GallonsChocolateProduced.x
variables['GallonsVanillaProduced'] = GallonsVanillaProduced.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
