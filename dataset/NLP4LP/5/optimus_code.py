# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Let x_Z, x_S, and x_W represent the number of advertisements on z-tube,
soorchle, and wassa respectively. The objective is to maximize the total
audience, which is calculated as ViewersZTube multiplied by x_Z plus
ViewersSoorchle multiplied by x_S plus ViewersWassa multiplied by x_W. The
constraints are as follows: the total cost, given by CostZTube times x_Z plus
CostSoorchle times x_S plus CostWassa times x_W, must not exceed the
WeeklyAdvertisingBudget; the number of soorchle advertisements x_S must be less
than or equal to MaxAdsSoorchle; the number of wassa advertisements x_W must be
at most MaxFractionWassaAds multiplied by the total number of advertisements
(x_Z + x_S + x_W); and the number of z-tube advertisements x_Z must be at least
MinFractionZTubeAds multiplied by the total number of advertisements (x_Z + x_S
+ x_W).
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/6/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostZTube @Def: Cost per advertisement on z-tube @Shape: [] 
CostZTube = data['CostZTube']
# @Parameter ViewersZTube @Def: Number of viewers attracted by each advertisement on z-tube @Shape: [] 
ViewersZTube = data['ViewersZTube']
# @Parameter CostSoorchle @Def: Cost per advertisement on soorchle @Shape: [] 
CostSoorchle = data['CostSoorchle']
# @Parameter ViewersSoorchle @Def: Number of viewers attracted by each advertisement on soorchle @Shape: [] 
ViewersSoorchle = data['ViewersSoorchle']
# @Parameter CostWassa @Def: Cost per advertisement on wassa @Shape: [] 
CostWassa = data['CostWassa']
# @Parameter ViewersWassa @Def: Number of viewers attracted by each advertisement on wassa @Shape: [] 
ViewersWassa = data['ViewersWassa']
# @Parameter MaxAdsSoorchle @Def: Maximum number of advertisements allowed on soorchle @Shape: [] 
MaxAdsSoorchle = data['MaxAdsSoorchle']
# @Parameter MaxFractionWassaAds @Def: Maximum fraction of total advertisements allowed on wassa @Shape: [] 
MaxFractionWassaAds = data['MaxFractionWassaAds']
# @Parameter MinFractionZTubeAds @Def: Minimum fraction of total advertisements required on z-tube @Shape: [] 
MinFractionZTubeAds = data['MinFractionZTubeAds']
# @Parameter WeeklyAdvertisingBudget @Def: Weekly advertising budget @Shape: [] 
WeeklyAdvertisingBudget = data['WeeklyAdvertisingBudget']

# Variables 
# @Variable NumberAdsZTube @Def: The number of advertisements on Z-Tube @Shape: [] 
NumberAdsZTube = model.addVar(vtype=GRB.INTEGER, name="NumberAdsZTube")
# @Variable NumberAdsSoorchle @Def: The number of advertisements on Soorchle @Shape: [] 
NumberAdsSoorchle = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxAdsSoorchle, name="NumberAdsSoorchle")
# @Variable NumberAdsWassa @Def: The number of advertisements on Wassa @Shape: [] 
NumberAdsWassa = model.addVar(vtype=GRB.INTEGER, name="NumberAdsWassa", lb=0)
# @Variable xZ @Def: The number of advertisements on Z-Tube @Shape: [] 
xZ = model.addVar(vtype=GRB.CONTINUOUS, name="xZ")
# @Variable xS @Def: The number of advertisements on Soorchle @Shape: [] 
xS = model.addVar(vtype=GRB.INTEGER, name="xS")
# @Variable xW @Def: The number of advertisements on Wassa @Shape: [] 
xW = model.addVar(vtype=GRB.INTEGER, name="xW")

# Constraints 
# @Constraint Constr_1 @Def: The total cost, given by CostZTube times x_Z plus CostSoorchle times x_S plus CostWassa times x_W, must not exceed the WeeklyAdvertisingBudget.
model.addConstr(CostZTube * NumberAdsZTube + CostSoorchle * NumberAdsSoorchle + CostWassa * NumberAdsWassa <= WeeklyAdvertisingBudget)
# @Constraint Constr_2 @Def: The number of soorchle advertisements x_S must be less than or equal to MaxAdsSoorchle.
model.addConstr(NumberAdsSoorchle <= MaxAdsSoorchle)
# @Constraint Constr_3 @Def: The number of wassa advertisements x_W must be at most MaxFractionWassaAds multiplied by the total number of advertisements (x_Z + x_S + x_W).
model.addConstr((1 - MaxFractionWassaAds) * xW <= MaxFractionWassaAds * (xZ + xS))
# @Constraint Constr_4 @Def: The number of z-tube advertisements x_Z must be at least MinFractionZTubeAds multiplied by the total number of advertisements (x_Z + x_S + x_W).
model.addConstr(xZ >= MinFractionZTubeAds * (xZ + xS + xW))

# Objective 
# @Objective Objective @Def: Maximize the total audience, which is calculated as ViewersZTube multiplied by x_Z plus ViewersSoorchle multiplied by x_S plus ViewersWassa multiplied by x_W.
model.setObjective(ViewersZTube * xZ + ViewersSoorchle * xS + ViewersWassa * xW, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberAdsZTube'] = NumberAdsZTube.x
variables['NumberAdsSoorchle'] = NumberAdsSoorchle.x
variables['NumberAdsWassa'] = NumberAdsWassa.x
variables['xZ'] = xZ.x
variables['xS'] = xS.x
variables['xW'] = xW.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
