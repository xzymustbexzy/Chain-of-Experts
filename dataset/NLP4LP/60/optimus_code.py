# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A laundromat can buy two types of washing machines, a top-loading model and a
front-loading model. The top-loading model can wash WashRateTopLoading items per
day while the front-loading model can wash WashRateFrontLoading items per day.
The top-loading model consumes EnergyConsumptionTopLoading kWh per day while the
front-loading model consumes EnergyConsumptionFrontLoading kWh per day. The
laundromat must be able to wash at least MinItemsPerDay items per day and has
available MaxEnergyPerDay kWh per day. Since the top-loading machines are harder
to use, at most MaxFractionTopLoading of the machines can be top-loading.
Further, at least MinNumFrontLoading machines should be front-loading. How many
of each machine should the laundromat buy to minimize the total number of
washing machines?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/61/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter WashRateTopLoading @Def: Number of items washed per day by a top-loading machine @Shape: [] 
WashRateTopLoading = data['WashRateTopLoading']
# @Parameter WashRateFrontLoading @Def: Number of items washed per day by a front-loading machine @Shape: [] 
WashRateFrontLoading = data['WashRateFrontLoading']
# @Parameter EnergyConsumptionTopLoading @Def: Energy consumed per day by a top-loading machine (kWh) @Shape: [] 
EnergyConsumptionTopLoading = data['EnergyConsumptionTopLoading']
# @Parameter EnergyConsumptionFrontLoading @Def: Energy consumed per day by a front-loading machine (kWh) @Shape: [] 
EnergyConsumptionFrontLoading = data['EnergyConsumptionFrontLoading']
# @Parameter MinItemsPerDay @Def: Minimum number of items to wash per day @Shape: [] 
MinItemsPerDay = data['MinItemsPerDay']
# @Parameter MaxEnergyPerDay @Def: Maximum available energy per day (kWh) @Shape: [] 
MaxEnergyPerDay = data['MaxEnergyPerDay']
# @Parameter MaxFractionTopLoading @Def: Maximum fraction of machines that can be top-loading @Shape: [] 
MaxFractionTopLoading = data['MaxFractionTopLoading']
# @Parameter MinNumFrontLoading @Def: Minimum number of front-loading machines @Shape: [] 
MinNumFrontLoading = data['MinNumFrontLoading']

# Variables 
# @Variable NumTopLoading @Def: The number of top-loading machines @Shape: [] 
NumTopLoading = model.addVar(vtype=GRB.INTEGER, name="NumTopLoading")
# @Variable NumFrontLoading @Def: The number of front-loading machines @Shape: [] 
NumFrontLoading = model.addVar(vtype=GRB.INTEGER, lb=MinNumFrontLoading, name="NumFrontLoading")

# Constraints 
# @Constraint Constr_1 @Def: A top-loading machine washes WashRateTopLoading items per day and a front-loading machine washes WashRateFrontLoading items per day. The total number of items washed per day must be at least MinItemsPerDay.
model.addConstr(WashRateTopLoading * NumTopLoading + WashRateFrontLoading * NumFrontLoading >= MinItemsPerDay)
# @Constraint Constr_2 @Def: A top-loading machine consumes EnergyConsumptionTopLoading kWh per day and a front-loading machine consumes EnergyConsumptionFrontLoading kWh per day. The total energy consumption per day cannot exceed MaxEnergyPerDay kWh.
model.addConstr(EnergyConsumptionTopLoading * NumTopLoading + EnergyConsumptionFrontLoading * NumFrontLoading <= MaxEnergyPerDay)
# @Constraint Constr_3 @Def: At most MaxFractionTopLoading fraction of the total machines can be top-loading.
model.addConstr(NumTopLoading <= MaxFractionTopLoading * (NumTopLoading + NumFrontLoading))
# @Constraint Constr_4 @Def: At least MinNumFrontLoading machines must be front-loading.
model.addConstr(NumFrontLoading >= MinNumFrontLoading)

# Objective 
# @Objective Objective @Def: Minimize the total number of washing machines purchased.
model.setObjective(NumTopLoading + NumFrontLoading, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumTopLoading'] = NumTopLoading.x
variables['NumFrontLoading'] = NumFrontLoading.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
