# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
The bakery produces x₁ strawberry cookies and x₂ sugar cookies, where each
strawberry cookie yields ProfitPerStrawberryCookie profit and each sugar cookie
yields ProfitPerSugarCookie profit. The daily demand for strawberry cookies is
limited by MaxDailyDemandStrawberry and for sugar cookies by
MaxDailyDemandSugar. The total number of cookies produced per day cannot exceed
MaxTotalCookiesPerDay. The objective is to maximize the total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/212/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitPerStrawberryCookie @Def: Profit per strawberry cookie @Shape: [] 
ProfitPerStrawberryCookie = data['ProfitPerStrawberryCookie']
# @Parameter ProfitPerSugarCookie @Def: Profit per sugar cookie @Shape: [] 
ProfitPerSugarCookie = data['ProfitPerSugarCookie']
# @Parameter MaxDailyDemandStrawberry @Def: Maximum daily demand for strawberry cookies @Shape: [] 
MaxDailyDemandStrawberry = data['MaxDailyDemandStrawberry']
# @Parameter MaxDailyDemandSugar @Def: Maximum daily demand for sugar cookies @Shape: [] 
MaxDailyDemandSugar = data['MaxDailyDemandSugar']
# @Parameter MaxTotalCookiesPerDay @Def: Maximum total cookies that can be made per day @Shape: [] 
MaxTotalCookiesPerDay = data['MaxTotalCookiesPerDay']

# Variables 
# @Variable NumStrawberryCookies @Def: The number of strawberry cookies produced @Shape: [] 
NumStrawberryCookies = model.addVar(vtype=GRB.CONTINUOUS, name="NumStrawberryCookies")
# @Variable NumSugarCookies @Def: The number of sugar cookies produced @Shape: [] 
NumSugarCookies = model.addVar(vtype=GRB.CONTINUOUS, name="NumSugarCookies")

# Constraints 
# @Constraint Constr_1 @Def: The number of strawberry cookies produced cannot exceed MaxDailyDemandStrawberry.
model.addConstr(NumStrawberryCookies <= MaxDailyDemandStrawberry)
# @Constraint Constr_2 @Def: The number of sugar cookies produced cannot exceed MaxDailyDemandSugar.
model.addConstr(NumSugarCookies <= MaxDailyDemandSugar)
# @Constraint Constr_3 @Def: The total number of cookies produced per day cannot exceed MaxTotalCookiesPerDay.
model.addConstr(NumStrawberryCookies + NumSugarCookies <= MaxTotalCookiesPerDay)

# Objective 
# @Objective Objective @Def: Total profit is the sum of the profits from strawberry and sugar cookies. The objective is to maximize the total profit.
model.setObjective(ProfitPerStrawberryCookie * NumStrawberryCookies + ProfitPerSugarCookie * NumSugarCookies, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumStrawberryCookies'] = NumStrawberryCookies.x
variables['NumSugarCookies'] = NumSugarCookies.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
