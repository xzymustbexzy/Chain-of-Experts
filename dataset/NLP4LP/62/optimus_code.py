# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A shipping company can purchase RegularVans and HybridVans to make deliveries.
Each RegularVan delivers PackagesDeliveredRegular packages per day and produces
PollutantsRegular units of pollutants, while each HybridVan delivers
PackagesDeliveredHybrid packages per day and produces PollutantsHybrid units of
pollutants. The company must deliver at least MinPackages packages per day and
ensure that total pollutants do not exceed MaxPollutants units per day. The
objective is to determine the number of RegularVans and HybridVans to purchase
in order to minimize the total number of vans used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/63/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PackagesDeliveredRegular @Def: Number of packages a regular van can deliver per day @Shape: [] 
PackagesDeliveredRegular = data['PackagesDeliveredRegular']
# @Parameter PackagesDeliveredHybrid @Def: Number of packages a hybrid van can deliver per day @Shape: [] 
PackagesDeliveredHybrid = data['PackagesDeliveredHybrid']
# @Parameter PollutantsRegular @Def: Number of pollutant units produced by a regular van per day @Shape: [] 
PollutantsRegular = data['PollutantsRegular']
# @Parameter PollutantsHybrid @Def: Number of pollutant units produced by a hybrid van per day @Shape: [] 
PollutantsHybrid = data['PollutantsHybrid']
# @Parameter MaxPollutants @Def: Maximum allowed pollutant units per day @Shape: [] 
MaxPollutants = data['MaxPollutants']
# @Parameter MinPackages @Def: Minimum required number of packages per day @Shape: [] 
MinPackages = data['MinPackages']

# Variables 
# @Variable RegularVans @Def: The number of regular vans used per day @Shape: [] 
RegularVans = model.addVar(vtype=GRB.INTEGER, name="RegularVans")
# @Variable HybridVans @Def: The number of hybrid vans used per day @Shape: [] 
HybridVans = model.addVar(vtype=GRB.INTEGER, name="HybridVans")

# Constraints 
# @Constraint Constr_1 @Def: The company must deliver at least MinPackages packages per day.
model.addConstr(RegularVans * PackagesDeliveredRegular + HybridVans * PackagesDeliveredHybrid >= MinPackages)
# @Constraint Constr_2 @Def: Ensure that total pollutants do not exceed MaxPollutants units per day.
model.addConstr(PollutantsRegular * RegularVans + PollutantsHybrid * HybridVans <= MaxPollutants)

# Objective 
# @Objective Objective @Def: Minimize the total number of vans used.
model.setObjective(RegularVans + HybridVans, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['RegularVans'] = RegularVans.x
variables['HybridVans'] = HybridVans.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
