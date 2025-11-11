# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An amusement park operates throwing and climbing games. Each throwing game
attracts CustomersPerThrowingGame customers per hour and incurs a
PrizeCostPerThrowingGame cost per hour. Each climbing game attracts
CustomersPerClimbingGame customers per hour and incurs a
PrizeCostPerClimbingGame cost per hour. The number of throwing games must be at
least MinRatioThrowingClimbing times the number of climbing games. At least
MinClimbingGames climbing games must be operated. The total prize cost per hour
must not exceed MaxPrizeCostPerHour. The objective is to maximize the total
number of customers attracted per hour.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/221/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CustomersPerThrowingGame @Def: Number of customers attracted per hour by throwing games @Shape: [] 
CustomersPerThrowingGame = data['CustomersPerThrowingGame']
# @Parameter CustomersPerClimbingGame @Def: Number of customers attracted per hour by climbing games @Shape: [] 
CustomersPerClimbingGame = data['CustomersPerClimbingGame']
# @Parameter PrizeCostPerThrowingGame @Def: Cost in prizes per hour for throwing games @Shape: [] 
PrizeCostPerThrowingGame = data['PrizeCostPerThrowingGame']
# @Parameter PrizeCostPerClimbingGame @Def: Cost in prizes per hour for climbing games @Shape: [] 
PrizeCostPerClimbingGame = data['PrizeCostPerClimbingGame']
# @Parameter MinRatioThrowingClimbing @Def: Minimum ratio of throwing games to climbing games @Shape: [] 
MinRatioThrowingClimbing = data['MinRatioThrowingClimbing']
# @Parameter MinClimbingGames @Def: Minimum number of climbing games required @Shape: [] 
MinClimbingGames = data['MinClimbingGames']
# @Parameter MaxPrizeCostPerHour @Def: Maximum total prize cost per hour @Shape: [] 
MaxPrizeCostPerHour = data['MaxPrizeCostPerHour']

# Variables 
# @Variable ThrowingGames @Def: The number of throwing games @Shape: [] 
ThrowingGames = model.addVar(vtype=GRB.INTEGER, name="ThrowingGames")
# @Variable ClimbingGames @Def: The number of climbing games @Shape: [] 
ClimbingGames = model.addVar(vtype=GRB.INTEGER, name="ClimbingGames")

# Constraints 
# @Constraint Constr_1 @Def: The number of throwing games must be at least MinRatioThrowingClimbing times the number of climbing games.
model.addConstr(ThrowingGames >= MinRatioThrowingClimbing * ClimbingGames)
# @Constraint Constr_2 @Def: At least MinClimbingGames climbing games must be operated.
model.addConstr(ClimbingGames >= MinClimbingGames)
# @Constraint Constr_3 @Def: The total prize cost per hour must not exceed MaxPrizeCostPerHour.
model.addConstr(PrizeCostPerThrowingGame * ThrowingGames + PrizeCostPerClimbingGame * ClimbingGames <= MaxPrizeCostPerHour)

# Objective 
# @Objective Objective @Def: Maximize the total number of customers attracted per hour, which is the sum of CustomersPerThrowingGame multiplied by the number of throwing games and CustomersPerClimbingGame multiplied by the number of climbing games.
model.setObjective(CustomersPerThrowingGame * ThrowingGames + CustomersPerClimbingGame * ClimbingGames, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ThrowingGames'] = ThrowingGames.x
variables['ClimbingGames'] = ClimbingGames.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
