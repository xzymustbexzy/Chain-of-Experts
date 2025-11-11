# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A strata-management company aims to purchase a combination of low-powered and
high-powered air conditioners. Each low-powered air conditioner provides
LowPowerCoolingCapacity and consumes LowPowerElectricityUsage units of
electricity daily. Each high-powered air conditioner provides
HighPowerCoolingCapacity and consumes HighPowerElectricityUsage units of
electricity daily. The number of low-powered air conditioners is restricted to
MaxLowPowerPercentage of the total air conditioners. Additionally, the company
must acquire at least MinHighPowerModels high-powered air conditioners. The
total cooling requirement is TotalCoolingRequired housing units, and the
available electricity is TotalElectricityAvailable units. The objective is to
minimize the total number of air conditioners purchased.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/219/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter LowPowerCoolingCapacity @Def: Cooling capacity of a low-powered air conditioner (number of housing units it can cool) @Shape: [] 
LowPowerCoolingCapacity = data['LowPowerCoolingCapacity']
# @Parameter LowPowerElectricityUsage @Def: Electricity usage of a low-powered air conditioner (units per day) @Shape: [] 
LowPowerElectricityUsage = data['LowPowerElectricityUsage']
# @Parameter HighPowerCoolingCapacity @Def: Cooling capacity of a high-powered air conditioner (number of housing units it can cool) @Shape: [] 
HighPowerCoolingCapacity = data['HighPowerCoolingCapacity']
# @Parameter HighPowerElectricityUsage @Def: Electricity usage of a high-powered air conditioner (units per day) @Shape: [] 
HighPowerElectricityUsage = data['HighPowerElectricityUsage']
# @Parameter MaxLowPowerPercentage @Def: Maximum percentage of low-powered air conditioners allowed @Shape: [] 
MaxLowPowerPercentage = data['MaxLowPowerPercentage']
# @Parameter MinHighPowerModels @Def: Minimum number of high-powered air conditioners required @Shape: [] 
MinHighPowerModels = data['MinHighPowerModels']
# @Parameter TotalCoolingRequired @Def: Total number of housing units to be cooled @Shape: [] 
TotalCoolingRequired = data['TotalCoolingRequired']
# @Parameter TotalElectricityAvailable @Def: Total units of electricity available @Shape: [] 
TotalElectricityAvailable = data['TotalElectricityAvailable']

# Variables 
# @Variable LowPowerUnits @Def: The number of low-powered air conditioners @Shape: [] 
LowPowerUnits = model.addVar(vtype=GRB.INTEGER, name="LowPowerUnits")
# @Variable HighPowerUnits @Def: The number of high-powered air conditioners @Shape: [] 
HighPowerUnits = model.addVar(vtype=GRB.INTEGER, name="HighPowerUnits")

# Constraints 
# @Constraint Constr_1 @Def: The total cooling capacity provided by low-powered and high-powered air conditioners must meet or exceed the total cooling requirement of TotalCoolingRequired housing units.
model.addConstr(LowPowerCoolingCapacity * LowPowerUnits + HighPowerCoolingCapacity * HighPowerUnits >= TotalCoolingRequired)
# @Constraint Constr_2 @Def: The total electricity consumption of all air conditioners must not exceed the available electricity of TotalElectricityAvailable units.
model.addConstr(LowPowerElectricityUsage * LowPowerUnits + HighPowerElectricityUsage * HighPowerUnits <= TotalElectricityAvailable)
# @Constraint Constr_3 @Def: The number of low-powered air conditioners must not exceed MaxLowPowerPercentage of the total number of air conditioners purchased.
model.addConstr(LowPowerUnits <= MaxLowPowerPercentage * (LowPowerUnits + HighPowerUnits))
# @Constraint Constr_4 @Def: At least MinHighPowerModels high-powered air conditioners must be acquired.
model.addConstr(HighPowerUnits >= MinHighPowerModels)

# Objective 
# @Objective Objective @Def: Minimize the total number of air conditioners purchased.
model.setObjective(LowPowerUnits + HighPowerUnits, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LowPowerUnits'] = LowPowerUnits.x
variables['HighPowerUnits'] = HighPowerUnits.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
