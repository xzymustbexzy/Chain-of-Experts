# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Minimize the total number of staff teachers and substitute teachers, where each
staff teacher works StaffShiftHours hours per shift and is paid StaffShiftPay
per shift, and each substitute teacher works SubstituteShiftHours hours per
shift and is paid SubstituteShiftPay per shift, subject to the constraints that
the total teaching hours meet TotalTeachingHours and the total payments do not
exceed TotalBudget.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/40/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter StaffShiftHours @Def: Number of hours worked per shift by a staff teacher @Shape: [] 
StaffShiftHours = data['StaffShiftHours']
# @Parameter StaffShiftPay @Def: Payment per shift to a staff teacher @Shape: [] 
StaffShiftPay = data['StaffShiftPay']
# @Parameter SubstituteShiftHours @Def: Number of hours worked per shift by a substitute teacher @Shape: [] 
SubstituteShiftHours = data['SubstituteShiftHours']
# @Parameter SubstituteShiftPay @Def: Payment per shift to a substitute teacher @Shape: [] 
SubstituteShiftPay = data['SubstituteShiftPay']
# @Parameter TotalTeachingHours @Def: Total required teaching hours for the summer term @Shape: [] 
TotalTeachingHours = data['TotalTeachingHours']
# @Parameter TotalBudget @Def: Total budget allocated for teacher payments @Shape: [] 
TotalBudget = data['TotalBudget']

# Variables 
# @Variable NumStaffShifts @Def: The number of shifts worked by staff teachers @Shape: [] 
NumStaffShifts = model.addVar(vtype=GRB.INTEGER, name="NumStaffShifts")
# @Variable NumSubstituteShifts @Def: The number of shifts worked by substitute teachers @Shape: [] 
NumSubstituteShifts = model.addVar(vtype=GRB.INTEGER, name="NumSubstituteShifts")
# @Variable NumStaffTeachers @Def: The number of staff teachers @Shape: ['Integer'] 
NumStaffTeachers = model.addVar(vtype=GRB.INTEGER, name="NumStaffTeachers")
# @Variable NumSubstituteTeachers @Def: The number of substitute teachers @Shape: ['Integer'] 
NumSubstituteTeachers = model.addVar(vtype=GRB.INTEGER, name="NumSubstituteTeachers")

# Constraints 
# @Constraint Constr_1 @Def: The total teaching hours provided by staff teachers and substitute teachers must meet TotalTeachingHours.
model.addConstr(NumStaffShifts * StaffShiftHours + NumSubstituteShifts * SubstituteShiftHours >= TotalTeachingHours)
# @Constraint Constr_2 @Def: The total payments to staff teachers and substitute teachers must not exceed TotalBudget.
model.addConstr(NumStaffShifts * StaffShiftPay + NumSubstituteShifts * SubstituteShiftPay <= TotalBudget)

# Objective 
# @Objective Objective @Def: The primary objective is to minimize the total number of staff teachers and substitute teachers while meeting the total teaching hours requirement and not exceeding the total budget.
model.setObjective(NumStaffTeachers + NumSubstituteTeachers, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumStaffShifts'] = NumStaffShifts.x
variables['NumSubstituteShifts'] = NumSubstituteShifts.x
variables['NumStaffTeachers'] = NumStaffTeachers.x
variables['NumSubstituteTeachers'] = NumSubstituteTeachers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
