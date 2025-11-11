# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A patient receives radiation treatment using Beam1 and Beam2. Beam1 delivers
DoseRateBeam1BenignPancreas units per minute to the benign area of the pancreas,
DoseRateBeam1BenignSkin units per minute to the benign area of the skin, and
DoseRateBeam1Tumor units per minute to the tumor. Similarly, Beam2 delivers
DoseRateBeam2BenignPancreas units per minute to the benign area of the pancreas,
DoseRateBeam2BenignSkin units per minute to the benign area of the skin, and
DoseRateBeam2Tumor units per minute to the tumor. The total dose to the skin
must not exceed MaxDoseSkin, and the total dose to the tumor must be at least
MinDoseTumor. The objective is to determine the number of minutes to use Beam1
and Beam2 to minimize the total radiation received by the pancreas.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/130/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter DoseRateBeam1BenignPancreas @Def: Dose delivered per minute by Beam 1 to the benign area of the pancreas @Shape: [] 
DoseRateBeam1BenignPancreas = data['DoseRateBeam1BenignPancreas']
# @Parameter DoseRateBeam1BenignSkin @Def: Dose delivered per minute by Beam 1 to the benign area of the skin @Shape: [] 
DoseRateBeam1BenignSkin = data['DoseRateBeam1BenignSkin']
# @Parameter DoseRateBeam1Tumor @Def: Dose delivered per minute by Beam 1 to the tumor @Shape: [] 
DoseRateBeam1Tumor = data['DoseRateBeam1Tumor']
# @Parameter DoseRateBeam2BenignPancreas @Def: Dose delivered per minute by Beam 2 to the benign area of the pancreas @Shape: [] 
DoseRateBeam2BenignPancreas = data['DoseRateBeam2BenignPancreas']
# @Parameter DoseRateBeam2BenignSkin @Def: Dose delivered per minute by Beam 2 to the benign area of the skin @Shape: [] 
DoseRateBeam2BenignSkin = data['DoseRateBeam2BenignSkin']
# @Parameter DoseRateBeam2Tumor @Def: Dose delivered per minute by Beam 2 to the tumor @Shape: [] 
DoseRateBeam2Tumor = data['DoseRateBeam2Tumor']
# @Parameter MaxDoseSkin @Def: Maximum allowable dose to the skin @Shape: [] 
MaxDoseSkin = data['MaxDoseSkin']
# @Parameter MinDoseTumor @Def: Minimum required dose to the tumor @Shape: [] 
MinDoseTumor = data['MinDoseTumor']

# Variables 
# @Variable MinutesBeam1 @Def: The number of minutes Beam 1 is used @Shape: [] 
MinutesBeam1 = model.addVar(vtype=GRB.CONTINUOUS, name="MinutesBeam1")
# @Variable MinutesBeam2 @Def: The number of minutes Beam 2 is used @Shape: [] 
MinutesBeam2 = model.addVar(vtype=GRB.CONTINUOUS, name="MinutesBeam2")

# Constraints 
# @Constraint Constr_1 @Def: The total dose to the skin is DoseRateBeam1BenignSkin multiplied by the number of minutes Beam1 is used plus DoseRateBeam2BenignSkin multiplied by the number of minutes Beam2 is used. The total dose to the skin must not exceed MaxDoseSkin.
model.addConstr(DoseRateBeam1BenignSkin * MinutesBeam1 + DoseRateBeam2BenignSkin * MinutesBeam2 <= MaxDoseSkin)
# @Constraint Constr_2 @Def: The total dose to the tumor is DoseRateBeam1Tumor multiplied by the number of minutes Beam1 is used plus DoseRateBeam2Tumor multiplied by the number of minutes Beam2 is used. The total dose to the tumor must be at least MinDoseTumor.
model.addConstr(DoseRateBeam1Tumor * MinutesBeam1 + DoseRateBeam2Tumor * MinutesBeam2 >= MinDoseTumor)

# Objective 
# @Objective Objective @Def: Minimize the total radiation received by the pancreas, which is calculated as DoseRateBeam1BenignPancreas multiplied by the number of minutes Beam1 is used plus DoseRateBeam2BenignPancreas multiplied by the number of minutes Beam2 is used.
model.setObjective(DoseRateBeam1BenignPancreas * MinutesBeam1 + DoseRateBeam2BenignPancreas * MinutesBeam2, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['MinutesBeam1'] = MinutesBeam1.x
variables['MinutesBeam2'] = MinutesBeam2.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
