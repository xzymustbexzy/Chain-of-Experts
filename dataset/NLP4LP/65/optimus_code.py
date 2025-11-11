# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A grilled cheese shop sells Light and Heavy grilled cheese sandwiches. A Light
grilled cheese sandwich requires BreadPerLight slices of bread and
CheesePerLight slices of cheese. A Heavy grilled cheese sandwich requires
BreadPerHeavy slices of bread and CheesePerHeavy slices of cheese. The store
must make at least MinHeavyToLightRatio times as many Heavy grilled cheese
sandwiches as Light grilled cheese sandwiches. The store has TotalBread slices
of bread and TotalCheese slices of cheese available. A Light grilled cheese
sandwich takes TimePerLight minutes to make and a Heavy grilled cheese sandwich
takes TimePerHeavy minutes to make. The objective is to minimize the total
production time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/66/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter BreadPerLight @Def: Number of slices of bread required to make one light grilled cheese sandwich @Shape: [] 
BreadPerLight = data['BreadPerLight']
# @Parameter CheesePerLight @Def: Number of slices of cheese required to make one light grilled cheese sandwich @Shape: [] 
CheesePerLight = data['CheesePerLight']
# @Parameter BreadPerHeavy @Def: Number of slices of bread required to make one heavy grilled cheese sandwich @Shape: [] 
BreadPerHeavy = data['BreadPerHeavy']
# @Parameter CheesePerHeavy @Def: Number of slices of cheese required to make one heavy grilled cheese sandwich @Shape: [] 
CheesePerHeavy = data['CheesePerHeavy']
# @Parameter MinHeavyToLightRatio @Def: Minimum ratio of heavy grilled cheese sandwiches to light grilled cheese sandwiches @Shape: [] 
MinHeavyToLightRatio = data['MinHeavyToLightRatio']
# @Parameter TotalBread @Def: Total number of slices of bread available @Shape: [] 
TotalBread = data['TotalBread']
# @Parameter TotalCheese @Def: Total number of slices of cheese available @Shape: [] 
TotalCheese = data['TotalCheese']
# @Parameter TimePerLight @Def: Time in minutes to make one light grilled cheese sandwich @Shape: [] 
TimePerLight = data['TimePerLight']
# @Parameter TimePerHeavy @Def: Time in minutes to make one heavy grilled cheese sandwich @Shape: [] 
TimePerHeavy = data['TimePerHeavy']

# Variables 
# @Variable LightSandwiches @Def: The number of light grilled cheese sandwiches produced @Shape: [] 
LightSandwiches = model.addVar(vtype=GRB.CONTINUOUS, name="LightSandwiches")
# @Variable HeavySandwiches @Def: The number of heavy grilled cheese sandwiches produced @Shape: [] 
HeavySandwiches = model.addVar(vtype=GRB.CONTINUOUS, name="HeavySandwiches")

# Constraints 
# @Constraint Constr_1 @Def: The total number of bread slices used for Light and Heavy sandwiches does not exceed TotalBread.
model.addConstr(BreadPerLight * LightSandwiches + BreadPerHeavy * HeavySandwiches <= TotalBread)
# @Constraint Constr_2 @Def: The total number of cheese slices used for Light and Heavy sandwiches does not exceed TotalCheese.
model.addConstr(CheesePerLight * LightSandwiches + CheesePerHeavy * HeavySandwiches <= TotalCheese)
# @Constraint Constr_3 @Def: The number of Heavy grilled cheese sandwiches is at least MinHeavyToLightRatio times the number of Light grilled cheese sandwiches.
model.addConstr(HeavySandwiches >= MinHeavyToLightRatio * LightSandwiches)

# Objective 
# @Objective Objective @Def: Total production time is the sum of the production times for Light and Heavy grilled cheese sandwiches. The objective is to minimize the total production time.
model.setObjective(TimePerLight * LightSandwiches + TimePerHeavy * HeavySandwiches, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LightSandwiches'] = LightSandwiches.x
variables['HeavySandwiches'] = HeavySandwiches.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
