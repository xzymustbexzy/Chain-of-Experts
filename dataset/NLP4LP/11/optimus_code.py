# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A glass factory produces Regular and Tempered glass panes. Producing one Regular
pane requires HeatingRegular time on the heating machine and CoolingRegular time
on the cooling machine. Producing one Tempered pane requires HeatingTempered
time on the heating machine and CoolingTempered time on the cooling machine. The
heating machine is available for a maximum of MaxHeatingTime per day, and the
cooling machine is available for a maximum of MaxCoolingTime per day. Each
Regular pane generates a profit of ProfitRegular, and each Tempered pane
generates a profit of ProfitTempered. The factory aims to determine the number
of Regular and Tempered panes to produce in order to maximize total profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/12/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MaxHeatingTime @Def: Maximum available time for the heating machine per day @Shape: [] 
MaxHeatingTime = data['MaxHeatingTime']
# @Parameter MaxCoolingTime @Def: Maximum available time for the cooling machine per day @Shape: [] 
MaxCoolingTime = data['MaxCoolingTime']
# @Parameter HeatingRegular @Def: Heating time required to produce one regular glass pane @Shape: [] 
HeatingRegular = data['HeatingRegular']
# @Parameter CoolingRegular @Def: Cooling time required to produce one regular glass pane @Shape: [] 
CoolingRegular = data['CoolingRegular']
# @Parameter HeatingTempered @Def: Heating time required to produce one tempered glass pane @Shape: [] 
HeatingTempered = data['HeatingTempered']
# @Parameter CoolingTempered @Def: Cooling time required to produce one tempered glass pane @Shape: [] 
CoolingTempered = data['CoolingTempered']
# @Parameter ProfitRegular @Def: Profit per regular glass pane @Shape: [] 
ProfitRegular = data['ProfitRegular']
# @Parameter ProfitTempered @Def: Profit per tempered glass pane @Shape: [] 
ProfitTempered = data['ProfitTempered']

# Variables 
# @Variable QuantityRegular @Def: The number of regular glass panes to produce @Shape: [] 
QuantityRegular = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityRegular")
# @Variable QuantityTempered @Def: The number of tempered glass panes to produce @Shape: [] 
QuantityTempered = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityTempered")

# Constraints 
# @Constraint Constr_1 @Def: The total heating time required for producing Regular and Tempered panes does not exceed MaxHeatingTime.
model.addConstr(HeatingRegular * QuantityRegular + HeatingTempered * QuantityTempered <= MaxHeatingTime, name="HeatingTime")
# @Constraint Constr_2 @Def: The total cooling time required for producing Regular and Tempered panes does not exceed MaxCoolingTime.
model.addConstr(CoolingRegular * QuantityRegular + CoolingTempered * QuantityTempered <= MaxCoolingTime)

# Objective 
# @Objective Objective @Def: Total profit is ProfitRegular multiplied by the number of Regular panes plus ProfitTempered multiplied by the number of Tempered panes. The objective is to maximize the total profit.
model.setObjective(ProfitRegular * QuantityRegular + ProfitTempered * QuantityTempered, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityRegular'] = QuantityRegular.x
variables['QuantityTempered'] = QuantityTempered.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
