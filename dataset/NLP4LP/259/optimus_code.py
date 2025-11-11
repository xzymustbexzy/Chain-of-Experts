# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
A woman must consume two types of meal preps: Smoothies and Protein Bars. Each
Smoothie provides ProteinPerSmoothie units of protein and CaloriesPerSmoothie
calories. Each Protein Bar provides ProteinPerBar units of protein and
CaloriesPerBar calories. The number of Protein Bars consumed must be
BarToSmoothieRatio times the number of Smoothies. The total calorie intake must
not exceed MaxCalories. Determine the quantities of Smoothies and Protein Bars
to maximize total protein intake.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/260/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter ProteinPerSmoothie @Def: Amount of protein per smoothie @Shape: [] 
ProteinPerSmoothie = data['ProteinPerSmoothie']
# @Parameter CaloriesPerSmoothie @Def: Amount of calories per smoothie @Shape: [] 
CaloriesPerSmoothie = data['CaloriesPerSmoothie']
# @Parameter ProteinPerBar @Def: Amount of protein per protein bar @Shape: [] 
ProteinPerBar = data['ProteinPerBar']
# @Parameter CaloriesPerBar @Def: Amount of calories per protein bar @Shape: [] 
CaloriesPerBar = data['CaloriesPerBar']
# @Parameter BarToSmoothieRatio @Def: Ratio of protein bars to smoothies @Shape: [] 
BarToSmoothieRatio = data['BarToSmoothieRatio']
# @Parameter MaxCalories @Def: Maximum allowable total calories @Shape: [] 
MaxCalories = data['MaxCalories']

# Variables 
# @Variable NumberSmoothies @Def: The number of smoothies selected @Shape: [] 
NumberSmoothies = model.addVar(vtype=GRB.INTEGER, name="NumberSmoothies")
# @Variable NumberProteinBars @Def: The number of protein bars selected @Shape: [] 
NumberProteinBars = model.addVar(vtype=GRB.INTEGER, name="NumberProteinBars")

# Constraints 
# @Constraint Constr_1 @Def: The total calorie intake from Smoothies and Protein Bars must not exceed MaxCalories.
model.addConstr(CaloriesPerSmoothie * NumberSmoothies + CaloriesPerBar * NumberProteinBars <= MaxCalories)
# @Constraint Constr_2 @Def: The number of Protein Bars consumed must be BarToSmoothieRatio times the number of Smoothies.
model.addConstr(NumberProteinBars == BarToSmoothieRatio * NumberSmoothies)

# Objective 
# @Objective Objective @Def: Maximize the total protein intake, which is the sum of the protein from Smoothies and Protein Bars.
model.setObjective(ProteinPerSmoothie * NumberSmoothies + ProteinPerBar * NumberProteinBars, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['NumberSmoothies'] = NumberSmoothies.x
variables['NumberProteinBars'] = NumberProteinBars.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
