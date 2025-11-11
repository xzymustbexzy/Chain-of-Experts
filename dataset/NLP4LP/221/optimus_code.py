# Code automatically generated from OptiMUS

# Problem type: MIP        
# Problem description
'''
Determine the number of circular tables and rectangular tables to set up, where
each circular table accommodates PosterBoardsPerCircularTable poster boards and
ParticipantsPerCircularTable participants, thereby catering to
GuestsPerCircularTable guests, and occupies SpacePerCircularTable space units.
Each rectangular table accommodates PosterBoardsPerRectangularTable poster
boards and ParticipantsPerRectangularTable participants, thereby catering to
GuestsPerRectangularTable guests, and occupies SpacePerRectangularTable space
units. The total number of participants must be at least MinimumParticipants,
the total number of poster boards must be at least MinimumPosterBoards, and the
total space used must not exceed AvailableSpace. The objective is to maximize
the number of catered guests.
'''
# Import necessary libraries
import json
from gurobipy import *
     
# Create a new model
model = Model()

# Load data 
with open("/Users/gaowenzhi/Desktop/optimus-OR-paper/data/new_dataset/sample_datasets/222/parameters.json", "r") as f:
    data = json.load(f)
    
# @Def: definition of a target
# @Shape: shape of a target
        
# Parameters 
# @Parameter PosterBoardsPerCircularTable @Def: Number of poster boards per circular table @Shape: [] 
PosterBoardsPerCircularTable = data['PosterBoardsPerCircularTable']
# @Parameter ParticipantsPerCircularTable @Def: Number of participants per circular table @Shape: [] 
ParticipantsPerCircularTable = data['ParticipantsPerCircularTable']
# @Parameter GuestsPerCircularTable @Def: Number of guests catered per circular table @Shape: [] 
GuestsPerCircularTable = data['GuestsPerCircularTable']
# @Parameter SpacePerCircularTable @Def: Space units taken by one circular table @Shape: [] 
SpacePerCircularTable = data['SpacePerCircularTable']
# @Parameter PosterBoardsPerRectangularTable @Def: Number of poster boards per rectangular table @Shape: [] 
PosterBoardsPerRectangularTable = data['PosterBoardsPerRectangularTable']
# @Parameter ParticipantsPerRectangularTable @Def: Number of participants per rectangular table @Shape: [] 
ParticipantsPerRectangularTable = data['ParticipantsPerRectangularTable']
# @Parameter GuestsPerRectangularTable @Def: Number of guests catered per rectangular table @Shape: [] 
GuestsPerRectangularTable = data['GuestsPerRectangularTable']
# @Parameter SpacePerRectangularTable @Def: Space units taken by one rectangular table @Shape: [] 
SpacePerRectangularTable = data['SpacePerRectangularTable']
# @Parameter MinimumParticipants @Def: Minimum number of participants to be accommodated @Shape: [] 
MinimumParticipants = data['MinimumParticipants']
# @Parameter MinimumPosterBoards @Def: Minimum number of poster boards to be accommodated @Shape: [] 
MinimumPosterBoards = data['MinimumPosterBoards']
# @Parameter AvailableSpace @Def: Total available space units @Shape: [] 
AvailableSpace = data['AvailableSpace']

# Variables 
# @Variable CircularTables @Def: The number of circular tables @Shape: ['integer'] 
CircularTables = model.addVar(vtype=GRB.INTEGER, name="CircularTables")
# @Variable RectangularTables @Def: The number of rectangular tables @Shape: ['integer'] 
RectangularTables = model.addVar(vtype=GRB.INTEGER, name="RectangularTables")

# Constraints 
# @Constraint Constr_1 @Def: The total number of participants from circular and rectangular tables must be at least MinimumParticipants.
model.addConstr(ParticipantsPerCircularTable * CircularTables + ParticipantsPerRectangularTable * RectangularTables >= MinimumParticipants)
# @Constraint Constr_2 @Def: The total number of poster boards from circular and rectangular tables must be at least MinimumPosterBoards.
model.addConstr(PosterBoardsPerCircularTable * CircularTables + PosterBoardsPerRectangularTable * RectangularTables >= MinimumPosterBoards)
# @Constraint Constr_3 @Def: The total space used by circular and rectangular tables must not exceed AvailableSpace.
model.addConstr(SpacePerCircularTable * CircularTables + SpacePerRectangularTable * RectangularTables <= AvailableSpace)

# Objective 
# @Objective Objective @Def: The total number of catered guests is the sum of guests from circular and rectangular tables. The objective is to maximize the number of catered guests.
model.setObjective(GuestsPerCircularTable * CircularTables + GuestsPerRectangularTable * RectangularTables, GRB.MAXIMIZE)

# Solve 
model.optimize()

# Extract solution 
solution = {}
variables = {}
objective = []
variables['CircularTables'] = CircularTables.x
variables['RectangularTables'] = RectangularTables.x
solution['variables'] = variables
solution['objective'] = model.objVal
with open('solution.json', 'w') as f:
    json.dump(solution, f, indent=4)
