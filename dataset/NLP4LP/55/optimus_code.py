# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A bakery produces almond and pistachio croissants. An almond croissant requires
ButterPerAlmondCroissant units of butter and FlourPerAlmondCroissant units of
flour. A pistachio croissant requires ButterPerPistachioCroissant units of
butter and FlourPerPistachioCroissant units of flour. The bakery has available
AvailableButter units of butter and AvailableFlour units of flour. At least
MinAlmondToPistachioRatio times as many almond croissants should be made as
pistachio croissants. Making an almond croissant takes
ProductionTimeAlmondCroissant minutes and making a pistachio croissant takes
ProductionTimePistachioCroissant minutes. How many of each should be made to
minimize the total production time?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/56/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter AvailableButter @Def: Amount of butter available @Shape: [] 
AvailableButter = data['AvailableButter']
# @Parameter AvailableFlour @Def: Amount of flour available @Shape: [] 
AvailableFlour = data['AvailableFlour']
# @Parameter ButterPerAlmondCroissant @Def: Amount of butter required to produce one almond croissant @Shape: [] 
ButterPerAlmondCroissant = data['ButterPerAlmondCroissant']
# @Parameter FlourPerAlmondCroissant @Def: Amount of flour required to produce one almond croissant @Shape: [] 
FlourPerAlmondCroissant = data['FlourPerAlmondCroissant']
# @Parameter ButterPerPistachioCroissant @Def: Amount of butter required to produce one pistachio croissant @Shape: [] 
ButterPerPistachioCroissant = data['ButterPerPistachioCroissant']
# @Parameter FlourPerPistachioCroissant @Def: Amount of flour required to produce one pistachio croissant @Shape: [] 
FlourPerPistachioCroissant = data['FlourPerPistachioCroissant']
# @Parameter MinAlmondToPistachioRatio @Def: Minimum ratio of almond croissants to pistachio croissants @Shape: [] 
MinAlmondToPistachioRatio = data['MinAlmondToPistachioRatio']
# @Parameter ProductionTimeAlmondCroissant @Def: Production time per almond croissant @Shape: [] 
ProductionTimeAlmondCroissant = data['ProductionTimeAlmondCroissant']
# @Parameter ProductionTimePistachioCroissant @Def: Production time per pistachio croissant @Shape: [] 
ProductionTimePistachioCroissant = data['ProductionTimePistachioCroissant']

# Variables 
# @Variable QuantityAlmondCroissant @Def: The number of almond croissants produced @Shape: [] 
QuantityAlmondCroissant = model.addVar(vtype=GRB.INTEGER, name='QuantityAlmondCroissant')
# @Variable QuantityPistachioCroissant @Def: The number of pistachio croissants produced @Shape: [] 
QuantityPistachioCroissant = model.addVar(vtype=GRB.INTEGER, name="QuantityPistachioCroissant")

# Constraints 
# @Constraint Constr_1 @Def: The total amount of butter used by almond and pistachio croissants cannot exceed AvailableButter.
model.addConstr(ButterPerAlmondCroissant * QuantityAlmondCroissant + ButterPerPistachioCroissant * QuantityPistachioCroissant <= AvailableButter)
# @Constraint Constr_2 @Def: The total amount of flour used by almond and pistachio croissants cannot exceed AvailableFlour.
model.addConstr(FlourPerAlmondCroissant * QuantityAlmondCroissant + 
                FlourPerPistachioCroissant * QuantityPistachioCroissant <= AvailableFlour, 
                name='FlourConstraint')
# @Constraint Constr_3 @Def: The number of almond croissants produced must be at least MinAlmondToPistachioRatio times the number of pistachio croissants.
model.addConstr(QuantityAlmondCroissant >= MinAlmondToPistachioRatio * QuantityPistachioCroissant)

# Objective 
# @Objective Objective @Def: Minimize the total production time, which is the sum of (ProductionTimeAlmondCroissant multiplied by the number of almond croissants) and (ProductionTimePistachioCroissant multiplied by the number of pistachio croissants).
model.setObjective(ProductionTimeAlmondCroissant * QuantityAlmondCroissant + ProductionTimePistachioCroissant * QuantityPistachioCroissant, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityAlmondCroissant'] = QuantityAlmondCroissant.x
variables['QuantityPistachioCroissant'] = QuantityPistachioCroissant.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
