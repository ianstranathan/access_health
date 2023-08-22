
from math import isnan
# --------------------------------------------------
import misc
import parsing as parsing

def lee_ann_education_levels(s) -> str:
    a = "Less than high school education"
    b = "High school education"
    c = "Some post secondary education"
    d = "Bachelor’s degree and higher"

    if s != s:
        return "blank"
    elif s == "Completed 4 year degree":
        return d
    elif s == "Completed 2 year degree":
        return c
    elif s == "Completed GED":
        return b
    elif s == "Completed high school":
        return b
    elif s == "Completed post graduate (Masters, Doctorate)":
        return d
    elif s == "Completed vocational school":
        return b
    elif s == "Don't Know":
        return s
    elif s == "Less than high school education":
        return s
    elif s == "Other":
        return "N/A"
    elif s == "Refused":
        return "N/A"
    elif s == "Some college":
        return c
    elif s == "Some high school":
        return a
    else:
        return "!ahhhh" + s


def clean_people_in_household(client: dict) -> str:
    people_in_household = client["People In Household"]
    if people_in_household == "-" or (people_in_household != people_in_household): #-- NaN or "-"
        return "1"
    elif people_in_household == "10+":
        return "10"
    return str( int( people_in_household) + 1 ) # -- increment by one to accoutn for formatting errors


def clean_income(client: dict) -> str:
    income = client["Income"]
    if income == "-" or income == "Don't Know" or income != income or income == "Unknown" or income == "unknown":
        return "$0,0 - $0,0"
    return income


def self_rate_scale(s: str) -> int:
    match s:
        case "Excellent":
            return 6
        case "Very Good":
            return 5
        case "Good":
            return 4
        case "Fair":
            return 3
        case "Poor":
            return 2
        case "Very Poor":
            return 1
        case "-":
            return 0
        case _:
            return 0
        
# -----------------------------------
# -- Federal Poverty Utils
# -----------------------------------
def print_fpl_bracket_dict(data: dict, bracket_interval):
    ret = FPL_Bracket_Dict(data_struct, bracket_size)
    for zip_code in ret:
        print(zip_code)
        for key in ret[zip_code]:
            if key != "Total Count":
                print(key, ":  ", round( 100.0 * ret[zip_code][key] / ret[zip_code]["Total Count"], 2), "%")
        print("==============================")


def fpl_bracket_string(fpl: float, bracket_interval: float) -> str:
    round_to_nearest_increment = lambda x, y: y * math.floor(x / y)
    lower_bound = round_to_nearest_increment(100.0 * fpl, bracket_interval)
    upper_bound = round_to_nearest_increment(100.0 * fpl, bracket_interval) + bracket_interval
    
    return str(lower_bound) + "% to " + str(upper_bound) + "% FPL"


def fpl_bracket_dict(data: dict, bracket_interval) -> dict:
    # -- zip codes have an empty dictionary to put bracketted fpls into
    ret = {x: {"Total Count": 0} for x in data["Zip Code"]}

    for i, v in enumerate( data["Zip Code"] ):
        ret[v]["Total Count"] += 1
        fpl_bracket_string = FPL_Bracket_String( data["FPL"][i], bracket_interval)
        if fpl_bracket_string not in ret[v]:
            ret[v][fpl_bracket_string] = 1
        else:
            ret[v][fpl_bracket_string] += 1
            
    return ret    


def percentage_below_threshold(threshold: float, ls: list):
    return ( round( 100.0 * len(list (filter (lambda x: x <= threshold, ls))) / len( ls), 2))


def avg_income(income: str) -> float: # -- formats income str ( "low" - "high" ) and return avg
    if "More" in income:
        return float(income.split("$")[1].replace(',',''))
    
    income_ls  = income.split("-")
    avg = 0.0
    for val in income_ls:
        avg += float(val.strip()[1:].replace(',',''))
    return (avg / len(income_ls))


def federal_poverty_base_and_multiplier(date: str) -> dict:
    datetime_date  = misc.str_to_datetime(date)
    base: float
    multiplier: float
    match datetime_date.year:
        case "2022":
             base        = 13590.0
             multiplier  = 4720.0
        case "2021":
             base        = 12880.0
             multiplier  = 4540.0
        case "2020":
             base        = 12760.0
             multiplier  = 4480.0
        case "2019":
             base        = 12490.0
             multiplier  = 4420.0
        case _: 
             base        = 13590.0
             multiplier  = 4720.0
    return {"base": base, "multiplier": multiplier}        


def federal_poverty_level(income_str: str, family_size_str: str, date: str) -> float: # magic numbers are from federal guidlines
    family_size = float(family_size_str) if "+" not in family_size_str else float(family_size_str[0: -1])
    famiy_size  = family_size if family_size > 0.0 else 1.0 # there are inconsistencies with what constitutes as single in database(0 or 1)
    income      = avg_income(income_str)
    base_and_multiplier = federal_poverty_base_and_multiplier( date )
    return round(income / (base_and_multiplier["base"] + (famiy_size - 1) * base_and_multiplier["multiplier"]), 2)


def is_in_federal_poverty(income: float, family_size: float, date: str):
    famiy_size          = family_size if family_size > 0.0 else 1.0 # there are inconsistencies with what constitutes as single in database(0 or 1)
    base_and_multiplier = federal_poverty_base_and_multiplier( date )
    return True if (income - base_and_multiplier["base"]) / base_and_multiplier["multiplier"] <= (famiy_size - 1) else False


def test_fpl( func: callable):
    incomes      = [13590, 18310, 23030, 25268, 27750, 	32470, 37190, 41910, 46630]
    dates        = ["1/1/2022" for x in incomes]

    assert(func == Federal_Poverty_Level or func == Is_In_Federal_Poverty)
    print(incomes)
    for family_size in [x for x in range(1, len(incomes) + 1, 1)]:
        family_sizes = [family_size for x in incomes]
        print("family_size: ", family_size, " - ", *map(func, incomes, family_sizes, dates))

# -----------------------------------
# -- General 
# -----------------------------------
def is_chronic_client(client: dict, file_name: str) -> bool:

    if "Program" in client:
        return (parsing.is_valid_str(client["Program"]) and ("Chronic" in client["Program"] or "CHRONIC" in client["Program"]))
    
    print("In Access Health script, there was no 'Program' column found!!!!!", "", file_name)
    return False


def is_thrive_client(client: dict, file_name: str) -> bool:

    if "Program" in client:
        return (parsing.is_valid_str(client["Program"]) and ("Thrive" in client["Program"] or "CHRONIC" in client["Program"]))
    
    print("In Access Health script, there was no 'Program' column found!!!!!", "", file_name)
    return False
                
    
def rq_considered_hr_or_i(arg: str | float) -> bool:
    if arg == "Urgent":
        return True
    elif arg == "Risk-High":
        return True
    # elif arg == "Moderate High":
    #     return True
    elif arg == "Risk-Very High":
        return True
    else:
        return False


def is_current_staff(coordinator: str) -> bool:
    current_employed_chws = ["JFOGLE",   "YHERNANDEZ", "DELLIS", # case load coordinator naming convention
                             "EWILLIAMS","DDANIELS",   "DTHOMPSON",
                             "KCASTEEL", "LHARPER",    "SBECKER",
                             "RBURKES",  "BDEAN",      "BHODGE"]
    
    if len(coordinator.split(",")) > 1:    # "Baylor, Alison (ABAYLOR)"  -> ["Baylor", "Alison (ABAYLOR)"]
        abbrev = coordinator.split(",")[1] # "Alison (ABAYLOR)"
        name_to_check = abbrev[abbrev.index("(") + 1: abbrev.index(")")] # "ABAYLOR"
        return name_to_check in current_employed_chws
    
    else:
        return coordinator in current_employed_chws              
