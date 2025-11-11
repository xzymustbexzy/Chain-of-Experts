# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A high rise building is purchasing new model furnaces and old model furnaces.
Each new model furnace can heat HeatingCapacityNew apartments and consumes
EnergyConsumptionNew kWh per day. Each old model furnace can heat
HeatingCapacityOld apartments and consumes EnergyConsumptionOld kWh per day. At
most MaxFractionOld fraction of the furnaces can be old model furnaces and at
least MinNewFurnaces new model furnaces must be used. The building needs to heat
at least MinHeatingRequirement apartments and has AvailableEnergy kWh of
electricity available. Determine the number of each type of furnace to purchase
to minimize the total number of furnaces.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/51/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter HeatingCapacityNew @Def: Heating capacity of a new model furnace in the number of apartments heated per furnace @Shape: [] 
HeatingCapacityNew = data['HeatingCapacityNew']
# @Parameter EnergyConsumptionNew @Def: Energy consumption of a new model furnace in kWh per day @Shape: [] 
EnergyConsumptionNew = data['EnergyConsumptionNew']
# @Parameter HeatingCapacityOld @Def: Heating capacity of an old model furnace in the number of apartments heated per furnace @Shape: [] 
HeatingCapacityOld = data['HeatingCapacityOld']
# @Parameter EnergyConsumptionOld @Def: Energy consumption of an old model furnace in kWh per day @Shape: [] 
EnergyConsumptionOld = data['EnergyConsumptionOld']
# @Parameter MaxFractionOld @Def: Maximum fraction of furnaces that can be the old model @Shape: [] 
MaxFractionOld = data['MaxFractionOld']
# @Parameter MinNewFurnaces @Def: Minimum number of new model furnaces that must be used @Shape: [] 
MinNewFurnaces = data['MinNewFurnaces']
# @Parameter MinHeatingRequirement @Def: Minimum number of apartments that need to be heated @Shape: [] 
MinHeatingRequirement = data['MinHeatingRequirement']
# @Parameter AvailableEnergy @Def: Total available electricity in kWh @Shape: [] 
AvailableEnergy = data['AvailableEnergy']

# Variables 
# @Variable NumberOldFurnaces @Def: The number of old model furnaces @Shape: ['Integer'] 
NumberOldFurnaces = model.addVar(vtype=GRB.INTEGER, name="NumberOldFurnaces")
# @Variable NumberNewFurnaces @Def: The number of new model furnaces @Shape: ['Integer'] 
NumberNewFurnaces = model.addVar(vtype=GRB.INTEGER, name="NumberNewFurnaces")

# Constraints 
# @Constraint Constr_1 @Def: The number of old model furnaces does not exceed MaxFractionOld fraction of the total furnaces.
model.addConstr(NumberOldFurnaces <= MaxFractionOld * (NumberOldFurnaces + NumberNewFurnaces))
# @Constraint Constr_2 @Def: At least MinNewFurnaces new model furnaces must be used.
model.addConstr(NumberNewFurnaces >= MinNewFurnaces)
# @Constraint Constr_3 @Def: The total heating capacity must be at least MinHeatingRequirement apartments.
model.addConstr(HeatingCapacityOld * NumberOldFurnaces + HeatingCapacityNew * NumberNewFurnaces >= MinHeatingRequirement)
# @Constraint Constr_4 @Def: The total energy consumption must not exceed AvailableEnergy kWh.
model.addConstr(EnergyConsumptionOld * NumberOldFurnaces + EnergyConsumptionNew * NumberNewFurnaces <= AvailableEnergy)

# Objective 
# @Objective Objective @Def: Minimize the total number of furnaces.
model.setObjective(NumberOldFurnaces + NumberNewFurnaces, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOldFurnaces'] = NumberOldFurnaces.x
variables['NumberNewFurnaces'] = NumberNewFurnaces.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
