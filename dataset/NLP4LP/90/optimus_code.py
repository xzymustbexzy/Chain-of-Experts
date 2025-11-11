# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A man selects quantities of alpha and omega brand meal replacement drink bottles
to minimize the total sugar intake, calculated as SugarAlpha multiplied by the
number of alpha bottles plus SugarOmega multiplied by the number of omega
bottles. The selection must ensure that the total protein intake, which is
ProteinAlpha times the number of alpha bottles plus ProteinOmega times the
number of omega bottles, is at least MinProtein. Additionally, the total calorie
intake, defined as CaloriesAlpha times the number of alpha bottles plus
CaloriesOmega times the number of omega bottles, must be at least MinCalories.
Furthermore, the proportion of omega brand bottles should not exceed
MaxOmegaFraction of the total number of bottles consumed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/91/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProteinAlpha @Def: Amount of protein per bottle of the alpha brand drink @Shape: [] 
ProteinAlpha = data['ProteinAlpha']
# @Parameter SugarAlpha @Def: Amount of sugar per bottle of the alpha brand drink @Shape: [] 
SugarAlpha = data['SugarAlpha']
# @Parameter CaloriesAlpha @Def: Number of calories per bottle of the alpha brand drink @Shape: [] 
CaloriesAlpha = data['CaloriesAlpha']
# @Parameter ProteinOmega @Def: Amount of protein per bottle of the omega brand drink @Shape: [] 
ProteinOmega = data['ProteinOmega']
# @Parameter SugarOmega @Def: Amount of sugar per bottle of the omega brand drink @Shape: [] 
SugarOmega = data['SugarOmega']
# @Parameter CaloriesOmega @Def: Number of calories per bottle of the omega brand drink @Shape: [] 
CaloriesOmega = data['CaloriesOmega']
# @Parameter MinProtein @Def: Minimum total protein required @Shape: [] 
MinProtein = data['MinProtein']
# @Parameter MinCalories @Def: Minimum total calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MaxOmegaFraction @Def: Maximum proportion of omega brand drinks allowed @Shape: [] 
MaxOmegaFraction = data['MaxOmegaFraction']

# Variables 
# @Variable QuantityAlpha @Def: The number of alpha brand drink bottles @Shape: [] 
QuantityAlpha = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityAlpha")
# @Variable QuantityOmega @Def: The number of omega brand drink bottles @Shape: [] 
QuantityOmega = model.addVar(vtype=GRB.CONTINUOUS, name="QuantityOmega")

# Constraints 
# @Constraint Constr_1 @Def: The total protein intake from alpha and omega bottles must be at least MinProtein.
model.addConstr(ProteinAlpha * QuantityAlpha + ProteinOmega * QuantityOmega >= MinProtein)
# @Constraint Constr_2 @Def: The total calorie intake from alpha and omega bottles must be at least MinCalories.
model.addConstr(CaloriesAlpha * QuantityAlpha + CaloriesOmega * QuantityOmega >= MinCalories)
# @Constraint Constr_3 @Def: The proportion of omega brand bottles must not exceed MaxOmegaFraction of the total number of bottles consumed.
model.addConstr((1 - MaxOmegaFraction) * QuantityOmega <= MaxOmegaFraction * QuantityAlpha)

# Objective 
# @Objective Objective @Def: Minimize the total sugar intake, calculated as SugarAlpha multiplied by the number of alpha bottles plus SugarOmega multiplied by the number of omega bottles.
model.setObjective(SugarAlpha * QuantityAlpha + SugarOmega * QuantityOmega, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityAlpha'] = QuantityAlpha.x
variables['QuantityOmega'] = QuantityOmega.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
