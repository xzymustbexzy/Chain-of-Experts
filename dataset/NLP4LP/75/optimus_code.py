# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A coffee shop produces two products, Mochas and Regular Coffees. Each Mocha
requires CoffeePowderPerMocha units of coffee powder and MilkPerMocha units of
milk. Each Regular Coffee requires CoffeePowderPerRegularCoffee units of coffee
powder and MilkPerRegularCoffee units of milk. The shop has
AvailableCoffeePowder units of coffee powder and AvailableMilk units of milk
available. Producing one Mocha takes TimePerMocha minutes and one Regular Coffee
takes TimePerRegularCoffee minutes. The number of Mochas produced must be at
least MochaToRegularRatio times the number of Regular Coffees produced.
Determine the number of Mochas and Regular Coffees to produce to minimize the
total production time.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/76/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CoffeePowderPerMocha @Def: Amount of coffee powder required to produce one mocha @Shape: [] 
CoffeePowderPerMocha = data['CoffeePowderPerMocha']
# @Parameter MilkPerMocha @Def: Amount of milk required to produce one mocha @Shape: [] 
MilkPerMocha = data['MilkPerMocha']
# @Parameter CoffeePowderPerRegularCoffee @Def: Amount of coffee powder required to produce one regular coffee @Shape: [] 
CoffeePowderPerRegularCoffee = data['CoffeePowderPerRegularCoffee']
# @Parameter MilkPerRegularCoffee @Def: Amount of milk required to produce one regular coffee @Shape: [] 
MilkPerRegularCoffee = data['MilkPerRegularCoffee']
# @Parameter AvailableCoffeePowder @Def: Total available units of coffee powder @Shape: [] 
AvailableCoffeePowder = data['AvailableCoffeePowder']
# @Parameter AvailableMilk @Def: Total available units of milk @Shape: [] 
AvailableMilk = data['AvailableMilk']
# @Parameter TimePerMocha @Def: Time taken to produce one mocha @Shape: [] 
TimePerMocha = data['TimePerMocha']
# @Parameter TimePerRegularCoffee @Def: Time taken to produce one regular coffee @Shape: [] 
TimePerRegularCoffee = data['TimePerRegularCoffee']
# @Parameter MochaToRegularRatio @Def: Minimum multiple of mochas required compared to regular coffees @Shape: [] 
MochaToRegularRatio = data['MochaToRegularRatio']

# Variables 
# @Variable NumMocha @Def: The number of Mochas produced @Shape: ['Integer'] 
NumMocha = model.addVar(vtype=GRB.INTEGER, name="NumMocha")
# @Variable NumRegularCoffee @Def: The number of Regular Coffees produced @Shape: ['Integer'] 
NumRegularCoffee = model.addVar(vtype=GRB.INTEGER, name="NumRegularCoffee")

# Constraints 
# @Constraint Constr_1 @Def: The total coffee powder used by Mochas and Regular Coffees does not exceed AvailableCoffeePowder.
model.addConstr(CoffeePowderPerMocha * NumMocha + CoffeePowderPerRegularCoffee * NumRegularCoffee <= AvailableCoffeePowder)
# @Constraint Constr_2 @Def: The total milk used by Mochas and Regular Coffees does not exceed AvailableMilk.
model.addConstr(MilkPerMocha * NumMocha + MilkPerRegularCoffee * NumRegularCoffee <= AvailableMilk)
# @Constraint Constr_3 @Def: The number of Mochas produced is at least MochaToRegularRatio times the number of Regular Coffees produced.
model.addConstr(NumMocha >= MochaToRegularRatio * NumRegularCoffee)

# Objective 
# @Objective Objective @Def: Minimize the total production time, which is the sum of (TimePerMocha × number of Mochas) and (TimePerRegularCoffee × number of Regular Coffees).
model.setObjective(TimePerMocha * NumMocha + TimePerRegularCoffee * NumRegularCoffee, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumMocha'] = NumMocha.x
variables['NumRegularCoffee'] = NumRegularCoffee.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
