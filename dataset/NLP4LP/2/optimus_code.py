# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A cleaning company aims to maximize exposure for promoting a new product without
exceeding AdvertisingBudget. They allocate funds to two advertising methods:
radio ads and social media ads. Each radio ad incurs a cost of CostRadioAd and
yields ExposureRadioAd expected viewers. Each social media ad costs
CostSocialMediaAd and generates ExposureSocialMediaAd expected viewers. The
company decides that the number of radio ads must be at least MinRadioAds and at
most MaxRadioAds, and that at least MinSocialMediaAds social media ads should be
contracted. Determine the number of each type of advertisement to maximize total
exposure while remaining within the advertising budget.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/3/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AdvertisingBudget @Def: The total advertising budget available @Shape: [] 
AdvertisingBudget = data['AdvertisingBudget']
# @Parameter CostRadioAd @Def: Cost of one radio advertisement @Shape: [] 
CostRadioAd = data['CostRadioAd']
# @Parameter CostSocialMediaAd @Def: Cost of one social media advertisement @Shape: [] 
CostSocialMediaAd = data['CostSocialMediaAd']
# @Parameter ExposureRadioAd @Def: Expected exposure (viewers) for each radio advertisement @Shape: [] 
ExposureRadioAd = data['ExposureRadioAd']
# @Parameter ExposureSocialMediaAd @Def: Expected exposure (viewers) for each social media advertisement @Shape: [] 
ExposureSocialMediaAd = data['ExposureSocialMediaAd']
# @Parameter MinRadioAds @Def: Minimum number of radio advertisements to be ordered @Shape: [] 
MinRadioAds = data['MinRadioAds']
# @Parameter MaxRadioAds @Def: Maximum number of radio advertisements to be ordered @Shape: [] 
MaxRadioAds = data['MaxRadioAds']
# @Parameter MinSocialMediaAds @Def: Minimum number of social media advertisements to be contracted @Shape: [] 
MinSocialMediaAds = data['MinSocialMediaAds']

# Variables 
# @Variable NumberRadioAds @Def: The number of radio advertisements to be ordered @Shape: [] 
NumberRadioAds = model.addVar(vtype=GRB.INTEGER, lb=MinRadioAds, ub=MaxRadioAds, name="NumberRadioAds")
# @Variable NumberSocialMediaAds @Def: The number of social media advertisements to be contracted @Shape: [] 
NumberSocialMediaAds = model.addVar(vtype=GRB.INTEGER, lb=MinSocialMediaAds, name="NumberSocialMediaAds")

# Constraints 
# @Constraint Constr_1 @Def: The total cost of radio ads and social media ads cannot exceed the AdvertisingBudget.
model.addConstr(CostRadioAd * NumberRadioAds + CostSocialMediaAd * NumberSocialMediaAds <= AdvertisingBudget)
# @Constraint Constr_2 @Def: The number of radio ads must be at least MinRadioAds and at most MaxRadioAds.
model.addConstr(NumberRadioAds >= MinRadioAds)
model.addConstr(NumberRadioAds <= MaxRadioAds)
# @Constraint Constr_3 @Def: At least MinSocialMediaAds social media ads must be contracted.
model.addConstr(NumberSocialMediaAds >= MinSocialMediaAds)

# Objective 
# @Objective Objective @Def: Maximize total exposure, which is the sum of expected viewers from radio ads and social media ads, while remaining within the advertising budget and satisfying constraints on the number of each type of advertisement.
model.setObjective(ExposureRadioAd * NumberRadioAds + ExposureSocialMediaAd * NumberSocialMediaAds, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberRadioAds'] = NumberRadioAds.x
variables['NumberSocialMediaAds'] = NumberSocialMediaAds.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
