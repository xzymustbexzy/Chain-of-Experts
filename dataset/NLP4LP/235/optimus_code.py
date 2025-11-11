# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A lighting company has access to NumTypes types of lights to provide their
customers. Each type uses ElectricityUsage[i] units of electricity per hour and
needs to be changed ChangesPerDecade[i] times per decade. Due to previous
installations, at least MinPercentageFluorescence fraction of implemented lights
must be fluorescence lamps. If the customer requires at least MinNumFixtures
light fixtures and can use at most MaxElectricity units of electricity,
determine the number of each type of light to install to minimize the total
number of light changes.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/236/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumTypes @Def: Number of types of lights available @Shape: [] 
NumTypes = data['NumTypes']
# @Parameter ElectricityUsage @Def: Electricity units used per hour by each type of light @Shape: ['NumTypes'] 
ElectricityUsage = data['ElectricityUsage']
# @Parameter ChangesPerDecade @Def: Number of times each type of light needs to be changed per decade @Shape: ['NumTypes'] 
ChangesPerDecade = data['ChangesPerDecade']
# @Parameter MinPercentageFluorescence @Def: Minimum fraction of implemented light fixtures that must be fluorescence lamps @Shape: [] 
MinPercentageFluorescence = data['MinPercentageFluorescence']
# @Parameter MinNumFixtures @Def: Minimum number of light fixtures required @Shape: [] 
MinNumFixtures = data['MinNumFixtures']
# @Parameter MaxElectricity @Def: Maximum number of electricity units that can be used @Shape: [] 
MaxElectricity = data['MaxElectricity']

# Variables 
# @Variable NumFixtures @Def: The number of fixtures for each type of light @Shape: ['NumTypes'] 
NumFixtures = model.addVars(NumTypes, vtype=GRB.INTEGER, name="NumFixtures")
# @Variable NumFluorescenceFixtures @Def: The number of fluorescence light fixtures @Shape: [] 
NumFluorescenceFixtures = model.addVar(vtype=GRB.INTEGER, name="NumFluorescenceFixtures")

# Constraints 
# @Constraint Constr_1 @Def: At least MinPercentageFluorescence fraction of the implemented light fixtures must be fluorescence lamps.
model.addConstr(NumFluorescenceFixtures >= MinPercentageFluorescence * quicksum(NumFixtures[i] for i in range(NumTypes)))
# @Constraint Constr_2 @Def: The total number of light fixtures installed must be at least MinNumFixtures.
model.addConstr(quicksum(NumFixtures[t] for t in range(NumTypes)) + NumFluorescenceFixtures >= MinNumFixtures)
# @Constraint Constr_3 @Def: The total electricity usage of all installed lights must not exceed MaxElectricity units.
model.addConstr(quicksum(ElectricityUsage[t] * NumFixtures[t] for t in range(NumTypes)) <= MaxElectricity)

# Objective 
# @Objective Objective @Def: Minimize the total number of light changes, calculated as the sum of ChangesPerDecade[i] multiplied by the number of each type of light installed.
model.setObjective(quicksum(ChangesPerDecade[i] * NumFixtures[i] for i in range(NumTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumFixtures'] = {i: NumFixtures[i].x for i in range(NumTypes)}
variables['NumFluorescenceFixtures'] = NumFluorescenceFixtures.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)