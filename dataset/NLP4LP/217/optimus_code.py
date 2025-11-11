# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A ski resort needs to install two types of ski lifts: densely-seated lifts and
loosely-seated lifts. The densely-seated ski lift transports
GuestsPerMinuteDenselySeatedLift guests per minute and consumes
ElectricityPerDenselySeatedLift units of electricity. The loosely-seated ski
lift transports GuestsPerMinuteLooselySeatedLift guests per minute and consumes
ElectricityPerLooselySeatedLift units of electricity. The resort must install at
least MinimumLooselySeatedLifts loosely-seated ski lifts. To achieve a minimum
of MinimumGuestsPerMinute guests per minute while not exceeding
TotalElectricityAvailable units of electricity, determine the number of each
type of ski lift to install in order to minimize the total number of ski lifts.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/218/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter GuestsPerMinuteDenselySeatedLift @Def: Number of guests transported per minute by a densely-seated ski lift @Shape: [] 
GuestsPerMinuteDenselySeatedLift = data['GuestsPerMinuteDenselySeatedLift']
# @Parameter GuestsPerMinuteLooselySeatedLift @Def: Number of guests transported per minute by a loosely-seated ski lift @Shape: [] 
GuestsPerMinuteLooselySeatedLift = data['GuestsPerMinuteLooselySeatedLift']
# @Parameter ElectricityPerDenselySeatedLift @Def: Electricity units used by a densely-seated ski lift @Shape: [] 
ElectricityPerDenselySeatedLift = data['ElectricityPerDenselySeatedLift']
# @Parameter ElectricityPerLooselySeatedLift @Def: Electricity units used by a loosely-seated ski lift @Shape: [] 
ElectricityPerLooselySeatedLift = data['ElectricityPerLooselySeatedLift']
# @Parameter MinimumLooselySeatedLifts @Def: Minimum number of loosely-seated ski lifts required @Shape: [] 
MinimumLooselySeatedLifts = data['MinimumLooselySeatedLifts']
# @Parameter MinimumGuestsPerMinute @Def: Minimum number of guests per minute required for profit @Shape: [] 
MinimumGuestsPerMinute = data['MinimumGuestsPerMinute']
# @Parameter TotalElectricityAvailable @Def: Total electricity units available @Shape: [] 
TotalElectricityAvailable = data['TotalElectricityAvailable']

# Variables 
# @Variable LooselySeatedLift @Def: The number of loosely-seated ski lifts @Shape: ['Integer'] 
LooselySeatedLift = model.addVar(vtype=GRB.INTEGER, lb=MinimumLooselySeatedLifts, name="LooselySeatedLift")
# @Variable DenselySeatedLift @Def: The number of densely-seated ski lifts @Shape: ['Integer'] 
DenselySeatedLift = model.addVar(vtype=GRB.INTEGER, name="DenselySeatedLift")

# Constraints 
# @Constraint Constr_1 @Def: At least MinimumLooselySeatedLifts loosely-seated ski lifts must be installed.
model.addConstr(LooselySeatedLift >= MinimumLooselySeatedLifts)
# @Constraint Constr_2 @Def: The total number of guests per minute must be at least MinimumGuestsPerMinute.
model.addConstr(
    GuestsPerMinuteDenselySeatedLift * DenselySeatedLift +
    GuestsPerMinuteLooselySeatedLift * LooselySeatedLift >= MinimumGuestsPerMinute
)
# @Constraint Constr_3 @Def: The total electricity consumption must not exceed TotalElectricityAvailable units.
model.addConstr(DenselySeatedLift * ElectricityPerDenselySeatedLift + LooselySeatedLift * ElectricityPerLooselySeatedLift <= TotalElectricityAvailable)

# Objective 
# @Objective Objective @Def: Minimize the total number of ski lifts installed.
model.setObjective(LooselySeatedLift + DenselySeatedLift, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['LooselySeatedLift'] = LooselySeatedLift.x
variables['DenselySeatedLift'] = DenselySeatedLift.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
