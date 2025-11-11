# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A manufacturing company produces NumProducts different types of sports
equipment. Each product requires MaterialRequirement units of materials and
TimeRequirement hours to produce. The company has a total of
TotalMaterialsAvailable units of materials and TotalLaborHoursAvailable labor
hours available. The production must ensure that the number of basketballs is at
least MinBasketballToFootballRatio times the number of footballs and that at
least MinimumFootballs footballs are produced. The objective is to maximize the
total number of sports equipment produced.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/257/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProducts @Def: Number of different sports equipment produced @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter MaterialRequirement @Def: Amount of materials required to produce one unit of each sports equipment @Shape: ['NumProducts'] 
MaterialRequirement = data['MaterialRequirement']
# @Parameter TimeRequirement @Def: Amount of labor hours required to produce one unit of each sports equipment @Shape: ['NumProducts'] 
TimeRequirement = data['TimeRequirement']
# @Parameter TotalMaterialsAvailable @Def: Total units of materials available for production @Shape: [] 
TotalMaterialsAvailable = data['TotalMaterialsAvailable']
# @Parameter TotalLaborHoursAvailable @Def: Total labor hours available for production @Shape: [] 
TotalLaborHoursAvailable = data['TotalLaborHoursAvailable']
# @Parameter MinBasketballToFootballRatio @Def: Minimum ratio of basketballs to footballs production @Shape: [] 
MinBasketballToFootballRatio = data['MinBasketballToFootballRatio']
# @Parameter MinimumFootballs @Def: Minimum number of footballs to produce @Shape: [] 
MinimumFootballs = data['MinimumFootballs']

# Variables 
# @Variable ProductionQuantity @Def: The number of each sports equipment produced @Shape: ['NumProducts'] 
ProductionQuantity = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="ProductionQuantity")
# @Variable ProductionQuantityBasketballs @Def: The number of basketballs produced @Shape: [] 
ProductionQuantityBasketballs = model.addVar(vtype=GRB.CONTINUOUS, name="ProductionQuantityBasketballs")
# @Variable ProductionQuantityFootballs @Def: The number of footballs produced @Shape: [] 
ProductionQuantityFootballs = model.addVar(vtype=GRB.CONTINUOUS, lb=MinimumFootballs, name="ProductionQuantityFootballs")

# Constraints 
# @Constraint Constr_1 @Def: The total materials used to produce all sports equipment cannot exceed TotalMaterialsAvailable units.
model.addConstr(quicksum(MaterialRequirement[i] * ProductionQuantity[i] for i in range(NumProducts)) <= TotalMaterialsAvailable)
# @Constraint Constr_2 @Def: The total labor hours used to produce all sports equipment cannot exceed TotalLaborHoursAvailable labor hours.
model.addConstr(quicksum(TimeRequirement[i] * ProductionQuantity[i] for i in range(NumProducts)) <= TotalLaborHoursAvailable)
# @Constraint Constr_3 @Def: The number of basketballs produced must be at least MinBasketballToFootballRatio times the number of footballs produced.
model.addConstr(ProductionQuantityBasketballs >= MinBasketballToFootballRatio * ProductionQuantityFootballs)
# @Constraint Constr_4 @Def: At least MinimumFootballs footballs must be produced.
model.addConstr(ProductionQuantityFootballs >= MinimumFootballs)

# Objective 
# @Objective Objective @Def: Maximize the total number of sports equipment produced.
model.setObjective(quicksum(ProductionQuantity[k] for k in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ProductionQuantity'] = model.getAttr('X', ProductionQuantity)
variables['ProductionQuantityBasketballs'] = ProductionQuantityBasketballs.x
variables['ProductionQuantityFootballs'] = ProductionQuantityFootballs.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
