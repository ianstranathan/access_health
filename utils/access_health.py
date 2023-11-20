from math import isnan
# --------------------------------------------------
import misc
import parsing as parsing


def clean_people_in_household(client: dict) -> str:
    people_in_household = client["People In Household"]
    # -- convention is zero for single -> increment by one if valid string, otherwise return 1
    people_in_household_is_valid = parsing.is_valid_str( people_in_household ) 

    increment_ret = lambda x: str( int( x ) + 1 )
    
    if people_in_household_is_valid:
        # -- there are occasional uses of N+
        if "+" in people_in_household:
            s = people_in_household.replace( "+", "")
            return increment_ret( s )
        else:
            increment_ret( people_in_household )
    else:
        return "1"


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
    ret = fpl_bracket_dict(data_struct, bracket_size)
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

    if "efused" in income:
        return 0.0
    
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
        case "2023":
             base        = 14,580
             multiplier  = 5140.0
             
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

    
def rq_considered_hr_or_i(arg: str | float) -> bool:
    if arg == "Urgent":
        return True
    elif arg == "Risk-High":
        return True
    elif arg == "Risk-Very High":
        return True
    else:
        return False


def is_jackson_fire( s: str) -> bool:
    return s in ["Jackson Fire",
                 "Jackson Fire Department",
                 "Jackson Fire Dept, Aultman",
                 "Jackson Fire Dept.",
                 "Jackson Township Department",
                 "Jackson Township Fire Department",
                 "Jackson Township Fire Dept",
                 "Jackson Township Fire Dept.",
                 "Jackson Twp Fire",
                 "Jackson Twp Fire Department",
                 "Jackson Twp Fire Dept",
                 "Jackson Twp."]
