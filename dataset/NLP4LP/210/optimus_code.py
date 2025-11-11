# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A company offers two types of subscription licenses: a personal license and a
commercial license. The cost to generate each personal license is
CostPersonalLicense, and the cost to generate each commercial license is
CostCommercialLicense. The marketing department estimates that the total number
of licenses sold per month cannot exceed MaxTotalLicenses. The profit earned
from each personal license is ProfitPersonalLicense, and the profit earned from
each commercial license is ProfitCommercialLicense. Additionally, the company
aims to ensure that the total expenditure does not surpass MaxTotalExpenditure.
The objective is to determine the number of personal and commercial licenses to
produce in order to maximize profits.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/211/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CostPersonalLicense @Def: Cost to generate a personal license @Shape: [] 
CostPersonalLicense = data['CostPersonalLicense']
# @Parameter CostCommercialLicense @Def: Cost to generate a commercial license @Shape: [] 
CostCommercialLicense = data['CostCommercialLicense']
# @Parameter ProfitPersonalLicense @Def: Profit per personal license @Shape: [] 
ProfitPersonalLicense = data['ProfitPersonalLicense']
# @Parameter ProfitCommercialLicense @Def: Profit per commercial license @Shape: [] 
ProfitCommercialLicense = data['ProfitCommercialLicense']
# @Parameter MaxTotalLicenses @Def: Maximum total licenses that can be sold per month @Shape: [] 
MaxTotalLicenses = data['MaxTotalLicenses']
# @Parameter MaxTotalExpenditure @Def: Maximum total expenditure allowed by the company @Shape: [] 
MaxTotalExpenditure = data['MaxTotalExpenditure']

# Variables 
# @Variable NumberOfPersonalLicenses @Def: The number of personal licenses sold per month @Shape: ['NonNegativeInteger'] 
NumberOfPersonalLicenses = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfPersonalLicenses")
# @Variable NumberOfCommercialLicenses @Def: The number of commercial licenses sold per month @Shape: ['NonNegativeInteger'] 
NumberOfCommercialLicenses = model.addVar(vtype=GRB.INTEGER, lb=0, name="NumberOfCommercialLicenses")

# Constraints 
# @Constraint Constr_1 @Def: The total number of licenses sold per month cannot exceed MaxTotalLicenses.
model.addConstr(NumberOfPersonalLicenses + NumberOfCommercialLicenses <= MaxTotalLicenses)
# @Constraint Constr_2 @Def: The total expenditure does not surpass MaxTotalExpenditure.
model.addConstr(CostPersonalLicense * NumberOfPersonalLicenses + CostCommercialLicense * NumberOfCommercialLicenses <= MaxTotalExpenditure)

# Objective 
# @Objective Objective @Def: Total profit is calculated as (ProfitPersonalLicense × number of personal licenses) + (ProfitCommercialLicense × number of commercial licenses). The objective is to maximize the total profit.
model.setObjective(ProfitPersonalLicense * NumberOfPersonalLicenses + ProfitCommercialLicense * NumberOfCommercialLicenses, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberOfPersonalLicenses'] = NumberOfPersonalLicenses.x
variables['NumberOfCommercialLicenses'] = NumberOfCommercialLicenses.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
