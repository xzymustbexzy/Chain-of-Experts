# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A farmer has TotalAcres of land on which hay must be processed using NumMachines
different machine types. For each acre of land, machine type i can process
HayProcessedPerAcre[i] units of hay, produce MethaneProducedPerAcre[i] units of
methane gas, and require FuelRequiredPerAcre[i] units of fuel. The total fuel
available is FuelAvailable, and the total methane production must not exceed
MethaneLimit. The farmer aims to determine the number of acres to allocate to
each machine type to maximize the total amount of hay processed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/45/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalAcres @Def: Total number of acres available for processing hay @Shape: [] 
TotalAcres = data['TotalAcres']
# @Parameter NumMachines @Def: Number of different machine types available for processing hay @Shape: [] 
NumMachines = data['NumMachines']
# @Parameter FuelAvailable @Def: Total amount of fuel available @Shape: [] 
FuelAvailable = data['FuelAvailable']
# @Parameter MethaneLimit @Def: Maximum allowable amount of methane gas production @Shape: [] 
MethaneLimit = data['MethaneLimit']
# @Parameter HayProcessedPerAcre @Def: Amount of hay processed per acre by each machine type @Shape: ['NumMachines'] 
HayProcessedPerAcre = data['HayProcessedPerAcre']
# @Parameter MethaneProducedPerAcre @Def: Amount of methane gas produced per acre by each machine type @Shape: ['NumMachines'] 
MethaneProducedPerAcre = data['MethaneProducedPerAcre']
# @Parameter FuelRequiredPerAcre @Def: Amount of fuel required per acre by each machine type @Shape: ['NumMachines'] 
FuelRequiredPerAcre = data['FuelRequiredPerAcre']

# Variables 
# @Variable AcresAllocated @Def: The number of acres allocated to each machine type @Shape: ['NumMachines'] 
AcresAllocated = model.addVars(NumMachines, vtype=GRB.CONTINUOUS, name="AcresAllocated")

# Constraints 
# @Constraint Constr_1 @Def: The total number of acres allocated to all machine types cannot exceed TotalAcres.
model.addConstr(quicksum(AcresAllocated[i] for i in range(NumMachines)) <= TotalAcres)
# @Constraint Constr_2 @Def: The total fuel required for processing, based on FuelRequiredPerAcre for each machine type, cannot exceed FuelAvailable.
model.addConstr(quicksum(FuelRequiredPerAcre[i] * AcresAllocated[i] for i in range(NumMachines)) <= FuelAvailable)
# @Constraint Constr_3 @Def: The total methane produced, based on MethaneProducedPerAcre for each machine type, cannot exceed MethaneLimit.
model.addConstr(quicksum(MethaneProducedPerAcre[i] * AcresAllocated[i] for i in range(NumMachines)) <= MethaneLimit)

# Objective 
# @Objective Objective @Def: Total hay processed is the sum of the hay processed per acre by each machine type. The objective is to maximize the total hay processed.
model.setObjective(quicksum(HayProcessedPerAcre[i] * AcresAllocated[i] for i in range(NumMachines)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['AcresAllocated'] = [AcresAllocated[i].x for i in range(NumMachines)]
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)