# Code automatically generated from OptiMUS

# Problem type: LP        
# Problem description
'''
The company produces two types of workbooks: math and English. It must produce
at least MinMathWorkbooks math workbooks and at least MinEnglishWorkbooks
English workbooks, but no more than MaxMathWorkbooks math workbooks and no more
than MaxEnglishWorkbooks English workbooks. Additionally, the total number of
workbooks produced must be at least MinTotalWorkbooks. The objective is to
maximize the total profit, which is calculated as ProfitMathWorkbook multiplied
by the number of math workbooks plus ProfitEnglishWorkbook multiplied by the
number of English workbooks.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/209/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter MinMathWorkbooks @Def: Minimum number of math workbooks to produce @Shape: [] 
MinMathWorkbooks = data['MinMathWorkbooks']
# @Parameter MinEnglishWorkbooks @Def: Minimum number of English workbooks to produce @Shape: [] 
MinEnglishWorkbooks = data['MinEnglishWorkbooks']
# @Parameter MaxMathWorkbooks @Def: Maximum number of math workbooks to produce @Shape: [] 
MaxMathWorkbooks = data['MaxMathWorkbooks']
# @Parameter MaxEnglishWorkbooks @Def: Maximum number of English workbooks to produce @Shape: [] 
MaxEnglishWorkbooks = data['MaxEnglishWorkbooks']
# @Parameter MinTotalWorkbooks @Def: Minimum total number of workbooks to produce @Shape: [] 
MinTotalWorkbooks = data['MinTotalWorkbooks']
# @Parameter ProfitMathWorkbook @Def: Profit per math workbook @Shape: [] 
ProfitMathWorkbook = data['ProfitMathWorkbook']
# @Parameter ProfitEnglishWorkbook @Def: Profit per English workbook @Shape: [] 
ProfitEnglishWorkbook = data['ProfitEnglishWorkbook']

# Variables 
# @Variable QuantityMathWorkbooks @Def: The number of math workbooks produced @Shape: [] 
QuantityMathWorkbooks = model.addVar(vtype=GRB.CONTINUOUS, lb=MinMathWorkbooks, ub=MaxMathWorkbooks, name="QuantityMathWorkbooks")
# @Variable QuantityEnglishWorkbooks @Def: The number of English workbooks produced @Shape: [] 
QuantityEnglishWorkbooks = model.addVar(lb=MinEnglishWorkbooks, ub=MaxEnglishWorkbooks, vtype=GRB.CONTINUOUS, name="QuantityEnglishWorkbooks")

# Constraints 
# @Constraint Constr_1 @Def: The number of math workbooks produced must be at least MinMathWorkbooks.
model.addConstr(QuantityMathWorkbooks >= MinMathWorkbooks)
# @Constraint Constr_2 @Def: The number of English workbooks produced must be at least MinEnglishWorkbooks.
model.addConstr(QuantityEnglishWorkbooks >= MinEnglishWorkbooks)
# @Constraint Constr_3 @Def: The number of math workbooks produced must not exceed MaxMathWorkbooks.
model.addConstr(QuantityMathWorkbooks <= MaxMathWorkbooks)
# @Constraint Constr_4 @Def: The number of English workbooks produced must not exceed MaxEnglishWorkbooks.
model.addConstr(QuantityEnglishWorkbooks <= MaxEnglishWorkbooks)
# @Constraint Constr_5 @Def: The total number of workbooks produced must be at least MinTotalWorkbooks.
model.addConstr(QuantityMathWorkbooks + QuantityEnglishWorkbooks >= MinTotalWorkbooks, "TotalWorkbooks")

# Objective 
# @Objective Objective @Def: Total profit is calculated as ProfitMathWorkbook multiplied by the number of math workbooks plus ProfitEnglishWorkbook multiplied by the number of English workbooks. The objective is to maximize the total profit.
model.setObjective(ProfitMathWorkbook * QuantityMathWorkbooks + ProfitEnglishWorkbook * QuantityEnglishWorkbooks, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['QuantityMathWorkbooks'] = QuantityMathWorkbooks.x
variables['QuantityEnglishWorkbooks'] = QuantityEnglishWorkbooks.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
