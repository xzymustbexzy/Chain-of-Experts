# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A company sells two types of products: scooters and bikes. The profit per
scooter is ProfitPerScooter and the profit per bike is ProfitPerBike. Each
scooter requires DesignHoursPerScooter hours with the design team and
EngineeringHoursPerScooter hours with the engineering team. Each bike requires
DesignHoursPerBike hours with the design team and EngineeringHoursPerBike hours
with the engineering team. The company has TotalDesignHoursAvailable design
hours and TotalEngineeringHoursAvailable engineering hours available each month.
Determine the number of scooters and bikes the company should produce each month
to maximize profit.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/34/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProfitPerScooter @Def: Profit per scooter @Shape: [] 
ProfitPerScooter = data['ProfitPerScooter']
# @Parameter ProfitPerBike @Def: Profit per bike @Shape: [] 
ProfitPerBike = data['ProfitPerBike']
# @Parameter DesignHoursPerScooter @Def: Design hours required per scooter @Shape: [] 
DesignHoursPerScooter = data['DesignHoursPerScooter']
# @Parameter DesignHoursPerBike @Def: Design hours required per bike @Shape: [] 
DesignHoursPerBike = data['DesignHoursPerBike']
# @Parameter EngineeringHoursPerScooter @Def: Engineering hours required per scooter @Shape: [] 
EngineeringHoursPerScooter = data['EngineeringHoursPerScooter']
# @Parameter EngineeringHoursPerBike @Def: Engineering hours required per bike @Shape: [] 
EngineeringHoursPerBike = data['EngineeringHoursPerBike']
# @Parameter TotalDesignHoursAvailable @Def: Total design hours available per month @Shape: [] 
TotalDesignHoursAvailable = data['TotalDesignHoursAvailable']
# @Parameter TotalEngineeringHoursAvailable @Def: Total engineering hours available per month @Shape: [] 
TotalEngineeringHoursAvailable = data['TotalEngineeringHoursAvailable']

# Variables 
# @Variable NumberOfScooters @Def: The number of scooters to be produced @Shape: [] 
NumberOfScooters = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfScooters")
# @Variable NumberOfBikes @Def: The number of bikes to be produced @Shape: [] 
NumberOfBikes = model.addVar(vtype=GRB.CONTINUOUS, name="NumberOfBikes")

# Constraints 
# @Constraint Constr_1 @Def: DesignHoursPerScooter * NumberOfScooters + DesignHoursPerBike * NumberOfBikes ≤ TotalDesignHoursAvailable
model.addConstr(DesignHoursPerScooter * NumberOfScooters + DesignHoursPerBike * NumberOfBikes <= TotalDesignHoursAvailable)
# @Constraint Constr_2 @Def: EngineeringHoursPerScooter * NumberOfScooters + EngineeringHoursPerBike * NumberOfBikes ≤ TotalEngineeringHoursAvailable
model.addConstr(EngineeringHoursPerScooter * NumberOfScooters + EngineeringHoursPerBike * NumberOfBikes <= TotalEngineeringHoursAvailable)

# Objective 
# @Objective Objective @Def: Maximize total profit, which is ProfitPerScooter * NumberOfScooters + ProfitPerBike * NumberOfBikes
model.setObjective(ProfitPerScooter * NumberOfScooters + ProfitPerBike * NumberOfBikes, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfScooters'] = NumberOfScooters.x
variables['NumberOfBikes'] = NumberOfBikes.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
