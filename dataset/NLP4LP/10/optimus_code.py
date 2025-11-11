# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bakery uses a stand mixer with MixerMaximumHours available operating hours per
year and an oven with OvenMaximumHours available operating hours per year.
Producing one loaf of bread requires BreadMixerTime hours in the stand mixer and
BreadOvenTime hours in the oven. Producing one batch of cookies requires
CookiesMixerTime hours in the stand mixer and CookiesOvenTime hours in the oven.
Each loaf of bread generates a profit of BreadProfit and each batch of cookies
generates a profit of CookiesProfit. The bakery aims to maximize its total
profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/11/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MixerMaximumHours @Def: Maximum available operating hours per year for the stand mixer @Shape: [] 
MixerMaximumHours = data['MixerMaximumHours']
# @Parameter OvenMaximumHours @Def: Maximum available operating hours per year for the oven @Shape: [] 
OvenMaximumHours = data['OvenMaximumHours']
# @Parameter BreadMixerTime @Def: Number of hours the stand mixer is required to bake one loaf of bread @Shape: [] 
BreadMixerTime = data['BreadMixerTime']
# @Parameter BreadOvenTime @Def: Number of hours the oven is required to bake one loaf of bread @Shape: [] 
BreadOvenTime = data['BreadOvenTime']
# @Parameter CookiesMixerTime @Def: Number of hours the stand mixer is required to bake one batch of cookies @Shape: [] 
CookiesMixerTime = data['CookiesMixerTime']
# @Parameter CookiesOvenTime @Def: Number of hours the oven is required to bake one batch of cookies @Shape: [] 
CookiesOvenTime = data['CookiesOvenTime']
# @Parameter BreadProfit @Def: Profit earned per loaf of bread @Shape: [] 
BreadProfit = data['BreadProfit']
# @Parameter CookiesProfit @Def: Profit earned per batch of cookies @Shape: [] 
CookiesProfit = data['CookiesProfit']

# Variables 
# @Variable BreadQuantity @Def: The number of loaves of bread produced @Shape: [] 
BreadQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="BreadQuantity")
# @Variable CookiesQuantity @Def: The number of batches of cookies produced @Shape: [] 
CookiesQuantity = model.addVar(vtype=GRB.CONTINUOUS, name="CookiesQuantity")

# Constraints 
# @Constraint Constr_1 @Def: The total stand mixer time used for producing bread and cookies must not exceed MixerMaximumHours hours per year.
model.addConstr(BreadMixerTime * BreadQuantity + CookiesMixerTime * CookiesQuantity <= MixerMaximumHours)
# @Constraint Constr_2 @Def: The total oven time used for producing bread and cookies must not exceed OvenMaximumHours hours per year.
model.addConstr(BreadOvenTime * BreadQuantity + CookiesOvenTime * CookiesQuantity <= OvenMaximumHours)

# Objective 
# @Objective Objective @Def: Maximize the total profit, where total profit is (BreadProfit × number of bread loaves) + (CookiesProfit × number of cookie batches).
model.setObjective(BreadProfit * BreadQuantity + CookiesProfit * CookiesQuantity, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['BreadQuantity'] = BreadQuantity.x
variables['CookiesQuantity'] = CookiesQuantity.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
