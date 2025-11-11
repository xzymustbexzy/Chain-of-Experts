# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A dog hospital has TotalToothMedication units of tooth medication available to
produce both small and large bones. Each small bone requires
ToothMedicationPerSmallBone units of tooth medication and MeatPerSmallBone units
of meat. Each large bone requires ToothMedicationPerLargeBone units of tooth
medication and MeatPerLargeBone units of meat. At least MinProportionSmallBones
proportion of the bones produced must be small. Additionally, the hospital must
produce at least MinLargeBones large bones. Determine the number of small and
large bones to produce to minimize the total amount of meat used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/93/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter TotalToothMedication @Def: Total units of tooth medication available for making bones @Shape: [] 
TotalToothMedication = data['TotalToothMedication']
# @Parameter ToothMedicationPerSmallBone @Def: Units of tooth medication required to make one small bone @Shape: [] 
ToothMedicationPerSmallBone = data['ToothMedicationPerSmallBone']
# @Parameter MeatPerSmallBone @Def: Units of meat required to make one small bone @Shape: [] 
MeatPerSmallBone = data['MeatPerSmallBone']
# @Parameter ToothMedicationPerLargeBone @Def: Units of tooth medication required to make one large bone @Shape: [] 
ToothMedicationPerLargeBone = data['ToothMedicationPerLargeBone']
# @Parameter MeatPerLargeBone @Def: Units of meat required to make one large bone @Shape: [] 
MeatPerLargeBone = data['MeatPerLargeBone']
# @Parameter MinProportionSmallBones @Def: Minimum proportion of bones that must be small @Shape: [] 
MinProportionSmallBones = data['MinProportionSmallBones']
# @Parameter MinLargeBones @Def: Minimum number of large bones to be made @Shape: [] 
MinLargeBones = data['MinLargeBones']

# Variables 
# @Variable SmallBones @Def: The number of small bones produced @Shape: [] 
SmallBones = model.addVar(vtype=GRB.INTEGER, name="SmallBones")
# @Variable LargeBones @Def: The number of large bones produced @Shape: [] 
LargeBones = model.addVar(vtype=GRB.INTEGER, name="LargeBones")

# Constraints 
# @Constraint Constr_1 @Def: The total tooth medication used to produce small and large bones cannot exceed TotalToothMedication units.
model.addConstr(ToothMedicationPerSmallBone * SmallBones + ToothMedicationPerLargeBone * LargeBones <= TotalToothMedication)
# @Constraint Constr_2 @Def: At least MinProportionSmallBones proportion of the bones produced must be small.
model.addConstr(SmallBones >= MinProportionSmallBones * (SmallBones + LargeBones), 'MinProportionSmallBones')
# @Constraint Constr_3 @Def: The hospital must produce at least MinLargeBones large bones.
model.addConstr(LargeBones >= MinLargeBones)

# Objective 
# @Objective Objective @Def: Minimize the total amount of meat used in producing small and large bones.
model.setObjective(MeatPerSmallBone * SmallBones + MeatPerLargeBone * LargeBones, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SmallBones'] = SmallBones.x
variables['LargeBones'] = LargeBones.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
