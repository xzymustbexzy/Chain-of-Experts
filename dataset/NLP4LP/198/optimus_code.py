# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Lucy aims to determine the number of regular and premium bags to purchase to
minimize the total cost, subject to the constraints that the combined calcium
from regular and premium bags is at least MinCalcium, the combined vitamin mix
is at least MinVitaminMix, and the combined protein is at least MinProtein. The
cost per regular bag is PriceRegular and per premium bag is PricePremium. Each
regular bag provides CalciumRegular units of calcium, VitaminMixRegular units of
vitamin mix, and ProteinRegular units of protein, while each premium bag
provides CalciumPremium units of calcium, VitaminMixPremium units of vitamin
mix, and ProteinPremium units of protein.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/199/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinCalcium @Def: Minimum required units of calcium @Shape: [] 
MinCalcium = data['MinCalcium']
# @Parameter MinVitaminMix @Def: Minimum required units of vitamin mix @Shape: [] 
MinVitaminMix = data['MinVitaminMix']
# @Parameter MinProtein @Def: Minimum required units of protein @Shape: [] 
MinProtein = data['MinProtein']
# @Parameter PriceRegular @Def: Price per bag of regular brand @Shape: [] 
PriceRegular = data['PriceRegular']
# @Parameter PricePremium @Def: Price per bag of premium brand @Shape: [] 
PricePremium = data['PricePremium']
# @Parameter CalciumRegular @Def: Units of calcium per bag of regular brand @Shape: [] 
CalciumRegular = data['CalciumRegular']
# @Parameter CalciumPremium @Def: Units of calcium per bag of premium brand @Shape: [] 
CalciumPremium = data['CalciumPremium']
# @Parameter VitaminMixRegular @Def: Units of vitamin mix per bag of regular brand @Shape: [] 
VitaminMixRegular = data['VitaminMixRegular']
# @Parameter VitaminMixPremium @Def: Units of vitamin mix per bag of premium brand @Shape: [] 
VitaminMixPremium = data['VitaminMixPremium']
# @Parameter ProteinRegular @Def: Units of protein per bag of regular brand @Shape: [] 
ProteinRegular = data['ProteinRegular']
# @Parameter ProteinPremium @Def: Units of protein per bag of premium brand @Shape: [] 
ProteinPremium = data['ProteinPremium']

# Variables 
# @Variable NumRegularBags @Def: The number of regular bags @Shape: ['Integer'] 
NumRegularBags = model.addVar(vtype=GRB.INTEGER, name="NumRegularBags")
# @Variable NumPremiumBags @Def: The number of premium bags @Shape: ['Integer'] 
NumPremiumBags = model.addVar(vtype=GRB.INTEGER, name="NumPremiumBags")

# Constraints 
# @Constraint Constr_1 @Def: The combined calcium from regular and premium bags is at least MinCalcium.
model.addConstr(CalciumRegular * NumRegularBags + CalciumPremium * NumPremiumBags >= MinCalcium)
# @Constraint Constr_2 @Def: The combined vitamin mix from regular and premium bags is at least MinVitaminMix.
model.addConstr(VitaminMixRegular * NumRegularBags + VitaminMixPremium * NumPremiumBags >= MinVitaminMix)
# @Constraint Constr_3 @Def: The combined protein from regular and premium bags is at least MinProtein.
model.addConstr(ProteinRegular * NumRegularBags + ProteinPremium * NumPremiumBags >= MinProtein)

# Objective 
# @Objective Objective @Def: Total cost is PriceRegular multiplied by the number of regular bags plus PricePremium multiplied by the number of premium bags. The objective is to minimize the total cost while meeting the nutritional requirements for calcium, vitamin mix, and protein.
model.setObjective(PriceRegular * NumRegularBags + PricePremium * NumPremiumBags, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumRegularBags'] = NumRegularBags.x
variables['NumPremiumBags'] = NumPremiumBags.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
