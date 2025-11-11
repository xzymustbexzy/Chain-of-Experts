# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of cheesecake slices and caramel cake slices to maximize
the total sugar consumed, where each cheesecake slice provides SugarCheesecake
grams of sugar and each caramel cake slice provides SugarCaramelCake grams of
sugar. Ensure that the total calories from cheesecake and caramel cake do not
exceed MaxTotalCalories, that the number of cheesecake slices is at least
MinCheesecakeToCaramelRatio times the number of caramel cake slices, and that
the number of caramel cake slices is at least MinCaramelSlices.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/124/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter CaloriesCheesecake @Def: Calories per slice of cheesecake @Shape: [] 
CaloriesCheesecake = data['CaloriesCheesecake']
# @Parameter SugarCheesecake @Def: Sugar per slice of cheesecake @Shape: [] 
SugarCheesecake = data['SugarCheesecake']
# @Parameter CaloriesCaramelCake @Def: Calories per slice of caramel cake @Shape: [] 
CaloriesCaramelCake = data['CaloriesCaramelCake']
# @Parameter SugarCaramelCake @Def: Sugar per slice of caramel cake @Shape: [] 
SugarCaramelCake = data['SugarCaramelCake']
# @Parameter MinCheesecakeToCaramelRatio @Def: Minimum ratio of cheesecake slices to caramel cake slices @Shape: [] 
MinCheesecakeToCaramelRatio = data['MinCheesecakeToCaramelRatio']
# @Parameter MinCaramelSlices @Def: Minimum number of caramel cake slices @Shape: [] 
MinCaramelSlices = data['MinCaramelSlices']
# @Parameter MaxTotalCalories @Def: Maximum total calories that can be consumed in one day @Shape: [] 
MaxTotalCalories = data['MaxTotalCalories']

# Variables 
# @Variable CheesecakeSlices @Def: The number of slices of cheesecake @Shape: [] 
CheesecakeSlices = model.addVar(vtype=GRB.INTEGER, name="CheesecakeSlices")
# @Variable CaramelCakeSlices @Def: The number of slices of caramel cake @Shape: [] 
CaramelCakeSlices = model.addVar(vtype=GRB.INTEGER, name="CaramelCakeSlices")

# Constraints 
# @Constraint Constr_1 @Def: The total calories from cheesecake and caramel cake do not exceed MaxTotalCalories
model.addConstr(CheesecakeSlices * CaloriesCheesecake + CaramelCakeSlices * CaloriesCaramelCake <= MaxTotalCalories)
# @Constraint Constr_2 @Def: The number of cheesecake slices is at least MinCheesecakeToCaramelRatio times the number of caramel cake slices
model.addConstr(CheesecakeSlices >= MinCheesecakeToCaramelRatio * CaramelCakeSlices)
# @Constraint Constr_3 @Def: The number of caramel cake slices is at least MinCaramelSlices
model.addConstr(CaramelCakeSlices >= MinCaramelSlices)

# Objective 
# @Objective Objective @Def: Maximize the total sugar consumed, where each cheesecake slice provides SugarCheesecake grams of sugar and each caramel cake slice provides SugarCaramelCake grams of sugar
model.setObjective(SugarCheesecake * CheesecakeSlices + SugarCaramelCake * CaramelCakeSlices, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['CheesecakeSlices'] = CheesecakeSlices.x
variables['CaramelCakeSlices'] = CaramelCakeSlices.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
