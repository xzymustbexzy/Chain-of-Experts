# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of cart delivery servers and hand delivery servers such
that CustomerInteractionsCart multiplied by the number of cart delivery servers
plus CustomerInteractionsHand multiplied by the number of hand delivery servers
meets or exceeds TargetCustomerInteractions. Ensure that at least
MinFractionCart fraction of delivery shifts are by cart and that the number of
hand delivery servers is at least MinServersHand. The objective is to minimize
the total number of refills per hour, calculated as RefillsCart multiplied by
the number of cart delivery servers plus RefillsHand multiplied by the number of
hand delivery servers.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/231/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CustomerInteractionsCart @Def: Customer interactions per cart delivery server per hour @Shape: [] 
CustomerInteractionsCart = data['CustomerInteractionsCart']
# @Parameter CustomerInteractionsHand @Def: Customer interactions per hand delivery server per hour @Shape: [] 
CustomerInteractionsHand = data['CustomerInteractionsHand']
# @Parameter RefillsCart @Def: Number of refills per cart delivery server per hour @Shape: [] 
RefillsCart = data['RefillsCart']
# @Parameter RefillsHand @Def: Number of refills per hand delivery server per hour @Shape: [] 
RefillsHand = data['RefillsHand']
# @Parameter MinFractionCart @Def: Minimum fraction of delivery shifts that must be by cart @Shape: [] 
MinFractionCart = data['MinFractionCart']
# @Parameter MinServersHand @Def: Minimum number of servers delivering by hand @Shape: [] 
MinServersHand = data['MinServersHand']
# @Parameter TargetCustomerInteractions @Def: Target total number of customer interactions per hour @Shape: [] 
TargetCustomerInteractions = data['TargetCustomerInteractions']

# Variables 
# @Variable NumberOfCartDeliveryServers @Def: The number of cart delivery servers @Shape: [] 
NumberOfCartDeliveryServers = model.addVar(vtype=GRB.INTEGER, name="NumberOfCartDeliveryServers")
# @Variable NumberOfHandDeliveryServers @Def: The number of hand delivery servers @Shape: [] 
NumberOfHandDeliveryServers = model.addVar(lb=MinServersHand, vtype=GRB.INTEGER, name="NumberOfHandDeliveryServers")

# Constraints 
# @Constraint Constr_1 @Def: CustomerInteractionsCart multiplied by the number of cart delivery servers plus CustomerInteractionsHand multiplied by the number of hand delivery servers must be greater than or equal to TargetCustomerInteractions.
model.addConstr(CustomerInteractionsCart * NumberOfCartDeliveryServers + CustomerInteractionsHand * NumberOfHandDeliveryServers >= TargetCustomerInteractions)
# @Constraint Constr_2 @Def: At least MinFractionCart fraction of delivery shifts must be by cart.
model.addConstr(NumberOfCartDeliveryServers >= MinFractionCart * (NumberOfCartDeliveryServers + NumberOfHandDeliveryServers))
# @Constraint Constr_3 @Def: The number of hand delivery servers must be at least MinServersHand.
model.addConstr(NumberOfHandDeliveryServers >= MinServersHand)

# Objective 
# @Objective Objective @Def: Minimize the total number of refills per hour, calculated as RefillsCart multiplied by the number of cart delivery servers plus RefillsHand multiplied by the number of hand delivery servers.
model.setObjective(RefillsCart * NumberOfCartDeliveryServers + RefillsHand * NumberOfHandDeliveryServers, GRB.MINIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfCartDeliveryServers'] = NumberOfCartDeliveryServers.x
variables['NumberOfHandDeliveryServers'] = NumberOfHandDeliveryServers.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
