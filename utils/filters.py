import parsing

def is_chronic_client(client: dict, date_range=None, file_name=None) -> bool:
    if "Program" in client:
        return (parsing.is_valid_str(client["Program"]) and ("Chronic" in client["Program"] or "CHRONIC" in client["Program"]))
    return False

def is_pregnant_client(client: dict, date_range=None, file_name=None) -> bool:
    if "Program" in client:
        return (parsing.is_valid_str(client["Program"]) and ("Pregnant" in client["Program"] or "PREGNANT" in client["Program"]))
    return False

# ----------------------------------------------------------------------------------------------------

def checklist_start_date_on_interval_filter(date_range: tuple, client: dict,  entry_struct: dict) -> bool:
    if parsing.on_time_interval(date_range, client[ entry_struct["col_names"]["start_date"]]):
        return True
    return False

def checklist_start_date_on_interval_filter_and_needed_meds(date_range: tuple, client: dict,  entry_struct: dict) -> bool:
    return parsing.on_time_interval(date_range, client[ entry_struct["col_names"]["start_date"]]) and client["Medications"] == "Y"

"""
See base funcs for argument signature -> doesn't need file name
"""
def served_on_interval_filter(client, date_range, file_name) -> bool:
    return parsing.enrolled_during_time_interval(date_range, client)


def enrolled_on_time_interval(client, date_range, file_name) -> bool:
    return (parsing.on_time_interval(date_range, client["Enrollment Date"])
            and client["Enrollment Status"] == "Enrolled")
    

def referred_on_time_interval(client, date_range, file_name) -> bool:
    return parsing.on_time_interval(date_range, client["Referral Date"])


# ----------------------------------------------------------------------------------------------------


def chronic_served_on_time_interval(client, date_range, file_name) -> bool:
    return (is_chronic_client( client) and served_on_interval_filter(client, date_range, file_name))


def chronic_enrolled_on_time_interval(client, date_range, file_name) -> bool:
    return (is_chronic_client( client) and enrolled_on_time_interval(client, date_range, file_name))


def chronic_referred_on_time_interval(date_range, client, file_name) -> bool:
    return (is_chronic_client( client) and referred_on_time_interval(client, date_range, file_name))


# ----------------------------------------------------------------------------------------------------


# def pregnant_served_on_time_interval(client, date_range, file_name) -> bool:
#     return (is_pregnant_client( client) and served_on_interval_filter(client, date_range, file_name))


# def pregnant_enrolled_on_time_interval(client, date_range, file_name) -> bool:
#     return (is_pregnant_client( client) and enrolled_on_time_interval(client, date_range, file_name))

def pregnant_enrolled_on_time_interval( client, date_range, file_name) -> bool:
    """
    Per conversation with Tonya: We're defining served here as either start or completed date on interval
                                 & enrolled as start date on interval
    This only works with Pregnancy Pathway file
    """
    assert file_name == "pw_pregnancy.csv", print("incorrect file used in pregnancy filter")
    return parsing.on_time_interval(date_range, client["Start Date"])


def pregnant_served_on_time_interval(client, date_range, file_name) -> bool:
    """
    Per conversation with Tonya: We're defining served here as either start or completed date on interval
                                 & enrolled as start date on interval  
    """
    return ( pregnant_enrolled_on_time_interval( client, date_range, file_name) or parsing.on_time_interval( date_range, client["Completed Date"]))
# ----------------------------------------------------------------------------------------------------


def phq9_filter_func(date_range, client, file_name) -> bool:
    is_valid_score = lambda score: (score != score or score == "" or score == "-")
    phq9_score = int(client["Phq9 Score"]) if is_valid_score(client["Phq9 Score"]) else 0
    return (parsing.enrolled_during_time_interval(date_range, client) and phq9_score >= 10)
