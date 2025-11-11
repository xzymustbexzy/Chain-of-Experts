# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A factory provides rides for its employees using either taxis or company cars.
Each taxi ride can transport EmployeesPerTaxiRide employees, and each company
car ride can transport EmployeesPerCompanyCarRide employees. At most
MaxCompanyCarRidePercentage of the total rides can be company car rides, and
there must be at least MinCompanyCarRides company car rides. The company needs
 to transport at least MinEmployees employees. Determine the number of taxi and
company car rides to minimize the total number of taxi rides.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/178/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter EmployeesPerTaxiRide @Def: Number of employees that can be transported in one taxi ride. @Shape: [] 
EmployeesPerTaxiRide = data['EmployeesPerTaxiRide']
# @Parameter EmployeesPerCompanyCarRide @Def: Number of employees that can be transported in one company car ride. @Shape: [] 
EmployeesPerCompanyCarRide = data['EmployeesPerCompanyCarRide']
# @Parameter MaxCompanyCarRidePercentage @Def: The upper limit on the proportion of total rides that can be company car rides. @Shape: [] 
MaxCompanyCarRidePercentage = data['MaxCompanyCarRidePercentage']
# @Parameter MinCompanyCarRides @Def: The minimum required number of company car rides. @Shape: [] 
MinCompanyCarRides = data['MinCompanyCarRides']
# @Parameter MinEmployees @Def: The minimum number of employees that need to be transported. @Shape: [] 
MinEmployees = data['MinEmployees']

# Variables 
# @Variable NumberOfTaxiRides @Def: The number of taxi rides @Shape: [] 
NumberOfTaxiRides = model.addVar(vtype=GRB.INTEGER, name="NumberOfTaxiRides")
# @Variable NumberOfCompanyCarRides @Def: The number of company car rides @Shape: [] 
NumberOfCompanyCarRides = model.addVar(vtype=GRB.INTEGER, name="NumberOfCompanyCarRides")

# Constraints 
# @Constraint Constr_1 @Def: The total number of employees transported by taxi and company car rides must be at least MinEmployees.
model.addConstr(EmployeesPerTaxiRide * NumberOfTaxiRides + EmployeesPerCompanyCarRide * NumberOfCompanyCarRides >= MinEmployees)
# @Constraint Constr_2 @Def: The number of company car rides must not exceed MaxCompanyCarRidePercentage of the total number of rides.
model.addConstr((1 - MaxCompanyCarRidePercentage) * NumberOfCompanyCarRides <= MaxCompanyCarRidePercentage * NumberOfTaxiRides)
# @Constraint Constr_3 @Def: There must be at least MinCompanyCarRides company car rides.
model.addConstr(NumberOfCompanyCarRides >= MinCompanyCarRides)

# Objective 
# @Objective Objective @Def: Minimize the total number of taxi rides.
model.setObjective(NumberOfTaxiRides, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfTaxiRides'] = NumberOfTaxiRides.x
variables['NumberOfCompanyCarRides'] = NumberOfCompanyCarRides.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)