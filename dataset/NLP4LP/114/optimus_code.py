# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient takes anxiety medication and anti-depressants sequentially. Each unit
of anxiety medication takes TimePerAnxietyUnit time to be effective, while each
unit of anti-depressant takes TimePerAntidepressantUnit time to be effective.
The patient must take at least MinimumTotalUnits of medication, with at least
MinimumAnxietyUnits being anxiety medication. Additionally, the amount of
anxiety medication cannot exceed MaximumAnxietyToAntidepressantRatio times the
amount of anti-depressants. The objective is to determine the number of units of
each medication to minimize the total time until the medications become
effective.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/115/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TimePerAnxietyUnit @Def: Time it takes for one unit of anxiety medication to be effective @Shape: [] 
TimePerAnxietyUnit = data['TimePerAnxietyUnit']
# @Parameter TimePerAntidepressantUnit @Def: Time it takes for one unit of anti-depressant to be effective @Shape: [] 
TimePerAntidepressantUnit = data['TimePerAntidepressantUnit']
# @Parameter MinimumTotalUnits @Def: Minimum total units of medication the patient must take @Shape: [] 
MinimumTotalUnits = data['MinimumTotalUnits']
# @Parameter MinimumAnxietyUnits @Def: Minimum units of anxiety medication the patient must take @Shape: [] 
MinimumAnxietyUnits = data['MinimumAnxietyUnits']
# @Parameter MaximumAnxietyToAntidepressantRatio @Def: Maximum ratio of anxiety medication units to anti-depressant units @Shape: [] 
MaximumAnxietyToAntidepressantRatio = data['MaximumAnxietyToAntidepressantRatio']

# Variables 
# @Variable AnxietyUnits @Def: Units of anxiety medication the patient takes @Shape: [] 
AnxietyUnits = model.addVar(vtype=GRB.CONTINUOUS, lb=MinimumAnxietyUnits, name="AnxietyUnits")
# @Variable AntidepressantUnits @Def: Units of anti-depressant medication the patient takes @Shape: [] 
AntidepressantUnits = model.addVar(vtype=GRB.CONTINUOUS, name="AntidepressantUnits")

# Constraints 
# @Constraint Constr_1 @Def: The patient must take at least MinimumTotalUnits of medication.
model.addConstr(AnxietyUnits + AntidepressantUnits >= MinimumTotalUnits)
# @Constraint Constr_2 @Def: At least MinimumAnxietyUnits must be anxiety medication.
model.addConstr(AnxietyUnits >= MinimumAnxietyUnits)
# @Constraint Constr_3 @Def: The amount of anxiety medication cannot exceed MaximumAnxietyToAntidepressantRatio times the amount of anti-depressants.
model.addConstr(AnxietyUnits <= MaximumAnxietyToAntidepressantRatio * AntidepressantUnits)

# Objective 
# @Objective Objective @Def: Minimize the total time until the medications become effective, calculated as (Number of Anxiety Units × TimePerAnxietyUnit) + (Number of Anti-depressant Units × TimePerAntidepressantUnit).
model.setObjective(AnxietyUnits * TimePerAnxietyUnit + AntidepressantUnits * TimePerAntidepressantUnit, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AnxietyUnits'] = AnxietyUnits.x
variables['AntidepressantUnits'] = AntidepressantUnits.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
