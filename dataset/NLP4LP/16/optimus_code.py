# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A hobbyist makes model trains and model planes using wood and paint. Each model
train requires WoodPerTrain units of wood and PaintPerTrain units of paint. Each
model plane requires WoodPerPlane units of wood and PaintPerPlane units of
paint. The hobbyist has AvailableWood units of wood and AvailablePaint units of
paint. The profit per model train is ProfitTrain and the profit per model plane
is ProfitPlane. The hobbyist aims to determine the number of each to produce to
maximize profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/17/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter WoodPerTrain @Def: Amount of wood required to produce one model train @Shape: [] 
WoodPerTrain = data['WoodPerTrain']
# @Parameter PaintPerTrain @Def: Amount of paint required to produce one model train @Shape: [] 
PaintPerTrain = data['PaintPerTrain']
# @Parameter WoodPerPlane @Def: Amount of wood required to produce one model plane @Shape: [] 
WoodPerPlane = data['WoodPerPlane']
# @Parameter PaintPerPlane @Def: Amount of paint required to produce one model plane @Shape: [] 
PaintPerPlane = data['PaintPerPlane']
# @Parameter AvailableWood @Def: Total available units of wood @Shape: [] 
AvailableWood = data['AvailableWood']
# @Parameter AvailablePaint @Def: Total available units of paint @Shape: [] 
AvailablePaint = data['AvailablePaint']
# @Parameter ProfitTrain @Def: Profit earned per model train @Shape: [] 
ProfitTrain = data['ProfitTrain']
# @Parameter ProfitPlane @Def: Profit earned per model plane @Shape: [] 
ProfitPlane = data['ProfitPlane']

# Variables 
# @Variable NumberOfTrains @Def: The number of model trains to produce @Shape: [] 
NumberOfTrains = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfTrains")
# @Variable NumberOfPlanes @Def: The number of model planes to produce @Shape: [] 
NumberOfPlanes = model.addVar(vtype=GRB.CONTINUOUS, name='NumberOfPlanes')

# Constraints 
# @Constraint Constr_1 @Def: The total wood required for producing model trains and model planes cannot exceed AvailableWood units of wood.
model.addConstr(NumberOfTrains * WoodPerTrain + NumberOfPlanes * WoodPerPlane <= AvailableWood)
# @Constraint Constr_2 @Def: The total paint required for producing model trains and model planes cannot exceed AvailablePaint units of paint.
model.addConstr(PaintPerTrain * NumberOfTrains + PaintPerPlane * NumberOfPlanes <= AvailablePaint)

# Objective 
# @Objective Objective @Def: The total profit is calculated as ProfitTrain times the number of model trains plus ProfitPlane times the number of model planes. The objective is to maximize the total profit.
model.setObjective(ProfitTrain * NumberOfTrains + ProfitPlane * NumberOfPlanes, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfTrains'] = NumberOfTrains.x
variables['NumberOfPlanes'] = NumberOfPlanes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
