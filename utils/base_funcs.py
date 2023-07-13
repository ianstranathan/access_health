
import aliasing_corrections as aliases
# -- path imports (file write) # -- func imports
import parsing



"""
Collection of general, utility functions that are useful for the similar style parsing that keeps coming up
They should be able to take in a unique modifier func to suit the particular collation
"""

def generic_key_client_columns() -> list:
    return ["Income",        "People In Household", "First",               "Last",            "Client Id", "Client Created Date",
            "Referral Date", "Enrollment Date",     "Enrollment Status",   "Discharged Date", "Program",   "Race",
            "Zip Code",      "Funder", "Ethnicity", "Gender", "Age"]

# def parse(date_range: tuple,
#           filter_func: callable,
#           client: dict,
#           file_name: str,
#           entry_struct: dict, **kwargs): 
#     if filter_func(date_range, client, file_name, entry_struct):
#         for column_name in entry_struct["data_struct"]:
#             if "track_file_name" in kwargs:
#                 (entry_struct["data_struct"][column_name].append( file_name )
#                  if column_name == "File Name"
#                  else entry_struct["data_struct"][column_name].append( client[ column_name] ))
#             else:
#                 entry_struct["data_struct"][column_name].append( client[ column_name] )


"""
Aliases can always be called with col name as snake case
"""
def checklist_parse(date_range: tuple, file_name: str, filter_func: callable, additional_parse_type=None, **kwargs) -> dict:   
    
    assert (additional_parse_type in aliases.get_allowable_aliases_funcs()), "aliases type not found, see aliasing_correction.py for allowed args"

    def col_interface() -> dict:
        if additional_parse_type:
            return dict(aliases.get_alias_func("base")(file_name), **aliases.get_alias_func(additional_parse_type)(file_name))
        return aliases.get_alias_func("base")(file_name)

    column_names_to_check = list(col_interface().values()) if not "track_file_name" else list(col_interface().values()) + ["File Name"]
    
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(date_range, client, file_name, entry_struct):
            for column_name in entry_struct["data_struct"]:
                if column_name == "File Name":
                    entry_struct["data_struct"][column_name].append( file_name )
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

    column_names_to_check = generic_key_client_columns() + additional_columns_to_check if additional_columns_to_check else generic_key_client_columns()
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(date_range, client, file_name):
            for column_name in entry_struct["data_struct"]:
                entry_struct["data_struct"][column_name].append( client[ column_name] )

    entry_struct = {"files":            ["client_key_information.csv"],
                    "parsing_function": parse,
                    "data_struct":      parsing.data_struct( column_names_to_check )
                    }
    
    data_struct = parsing.parsing_loop( entry_struct )

    if "write_name" in kwargs:
        parsing.write_direct_data_struct_to_excel(data_struct, kwargs["write_name"], date_range)

    return data_struct

def one_off_generic_parsse(date_range: tuple,
                           f: str,
                           filter_func: callable, 
                           column_names_to_check: list,
                           **kwargs) -> dict:

    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if filter_func(date_range, client, file_name):
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
