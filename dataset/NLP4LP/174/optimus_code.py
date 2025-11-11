# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A dog school trains NumDogTypes different dog types to deliver newspapers. Each
dog type delivers NewspapersPerService newspapers per service and requires
TreatsPerService small bone treats per service. The total number of small bone
treats available is TotalBoneTreatsAvailable. At least MinGoldenRetrievers
golden retrievers must be used, and at most MaxPercentageLabradors of the dogs
can be labradors. The goal is to maximize the number of newspapers delivered.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/175/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumDogTypes @Def: Number of different dog types used in the school @Shape: [] 
NumDogTypes = data['NumDogTypes']
# @Parameter NewspapersPerService @Def: Number of newspapers delivered per service by each dog type @Shape: ['NumDogTypes'] 
NewspapersPerService = data['NewspapersPerService']
# @Parameter TreatsPerService @Def: Number of small bone treats required per service by each dog type @Shape: ['NumDogTypes'] 
TreatsPerService = data['TreatsPerService']
# @Parameter TotalBoneTreatsAvailable @Def: Total number of small bone treats available @Shape: [] 
TotalBoneTreatsAvailable = data['TotalBoneTreatsAvailable']
# @Parameter MinGoldenRetrievers @Def: Minimum number of golden retrievers to be used @Shape: [] 
MinGoldenRetrievers = data['MinGoldenRetrievers']
# @Parameter MaxPercentageLabradors @Def: Maximum percentage of dogs that can be labradors @Shape: [] 
MaxPercentageLabradors = data['MaxPercentageLabradors']

# Variables 
# @Variable ServicesDelivered @Def: The number of services delivered by each dog type @Shape: ['NumDogTypes'] 
ServicesDelivered = model.addVars(NumDogTypes, vtype=GRB.INTEGER, name="ServicesDelivered")
# @Variable NumGoldenRetrievers @Def: The number of golden retrievers used @Shape: [] 
NumGoldenRetrievers = model.addVar(vtype=GRB.INTEGER, name="NumGoldenRetrievers")
# @Variable NumLabradors @Def: The number of Labradors used @Shape: [] 
NumLabradors = model.addVar(vtype=GRB.INTEGER, name="NumLabradors")

# Constraints 
# @Constraint Constr_1 @Def: The total number of small bone treats required by all dog types cannot exceed TotalBoneTreatsAvailable.
model.addConstr(quicksum(TreatsPerService[d] * ServicesDelivered[d] for d in range(NumDogTypes)) <= TotalBoneTreatsAvailable)
# @Constraint Constr_2 @Def: At least MinGoldenRetrievers golden retrievers must be used.
model.addConstr(NumGoldenRetrievers >= MinGoldenRetrievers)
# @Constraint Constr_3 @Def: No more than MaxPercentageLabradors of the total number of dogs can be labradors.
model.addConstr(NumLabradors <= MaxPercentageLabradors * (NumGoldenRetrievers + NumLabradors))

# Objective 
# @Objective Objective @Def: Maximize the total number of newspapers delivered by the dog school while adhering to constraints on treat availability, minimum golden retrievers, and the proportion of labradors.
model.setObjective(quicksum(ServicesDelivered[i] * NewspapersPerService[i] for i in range(NumDogTypes)), GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['ServicesDelivered'] = {d: ServicesDelivered[d].x for d in range(NumDogTypes)}
variables['NumGoldenRetrievers'] = NumGoldenRetrievers.x
variables['NumLabradors'] = NumLabradors.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)