# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A honey farmer sells his honey in glass and plastic jars. A glass jar can hold
GlassJarCapacity of honey while a plastic jar can hold PlasticJarCapacity of
honey. Since glass jars are more expensive, at least MinPlasticToGlassRatio as
many plastic jars must be filled as glass jars. However, at least
MinNumberGlassJars glass jars should be filled. If the farmer has TotalHoney of
honey, how many jars of each should be filled to maximize the total number of
bottles filled?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/48/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GlassJarCapacity @Def: The capacity of a glass jar in milliliters @Shape: [] 
GlassJarCapacity = data['GlassJarCapacity']
# @Parameter PlasticJarCapacity @Def: The capacity of a plastic jar in milliliters @Shape: [] 
PlasticJarCapacity = data['PlasticJarCapacity']
# @Parameter MinPlasticToGlassRatio @Def: The minimum ratio of plastic jars to glass jars that must be filled @Shape: [] 
MinPlasticToGlassRatio = data['MinPlasticToGlassRatio']
# @Parameter MinNumberGlassJars @Def: The minimum number of glass jars that must be filled @Shape: [] 
MinNumberGlassJars = data['MinNumberGlassJars']
# @Parameter TotalHoney @Def: Total amount of honey available in milliliters @Shape: [] 
TotalHoney = data['TotalHoney']

# Variables 
# @Variable GlassJarsFilled @Def: The number of glass jars that are filled @Shape: [] 
GlassJarsFilled = model.addVar(vtype=GRB.INTEGER, name="GlassJarsFilled")
# @Variable PlasticJarsFilled @Def: The number of plastic jars filled @Shape: [] 
PlasticJarsFilled = model.addVar(vtype=GRB.INTEGER, name='PlasticJarsFilled')

# Constraints 
# @Constraint Constr_1 @Def: At least MinNumberGlassJars glass jars must be filled.
model.addConstr(GlassJarsFilled >= MinNumberGlassJars)
# @Constraint Constr_2 @Def: The number of plastic jars filled must be at least MinPlasticToGlassRatio times the number of glass jars filled.
model.addConstr(PlasticJarsFilled >= MinPlasticToGlassRatio * GlassJarsFilled)
# @Constraint Constr_3 @Def: The total amount of honey used by the filled jars cannot exceed TotalHoney.
model.addConstr(GlassJarCapacity * GlassJarsFilled + PlasticJarCapacity * PlasticJarsFilled <= TotalHoney)

# Objective 
# @Objective Objective @Def: The total number of jars filled is the sum of glass jars and plastic jars. The objective is to maximize the total number of jars filled.
model.setObjective(GlassJarsFilled + PlasticJarsFilled, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['GlassJarsFilled'] = GlassJarsFilled.x
variables['PlasticJarsFilled'] = PlasticJarsFilled.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
