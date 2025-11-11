# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A hospital purchases two types of pills: prevention pills and treatment pills.
Each prevention pill costs PreventionPillCost to make, while each treatment pill
costs TreatmentPillCost to make. The hospital must purchase at least
PreventionToTreatmentRatio times as many prevention pills as treatment pills and
must purchase at least MinimumTreatmentPills treatment pills. With a total
budget of Budget, the objective is to maximize the number of patients that can
be treated.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/230/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PreventionPillCost @Def: Cost to make one prevention pill @Shape: [] 
PreventionPillCost = data['PreventionPillCost']
# @Parameter TreatmentPillCost @Def: Cost to make one treatment pill @Shape: [] 
TreatmentPillCost = data['TreatmentPillCost']
# @Parameter PreventionToTreatmentRatio @Def: Minimum ratio of prevention pills to treatment pills @Shape: [] 
PreventionToTreatmentRatio = data['PreventionToTreatmentRatio']
# @Parameter MinimumTreatmentPills @Def: Minimum number of treatment pills to purchase @Shape: [] 
MinimumTreatmentPills = data['MinimumTreatmentPills']
# @Parameter Budget @Def: Total budget available for purchasing pills @Shape: [] 
Budget = data['Budget']

# Variables 
# @Variable NumPreventionPills @Def: The number of prevention pills to purchase @Shape: [] 
NumPreventionPills = model.addVar(vtype=GRB.INTEGER, name="NumPreventionPills")
# @Variable NumTreatmentPills @Def: The number of treatment pills to purchase @Shape: [] 
NumTreatmentPills = model.addVar(vtype=GRB.INTEGER, name="NumTreatmentPills")

# Constraints 
# @Constraint Constr_1 @Def: The total cost of prevention and treatment pills cannot exceed the budget.
model.addConstr(PreventionPillCost * NumPreventionPills + TreatmentPillCost * NumTreatmentPills <= Budget)
# @Constraint Constr_2 @Def: The number of prevention pills purchased must be at least PreventionToTreatmentRatio times the number of treatment pills purchased.
model.addConstr(NumPreventionPills >= PreventionToTreatmentRatio * NumTreatmentPills)
# @Constraint Constr_3 @Def: At least MinimumTreatmentPills treatment pills must be purchased.
model.addConstr(NumTreatmentPills >= MinimumTreatmentPills)

# Objective 
# @Objective Objective @Def: The objective is to maximize the number of patients that can be treated without exceeding the budget and while satisfying the purchase ratios and minimum treatment pill requirements.
model.setObjective(NumTreatmentPills, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPreventionPills'] = NumPreventionPills.x
variables['NumTreatmentPills'] = NumTreatmentPills.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
