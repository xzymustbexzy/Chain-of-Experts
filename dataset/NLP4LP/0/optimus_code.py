# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
Maximize the sum of ProfitPerDollarCondos multiplied by the investment in condos
and ProfitPerDollarDetachedHouses multiplied by the investment in detached
houses. The total investment must not exceed TotalBudget. The investment in
condos must be at least MinimumPercentageCondos of the total investment. The
investment in detached houses must be at least MinimumInvestmentDetachedHouses.
All investment amounts must be non-negative.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/1/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalBudget @Def: Total budget available for investment @Shape: [] 
TotalBudget = data['TotalBudget']
# @Parameter ProfitPerDollarCondos @Def: Profit per dollar invested in condos @Shape: [] 
ProfitPerDollarCondos = data['ProfitPerDollarCondos']
# @Parameter ProfitPerDollarDetachedHouses @Def: Profit per dollar invested in detached houses @Shape: [] 
ProfitPerDollarDetachedHouses = data['ProfitPerDollarDetachedHouses']
# @Parameter MinimumPercentageCondos @Def: Minimum percentage of total investment that must be in condos @Shape: [] 
MinimumPercentageCondos = data['MinimumPercentageCondos']
# @Parameter MinimumInvestmentDetachedHouses @Def: Minimum investment required in detached houses @Shape: [] 
MinimumInvestmentDetachedHouses = data['MinimumInvestmentDetachedHouses']

# Variables 
# @Variable InvestmentCondos @Def: The amount invested in condos @Shape: [] 
InvestmentCondos = model.addVar(vtype=GRB.CONTINUOUS, name="InvestmentCondos")
# @Variable InvestmentDetachedHouses @Def: The amount invested in detached houses @Shape: [] 
InvestmentDetachedHouses = model.addVar(vtype=GRB.CONTINUOUS, lb=MinimumInvestmentDetachedHouses, name="InvestmentDetachedHouses")

# Constraints 
# @Constraint Constr_1 @Def: The total investment must not exceed TotalBudget.
model.addConstr(InvestmentCondos + InvestmentDetachedHouses <= TotalBudget)
# @Constraint Constr_2 @Def: The investment in condos must be at least MinimumPercentageCondos of the total investment.
model.addConstr(InvestmentCondos >= MinimumPercentageCondos * (InvestmentCondos + InvestmentDetachedHouses))
# @Constraint Constr_3 @Def: The investment in detached houses must be at least MinimumInvestmentDetachedHouses.
model.addConstr(InvestmentDetachedHouses >= MinimumInvestmentDetachedHouses)
# @Constraint Constr_4 @Def: All investment amounts must be non-negative.
model.addConstr(InvestmentCondos >= 0)
model.addConstr(InvestmentDetachedHouses >= 0)

# Objective 
# @Objective Objective @Def: Maximize the sum of ProfitPerDollarCondos multiplied by the investment in condos and ProfitPerDollarDetachedHouses multiplied by the investment in detached houses.
model.setObjective(ProfitPerDollarCondos * InvestmentCondos + ProfitPerDollarDetachedHouses * InvestmentDetachedHouses, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['InvestmentCondos'] = InvestmentCondos.x
variables['InvestmentDetachedHouses'] = InvestmentDetachedHouses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
