from pulp import *

def farm_planning(Yield, Price, AmountInBundle, LandAvailable, BP_land, FractionOccupiesLand, LaborRequired, 
                  AnnualWageRateFamilyLabor, AnnualWageRatePermanentLabor, HourlyWageRateTemporaryLabor,  
                  WorkingHours, FamilyLaborAvailable, AnnualAmountOfWaterAvailable, WaterLimit, WaterRequirement, 
                  PriceOfWater):

    Crops = range(len(Yield))
    Months = range(len(WorkingHours))
    ConsumptionBundles = range(len(AmountInBundle[0]))
    
    m = LpProblem("FarmPlanning", LpMaximize)
    
    AmountPlanted = LpVariable.dicts("AmountPlanted", Crops, 0)
    PermanentLaborHired = LpVariable("PermanentLaborHired", 0)
    TemporaryLaborHired = LpVariable.dicts("TemporaryLaborHired", Months, 0)
    Sales = LpVariable.dicts("Sales", Crops, 0)
    FractionConsumed = LpVariable.dicts("FractionConsumed", ConsumptionBundles, 0, 1)

    m += lpSum([Price[c] * Sales[c] for c in Crops] 
               - AnnualWageRateFamilyLabor * FamilyLaborAvailable 
               - AnnualWageRatePermanentLabor * PermanentLaborHired 
               - lpSum([HourlyWageRateTemporaryLabor * TemporaryLaborHired[t] for t in Months])
               - lpSum([PriceOfWater * WaterRequirement[t][c] * AmountPlanted[c] for t in Months for c in Crops]) ) 

    for t in Months:
        m += lpSum([FractionOccupiesLand[t][c] * AmountPlanted[c] for c in Crops]) <= LandAvailable 
        m += lpSum([LaborRequired[t][c] * AmountPlanted[c] for c in Crops]) <= WorkingHours[t] * (FamilyLaborAvailable + PermanentLaborHired) + TemporaryLaborHired[t]
        m += lpSum([WaterRequirement[t][c] * AmountPlanted[c] for c in Crops]) <= WaterLimit[t]

    m += lpSum([WaterRequirement[t][c] * AmountPlanted[c] for t in Months for c in Crops]) <= AnnualAmountOfWaterAvailable  

    for c in Crops:
        m += Yield[c] * AmountPlanted[c] == lpSum([AmountInBundle[c][b] * FractionConsumed[b] for b in ConsumptionBundles]) + Sales[c]

    m += lpSum([FractionConsumed[b] for b in ConsumptionBundles]) == 1
    
    m.solve()
    
    max_farm_earnings = value(m.objective)
    
    return max_farm_earnings