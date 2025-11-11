# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A crepe store produces two types of crepes: chocolate and peanut butter. Each
chocolate crepe requires ChocolateSpreadPerChocolateCrepe units of chocolate
spread and CrepeMixPerChocolateCrepe units of crepe mix. Each peanut butter
crepe requires PeanutButterSpreadPerPeanutButterCrepe units of peanut butter
spread and CrepeMixPerPeanutButterCrepe units of crepe mix. The number of peanut
butter crepes produced must exceed the number of chocolate crepes, and at least
MinimumProportionChocolateCrepes proportion of the total crepes must be
chocolate. The store has TotalAvailableChocolateSpread units of chocolate spread
and TotalAvailablePeanutButterSpread units of peanut butter spread available.
The objective is to determine the number of each type of crepe to minimize the
total amount of crepe mix used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/69/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ChocolateSpreadPerChocolateCrepe @Def: Amount of chocolate spread required to make one chocolate crepe @Shape: [] 
ChocolateSpreadPerChocolateCrepe = data['ChocolateSpreadPerChocolateCrepe']
# @Parameter PeanutButterSpreadPerPeanutButterCrepe @Def: Amount of peanut butter spread required to make one peanut butter crepe @Shape: [] 
PeanutButterSpreadPerPeanutButterCrepe = data['PeanutButterSpreadPerPeanutButterCrepe']
# @Parameter CrepeMixPerChocolateCrepe @Def: Amount of crepe mix required to make one chocolate crepe @Shape: [] 
CrepeMixPerChocolateCrepe = data['CrepeMixPerChocolateCrepe']
# @Parameter CrepeMixPerPeanutButterCrepe @Def: Amount of crepe mix required to make one peanut butter crepe @Shape: [] 
CrepeMixPerPeanutButterCrepe = data['CrepeMixPerPeanutButterCrepe']
# @Parameter TotalAvailableChocolateSpread @Def: Total available units of chocolate spread @Shape: [] 
TotalAvailableChocolateSpread = data['TotalAvailableChocolateSpread']
# @Parameter TotalAvailablePeanutButterSpread @Def: Total available units of peanut butter spread @Shape: [] 
TotalAvailablePeanutButterSpread = data['TotalAvailablePeanutButterSpread']
# @Parameter MinimumProportionChocolateCrepes @Def: Minimum proportion of crepes that must be chocolate @Shape: [] 
MinimumProportionChocolateCrepes = data['MinimumProportionChocolateCrepes']

# Variables 
# @Variable NumberOfChocolateCrepes @Def: The number of chocolate crepes made @Shape: [] 
NumberOfChocolateCrepes = model.addVar(vtype=GRB.INTEGER, name="NumberOfChocolateCrepes")
# @Variable NumberOfPeanutButterCrepes @Def: The number of peanut butter crepes made @Shape: [] 
NumberOfPeanutButterCrepes = model.addVar(vtype=GRB.INTEGER, name="NumberOfPeanutButterCrepes")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of chocolate spread used is equal to ChocolateSpreadPerChocolateCrepe multiplied by the number of chocolate crepes. This must not exceed TotalAvailableChocolateSpread.
model.addConstr(ChocolateSpreadPerChocolateCrepe * NumberOfChocolateCrepes <= TotalAvailableChocolateSpread)
# @Constraint Constr_2 @Def: The total amount of peanut butter spread used is equal to PeanutButterSpreadPerPeanutButterCrepe multiplied by the number of peanut butter crepes. This must not exceed TotalAvailablePeanutButterSpread.
model.addConstr(PeanutButterSpreadPerPeanutButterCrepe * NumberOfPeanutButterCrepes <= TotalAvailablePeanutButterSpread)
# @Constraint Constr_3 @Def: The number of peanut butter crepes produced must exceed the number of chocolate crepes.
model.addConstr(NumberOfPeanutButterCrepes >= NumberOfChocolateCrepes + 1)
# @Constraint Constr_4 @Def: At least MinimumProportionChocolateCrepes proportion of the total crepes produced must be chocolate crepes.
model.addConstr(NumberOfChocolateCrepes >= MinimumProportionChocolateCrepes * (NumberOfChocolateCrepes + NumberOfPeanutButterCrepes))

# Objective 
# @Objective Objective @Def: Minimize the total amount of crepe mix used, which is the sum of CrepeMixPerChocolateCrepe multiplied by the number of chocolate crepes and CrepeMixPerPeanutButterCrepe multiplied by the number of peanut butter crepes.
model.setObjective(CrepeMixPerChocolateCrepe * NumberOfChocolateCrepes + CrepeMixPerPeanutButterCrepe * NumberOfPeanutButterCrepes, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfChocolateCrepes'] = NumberOfChocolateCrepes.x
variables['NumberOfPeanutButterCrepes'] = NumberOfPeanutButterCrepes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
