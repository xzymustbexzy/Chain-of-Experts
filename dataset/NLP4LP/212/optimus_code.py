# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A food company aims to determine the number of commercials to run on Pi TV, Beta
Video, and Gamma Live to maximize the total audience. The total cost, calculated
using CostPiTV, CostBetaVideo, and CostGammaLive, must not exceed TotalBudget.
Additionally, the number of commercials on Beta Video must not exceed
MaxCommercialsBetaVideo, the proportion of commercials on Gamma Live must not
exceed MaxGammaProportion, and the proportion of commercials on Pi TV must be at
least MinPiTVProportion.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/213/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostPiTV @Def: Cost per commercial on Pi TV @Shape: [] 
CostPiTV = data['CostPiTV']
# @Parameter CostBetaVideo @Def: Cost per commercial on Beta Video @Shape: [] 
CostBetaVideo = data['CostBetaVideo']
# @Parameter CostGammaLive @Def: Cost per commercial on Gamma Live @Shape: [] 
CostGammaLive = data['CostGammaLive']
# @Parameter AudiencePiTV @Def: Audience per commercial on Pi TV @Shape: [] 
AudiencePiTV = data['AudiencePiTV']
# @Parameter AudienceBetaVideo @Def: Audience per commercial on Beta Video @Shape: [] 
AudienceBetaVideo = data['AudienceBetaVideo']
# @Parameter AudienceGammaLive @Def: Audience per commercial on Gamma Live @Shape: [] 
AudienceGammaLive = data['AudienceGammaLive']
# @Parameter MaxCommercialsBetaVideo @Def: Maximum number of commercials on Beta Video @Shape: [] 
MaxCommercialsBetaVideo = data['MaxCommercialsBetaVideo']
# @Parameter TotalBudget @Def: Total weekly budget @Shape: [] 
TotalBudget = data['TotalBudget']
# @Parameter MaxGammaProportion @Def: Maximum proportion of all commercials on Gamma Live @Shape: [] 
MaxGammaProportion = data['MaxGammaProportion']
# @Parameter MinPiTVProportion @Def: Minimum proportion of all commercials on Pi TV @Shape: [] 
MinPiTVProportion = data['MinPiTVProportion']

# Variables 
# @Variable NumberPiTV @Def: The number of commercials on Pi TV @Shape: [] 
NumberPiTV = model.addVar(vtype=GRB.INTEGER, name="NumberPiTV")
# @Variable NumberBetaVideo @Def: The number of commercials on Beta Video @Shape: [] 
NumberBetaVideo = model.addVar(vtype=GRB.INTEGER, lb=0, ub=MaxCommercialsBetaVideo, name="NumberBetaVideo")
# @Variable NumberGammaLive @Def: The number of commercials on Gamma Live @Shape: [] 
NumberGammaLive = model.addVar(vtype=GRB.INTEGER, name="NumberGammaLive")

# Constraints 
# @Constraint Constr_1 @Def: The total cost, calculated as (CostPiTV * NumberPiTV) + (CostBetaVideo * NumberBetaVideo) + (CostGammaLive * NumberGammaLive), must not exceed TotalBudget.
model.addConstr(CostPiTV * NumberPiTV + CostBetaVideo * NumberBetaVideo + CostGammaLive * NumberGammaLive <= TotalBudget)
# @Constraint Constr_2 @Def: The number of commercials on Beta Video must not exceed MaxCommercialsBetaVideo.
model.addConstr(NumberBetaVideo <= MaxCommercialsBetaVideo)
# @Constraint Constr_3 @Def: The proportion of all commercials on Gamma Live must not exceed MaxGammaProportion.
model.addConstr(NumberGammaLive <= MaxGammaProportion * (NumberPiTV + NumberBetaVideo + NumberGammaLive))
# @Constraint Constr_4 @Def: The proportion of all commercials on Pi TV must be at least MinPiTVProportion.
model.addConstr(NumberPiTV >= MinPiTVProportion * (NumberPiTV + NumberBetaVideo + NumberGammaLive))

# Objective 
# @Objective Objective @Def: Maximize the total audience, which is the sum of (AudiencePiTV * NumberPiTV) + (AudienceBetaVideo * NumberBetaVideo) + (AudienceGammaLive * NumberGammaLive), while adhering to the budget and placement constraints.
model.setObjective(AudiencePiTV * NumberPiTV + AudienceBetaVideo * NumberBetaVideo + AudienceGammaLive * NumberGammaLive, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberPiTV'] = NumberPiTV.x
variables['NumberBetaVideo'] = NumberBetaVideo.x
variables['NumberGammaLive'] = NumberGammaLive.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
