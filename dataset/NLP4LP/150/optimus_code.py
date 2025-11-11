# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A toy store decides to deliver gifts using two shipping companies. The new
company can deliver NewCompanyCapacity gifts per trip while the old company can
deliver OldCompanyCapacity gifts per trip. The new company uses NewCompanyDiesel
liters of diesel per trip, whereas the old company uses OldCompanyDiesel liters
of diesel per trip. The toy store needs to deliver at least MinimumGifts gifts.
There can be at most MaxTripsNewCompany trips made by the new shipping company.
To ensure that the old company does not go out of business, at least
MinimumOldCompanyTripPercentage of all trips must be made by the old shipping
company. The objective is to determine the number of trips each company should
make to minimize the total amount of diesel used.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/151/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter NewCompanyCapacity @Def: Delivery capacity per trip of the new shipping company @Shape: [] 
NewCompanyCapacity = data['NewCompanyCapacity']
# @Parameter OldCompanyCapacity @Def: Delivery capacity per trip of the old shipping company @Shape: [] 
OldCompanyCapacity = data['OldCompanyCapacity']
# @Parameter NewCompanyDiesel @Def: Diesel consumption per trip of the new shipping company @Shape: [] 
NewCompanyDiesel = data['NewCompanyDiesel']
# @Parameter OldCompanyDiesel @Def: Diesel consumption per trip of the old shipping company @Shape: [] 
OldCompanyDiesel = data['OldCompanyDiesel']
# @Parameter MinimumGifts @Def: Minimum number of gifts to deliver @Shape: [] 
MinimumGifts = data['MinimumGifts']
# @Parameter MaxTripsNewCompany @Def: Maximum number of trips by the new shipping company @Shape: [] 
MaxTripsNewCompany = data['MaxTripsNewCompany']
# @Parameter MinimumOldCompanyTripPercentage @Def: Minimum percentage of trips that must be made by the old shipping company @Shape: [] 
MinimumOldCompanyTripPercentage = data['MinimumOldCompanyTripPercentage']

# Variables 
# @Variable TripsNewCompany @Def: The number of trips made by the new shipping company @Shape: [] 
TripsNewCompany = model.addVar(vtype=GRB.INTEGER, name="TripsNewCompany", ub=MaxTripsNewCompany)
# @Variable TripsOldCompany @Def: The number of trips made by the old shipping company @Shape: [] 
TripsOldCompany = model.addVar(vtype=GRB.INTEGER, name="TripsOldCompany")

# Constraints 
# @Constraint Constr_1 @Def: The total number of gifts delivered by the new and old shipping companies must be at least MinimumGifts.
model.addConstr(NewCompanyCapacity * TripsNewCompany + OldCompanyCapacity * TripsOldCompany >= MinimumGifts)
# @Constraint Constr_2 @Def: The number of trips made by the new shipping company cannot exceed MaxTripsNewCompany.
model.addConstr(TripsNewCompany <= MaxTripsNewCompany)
# @Constraint Constr_3 @Def: At least MinimumOldCompanyTripPercentage proportion of all trips must be made by the old shipping company.
model.addConstr(TripsOldCompany >= MinimumOldCompanyTripPercentage * (TripsOldCompany + TripsNewCompany))

# Objective 
# @Objective Objective @Def: Minimize the total amount of diesel used, which is the sum of diesel consumed by the new and old shipping companies.
model.setObjective(NewCompanyDiesel * TripsNewCompany + OldCompanyDiesel * TripsOldCompany, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['TripsNewCompany'] = TripsNewCompany.x
variables['TripsOldCompany'] = TripsOldCompany.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
