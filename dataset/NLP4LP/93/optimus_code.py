# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A scientist needs to determine the number of orange juice boxes and apple juice
boxes to consume. Each orange juice box provides VitaminDOrange units of vitamin
D and VitaminCOrange units of vitamin C. Each apple juice box provides
VitaminDApple units of vitamin D and VitaminCApple units of vitamin C. The
number of apple juice boxes must be at least PreferenceRatio times the number of
orange juice boxes. The scientist must consume at least MinimumOrangeBoxes
orange juice boxes. To prevent vitamin C overdose, the total vitamin C intake
must not exceed MaxVitaminC. The objective is to maximize the total vitamin D
intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/94/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VitaminDOrange @Def: Amount of vitamin D in each box of orange juice @Shape: [] 
VitaminDOrange = data['VitaminDOrange']
# @Parameter VitaminCOrange @Def: Amount of vitamin C in each box of orange juice @Shape: [] 
VitaminCOrange = data['VitaminCOrange']
# @Parameter VitaminDApple @Def: Amount of vitamin D in each box of apple juice @Shape: [] 
VitaminDApple = data['VitaminDApple']
# @Parameter VitaminCApple @Def: Amount of vitamin C in each box of apple juice @Shape: [] 
VitaminCApple = data['VitaminCApple']
# @Parameter PreferenceRatio @Def: Minimum ratio of apple juice boxes to orange juice boxes @Shape: [] 
PreferenceRatio = data['PreferenceRatio']
# @Parameter MinimumOrangeBoxes @Def: Minimum number of orange juice boxes to be consumed @Shape: [] 
MinimumOrangeBoxes = data['MinimumOrangeBoxes']
# @Parameter MaxVitaminC @Def: Maximum allowed units of vitamin C intake @Shape: [] 
MaxVitaminC = data['MaxVitaminC']

# Variables 
# @Variable NumberOfAppleJuiceBoxes @Def: The number of apple juice boxes @Shape: [] 
NumberOfAppleJuiceBoxes = model.addVar(vtype=GRB.INTEGER, name="NumberOfAppleJuiceBoxes")
# @Variable NumberOfOrangeJuiceBoxes @Def: The number of orange juice boxes @Shape: [] 
NumberOfOrangeJuiceBoxes = model.addVar(vtype=GRB.INTEGER, name="NumberOfOrangeJuiceBoxes")

# Constraints 
# @Constraint Constr_1 @Def: The number of apple juice boxes must be at least PreferenceRatio times the number of orange juice boxes.
model.addConstr(NumberOfAppleJuiceBoxes >= PreferenceRatio * NumberOfOrangeJuiceBoxes)
# @Constraint Constr_2 @Def: The scientist must consume at least MinimumOrangeBoxes orange juice boxes.
model.addConstr(NumberOfOrangeJuiceBoxes >= MinimumOrangeBoxes)
# @Constraint Constr_3 @Def: The total vitamin C intake from orange and apple juice boxes must not exceed MaxVitaminC.
model.addConstr(VitaminCOrange * NumberOfOrangeJuiceBoxes + VitaminCApple * NumberOfAppleJuiceBoxes <= MaxVitaminC)

# Objective 
# @Objective Objective @Def: Total vitamin D intake is the sum of the vitamin D provided by orange juice boxes and the vitamin D provided by apple juice boxes. The objective is to maximize the total vitamin D intake.
model.setObjective(NumberOfAppleJuiceBoxes * VitaminDApple + NumberOfOrangeJuiceBoxes * VitaminDOrange, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfAppleJuiceBoxes'] = NumberOfAppleJuiceBoxes.x
variables['NumberOfOrangeJuiceBoxes'] = NumberOfOrangeJuiceBoxes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
