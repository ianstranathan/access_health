
import aliasing_corrections as aliases
# -- path imports (file write) # -- func imports
import parsing
import filters
import access_health as AH


"""
Collection of general, utility functions that are useful for the similar style parsing that keeps coming up
They should be able to take in a unique modifier func to suit the particular collation
"""

def generic_key_client_columns() -> list:
    return ["Income",        "People In Household", "First",               "Last",            "Client Id", "Client Created Date",
            "Referral Date", "Referral In-detail", "Enrollment Date",     "Enrollment Status",   "Discharged Date", "Program",   "Race",
            "Zip Code",      "Funder", "Ethnicity", "Gender", "Age", "Coordinator", "Client Type", "Education"]


"""
Ohio state university wants the following categories:
"""
def thrive_key_client_columns() -> list:
    return ["Client Id", "First", "Last", "Dob", "Gender", "Phone Number", "Telephone Contact", "Telephone Other", "Zip Code", "Ethnicity", "Race", "Age", "Program", "Client Type", "Enrollment Date",     "Enrollment Status",   "Discharged Date"]


"""
Aliases can always be called with col name as snake case
"""
def checklist_parse(date_range: tuple, file_name: str, filter_func: callable, additional_parse_type=None, **kwargs) -> dict:   

    if additional_parse_type:
        assert (additional_parse_type in aliases.get_allowable_aliases_funcs()), "aliases type not found, see aliasing_correction.py for allowed args"

    def col_interface() -> dict:
        if additional_parse_type:
            # print( file_name)
            # print( additional_parse_type)
            # print(aliases.get_alias_func(additional_parse_type)(file_name))
            return dict(aliases.get_alias_func("base")(file_name), **(aliases.get_alias_func(additional_parse_type)(file_name)))
        return aliases.get_alias_func("base")(file_name)


    # -- additional columns:
    column_names_to_check = list(col_interface().values()) + ["Medications"]
    if additional_parse_type == "health_self_rate":
        column_names_to_check += ["Health Self Rate Number"]

    # --------------------------------------------------
    if "track_appointment_hours" in kwargs:
        column_names_to_check += ["Apointment Time in Hours"]  
    elif "track_file_name" in kwargs:
        column_names_to_check += ["File Name"]
    elif "western" in kwargs:      
        column_names_to_check += ["Western Stark"]
        

    # -- 
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(date_range, client, entry_struct):
            for column_name in entry_struct["data_struct"]:
                if column_name == "File Name":
                    entry_struct["data_struct"][column_name].append( file_name )
                elif column_name == "Health Self Rate Number":
                    entry_struct["data_struct"][column_name].append( AH.self_rate_scale( client[entry_struct["col_names"]["health_self_rate"]] ))
                elif column_name == "Apointment Time in Hours":
                    """
                    initial -> 2 hours
                    monthly -> 1 hour
                    """
                    start_time = client[entry_struct["col_names"]["start_time"]]
                    end_time   = client[entry_struct["col_names"]["end_time"]]
                    total_time = 0.0
                    if parsing.is_valid_str(start_time) and parsing.is_valid_str(end_time):
                        appt_time = 0
                        try:
                            appt_time = parsing.delta_time_in_hours_12_hour_basis(client[entry_struct["col_names"]["start_time"]],
                                                                                  client[entry_struct["col_names"]["end_time"]])
                        except ValueError:
                            appt_time = 2.0 if "init" in file_name else 1.0
                        
                        total_time += appt_time
                    else:
                        total_time += 2.0 if "init" in file_name else 1.0
                        
                    entry_struct["data_struct"][column_name].append( total_time )
                elif column_name == "Western Stark":
                    if client["Zip Code"] in parsing.western_stark_zips_codes:
                        entry_struct["data_struct"][column_name].append( "Y" )
                    else:
                        entry_struct["data_struct"][column_name].append( "N" )
                else:
                    entry_struct["data_struct"][column_name].append( client[ column_name] )

    entry_struct = {"files":            [file_name],
                    "parsing_function": parse,
                    "col_function":     col_interface,
                    "data_struct":      parsing.data_struct( column_names_to_check )
                    }

    data_struct = parsing.parsing_loop( entry_struct )
    
    if "write_name" in kwargs:
        parsing.write_direct_data_struct_to_excel(data_struct, kwargs["write_name"], date_range)
        
    return data_struct
    
    

def client_key_info_parse(date_range: tuple,
                          filter_func: callable, 
                          additional_columns_to_check: list = None,
                          **kwargs) -> dict:

    column_names_to_check = generic_key_client_columns()

    # -- (03.11.23) Thrive columns change
    if "OSU" in kwargs:
        column_names_to_check = thrive_key_client_columns()

    if additional_columns_to_check:
        column_names_to_check += additional_columns_to_check
    
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(client, date_range, file_name):
            for column_name in entry_struct["data_struct"]:
                if column_name == "FPL":
                    entry_struct["data_struct"][column_name].append(AH.federal_poverty_level( AH.clean_income(client),
                                                                                              AH.clean_people_in_household(client),
                                                                                              date_range[0]))
                elif column_name == "Time in Program":
                    entry_struct["data_struct"][column_name].append( parsing.time_in_program( client, date_range ))
                else:
                    entry_struct["data_struct"][column_name].append( client[ column_name] )

    entry_struct = {"files":            ["client_key_information.csv"] if "file_name" not in kwargs else [ kwargs["file_name"] ], # -- client key info changes over time and sometimes I'd like to use an older version
                    "parsing_function": parse,
                    "data_struct":      parsing.data_struct( column_names_to_check  )
                    }
    
    data_struct = parsing.parsing_loop( entry_struct )

    if "write_name" in kwargs:
        parsing.write_direct_data_struct_to_excel(data_struct, kwargs["write_name"], date_range)

    return data_struct

def one_off_generic_parse(date_range: tuple,
                           f: str,
                           filter_func: callable, 
                           column_names_to_check: list,
                           **kwargs) -> dict:

    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(client, date_range, file_name):
            for column_name in entry_struct["data_struct"]:
                if column_name == "File Name":
                    entry_struct["data_struct"][column_name].append( file_name )
                else:
                    entry_struct["data_struct"][column_name].append( client[ column_name] )

    entry_struct = {"files":            [f],
                    "parsing_function": parse,
                    "data_struct":      parsing.data_struct( column_names_to_check )
                    }
    
    data_struct = parsing.parsing_loop( entry_struct )

    if "write_name" in kwargs:
        parsing.write_direct_data_struct_to_excel(data_struct, kwargs["write_name"], date_range)

    return data_struct




def initial_self_health( date_range: tuple, file_name: str, **kwargs) -> dict:

    def col_interface() -> dict:
        return dict( aliases.base(file_name), **aliases.health_self_rates( file_name))
    
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filters.checklist_start_date_on_interval_filter( date_range, client, entry_struct):
            # -- update data struct to compare against the monthly files
            self_health_rating_integer = AH.self_rate_scale( client[ entry_struct["col_names"]["health_self_rate"]] )
            entry_struct["data_struct"][ client[ entry_struct["col_names"]["client_id"]]] = self_health_rating_integer

            for column_name in entry_struct["write_struct"]:
                if column_name == "Client Id":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["client_id"]] )
                elif column_name == "File Name":
                    entry_struct["write_struct"][column_name].append( file_name )
                elif column_name == "Start Date":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["start_date"]] )
                elif column_name == "Self-Health Rating":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["health_self_rate"]] )
                elif column_name == "Self-Health Integer":
                    entry_struct["write_struct"][column_name].append( self_health_rating_integer )
                    
    entry_struct = {"files":            [file_name],
                    "parsing_function": parse,
                    "col_function":     col_interface,
                    "data_struct":      {},
                    "write_struct":     parsing.data_struct( ["Client Id", "File Name", "Start Date", "Self-Health Rating", "Self-Health Integer"] )}
    
    data_struct = parsing.parsing_loop( entry_struct, entire_entry_struct=True)
    
    if "write_name" in kwargs:
        parsing.write_direct_data_struct_to_excel( entry_struct["write_struct"],
                                                   kwargs["write_name"], date_range )
        
    return data_struct["data_struct"] # -- return the dictionary of client ids: health self ratings

def self_health_rate( t: str, date_range: tuple):
    assert t in ["Adult", "Maternal", "Pregnancy"]
    
    initial_clients = {}
    file_name = ""
    match t:
        case "Adult":
            file_name = "adult_checklist.csv"
            initial_clients = initial_self_health( date_range, "initial_adult_checklist.csv", write_name="Initial Adult Clients Self Health Rating ")
        case "Maternal":
            file_name = "maternal_checklist.csv"
            initial_clients = initial_self_health( date_range, "initial_maternal_checklist.csv", write_name="Initial Maternal Clients Self Health Rating ")
        case "Pregnancy":
            file_name = "pregnancy_checklist.csv"
            initial_clients = initial_self_health( date_range, "initial_pregnancy_checklist.csv", write_name="Initial Pregnancy Clients Self Health Rating ")

    def col_interface() -> dict:
        return dict( aliases.base(file_name), **aliases.health_self_rates( file_name))
    
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        # -- if the client is in the initial client ids
        if client[ entry_struct["col_names"]["client_id"]] in initial_clients and filters.checklist_start_date_on_interval_filter( date_range, client, entry_struct):
            # -- write a simple parse to file as a record
            for column_name in entry_struct["write_struct"]:
                if column_name == "Client Id":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["client_id"]] )
                elif column_name == "File Name":
                    entry_struct["write_struct"][column_name].append( file_name )
                elif column_name == "Start Date":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["start_date"]] )
                elif column_name == "Self-Health Rating":
                    entry_struct["write_struct"][column_name].append( client[ entry_struct["col_names"]["health_self_rate"]] )
                elif column_name == "Self-Health Integer":
                    entry_struct["write_struct"][column_name].append(  AH.self_rate_scale( client[ entry_struct["col_names"]["health_self_rate"]] ))

            # -- if the id is seen for first time, make an arr with health-self-rating value
            if client[ entry_struct["col_names"]["client_id"]] not in entry_struct[ "health_self_rating_average_struct"]:
                # -- save self health rating in array
                entry_struct[ "health_self_rating_average_struct"][ client[ entry_struct["col_names"]["client_id"]]] = [
                    AH.self_rate_scale( client[ entry_struct["col_names"]["health_self_rate"]]) ]
            # -- otherwise, add it to the list for later averaging
            else:
                entry_struct[ "health_self_rating_average_struct"][ client[ entry_struct["col_names"]["client_id"]]].append( AH.self_rate_scale( client[ entry_struct["col_names"]["health_self_rate"]]))
                
    entry_struct = {"files":            [file_name],
                    "parsing_function": parse,
                    "col_function":     col_interface,
                    "health_self_rating_average_struct": {},
                    "write_struct": parsing.data_struct( ["Client Id", "File Name", "Start Date", "Self-Health Rating", "Self-Health Integer"] )}

    
    data_struct = parsing.parsing_loop( entry_struct, entire_entry_struct=True)

    avg = lambda x: round( (sum(x) / len(x)), 2)
    # -- write file with pairs
    parsing.write_direct_data_struct_to_excel( {"Client Id": list( data_struct["health_self_rating_average_struct"].keys()),
                                                "Self-Health Rating Average Difference": [ avg( data_struct["health_self_rating_average_struct"][x]) - float(initial_clients[x])
                                                                                           for x in data_struct["health_self_rating_average_struct"]]},
                                                "Average Self-Health Rating Difference ",
                                                date_range )
    
    # -- write simple parse for record
    parsing.write_direct_data_struct_to_excel( entry_struct["write_struct"],
                                               "Matching monthly clients to initial clients Raw", date_range )

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
"""
# base_funcs.client_key_info_parse( date_range, filters.chronic_enrolled_on_time_interval, write_name="Enrolled On Interval ")
"""

def pathway_opened_or_closed(date_range: tuple, file_name: str, open_close: str, **kwargs) -> None | dict:
    additional_filter_func = kwargs["filter_func"] if "filter_func" in kwargs else None
    """
    :param tupe date_range:   The date you're looking on in mm/dd/yyyy format
    :param str  file_name:    The pathway you're wanting to process, must end in .csv or .xlsx; e.g. "education.csv"
    :param str   open_close:  [open/ opened / Open/ Opened/ OPEN/ OPENED/ ... close/ closed / ... /CLOSED]; are you looking for the pathways opened or closed
    :param kwargs:            Write or use as data structure return
                              "filter_func" if the particular report requires additional filtering (e.g. Aultman needs to know about being an aultman client)
    """

    assert (open_close in ["opened", "closed"]), "opened/ closed distinction not made, must be ['opened' or 'closed']"
    
    cols_to_look_at = ["Client Id", "Start Date", "Completed Date", "Completed Status", "Zip Code", "Referral In-Detail", "Program", "Funder", "Race Detail", "Ethnicity", "Enroll Date", ]
    
    # --------------------------------------------------
    # -- Account for pathway specific metrics / naming conventions
    # --------------------------------------------------

    # cols_to_look_at = ["Race Detail" if x=="Race" else x for x in cols_to_look_at]
    match file_name:
        
        case "pw_social_service_referral.csv":
            cols_to_look_at += ["Service", "Pw Referral Name"]
        case "pw_pregnancy.csv":
            #cols_to_look_at = list(map(lambda x: x.replace('Pant', 'Ishan'), cols_to_look_at))
            cols_to_look_at = ["Client" if x=="Client Id" else x for x in cols_to_look_at]
            cols_to_look_at = ["Race" if x=="Race Detail" else x for x in cols_to_look_at]
            cols_to_look_at += ["Birth Type", "Birth Weight Grams", "Gestation Age", "Trimester At Enrollment"]
            
        case "pw_immunization_referral.csv":
            #cols_to_look_at = list(map(lambda x: x.replace('Pant', 'Ishan'), cols_to_look_at))
            cols_to_look_at = ["Client" if x=="Client Id" else x for x in cols_to_look_at]
            cols_to_look_at = ["Race" if x=="Race Detail" else x for x in cols_to_look_at]
            
        case "pw_medical_referral.csv":
            cols_to_look_at += ["Referral"]
            
        case "pw_education.csv":
            cols_to_look_at += ["Other Module", "Module", "Section"]
        case "pw_medication_assessment.csv":
            cols_to_look_at += ["MAC Prob Getting Medication", "MAC Prob Paying Medication", "MAC Having Side Effects", "MAC More Than One Pharmacy"]
            
            
    def correct_date_str(s: str) -> str:
        return "Start Date" if s == "opened" else "Completed Date"

    
    def completed_func(client: dict):
        if open_close == "opened":
            return True
        if file_name in ["pw_health_insurance.csv", "pw_pregnancy.csv"]:
            match file_name:
                case "pw_health_insurance.csv":
                    return client["Completed Status"] == "Complete-Insured"
                
        #return client["Completed Status"] == "Completed"
        return ("Completed" in client["Completed Status"])

    def append_struct_data(client: dict, entry_struct: dict) -> None:
        for column_name in entry_struct["data_struct"]:
            if column_name == "Referral In-Detail":
                ref_in_detail = "Referral In-Detail" if "Referral In-Detail" in client else "Referral In-detail"
                entry_struct["data_struct"][column_name].append( client[ ref_in_detail] )
            else:
                entry_struct["data_struct"][column_name].append( client[ column_name] )


    def parse(client: dict, _file_name: str, entry_struct: dict) -> None:
        # -- if opened: we care if the start date is on the time interval
        # -- if closed: we care if the close date is on the time interval && the completed status == "Completed" (or whatever that file is)
        if entry_struct["filter_func"]:
            if (entry_struct["filter_func"](client)
                and parsing.on_time_interval(date_range, client[ correct_date_str(open_close) ])
                and completed_func( client)):
                append_struct_data( client, entry_struct )
        else:
            if (parsing.on_time_interval(date_range, client[ correct_date_str(open_close) ])
                and completed_func( client)):
                append_struct_data( client, entry_struct)

        
    entry_struct = {"files":            [file_name],
                    "parsing_function": parse,
                    "data_struct":      parsing.data_struct( cols_to_look_at ),
                    "filter_func":      kwargs["filter_func"] if "filter_func" in kwargs else None}
    
    ret_or_write_struct = parsing.parsing_loop( entry_struct )

    if "write" in kwargs and kwargs["write"]:
        parsing.write_direct_data_struct_to_excel( ret_or_write_struct, f"{file_name } {open_close} " , date_range)
        print("++++++++++  Writing now ++++++++++")
              
    if "ret" in kwargs and kwargs["ret"]:
        print("++++++++++  Returning now ++++++++++")
        return ret_or_write_struct

    
def pathways_ratio(date_range: tuple, file_name: str, write_name: str, **kwargs):

    opened = ( pathway_opened_or_closed( date_range, file_name, "opened", ret=True, filter_func=kwargs["filter_func"])
               if "filter_func" in kwargs
               else pathway_opened_or_closed( date_range, file_name, "opened", ret=True) )

    closed = ( pathway_opened_or_closed( date_range, file_name, "closed", ret=True, filter_func=kwargs["filter_func"])
               if "filter_func" in kwargs
               else pathway_opened_or_closed( date_range, file_name, "closed", ret=True) )
    
    opened = parsing.remove_exactly_repeating_clients(opened)
    closed = parsing.remove_exactly_repeating_clients(closed)
    
    parsing.write_multiple_sheets_direct_data_struct([opened, closed],
                                                     ["opened", "closed"],
                                                     f"{write_name} ",
                                                     date_range)
