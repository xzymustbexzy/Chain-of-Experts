# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A patient must consume at least RequiredZ1 grams of medicine Z1 and at least
RequiredD3 grams of medicine D3 daily by taking Zodiac and Sunny pills. Each
Zodiac pill provides Z1PerZodiac grams of Z1 and D3PerZodiac grams of D3 and
costs CostZodiac dollars. Each Sunny pill provides Z1PerSunny grams of Z1 and
D3PerSunny grams of D3 and costs CostSunny dollars. The objective is to minimize
the total cost while satisfying the medicine requirements.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/16/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter RequiredZ1 @Def: Minimum required daily amount of medicine Z1 in grams @Shape: [] 
RequiredZ1 = data['RequiredZ1']
# @Parameter RequiredD3 @Def: Minimum required daily amount of medicine D3 in grams @Shape: [] 
RequiredD3 = data['RequiredD3']
# @Parameter Z1PerZodiac @Def: Amount of medicine Z1 in grams per pill of Zodiac @Shape: [] 
Z1PerZodiac = data['Z1PerZodiac']
# @Parameter Z1PerSunny @Def: Amount of medicine Z1 in grams per pill of Sunny @Shape: [] 
Z1PerSunny = data['Z1PerSunny']
# @Parameter D3PerZodiac @Def: Amount of medicine D3 in grams per pill of Zodiac @Shape: [] 
D3PerZodiac = data['D3PerZodiac']
# @Parameter D3PerSunny @Def: Amount of medicine D3 in grams per pill of Sunny @Shape: [] 
D3PerSunny = data['D3PerSunny']
# @Parameter CostZodiac @Def: Cost per pill of Zodiac in dollars @Shape: [] 
CostZodiac = data['CostZodiac']
# @Parameter CostSunny @Def: Cost per pill of Sunny in dollars @Shape: [] 
CostSunny = data['CostSunny']

# Variables 
# @Variable QuantityZodiac @Def: The number of Zodiac pills selected @Shape: ['Integer'] 
QuantityZodiac = model.addVar(vtype=GRB.INTEGER, name="QuantityZodiac")
# @Variable QuantitySunny @Def: The number of Sunny pills selected @Shape: ['Integer'] 
QuantitySunny = model.addVar(vtype=GRB.INTEGER, name="QuantitySunny")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of medicine Z1 provided by Zodiac and Sunny pills must be at least RequiredZ1 grams.
model.addConstr(Z1PerZodiac * QuantityZodiac + Z1PerSunny * QuantitySunny >= RequiredZ1)
# @Constraint Constr_2 @Def: The total amount of medicine D3 provided by Zodiac and Sunny pills must be at least RequiredD3 grams.
model.addConstr(D3PerZodiac * QuantityZodiac + D3PerSunny * QuantitySunny >= RequiredD3)

# Objective 
# @Objective Objective @Def: Minimize the total cost, which is the sum of CostZodiac multiplied by the number of Zodiac pills and CostSunny multiplied by the number of Sunny pills, while satisfying the daily minimum requirements for medicines Z1 and D3.
model.setObjective(CostZodiac * QuantityZodiac + CostSunny * QuantitySunny, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityZodiac'] = QuantityZodiac.x
variables['QuantitySunny'] = QuantitySunny.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
