# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company sells NumProducts different products. Each product requires
MoverTimePerProduct amount of mover time and SetupTimePerProduct amount of setup
time to sell one unit. The company has TotalMoverTime available mover time and
TotalSetupTime available setup time. The profit for each product is
ProfitPerProduct per unit. Determine the number of each product to sell in order
to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/191/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NumProducts @Def: Number of different products sold by the company @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter MoverTimePerProduct @Def: Amount of mover time required to sell one unit of each product @Shape: ['NumProducts'] 
MoverTimePerProduct = data['MoverTimePerProduct']
# @Parameter SetupTimePerProduct @Def: Amount of setup time required to sell one unit of each product @Shape: ['NumProducts'] 
SetupTimePerProduct = data['SetupTimePerProduct']
# @Parameter ProfitPerProduct @Def: Profit per unit of each product @Shape: ['NumProducts'] 
ProfitPerProduct = data['ProfitPerProduct']
# @Parameter TotalMoverTime @Def: Total available mover time @Shape: [] 
TotalMoverTime = data['TotalMoverTime']
# @Parameter TotalSetupTime @Def: Total available setup time @Shape: [] 
TotalSetupTime = data['TotalSetupTime']

# Variables 
# @Variable QuantityOfProduct @Def: The quantity of each product sold @Shape: ['NumProducts'] 
QuantityOfProduct = model.addVars(NumProducts, vtype=GRB.CONTINUOUS, name="QuantityOfProduct")

# Constraints 
# @Constraint Constr_1 @Def: Each product requires MoverTimePerProduct amount of mover time to sell one unit. The total mover time used cannot exceed TotalMoverTime.
model.addConstr(quicksum(MoverTimePerProduct[i] * QuantityOfProduct[i] for i in range(NumProducts)) <= TotalMoverTime)
# @Constraint Constr_2 @Def: Each product requires SetupTimePerProduct amount of setup time to sell one unit. The total setup time used cannot exceed TotalSetupTime.
model.addConstr(quicksum(SetupTimePerProduct[p] * QuantityOfProduct[p] for p in range(NumProducts)) <= TotalSetupTime)

# Objective 
# @Objective Objective @Def: The total profit is the sum of the profits of each product sold. The objective is to maximize the total profit.
model.setObjective(quicksum(ProfitPerProduct[i] * QuantityOfProduct[i] for i in range(NumProducts)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityOfProduct'] = {i: QuantityOfProduct[i].X for i in range(NumProducts)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)