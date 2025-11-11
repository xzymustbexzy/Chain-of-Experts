# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A store purchases quantities of plush toys and dolls. The cost per plush toy is
CostPlushToy and the cost per doll is CostDoll. The total inventory cost must
not exceed InventoryBudget. Each plush toy sold yields ProfitPlushToy profit and
each doll sold yields ProfitDoll profit. The number of plush toys sold must be
at least MinPlushSold and at most MaxPlushSold. Additionally, the number of
dolls sold must not exceed MaxDollToPlushRatio multiplied by the number of plush
toys sold. The objective is to determine the quantities to buy and sell to
maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/196/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostPlushToy @Def: Cost to the store for one plush toy @Shape: [] 
CostPlushToy = data['CostPlushToy']
# @Parameter CostDoll @Def: Cost to the store for one doll @Shape: [] 
CostDoll = data['CostDoll']
# @Parameter InventoryBudget @Def: Maximum total cost for inventory @Shape: [] 
InventoryBudget = data['InventoryBudget']
# @Parameter ProfitPlushToy @Def: Profit earned per plush toy sold @Shape: [] 
ProfitPlushToy = data['ProfitPlushToy']
# @Parameter ProfitDoll @Def: Profit earned per doll sold @Shape: [] 
ProfitDoll = data['ProfitDoll']
# @Parameter MinPlushSold @Def: Minimum number of plush toys sold each month @Shape: [] 
MinPlushSold = data['MinPlushSold']
# @Parameter MaxPlushSold @Def: Maximum number of plush toys sold each month @Shape: [] 
MaxPlushSold = data['MaxPlushSold']
# @Parameter MaxDollToPlushRatio @Def: Maximum ratio of number of dolls sold to number of plush toys sold @Shape: [] 
MaxDollToPlushRatio = data['MaxDollToPlushRatio']

# Variables 
# @Variable NumberPlushToys @Def: The number of plush toys purchased @Shape: [] 
NumberPlushToys = model.addVar(vtype=GRB.INTEGER, name="NumberPlushToys")
# @Variable NumberDolls @Def: The number of dolls purchased @Shape: [] 
NumberDolls = model.addVar(vtype=GRB.INTEGER, name="NumberDolls")
# @Variable NumberPlushToysSold @Def: The number of plush toys sold each month @Shape: [] 
NumberPlushToysSold = model.addVar(vtype=GRB.INTEGER, name="NumberPlushToysSold")
# @Variable NumberDollsSold @Def: The number of dolls sold each month @Shape: [] 
NumberDollsSold = model.addVar(vtype=GRB.INTEGER, name="NumberDollsSold")

# Constraints 
# @Constraint Constr_1 @Def: The total cost of purchasing plush toys and dolls must not exceed InventoryBudget.
model.addConstr(NumberPlushToys * CostPlushToy + NumberDolls * CostDoll <= InventoryBudget)
# @Constraint Constr_2 @Def: The number of plush toys sold must be at least MinPlushSold and at most MaxPlushSold.
model.addConstr(NumberPlushToysSold >= MinPlushSold)
model.addConstr(NumberPlushToysSold <= MaxPlushSold)
# @Constraint Constr_3 @Def: The number of dolls sold must not exceed MaxDollToPlushRatio multiplied by the number of plush toys sold.
model.addConstr(NumberDollsSold <= MaxDollToPlushRatio * NumberPlushToysSold)
# @Constraint Constr_4 @Def: The quantity of plush toys purchased must be at least equal to the number of plush toys sold.
model.addConstr(NumberPlushToys >= NumberPlushToysSold)
# @Constraint Constr_5 @Def: The quantity of dolls purchased must be at least equal to the number of dolls sold.
model.addConstr(NumberDolls >= NumberDollsSold)

# Objective 
# @Objective Objective @Def: Total profit is the sum of ProfitPlushToy multiplied by the number of plush toys sold and ProfitDoll multiplied by the number of dolls sold. The objective is to maximize total profit.
model.setObjective(ProfitPlushToy * NumberPlushToysSold + ProfitDoll * NumberDollsSold, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberPlushToys'] = NumberPlushToys.x
variables['NumberDolls'] = NumberDolls.x
variables['NumberPlushToysSold'] = NumberPlushToysSold.x
variables['NumberDollsSold'] = NumberDollsSold.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
