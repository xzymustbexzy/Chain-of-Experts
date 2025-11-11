# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The food truck owner allocates funds up to MaxSpendingBudget for purchasing
mangos and guavas, with each mango costing CostMango and each guava costing
CostGuava. Each mango sold generates a profit of ProfitMango and each guava sold
generates a profit of ProfitGuava. The monthly sales of mangos are constrained
to be at least MinMangosSold and at most MaxMangosSold. Furthermore, the number
of guavas sold is limited to a maximum ratio defined by MaxGuavaToMangoRatio
relative to the number of mangos sold. The goal is to determine the optimal
quantities of mangos and guavas to sell in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/27/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MaxSpendingBudget @Def: The maximum amount the owner can spend on mangos and guavas @Shape: [] 
MaxSpendingBudget = data['MaxSpendingBudget']
# @Parameter CostMango @Def: The cost to purchase one mango @Shape: [] 
CostMango = data['CostMango']
# @Parameter CostGuava @Def: The cost to purchase one guava @Shape: [] 
CostGuava = data['CostGuava']
# @Parameter ProfitMango @Def: The profit earned from selling one mango @Shape: [] 
ProfitMango = data['ProfitMango']
# @Parameter ProfitGuava @Def: The profit earned from selling one guava @Shape: [] 
ProfitGuava = data['ProfitGuava']
# @Parameter MinMangosSold @Def: The minimum number of mangos sold each month @Shape: [] 
MinMangosSold = data['MinMangosSold']
# @Parameter MaxMangosSold @Def: The maximum number of mangos sold each month @Shape: [] 
MaxMangosSold = data['MaxMangosSold']
# @Parameter MaxGuavaToMangoRatio @Def: The maximum proportion of guavas sold relative to mangos sold @Shape: [] 
MaxGuavaToMangoRatio = data['MaxGuavaToMangoRatio']

# Variables 
# @Variable QuantityMango @Def: The number of mangos purchased @Shape: [] 
QuantityMango = model.addVar(vtype=GRB.INTEGER, name="QuantityMango")
# @Variable QuantityGuava @Def: The number of guavas purchased @Shape: [] 
QuantityGuava = model.addVar(vtype=GRB.INTEGER, name="QuantityGuava")
# @Variable MangosSold @Def: The number of mangos sold each month @Shape: [] 
MangosSold = model.addVar(vtype=GRB.INTEGER, lb=MinMangosSold, ub=MaxMangosSold, name="MangosSold")
# @Variable GuavasSold @Def: The number of guavas sold each month @Shape: [] 
GuavasSold = model.addVar(vtype=GRB.INTEGER, name="GuavasSold")

# Constraints 
# @Constraint Constr_1 @Def: The total spending on mangos and guavas cannot exceed MaxSpendingBudget.
model.addConstr(CostMango * QuantityMango + CostGuava * QuantityGuava <= MaxSpendingBudget)
# @Constraint Constr_2 @Def: The number of mangos sold must be at least MinMangosSold and at most MaxMangosSold each month.
model.addConstr(MangosSold >= MinMangosSold)
model.addConstr(MangosSold <= MaxMangosSold)
# @Constraint Constr_3 @Def: The number of guavas sold cannot exceed MaxGuavaToMangoRatio times the number of mangos sold.
model.addConstr(GuavasSold <= MaxGuavaToMangoRatio * MangosSold)

# Objective 
# @Objective Objective @Def: Total profit is the sum of (ProfitMango multiplied by the number of mangos sold) and (ProfitGuava multiplied by the number of guavas sold). The objective is to maximize the total profit.
model.setObjective(ProfitMango * MangosSold + ProfitGuava * GuavasSold, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityMango'] = QuantityMango.x
variables['QuantityGuava'] = QuantityGuava.x
variables['MangosSold'] = MangosSold.x
variables['GuavasSold'] = GuavasSold.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
