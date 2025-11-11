# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Define decision variables for the number of seasonal volunteers and full-time
volunteers. The objective is to maximize the total number of gifts delivered,
calculated as GiftsPerSeasonal multiplied by the number of seasonal volunteers
plus GiftsPerFullTime multiplied by the number of full-time volunteers. The
constraints are that the total points awarded, PointsPerSeasonal times seasonal
volunteers plus PointsPerFullTime times full-time volunteers, does not exceed
PointsLimit; the number of seasonal volunteers does not exceed
MaxSeasonalPercentage of the total number of volunteers; and the number of full-
time volunteers is at least MinFullTimeVolunteers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/165/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PointsLimit @Def: Number of points available to distribute @Shape: [] 
PointsLimit = data['PointsLimit']
# @Parameter MaxSeasonalPercentage @Def: Maximum percentage of volunteers that can be seasonal @Shape: [] 
MaxSeasonalPercentage = data['MaxSeasonalPercentage']
# @Parameter MinFullTimeVolunteers @Def: Minimum number of full-time volunteers required @Shape: [] 
MinFullTimeVolunteers = data['MinFullTimeVolunteers']
# @Parameter GiftsPerSeasonal @Def: Number of gifts delivered by each seasonal volunteer @Shape: [] 
GiftsPerSeasonal = data['GiftsPerSeasonal']
# @Parameter PointsPerSeasonal @Def: Points awarded to each seasonal volunteer @Shape: [] 
PointsPerSeasonal = data['PointsPerSeasonal']
# @Parameter GiftsPerFullTime @Def: Number of gifts delivered by each full-time volunteer @Shape: [] 
GiftsPerFullTime = data['GiftsPerFullTime']
# @Parameter PointsPerFullTime @Def: Points awarded to each full-time volunteer @Shape: [] 
PointsPerFullTime = data['PointsPerFullTime']

# Variables 
# @Variable SeasonalVolunteers @Def: The number of seasonal volunteers @Shape: ['integer'] 
SeasonalVolunteers = model.addVar(vtype=GRB.INTEGER, name="SeasonalVolunteers")
# @Variable FullTimeVolunteers @Def: The number of full-time volunteers @Shape: ['integer'] 
FullTimeVolunteers = model.addVar(lb=MinFullTimeVolunteers, vtype=GRB.INTEGER, name="FullTimeVolunteers")

# Constraints 
# @Constraint Constr_1 @Def: The total points awarded to volunteers must not exceed PointsLimit. This is calculated as PointsPerSeasonal multiplied by the number of seasonal volunteers plus PointsPerFullTime multiplied by the number of full-time volunteers.
model.addConstr(PointsPerSeasonal * SeasonalVolunteers + PointsPerFullTime * FullTimeVolunteers <= PointsLimit)
# @Constraint Constr_2 @Def: The number of seasonal volunteers must not exceed MaxSeasonalPercentage of the total number of volunteers. Mathematically, SeasonalVolunteers ≤ MaxSeasonalPercentage * (SeasonalVolunteers + FullTimeVolunteers).
model.addConstr(SeasonalVolunteers <= MaxSeasonalPercentage * (SeasonalVolunteers + FullTimeVolunteers))
# @Constraint Constr_3 @Def: The number of full-time volunteers must be at least MinFullTimeVolunteers.
model.addConstr(FullTimeVolunteers >= MinFullTimeVolunteers)

# Objective 
# @Objective Objective @Def: Maximize the total number of gifts delivered, calculated as GiftsPerSeasonal multiplied by the number of seasonal volunteers plus GiftsPerFullTime multiplied by the number of full-time volunteers.
model.setObjective(GiftsPerSeasonal * SeasonalVolunteers + GiftsPerFullTime * FullTimeVolunteers, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['SeasonalVolunteers'] = SeasonalVolunteers.x
variables['FullTimeVolunteers'] = FullTimeVolunteers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
