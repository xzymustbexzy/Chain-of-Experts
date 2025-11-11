# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A hospital hires UltrasoundTechnician and GraduateResearcher to image patients.
An UltrasoundTechnician works UltrasoundTechnicianShiftHours per shift while a
GraduateResearcher works GraduateResearcherShiftHours per shift.
UltrasoundTechnicians are paid UltrasoundTechnicianPayment per shift while
GraduateResearchers are paid GraduateResearcherPayment per shift. Due to
regulations, there must be ShiftRatio times as many UltrasoundTechnician shifts
as GraduateResearcher shifts. Currently, the hospital needs
RequiredUltrasoundServiceHours of ultrasound services to meet needs. If the
hospital has a budget of TotalBudget, how many of each worker certified to use
the ultrasound should be scheduled to reduce the total number of workers?
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/224/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter UltrasoundTechnicianShiftHours @Def: The number of hours an ultrasound technician works per shift @Shape: [] 
UltrasoundTechnicianShiftHours = data['UltrasoundTechnicianShiftHours']
# @Parameter GraduateResearcherShiftHours @Def: The number of hours a graduate researcher works per shift @Shape: [] 
GraduateResearcherShiftHours = data['GraduateResearcherShiftHours']
# @Parameter UltrasoundTechnicianPayment @Def: The payment an ultrasound technician receives per shift @Shape: [] 
UltrasoundTechnicianPayment = data['UltrasoundTechnicianPayment']
# @Parameter GraduateResearcherPayment @Def: The payment a graduate researcher receives per shift @Shape: [] 
GraduateResearcherPayment = data['GraduateResearcherPayment']
# @Parameter ShiftRatio @Def: The required ratio of ultrasound technician shifts to graduate researcher shifts @Shape: [] 
ShiftRatio = data['ShiftRatio']
# @Parameter RequiredUltrasoundServiceHours @Def: The total number of ultrasound service hours required @Shape: [] 
RequiredUltrasoundServiceHours = data['RequiredUltrasoundServiceHours']
# @Parameter TotalBudget @Def: The total budget available for workers' payments @Shape: [] 
TotalBudget = data['TotalBudget']

# Variables 
# @Variable NumberOfUltrasoundTechnicianShifts @Def: The number of shifts for ultrasound technicians @Shape: [] 
NumberOfUltrasoundTechnicianShifts = model.addVar(vtype=GRB.INTEGER, name="NumberOfUltrasoundTechnicianShifts")
# @Variable NumberOfGraduateResearcherShifts @Def: The number of shifts for graduate researchers @Shape: [] 
NumberOfGraduateResearcherShifts = model.addVar(vtype=GRB.INTEGER, name="NumberOfGraduateResearcherShifts")

# Constraints 
# @Constraint Constr_1 @Def: There must be ShiftRatio times as many UltrasoundTechnician shifts as GraduateResearcher shifts.
model.addConstr(NumberOfUltrasoundTechnicianShifts == ShiftRatio * NumberOfGraduateResearcherShifts)
# @Constraint Constr_2 @Def: The total ultrasound service hours provided by UltrasoundTechnicians and GraduateResearchers must be at least RequiredUltrasoundServiceHours.
model.addConstr(NumberOfUltrasoundTechnicianShifts * UltrasoundTechnicianShiftHours + NumberOfGraduateResearcherShifts * GraduateResearcherShiftHours >= RequiredUltrasoundServiceHours)
# @Constraint Constr_3 @Def: The total payment for UltrasoundTechnicians and GraduateResearchers must not exceed TotalBudget.
model.addConstr(UltrasoundTechnicianPayment * NumberOfUltrasoundTechnicianShifts + GraduateResearcherPayment * NumberOfGraduateResearcherShifts <= TotalBudget)

# Objective 
# @Objective Objective @Def: Total number of workers is the sum of UltrasoundTechnician shifts and GraduateResearcher shifts. The objective is to minimize the total number of workers.
model.setObjective(NumberOfUltrasoundTechnicianShifts + NumberOfGraduateResearcherShifts, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfUltrasoundTechnicianShifts'] = NumberOfUltrasoundTechnicianShifts.x
variables['NumberOfGraduateResearcherShifts'] = NumberOfGraduateResearcherShifts.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
