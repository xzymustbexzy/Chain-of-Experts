# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
The butcher shop purchases a certain number of Manual and Automatic slicers.
Each Manual slicer can cut ManualSliceRate slices per minute and requires
ManualGreaseRate units of grease per minute. Each Automatic slicer can cut
AutomaticSliceRate slices per minute and requires AutomaticGreaseRate units of
grease per minute. The total number of slices cut per minute must be at least
MinimumSlicesPerMinute. The total grease usage per minute must not exceed
MaximumGreasePerMinute. Additionally, the number of Manual slicers must be less
than the number of Automatic slicers. The objective is to minimize the total
number of slicers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/77/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ManualSliceRate @Def: The number of slices a manual slicer can cut per minute @Shape: [] 
ManualSliceRate = data['ManualSliceRate']
# @Parameter AutomaticSliceRate @Def: The number of slices an automatic slicer can cut per minute @Shape: [] 
AutomaticSliceRate = data['AutomaticSliceRate']
# @Parameter ManualGreaseRate @Def: The number of units of grease a manual slicer requires per minute @Shape: [] 
ManualGreaseRate = data['ManualGreaseRate']
# @Parameter AutomaticGreaseRate @Def: The number of units of grease an automatic slicer requires per minute @Shape: [] 
AutomaticGreaseRate = data['AutomaticGreaseRate']
# @Parameter MinimumSlicesPerMinute @Def: The minimum number of slices the shop needs to cut per minute @Shape: [] 
MinimumSlicesPerMinute = data['MinimumSlicesPerMinute']
# @Parameter MaximumGreasePerMinute @Def: The maximum number of units of grease the shop can use per minute @Shape: [] 
MaximumGreasePerMinute = data['MaximumGreasePerMinute']

# Variables 
# @Variable NumberManualSlicers @Def: The number of manual slicers @Shape: [] 
NumberManualSlicers = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberManualSlicers")
# @Variable NumberAutomaticSlicers @Def: The number of automatic slicers @Shape: [] 
NumberAutomaticSlicers = model.addVar(vtype=GRB.INTEGER, name="NumberAutomaticSlicers")

# Constraints 
# @Constraint Constr_1 @Def: The total number of slices cut per minute by manual and automatic slicers must be at least MinimumSlicesPerMinute.
model.addConstr(ManualSliceRate * NumberManualSlicers + AutomaticSliceRate * NumberAutomaticSlicers >= MinimumSlicesPerMinute)
# @Constraint Constr_2 @Def: The total grease usage per minute by manual and automatic slicers must not exceed MaximumGreasePerMinute.
model.addConstr(ManualGreaseRate * NumberManualSlicers + AutomaticGreaseRate * NumberAutomaticSlicers <= MaximumGreasePerMinute)
# @Constraint Constr_3 @Def: The number of Manual slicers must be less than the number of Automatic slicers.
model.addConstr(NumberManualSlicers <= NumberAutomaticSlicers - 1)

# Objective 
# @Objective Objective @Def: The total number of slicers is the sum of manual and automatic slicers. The objective is to minimize the total number of slicers.
model.setObjective(NumberManualSlicers + NumberAutomaticSlicers, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberManualSlicers'] = NumberManualSlicers.x
variables['NumberAutomaticSlicers'] = NumberAutomaticSlicers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
