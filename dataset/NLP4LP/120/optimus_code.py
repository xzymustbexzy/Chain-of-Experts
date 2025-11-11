# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A zookeeper feeds a gorilla with bananas and mangoes. Each banana contains
CalorieBanana calories, PotassiumBanana grams of potassium, and SugarBanana
grams of sugar. Each mango contains CalorieMango calories, PotassiumMango grams
of potassium, and SugarMango grams of sugar. The gorilla must consume at least
MinCalories calories and MinPotassium grams of potassium. At most
MaxMangoFraction of the fruits he eats can be mangoes. To prevent excess sugar
intake, determine the number of each fruit he should consume to minimize his
sugar intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/121/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CalorieBanana @Def: Amount of calories per banana @Shape: [] 
CalorieBanana = data['CalorieBanana']
# @Parameter CalorieMango @Def: Amount of calories per mango @Shape: [] 
CalorieMango = data['CalorieMango']
# @Parameter PotassiumBanana @Def: Amount of potassium per banana @Shape: [] 
PotassiumBanana = data['PotassiumBanana']
# @Parameter PotassiumMango @Def: Amount of potassium per mango @Shape: [] 
PotassiumMango = data['PotassiumMango']
# @Parameter SugarBanana @Def: Amount of sugar per banana @Shape: [] 
SugarBanana = data['SugarBanana']
# @Parameter SugarMango @Def: Amount of sugar per mango @Shape: [] 
SugarMango = data['SugarMango']
# @Parameter MinCalories @Def: Minimum total calories required @Shape: [] 
MinCalories = data['MinCalories']
# @Parameter MinPotassium @Def: Minimum total potassium required @Shape: [] 
MinPotassium = data['MinPotassium']
# @Parameter MaxMangoFraction @Def: Maximum fraction of fruits that can be mangoes @Shape: [] 
MaxMangoFraction = data['MaxMangoFraction']

# Variables 
# @Variable XBanana @Def: The number of bananas consumed by the gorilla @Shape: ['Integer'] 
XBanana = model.addVar(vtype=GRB.INTEGER, name="XBanana")
# @Variable XMango @Def: The number of mangoes consumed by the gorilla @Shape: ['Integer'] 
XMango = model.addVar(vtype=GRB.INTEGER, name="XMango")

# Constraints 
# @Constraint Constr_1 @Def: The gorilla must consume at least MinCalories calories.
model.addConstr(CalorieBanana * XBanana + CalorieMango * XMango >= MinCalories)
# @Constraint Constr_2 @Def: The gorilla must consume at least MinPotassium grams of potassium.
model.addConstr(PotassiumBanana * XBanana + PotassiumMango * XMango >= MinPotassium)
# @Constraint Constr_3 @Def: At most MaxMangoFraction of the fruits the gorilla eats can be mangoes.
model.addConstr(XMango <= MaxMangoFraction * (XBanana + XMango))

# Objective 
# @Objective Objective @Def: Minimize the total sugar intake.
model.setObjective(SugarBanana * XBanana + SugarMango * XMango, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['XBanana'] = XBanana.x
variables['XMango'] = XMango.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
