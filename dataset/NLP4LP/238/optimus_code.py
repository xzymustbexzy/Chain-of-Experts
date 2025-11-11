# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A clothing company can sell their product in two types of stores: a retail store
and a factory outlet. A retail store brings in CustomersPerRetailStore customers
every day and requires EmployeesPerRetailStore employees to operate. A factory
outlet brings in CustomersPerFactoryOutlet customers every day and requires
EmployeesPerFactoryOutlet employees to run. Company executives decided that
there must be at least MinTotalCustomers customers every day and can make
available MaxTotalEmployees employees. The company aims to minimize the number
of stores that must be open.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/239/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CustomersPerRetailStore @Def: Number of customers served per retail store each day @Shape: [] 
CustomersPerRetailStore = data['CustomersPerRetailStore']
# @Parameter EmployeesPerRetailStore @Def: Number of employees required to operate a retail store @Shape: [] 
EmployeesPerRetailStore = data['EmployeesPerRetailStore']
# @Parameter CustomersPerFactoryOutlet @Def: Number of customers served per factory outlet each day @Shape: [] 
CustomersPerFactoryOutlet = data['CustomersPerFactoryOutlet']
# @Parameter EmployeesPerFactoryOutlet @Def: Number of employees required to operate a factory outlet @Shape: [] 
EmployeesPerFactoryOutlet = data['EmployeesPerFactoryOutlet']
# @Parameter MinTotalCustomers @Def: Minimum total number of customers required each day @Shape: [] 
MinTotalCustomers = data['MinTotalCustomers']
# @Parameter MaxTotalEmployees @Def: Maximum number of employees available @Shape: [] 
MaxTotalEmployees = data['MaxTotalEmployees']

# Variables 
# @Variable NumberRetailStores @Def: The number of retail stores to open @Shape: ['integer'] 
NumberRetailStores = model.addVar(vtype=GRB.INTEGER, name="NumberRetailStores")
# @Variable NumberFactoryOutlets @Def: The number of factory outlets to open @Shape: ['integer'] 
NumberFactoryOutlets = model.addVar(vtype=GRB.INTEGER, name="NumberFactoryOutlets")

# Constraints 
# @Constraint Constr_1 @Def: The total number of customers served each day must be at least MinTotalCustomers.
model.addConstr(CustomersPerRetailStore * NumberRetailStores + CustomersPerFactoryOutlet * NumberFactoryOutlets >= MinTotalCustomers)
# @Constraint Constr_2 @Def: The total number of employees used to operate the stores must not exceed MaxTotalEmployees.
model.addConstr(EmployeesPerRetailStore * NumberRetailStores + EmployeesPerFactoryOutlet * NumberFactoryOutlets <= MaxTotalEmployees)

# Objective 
# @Objective Objective @Def: Minimize the total number of stores (retail stores and factory outlets) that must be open.
model.setObjective(NumberRetailStores + NumberFactoryOutlets, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberRetailStores'] = NumberRetailStores.x
variables['NumberFactoryOutlets'] = NumberFactoryOutlets.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
