# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A bakery produces Brownies and LemonSquares. Each Brownie requires
ChocolateMixPerBrownie units of ChocolateMix and FiberPerBrownie units of Fiber.
Each LemonSquare requires LemonMixPerLemonSquare units of LemonMix and
FiberPerLemonSquare units of Fiber. The number of LemonSquares produced must
exceed the number of Brownies produced. Additionally, at least
MinBrowniePercentage of the total items produced must be Brownies. The bakery
has TotalChocolateMix units of ChocolateMix and TotalLemonMix units of LemonMix
available. The objective is to minimize the total Fiber used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/59/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ChocolateMixPerBrownie @Def: Amount of chocolate mix required to produce one brownie @Shape: [] 
ChocolateMixPerBrownie = data['ChocolateMixPerBrownie']
# @Parameter FiberPerBrownie @Def: Amount of fiber required to produce one brownie @Shape: [] 
FiberPerBrownie = data['FiberPerBrownie']
# @Parameter LemonMixPerLemonSquare @Def: Amount of lemon mix required to produce one lemon square @Shape: [] 
LemonMixPerLemonSquare = data['LemonMixPerLemonSquare']
# @Parameter FiberPerLemonSquare @Def: Amount of fiber required to produce one lemon square @Shape: [] 
FiberPerLemonSquare = data['FiberPerLemonSquare']
# @Parameter TotalChocolateMix @Def: Total units of chocolate mix available @Shape: [] 
TotalChocolateMix = data['TotalChocolateMix']
# @Parameter TotalLemonMix @Def: Total units of lemon mix available @Shape: [] 
TotalLemonMix = data['TotalLemonMix']
# @Parameter MinBrowniePercentage @Def: Minimum percentage of items that must be brownies @Shape: [] 
MinBrowniePercentage = data['MinBrowniePercentage']
# @Parameter MinLemonExceedsBrownie @Def: Minimum required difference between the number of lemon squares and brownies @Shape: [] 
MinLemonExceedsBrownie = data['MinLemonExceedsBrownie']

# Variables 
# @Variable NumberOfBrownies @Def: The number of brownies to be produced @Shape: [] 
NumberOfBrownies = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfBrownies")
# @Variable NumberOfLemonSquares @Def: The number of lemon squares to be produced @Shape: [] 
NumberOfLemonSquares = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfLemonSquares")

# Constraints 
# @Constraint Constr_1 @Def: The total ChocolateMix used does not exceed TotalChocolateMix units.
model.addConstr(ChocolateMixPerBrownie * NumberOfBrownies <= TotalChocolateMix)
# @Constraint Constr_2 @Def: The total LemonMix used does not exceed TotalLemonMix units.
model.addConstr(LemonMixPerLemonSquare * NumberOfLemonSquares <= TotalLemonMix)
# @Constraint Constr_3 @Def: The number of LemonSquares produced exceeds the number of Brownies produced by at least MinLemonExceedsBrownie.
model.addConstr(NumberOfLemonSquares - NumberOfBrownies >= MinLemonExceedsBrownie)
# @Constraint Constr_4 @Def: At least MinBrowniePercentage of the total items produced are Brownies.
model.addConstr(NumberOfBrownies >= MinBrowniePercentage * (NumberOfBrownies + NumberOfLemonSquares))

# Objective 
# @Objective Objective @Def: Minimize the total Fiber used, calculated as FiberPerBrownie multiplied by the number of Brownies plus FiberPerLemonSquare multiplied by the number of LemonSquares.
model.setObjective(FiberPerBrownie * NumberOfBrownies + FiberPerLemonSquare * NumberOfLemonSquares, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfBrownies'] = NumberOfBrownies.x
variables['NumberOfLemonSquares'] = NumberOfLemonSquares.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
