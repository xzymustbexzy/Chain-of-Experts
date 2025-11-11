# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A grocery store aims to liquidate its stock of NumItems different items. It has
an Available quantity for each item. The store can prepare NumPackages different
package types, where each package requires a certain amount of each item as
specified by Required. Each package yields a PackageProfit. Determine the number
of each package to prepare in order to maximize the total profit without
exceeding the available stock of any item.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/10/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumItems @Def: Number of different items to be liquidated @Shape: [] 
NumItems = data['NumItems']
# @Parameter NumPackages @Def: Number of different package types @Shape: [] 
NumPackages = data['NumPackages']
# @Parameter Available @Def: Available quantity of each item @Shape: ['NumItems'] 
Available = data['Available']
# @Parameter Required @Def: Amount of each item required to prepare one unit of each package @Shape: ['NumItems', 'NumPackages'] 
Required = data['Required']
# @Parameter PackageProfit @Def: Profit for each package @Shape: ['NumPackages'] 
PackageProfit = data['PackageProfit']

# Variables 
# @Variable PackageCount @Def: The number of each type of package to produce @Shape: ['NumPackages'] 
PackageCount = model.addVars(NumPackages, vtype=GRB.INTEGER, name="PackageCount")

# Constraints 
# @Constraint Constr_1 @Def: Each package requires the specified amounts of each item as defined by Required.
model.addConstrs((quicksum(Required[i][p] * PackageCount[p] for p in range(NumPackages)) <= Available[i] for i in range(NumItems)), name="ResourceConstraints")

# Objective 
# @Objective Objective @Def: Total profit is the sum of the PackageProfit of all prepared packages. The objective is to maximize the total profit without exceeding the available stock of any item.
model.setObjective(quicksum(PackageProfit[j] * PackageCount[j] for j in range(NumPackages)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['PackageCount'] = {p: PackageCount[p].X for p in range(NumPackages)}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)