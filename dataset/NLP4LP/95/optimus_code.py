# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
A drug company operates NumFactories factories to produce NumProducts products.
Each factory j has a ProductionRate[i][j] for each product i per hour. Each
factory j requires ResourceRequirement[j] units of a rare compound per hour. The
company has TotalResource units of the rare compound available. The company must
produce at least MinProduction[i] units of each product i. Determine the
operating hours for each factory to minimize the total time needed.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/96/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target            
        
# Parameters 
# @Parameter NumFactories @Def: Number of factories @Shape: [] 
NumFactories = data['NumFactories']
# @Parameter NumProducts @Def: Number of product types @Shape: [] 
NumProducts = data['NumProducts']
# @Parameter ProductionRate @Def: Production rate of product i in factory j per hour @Shape: ['NumProducts', 'NumFactories'] 
ProductionRate = data['ProductionRate']
# @Parameter ResourceRequirement @Def: Resource requirement of factory j per hour @Shape: ['NumFactories'] 
ResourceRequirement = data['ResourceRequirement']
# @Parameter TotalResource @Def: Total available units of the rare compound @Shape: [] 
TotalResource = data['TotalResource']
# @Parameter MinProduction @Def: Minimum required production of product i @Shape: ['NumProducts'] 
MinProduction = data['MinProduction']
    
# Variables 
# @Variable OperationalLevel @Def: The operational level of each factory j @Shape: ['NumFactories'] 
OperationalLevel = model.addVars(NumFactories, vtype=GRB.CONTINUOUS, name="OperationalLevel")
# @Variable MaxOperatingHours @Def: The maximum operating hours across all factories @Shape: [] 
MaxOperatingHours = model.addVar(vtype=GRB.CONTINUOUS, name="MaxOperatingHours")
        
# Constraints 
# @Constraint Constr_1 @Def: Each factory requires ResourceRequirement[j] units of the rare compound per hour. The total consumption of the rare compound across all factories cannot exceed TotalResource units.
model.addConstr(quicksum(ResourceRequirement[j] * OperationalLevel[j] for j in range(NumFactories)) <= TotalResource)
# @Constraint Constr_2 @Def: Each factory j produces ProductionRate[i][j] units of product i per hour. The total production of each product i across all factories must be at least MinProduction[i] units.
model.addConstrs(
    (quicksum(ProductionRate[i][j] * OperationalLevel[j] for j in range(NumFactories)) 
     >= MinProduction[i] for i in range(NumProducts)),
    name="MinProduction"
)

# Add constraints to link MaxOperatingHours with OperationalLevel
model.addConstrs((OperationalLevel[j] <= MaxOperatingHours for j in range(NumFactories)), name="MaxOperatingHoursConstr")
    
# Objective 
# @Objective Objective @Def: Minimize the maximum operating hours across all factories required to meet the minimum production requirements while adhering to the limited availability of the rare compound.
model.setObjective(MaxOperatingHours, GRB.MINIMIZE)
    
# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['OperationalLevel'] = {j: OperationalLevel[j].X for j in range(NumFactories)}
variables['MaxOperatingHours'] = MaxOperatingHours.X
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
