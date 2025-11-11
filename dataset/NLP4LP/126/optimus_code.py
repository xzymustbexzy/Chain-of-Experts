# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A patient must consume oranges and grapefruits to satisfy minimum vitamin
requirements. Each orange provides VitaminCPerOrange units of vitamin C and
VitaminAPerOrange units of vitamin A, contributing SugarPerOrange grams of
sugar. Each grapefruit provides VitaminCPerGrapefruit units of vitamin C and
VitaminAPerGrapefruit units of vitamin A, contributing SugarPerGrapefruit grams
of sugar. The patient must obtain at least MinVitaminC units of vitamin C and at
least MinVitaminA units of vitamin A. Additionally, the number of oranges
consumed must be at least MinOrangeToGrapefruitRatio times the number of
grapefruits. The objective is to minimize the total sugar intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/127/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter VitaminCPerOrange @Def: Units of vitamin C per orange @Shape: [] 
VitaminCPerOrange = data['VitaminCPerOrange']
# @Parameter VitaminAPerOrange @Def: Units of vitamin A per orange @Shape: [] 
VitaminAPerOrange = data['VitaminAPerOrange']
# @Parameter SugarPerOrange @Def: Grams of sugar per orange @Shape: [] 
SugarPerOrange = data['SugarPerOrange']
# @Parameter VitaminCPerGrapefruit @Def: Units of vitamin C per grapefruit @Shape: [] 
VitaminCPerGrapefruit = data['VitaminCPerGrapefruit']
# @Parameter VitaminAPerGrapefruit @Def: Units of vitamin A per grapefruit @Shape: [] 
VitaminAPerGrapefruit = data['VitaminAPerGrapefruit']
# @Parameter SugarPerGrapefruit @Def: Grams of sugar per grapefruit @Shape: [] 
SugarPerGrapefruit = data['SugarPerGrapefruit']
# @Parameter MinVitaminC @Def: Minimum required units of vitamin C @Shape: [] 
MinVitaminC = data['MinVitaminC']
# @Parameter MinVitaminA @Def: Minimum required units of vitamin A @Shape: [] 
MinVitaminA = data['MinVitaminA']
# @Parameter MinOrangeToGrapefruitRatio @Def: Minimum ratio of oranges to grapefruits indicating preference @Shape: [] 
MinOrangeToGrapefruitRatio = data['MinOrangeToGrapefruitRatio']

# Variables 
# @Variable NumberOfOranges @Def: The number of oranges the patient consumes @Shape: ['Integer'] 
NumberOfOranges = model.addVar(vtype=GRB.INTEGER, name="NumberOfOranges")
# @Variable NumberOfGrapefruits @Def: The number of grapefruits the patient consumes @Shape: ['Integer'] 
NumberOfGrapefruits = model.addVar(vtype=GRB.INTEGER, name="NumberOfGrapefruits")

# Constraints 
# @Constraint Constr_1 @Def: The patient must obtain at least MinVitaminC units of vitamin C.
model.addConstr(VitaminCPerOrange * NumberOfOranges + VitaminCPerGrapefruit * NumberOfGrapefruits >= MinVitaminC)
# @Constraint Constr_2 @Def: The patient must obtain at least MinVitaminA units of vitamin A.
model.addConstr(VitaminAPerOrange * NumberOfOranges + VitaminAPerGrapefruit * NumberOfGrapefruits >= MinVitaminA)
# @Constraint Constr_3 @Def: The number of oranges consumed must be at least MinOrangeToGrapefruitRatio times the number of grapefruits.
model.addConstr(NumberOfOranges >= MinOrangeToGrapefruitRatio * NumberOfGrapefruits)

# Objective 
# @Objective Objective @Def: Total sugar intake is calculated as SugarPerOrange times the number of oranges plus SugarPerGrapefruit times the number of grapefruits. The objective is to minimize the total sugar intake.
model.setObjective(SugarPerOrange * NumberOfOranges + SugarPerGrapefruit * NumberOfGrapefruits, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfOranges'] = NumberOfOranges.x
variables['NumberOfGrapefruits'] = NumberOfGrapefruits.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
