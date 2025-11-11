# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
An office purchases NumPrinterTypes different printer types, each with a
specific PrintingSpeed and InkUsage. The office must ensure that the total pages
printed per minute is at least MinPagesPerMinute and that the total ink used per
minute does not exceed MaxInkPerMinute. Additionally, the quantity of one
printer type must be greater than the quantity of another printer type. The
objective is to minimize the total number of printers purchased.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/87/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target        
        
# Parameters 
# @Parameter NumPrinterTypes @Def: Number of different printer types @Shape: [] 
NumPrinterTypes = data['NumPrinterTypes']
# @Parameter PrintingSpeed @Def: Pages printed per minute by each printer type @Shape: ['NumPrinterTypes'] 
PrintingSpeed = data['PrintingSpeed']
# @Parameter InkUsage @Def: Ink units used per minute by each printer type @Shape: ['NumPrinterTypes'] 
InkUsage = data['InkUsage']
# @Parameter MinPagesPerMinute @Def: Minimum number of pages to be printed per minute @Shape: [] 
MinPagesPerMinute = data['MinPagesPerMinute']
# @Parameter MaxInkPerMinute @Def: Maximum number of ink units allowed per minute @Shape: [] 
MaxInkPerMinute = data['MaxInkPerMinute']

# Variables 
# @Variable NumPrinters @Def: Number of printers for each printer type @Shape: ['NumPrinterTypes'] 
NumPrinters = model.addVars(NumPrinterTypes, vtype=GRB.INTEGER, name="NumPrinters")

# Constraints 
# @Constraint Constr_1 @Def: The total pages printed per minute must be at least MinPagesPerMinute.
model.addConstr(quicksum(PrintingSpeed[j] * NumPrinters[j] for j in range(NumPrinterTypes)) >= MinPagesPerMinute)
# @Constraint Constr_2 @Def: The total ink used per minute must not exceed MaxInkPerMinute.
model.addConstr(quicksum(NumPrinters[i] * InkUsage[i] for i in range(NumPrinterTypes)) <= MaxInkPerMinute)
# @Constraint Constr_3 @Def: The quantity of one printer type must be greater than the quantity of another printer type.
i = 0  # Define i
j = 1  # Define j
model.addConstr(NumPrinters[i] >= NumPrinters[j], name="PrinterTypeConstraint")

# Objective 
# @Objective Objective @Def: The objective is to minimize the total number of printers purchased.
model.setObjective(quicksum(NumPrinters[i] for i in range(NumPrinterTypes)), GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumPrinters'] = {k: v.X for k, v in NumPrinters.items()}
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)