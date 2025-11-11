# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A hospital prepares two types of medication: medication patches and anti-biotic
creams. Each batch of medication patches requires PreparationTimeMedicationPatch
minutes to prepare and MaterialRequiredMedicationPatch units of materials. Each
batch of anti-biotic creams requires PreparationTimeAntiBioticCream minutes to
prepare and MaterialRequiredAntiBioticCream units of materials. Since anti-
biotic creams are used more often, the number of batches of anti-biotic creams
must be at least MinRatioAntiBioticCreamToMedicationPatch times the number of
batches of medication patches. Due to storage constraints, the total number of
batches of medication patches and anti-biotic creams cannot exceed
MaxTotalBatches. The hospital has AvailableStaffTime minutes of staff time
available and AvailableMaterials units of materials. Each batch of medication
patches can treat TreatmentPerBatchMedicationPatch people, and each batch of
anti-biotic creams can treat TreatmentPerBatchAntiBioticCream people. The
hospital aims to determine the number of batches of each product to maximize the
number of people that can be treated.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/262/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PreparationTimeMedicationPatch @Def: Preparation time per batch of medication patches @Shape: [] 
PreparationTimeMedicationPatch = data['PreparationTimeMedicationPatch']
# @Parameter PreparationTimeAntiBioticCream @Def: Preparation time per batch of anti-biotic creams @Shape: [] 
PreparationTimeAntiBioticCream = data['PreparationTimeAntiBioticCream']
# @Parameter MaterialRequiredMedicationPatch @Def: Material required per batch of medication patches @Shape: [] 
MaterialRequiredMedicationPatch = data['MaterialRequiredMedicationPatch']
# @Parameter MaterialRequiredAntiBioticCream @Def: Material required per batch of anti-biotic creams @Shape: [] 
MaterialRequiredAntiBioticCream = data['MaterialRequiredAntiBioticCream']
# @Parameter MinRatioAntiBioticCreamToMedicationPatch @Def: Minimum ratio of anti-biotic creams to medication patches @Shape: [] 
MinRatioAntiBioticCreamToMedicationPatch = data['MinRatioAntiBioticCreamToMedicationPatch']
# @Parameter MaxTotalBatches @Def: Maximum total number of batches @Shape: [] 
MaxTotalBatches = data['MaxTotalBatches']
# @Parameter AvailableStaffTime @Def: Available staff time in minutes @Shape: [] 
AvailableStaffTime = data['AvailableStaffTime']
# @Parameter AvailableMaterials @Def: Available units of materials @Shape: [] 
AvailableMaterials = data['AvailableMaterials']
# @Parameter TreatmentPerBatchMedicationPatch @Def: Number of people treated by each batch of medication patches @Shape: [] 
TreatmentPerBatchMedicationPatch = data['TreatmentPerBatchMedicationPatch']
# @Parameter TreatmentPerBatchAntiBioticCream @Def: Number of people treated by each batch of anti-biotic creams @Shape: [] 
TreatmentPerBatchAntiBioticCream = data['TreatmentPerBatchAntiBioticCream']

# Variables 
# @Variable NumBatchesAntiBioticCream @Def: The number of batches of anti-biotic creams @Shape: [] 
NumBatchesAntiBioticCream = model.addVar(vtype=GRB.INTEGER, name="NumBatchesAntiBioticCream")
# @Variable NumBatchesMedicationPatch @Def: The number of batches of medication patches @Shape: [] 
NumBatchesMedicationPatch = model.addVar(vtype=GRB.INTEGER, name="NumBatchesMedicationPatch")

# Constraints 
# @Constraint Constr_1 @Def: The number of batches of anti-biotic creams must be at least MinRatioAntiBioticCreamToMedicationPatch times the number of batches of medication patches.
model.addConstr(NumBatchesAntiBioticCream >= MinRatioAntiBioticCreamToMedicationPatch * NumBatchesMedicationPatch)
# @Constraint Constr_2 @Def: The total number of batches of medication patches and anti-biotic creams cannot exceed MaxTotalBatches.
model.addConstr(NumBatchesAntiBioticCream + NumBatchesMedicationPatch <= MaxTotalBatches)
# @Constraint Constr_3 @Def: The total preparation time for medication patches and anti-biotic creams must not exceed AvailableStaffTime minutes.
model.addConstr(PreparationTimeMedicationPatch * NumBatchesMedicationPatch + PreparationTimeAntiBioticCream * NumBatchesAntiBioticCream <= AvailableStaffTime)
# @Constraint Constr_4 @Def: The total materials required for medication patches and anti-biotic creams must not exceed AvailableMaterials units.
model.addConstr(NumBatchesMedicationPatch * MaterialRequiredMedicationPatch + NumBatchesAntiBioticCream * MaterialRequiredAntiBioticCream <= AvailableMaterials)

# Objective 
# @Objective Objective @Def: Maximize the total number of people treated, which is calculated as (TreatmentPerBatchMedicationPatch * number of medication patch batches) plus (TreatmentPerBatchAntiBioticCream * number of anti-biotic cream batches).
model.setObjective(TreatmentPerBatchMedicationPatch * NumBatchesMedicationPatch + TreatmentPerBatchAntiBioticCream * NumBatchesAntiBioticCream, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumBatchesAntiBioticCream'] = NumBatchesAntiBioticCream.x
variables['NumBatchesMedicationPatch'] = NumBatchesMedicationPatch.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
