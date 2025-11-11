# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The company sells a quantity of regular handbags and a quantity of premium
handbags, generating profits equal to RegularHandbagProfit multiplied by the
number of regular handbags and PremiumHandbagProfit multiplied by the number of
premium handbags. The total manufacturing cost is calculated as
RegularHandbagCost multiplied by the number of regular handbags plus
PremiumHandbagCost multiplied by the number of premium handbags, which must not
exceed TotalBudget. Additionally, the combined number of regular and premium
handbags sold must not exceed MaxHandbagsPerMonth. The objective is to determine
the quantities of each type of handbag to sell in order to maximize the total
profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/203/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter RegularHandbagProfit @Def: Profit per regular handbag @Shape: [] 
RegularHandbagProfit = data['RegularHandbagProfit']
# @Parameter PremiumHandbagProfit @Def: Profit per premium handbag @Shape: [] 
PremiumHandbagProfit = data['PremiumHandbagProfit']
# @Parameter RegularHandbagCost @Def: Manufacturing cost per regular handbag @Shape: [] 
RegularHandbagCost = data['RegularHandbagCost']
# @Parameter PremiumHandbagCost @Def: Manufacturing cost per premium handbag @Shape: [] 
PremiumHandbagCost = data['PremiumHandbagCost']
# @Parameter TotalBudget @Def: Total budget available for manufacturing @Shape: [] 
TotalBudget = data['TotalBudget']
# @Parameter MaxHandbagsPerMonth @Def: Maximum number of handbags that can be sold per month @Shape: [] 
MaxHandbagsPerMonth = data['MaxHandbagsPerMonth']

# Variables 
# @Variable NumberRegularHandbags @Def: The number of regular handbags to manufacture @Shape: ['Integer', 'NonNegative'] 
NumberRegularHandbags = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberRegularHandbags")
# @Variable NumberPremiumHandbags @Def: The number of premium handbags to manufacture @Shape: ['Integer', 'NonNegative'] 
NumberPremiumHandbags = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberPremiumHandbags")

# Constraints 
# @Constraint Constr_1 @Def: The total manufacturing cost, calculated as RegularHandbagCost multiplied by the number of regular handbags plus PremiumHandbagCost multiplied by the number of premium handbags, must not exceed TotalBudget.
model.addConstr(RegularHandbagCost * NumberRegularHandbags + PremiumHandbagCost * NumberPremiumHandbags <= TotalBudget)
# @Constraint Constr_2 @Def: The combined number of regular and premium handbags sold must not exceed MaxHandbagsPerMonth.
model.addConstr(NumberRegularHandbags + NumberPremiumHandbags <= MaxHandbagsPerMonth)

# Objective 
# @Objective Objective @Def: Maximize the total profit, which is the sum of RegularHandbagProfit multiplied by the number of regular handbags and PremiumHandbagProfit multiplied by the number of premium handbags.
model.setObjective(RegularHandbagProfit * NumberRegularHandbags + PremiumHandbagProfit * NumberPremiumHandbags, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberRegularHandbags'] = NumberRegularHandbags.x
variables['NumberPremiumHandbags'] = NumberPremiumHandbags.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
