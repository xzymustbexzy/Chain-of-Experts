# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A clinical firm operates two factories, northern and western. The firm decides
the number of hours to run each factory. The northern factory produces
NorthernFactoryAntiItchRate grams of anti-itch injections and
NorthernFactoryTopicalCreamRate grams of topical cream per hour. The western
factory produces WesternFactoryAntiItchRate grams of anti-itch injections and
WesternFactoryTopicalCreamRate grams of topical cream per hour. The northern
factory uses NorthernFactoryPlasticUsage units of plastic per hour, and the
western factory uses WesternFactoryPlasticUsage units of plastic per hour. The
total plastic available is TotalPlasticAvailable units. The firm must produce at
least MinimumAntiItchProduction grams of anti-itch injections and
MinimumTopicalCreamProduction grams of topical cream. The objective is to
minimize the total time the factories are run.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/261/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NorthernFactoryAntiItchRate @Def: Production rate of anti-itch injections per hour at the northern factory @Shape: [] 
NorthernFactoryAntiItchRate = data['NorthernFactoryAntiItchRate']
# @Parameter NorthernFactoryTopicalCreamRate @Def: Production rate of topical cream per hour at the northern factory @Shape: [] 
NorthernFactoryTopicalCreamRate = data['NorthernFactoryTopicalCreamRate']
# @Parameter WesternFactoryAntiItchRate @Def: Production rate of anti-itch injections per hour at the western factory @Shape: [] 
WesternFactoryAntiItchRate = data['WesternFactoryAntiItchRate']
# @Parameter WesternFactoryTopicalCreamRate @Def: Production rate of topical cream per hour at the western factory @Shape: [] 
WesternFactoryTopicalCreamRate = data['WesternFactoryTopicalCreamRate']
# @Parameter NorthernFactoryPlasticUsage @Def: Units of plastic required per hour at the northern factory @Shape: [] 
NorthernFactoryPlasticUsage = data['NorthernFactoryPlasticUsage']
# @Parameter WesternFactoryPlasticUsage @Def: Units of plastic required per hour at the western factory @Shape: [] 
WesternFactoryPlasticUsage = data['WesternFactoryPlasticUsage']
# @Parameter TotalPlasticAvailable @Def: Total units of plastic available @Shape: [] 
TotalPlasticAvailable = data['TotalPlasticAvailable']
# @Parameter MinimumAntiItchProduction @Def: Minimum grams of anti-itch injections to produce @Shape: [] 
MinimumAntiItchProduction = data['MinimumAntiItchProduction']
# @Parameter MinimumTopicalCreamProduction @Def: Minimum grams of topical cream to produce @Shape: [] 
MinimumTopicalCreamProduction = data['MinimumTopicalCreamProduction']

# Variables 
# @Variable NorthernFactoryAntiItchProduction @Def: The production quantity of anti-itch injections at the Northern factory @Shape: [] 
NorthernFactoryAntiItchProduction = model.addVar(vtype=GRB.CONTINUOUS, name="NorthernFactoryAntiItchProduction")
# @Variable NorthernFactoryTopicalCreamProduction @Def: The production quantity of topical cream at the Northern factory @Shape: [] 
NorthernFactoryTopicalCreamProduction = model.addVar(vtype=GRB.CONTINUOUS, name="NorthernFactoryTopicalCreamProduction")
# @Variable WesternFactoryAntiItchProduction @Def: The production quantity of anti-itch injections at the Western factory @Shape: [] 
WesternFactoryAntiItchProduction = model.addVar(vtype=GRB.CONTINUOUS, name="WesternFactoryAntiItchProduction")
# @Variable WesternFactoryTopicalCreamProduction @Def: The production quantity of topical cream at the Western factory @Shape: [] 
WesternFactoryTopicalCreamProduction = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="WesternFactoryTopicalCreamProduction")
# @Variable NorthernRunTime @Def: The run time of the Northern factory in hours @Shape: [] 
NorthernRunTime = model.addVar(vtype=GRB.CONTINUOUS, name="NorthernRunTime")
# @Variable WesternRunTime @Def: The run time of the Western factory in hours @Shape: [] 
WesternRunTime = model.addVar(vtype=GRB.CONTINUOUS, name="WesternRunTime")

# Constraints 
# @Constraint Constr_1 @Def: The total plastic used by the northern and western factories cannot exceed TotalPlasticAvailable units.
model.addConstr((NorthernFactoryPlasticUsage / NorthernFactoryAntiItchRate) * NorthernFactoryAntiItchProduction + (NorthernFactoryPlasticUsage / NorthernFactoryTopicalCreamRate) * NorthernFactoryTopicalCreamProduction + (WesternFactoryPlasticUsage / WesternFactoryAntiItchRate) * WesternFactoryAntiItchProduction + (WesternFactoryPlasticUsage / WesternFactoryTopicalCreamRate) * WesternFactoryTopicalCreamProduction <= TotalPlasticAvailable)
# @Constraint Constr_2 @Def: The production of anti-itch injections by the northern and western factories must be at least MinimumAntiItchProduction grams.
model.addConstr(NorthernFactoryAntiItchProduction + WesternFactoryAntiItchProduction >= MinimumAntiItchProduction)
# @Constraint Constr_3 @Def: The production of topical cream by the northern and western factories must be at least MinimumTopicalCreamProduction grams.
model.addConstr(NorthernFactoryTopicalCreamProduction + WesternFactoryTopicalCreamProduction >= MinimumTopicalCreamProduction)

# Objective 
# @Objective Objective @Def: The objective is to minimize the total time the northern and western factories are run.
model.setObjective(NorthernRunTime + WesternRunTime, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NorthernFactoryAntiItchProduction'] = NorthernFactoryAntiItchProduction.x
variables['NorthernFactoryTopicalCreamProduction'] = NorthernFactoryTopicalCreamProduction.x
variables['WesternFactoryAntiItchProduction'] = WesternFactoryAntiItchProduction.x
variables['WesternFactoryTopicalCreamProduction'] = WesternFactoryTopicalCreamProduction.x
variables['NorthernRunTime'] = NorthernRunTime.x
variables['WesternRunTime'] = WesternRunTime.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
