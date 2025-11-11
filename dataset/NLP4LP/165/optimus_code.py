# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A jam company sends its product out in small and large jars. A small jar can
hold SmallJarCapacity milliliters of jam while a large jar can hold
LargeJarCapacity milliliters of jam. Most stores prefer the smaller size and so
the number of large jars cannot exceed MaxLargeJarsRatio times the number of
small jars. If the company wants to ship at least MinJamVolume milliliters of
jam, find the minimum number of jars that can be used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/166/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter SmallJarCapacity @Def: Capacity of a small jar in milliliters @Shape: [] 
SmallJarCapacity = data['SmallJarCapacity']
# @Parameter LargeJarCapacity @Def: Capacity of a large jar in milliliters @Shape: [] 
LargeJarCapacity = data['LargeJarCapacity']
# @Parameter MinJamVolume @Def: Minimum total volume of jam to ship in milliliters @Shape: [] 
MinJamVolume = data['MinJamVolume']
# @Parameter MaxLargeJarsRatio @Def: Maximum allowed ratio of large jars to small jars @Shape: [] 
MaxLargeJarsRatio = data['MaxLargeJarsRatio']

# Variables 
# @Variable NumberOfSmallJars @Def: The number of small jars to ship @Shape: [] 
NumberOfSmallJars = model.addVar(vtype=GRB.INTEGER, name='NumberOfSmallJars')
# @Variable NumberOfLargeJars @Def: The number of large jars to ship @Shape: [] 
NumberOfLargeJars = model.addVar(vtype=GRB.INTEGER, name="NumberOfLargeJars")

# Constraints 
# @Constraint Constr_1 @Def: The total volume of jam shipped is at least MinJamVolume milliliters.
model.addConstr(SmallJarCapacity * NumberOfSmallJars + LargeJarCapacity * NumberOfLargeJars >= MinJamVolume)
# @Constraint Constr_2 @Def: The number of large jars does not exceed MaxLargeJarsRatio times the number of small jars.
model.addConstr(NumberOfLargeJars <= MaxLargeJarsRatio * NumberOfSmallJars)

# Objective 
# @Objective Objective @Def: Minimize the total number of small and large jars used to ship the jam.
model.setObjective(NumberOfSmallJars + NumberOfLargeJars, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfSmallJars'] = NumberOfSmallJars.x
variables['NumberOfLargeJars'] = NumberOfLargeJars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
