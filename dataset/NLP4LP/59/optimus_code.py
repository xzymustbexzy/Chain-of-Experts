# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A clinic employs nurses and pharmacists to deliver shots to patients. A nurse
works NurseShiftHours per shift while a pharmacist works PharmacistShiftHours
per shift. Nurses are paid NurseCostPerShift per shift while pharmacists are
paid PharmacistCostPerShift per shift. Currently, the clinic needs
TotalLaborHours hours of healthcare labor to meet needs. If the firm has a
budget of TotalBudget, how many of each healthcare worker should be scheduled to
minimize the total number of workers?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/60/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NurseShiftHours @Def: Number of hours a nurse works per shift @Shape: [] 
NurseShiftHours = data['NurseShiftHours']
# @Parameter PharmacistShiftHours @Def: Number of hours a pharmacist works per shift @Shape: [] 
PharmacistShiftHours = data['PharmacistShiftHours']
# @Parameter NurseCostPerShift @Def: Cost to employ one nurse per shift @Shape: [] 
NurseCostPerShift = data['NurseCostPerShift']
# @Parameter PharmacistCostPerShift @Def: Cost to employ one pharmacist per shift @Shape: [] 
PharmacistCostPerShift = data['PharmacistCostPerShift']
# @Parameter TotalLaborHours @Def: Total required healthcare labor hours @Shape: [] 
TotalLaborHours = data['TotalLaborHours']
# @Parameter TotalBudget @Def: Total budget for labor costs @Shape: [] 
TotalBudget = data['TotalBudget']

# Variables 
# @Variable NumberOfNurseShifts @Def: The number of nurse shifts @Shape: ['NonNegative Integer'] 
NumberOfNurseShifts = model.addVar(vtype=GRB.INTEGER, name="NumberOfNurseShifts")
# @Variable NumberOfPharmacistShifts @Def: The number of pharmacist shifts @Shape: ['NonNegative Integer'] 
NumberOfPharmacistShifts = model.addVar(vtype=GRB.INTEGER, name="NumberOfPharmacistShifts")
# @Variable NumberOfNurses @Def: The number of nurses employed @Shape: ['NonNegative Integer'] 
NumberOfNurses = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfNurses")
# @Variable NumberOfPharmacists @Def: The number of pharmacists employed @Shape: ['NonNegative Integer'] 
NumberOfPharmacists = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfPharmacists")

# Constraints 
# @Constraint Constr_1 @Def: The total healthcare labor hours provided by nurses and pharmacists must be at least TotalLaborHours.
model.addConstr(NurseShiftHours * NumberOfNurseShifts + PharmacistShiftHours * NumberOfPharmacistShifts >= TotalLaborHours)
# @Constraint Constr_2 @Def: The total labor cost for nurses and pharmacists must not exceed TotalBudget.
model.addConstr(NurseCostPerShift * NumberOfNurseShifts + PharmacistCostPerShift * NumberOfPharmacistShifts <= TotalBudget)

# Objective 
# @Objective Objective @Def: Minimize the total number of workers, which is the sum of nurses and pharmacists, while meeting the required healthcare labor hours and adhering to the budget.
model.setObjective(NumberOfNurses + NumberOfPharmacists, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfNurseShifts'] = NumberOfNurseShifts.x
variables['NumberOfPharmacistShifts'] = NumberOfPharmacistShifts.x
variables['NumberOfNurses'] = NumberOfNurses.x
variables['NumberOfPharmacists'] = NumberOfPharmacists.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
