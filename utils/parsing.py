
import functools
import pandas as pd
from datetime        import datetime
from os              import listdir


# ----------------------------------------------------------------------------------------------------

excel_file_src_dir  = "../CCS_Excel_File_Source/"
generated_excel_dir = "Generated_Excel_Files/"

# ----------------------------------------------------------------------------------------------------
# -- Pandas util funcs
# ----------------------------------------------------------------------------------------------------
def load_csv(fileName: str, path: str):
    return pd.read_csv(path + fileName, encoding = "ISO-8859-1")


def load_csv(fileName: str):
    return pd.read_csv(fileName, encoding = "ISO-8859-1")

def load_xlsx_sheet(xls: type[pd.io.excel._base.ExcelFile], sheetName: str) -> type[pd.core.frame.DataFrame]:
    return pd.read_excel(xls, sheetName)


def load_xlsx(fileName: str) -> type[pd.io.excel._base.ExcelFile]:
    return pd.ExcelFile(fileName)

# ----------------------------------------------------------------------------------------------------


def file_date_str(date_range: str) -> str:
    return ("-".join(date_range[0].split("/")) + "_to_" + "-".join(date_range[1].split("/")))


def filter_for_matching_client_ids(d: dict, ls: list, col:str) -> dict:
    key_list = list(d.keys())
    # print(key_list)
    # print(key_list.index(col))
    # print(ls)
    matching_clients     = list(filter( lambda x : x[key_list.index(col)] in ls, list(zip(*d.values()))))
    return { list(d.keys())[i] : list(x) for i, x in enumerate( list( zip (*matching_clients)))}


def remove_exactly_repeating_clients(d: dict) -> dict:
    tmp = { x: True for x in zip(*d.values()) } # -- remove repeating clients by making dict (unique keys)
    return { list(d.keys())[i] : list(x) for i, x in enumerate( zip(*tmp.keys()) ) } # -- python is amazing sometimes
    # -- this zips back the matching elements in the keys from tmp, then sets them as a dictionary with the corresponding original name


def data_struct(cols: list) -> dict:
    """
    cols is an array of column names that the parse function will look at
    """
    return {x: [] for x in sorted(cols)}
    
def write_direct_data_struct_to_excel(data_struct: dict, start_of_file_name: str, date_range: tuple):
    date_str = file_date_str(date_range)
    writer   = pd.ExcelWriter(generated_excel_dir + start_of_file_name + date_str + '.xlsx', engine='xlsxwriter')
    df       = pd.DataFrame({k: pd.Series(v, dtype='object') for k,v in data_struct.items()}) # -- = DataFrame(write_struct)
    df.to_excel(writer, sheet_name="parsed")
    writer.save()


def write_multiple_sheets_direct_data_struct(arr_of_data_struct: list, arr_of_sheet_namnes: list, start_of_file_name: str, date_range: tuple):
    date_str = file_date_str(date_range)
    writer   = pd.ExcelWriter(generated_excel_dir + start_of_file_name + date_str + '.xlsx', engine='xlsxwriter')
    for i, data_struct in enumerate(arr_of_data_struct):    
        df       = pd.DataFrame({k: pd.Series(v, dtype='object') for k,v in data_struct.items()}) # -- = DataFrame(write_struct)
        df.to_excel(writer, sheet_name=arr_of_sheet_namnes[i])
    writer.save()


def is_xlsx(file_name: str):
    return file_name.split(".")[1] == "xlsx"


def parsing_loop(entry_struct: dict, **kwargs):
    """
    'Templated' excel file operation to try to keep things D.R.Y
    """
    for file_name in entry_struct["files"]:
        print("-------------------------")
        print(file_name)
        print("-------------------------")
        
        if is_xlsx(file_name):
            xlsx_file = load_xlsx(excel_file_src_dir + file_name)
            for sheet_name in xlsx_file.sheet_names:
                # print("Processing", sheet_name)
                # print("-----------------------")
                df  = load_xlsx_sheet(xlsx_file, sheet_name)
                df = df.drop_duplicates(subset=None, keep="first", inplace=False)
                #df.drop_duplicates(inplace=True)
                # dfDict = df.to_dict('records')
                dfDict = df.to_dict('records')
                # if "remove_duplicates" in kwargs:
                #     dfDict = remove_exactly_repeating_clients(dfDict)
                # +++
                #entry_struct["col_names"] =  entry_struct["col_function"](file_name, dfDict[0]) if "col_function" in entry_struct else None
                entry_struct["col_names"] =  entry_struct["col_function"]() if "col_function" in entry_struct else None
                
                for client in dfDict: # note this doesn't work with my checklist aliasing
                    entry_struct["parsing_function"](client, sheet_name, entry_struct)
        else:   
            # print("checking: " + file_name)
            # print("-----------------------------")

            df     = load_csv(excel_file_src_dir + file_name)
            # df.drop_duplicates(inplace=True)
            # dfDict = df.to_dict('records')
            df = df.drop_duplicates(subset=None, keep="first", inplace=False)
            dfDict = df.to_dict('records')
            # +++
            #entry_struct["col_names"] =  entry_struct["col_function"](file_name, dfDict[0]) if "col_function" in entry_struct else None
            entry_struct["col_names"] =  entry_struct["col_function"]() if "col_function" in entry_struct else None
            
            for client in dfDict:
                entry_struct["parsing_function"](client, file_name, entry_struct)

    return(entry_struct["data_struct"])


def is_valid_str(s: str) -> bool:
    return (isinstance(s, str) and s != "-")


def all_are_valid_strs(*args):
    ret = True
    for a in args:
        ret = is_valid_str(a)
        if ret == False:
            return ret
    return ret


def delta_time_in_hours_12_hour_basis(a: str, b: str) -> float:
    delta = (datetime.strptime(b, '%I:%M %p') - datetime.strptime(a, '%I:%M %p')).total_seconds()
    return round( delta / 3600.0, 2)


def delta_time_in_days(a: str, b: str) -> int:
    return (datetime.strptime(b, '%m/%d/%Y') - datetime.strptime(a, '%m/%d/%Y')).days
    # except ValueError as error:
    #     print(a)
    #     print(b)
    #     print( error)
    #     return (datetime.strptime(b, '%m/%d/%y') - datetime.strptime(a, '%m/%d/%y')).days
    

def on_time_interval(date_range: tuple, a_date: str) -> bool:
    # -- a_date: 'mmddyyyy'
    return ( is_valid_str(a_date) and delta_time_in_days(a_date, date_range[1]) >= 0 and delta_time_in_days( date_range[0], a_date ) >= 0   )


def decrement_mmddyy_str( s: str, delta_amount: int) -> str:
    d = datetime.strptime(date_range[0], '%m/%d/%Y')
    d -= timedelta(days=delta_amount)
    return datetime.strftime(d, '%m/%d/%Y')


def enrolled_during_time_interval(date_range: tuple, client: dict, **kwargs):
    if is_valid_str(client["Enrollment Date"]):
        if is_valid_str(client["Discharged Date"]): # case: Discharge date exists
            # discharge date was at or after beginning of interval
            # enroll date was at or before end  of interval
            return (delta_time_in_days(date_range[0], client["Discharged Date"]) >= 0
                    and 
                    delta_time_in_days(client["Enrollment Date"], date_range[1]) >= 0
                    and
                    client["Enrollment Status"] == "Enrolled")

        else: # case Discharge date doesn't exist
            return (delta_time_in_days(client["Enrollment Date"], date_range[1]) >= 0 and client["Enrollment Status"] == "Enrolled")


def column_name_assertion(col_names: list, files: list, **kwargs) -> None:    
    def parse(client: dict, file_name: str, entry_struct: dict) -> None:
        if "aliasing_check" in kwargs:
            ls = list( map( lambda x: x in client, col_names))
            combined_bool = functools.reduce( lambda x, y: x or y,  ls)
            assert combined_bool, f"Missing column in file: {file_name}"
        else:
            for col_name in col_names:
                assert (col_name in client), f"Missing column: {col_name}, in file: {file_name}"

        
    entry_struct = {"files":            files,
                    "parsing_function": parse,
                    "col_function":     None,
                    "data_struct":      {}}
    
    parsing_loop(entry_struct)


def pathway_opened_or_closed(date_range: tuple, file_name: str, open_close: str, **kwargs) -> None | dict:
    additional_filter_func = kwargs["filter_func"] if "filter_func" in kwargs else None
    """
    :param tupe date_range:   The date you're looking on in mm/dd/yyyy format
    :param str  file_name:    The pathway you're wanting to process, must end in .csv or .xlsx; e.g. "education.csv"
    :param str   open_close:  [open/ opened / Open/ Opened/ OPEN/ OPENED/ ... close/ closed / ... /CLOSED]; are you looking for the pathways opened or closed
    :param kwargs:            Write or use as data structure return
                              "filter_func" if the particular report requires additional filtering (e.g. Aultman needs to know about being an aultman client)
    """
    cols_to_look_at = ["Client Id", "Start Date", "Completed Date", "Completed Status", "Zip Code", "Referral In-Detail"]
    
    # -- account for social services:
    if file_name == "pw_social_service_referral.csv":
        cols_to_look_at += ["Service"]
    elif file_name == "pw_pregnancy.csv":
        cols_to_look_at = ["Client" if x=="Client Id" else x for x in cols_to_look_at]
        
    allowed_types = ["open", "opened", "Open", "Opened", "OPEN", "OPENED", "close", "closed", "Close", "Closed", "CLOSE", "CLOSED"]
    
    assert open_close.lower() in allowed_types, f"{open_close} not in {allowed_types}, check argument spelling"
    
    # -- It's too much mnental overhead to keep track of the string arg -> anything remotely close to open/ opened / Open/ Opened
    def correct_pathway_type_string_arg( s: str) -> str:
        lower_s = s.lower()
        match lower_s:
            case "open":
                return "opened"
            case "close":
                return "closed"
            case _:
                return lower_s
            
    def correct_date_str(s: str) -> str:
        return "Start Date" if correct_pathway_type_string_arg(s) == "opened" else "Completed Date"
    
    def completed_func(client: dict):
        # -- if we're looking at opened files, we don't care about this extra condition
        if correct_pathway_type_string_arg( open_close ) == "opened":
            return True
        # -- otherwise, we need to know what the completed status column name is && if that matches a completed status
        completed_str = "Completed" if file_name != "pw_health_insurance.csv" else "Complete-Insured"
        return ( client["Completed Status"] == completed_str )

    
    def parse(client: dict, _file_name: str, entry_struct: dict) -> None:
        # -- if opened: we care if the start date is on the time interval
        # -- if closed: we care if the close date is on the time interval && the completed status == "Completed" (or whatever that file is)
        if entry_struct["filter_func"]:
            if entry_struct["filter_func"](client) and on_time_interval(date_range, client[ correct_date_str(open_close) ]) and completed_func( client):
                for column_name in entry_struct["data_struct"]:
                    if column_name == "Referral In-Detail":
                        ref_in_detail = "Referral In-Detail" if "Referral In-Detail" in client else "Referral In-detail"
                        entry_struct["data_struct"][column_name].append( client[ ref_in_detail] )
                    else:
                        entry_struct["data_struct"][column_name].append( client[ column_name] )
        else:
            if on_time_interval(date_range, client[ correct_date_str(open_close) ]) and completed_func( client): #and entry_struct["filter_func"](client):
                for column_name in entry_struct["data_struct"]:
                    if column_name == "Referral In-Detail":
                        ref_in_detail = "Referral In-Detail" if "Referral In-Detail" in client else "Referral In-detail"
                        entry_struct["data_struct"][column_name].append( client[ ref_in_detail] )
                    else:
                        entry_struct["data_struct"][column_name].append( client[ column_name] )

        
    entry_struct = {"files":            [file_name],
                    "parsing_function": parse,
                    "col_function":     None,
                    "data_struct":      data_struct( cols_to_look_at ),
                    "filter_func":      kwargs["filter_func"] if "filter_func" in kwargs else None
                    }
    
    struct = parsing_loop( entry_struct )

    if "write" in kwargs and kwargs["write"]:
        write_direct_data_struct_to_excel(struct, f"{file_name } {open_close} " , date_range)

    if "ret" in kwargs and kwargs["ret"]:
        return struct


def pathways_ratio(date_range: tuple, file_name: str, write_name: str, **kwargs):

    if "filter_func" in kwargs:
        opened = pathway_opened_or_closed( date_range, file_name, "Opened", ret=True, filter_func=kwargs["filter_func"])
        closed = pathway_opened_or_closed( date_range, file_name, "Closed", ret=True, filter_func=kwargs["filter_func"])
       
    else:
        opened = pathway_opened_or_closed( date_range, file_name, "Opened", ret=True)
        closed = pathway_opened_or_closed( date_range, file_name, "Closed", ret=True)

    # pands makes this irrelevant
    #if "clean" in kwargs:
    opened = remove_exactly_repeating_clients(opened)
    closed = remove_exactly_repeating_clients(closed)
    
    write_multiple_sheets_direct_data_struct([opened, closed],
                                             ["opened_cleaned", "closed_cleaned"],
                                             (write_name + "_"),
                                             date_range)


def generic_key_client_columns() -> list:
    return ["Income",        "People In Household", "First",               "Last",              "Client Id", "Client Created Date",
            "Referral Date", "Enrollment Date",     "Enrollment Status",   "Discharged Date",   "Program",   "Race",
            "Zip Code",      "Funder", "Ethnicity", "Gender", "Age",       "Referral In-detail"]


def get_checklist_files():
    f = listdir(excel_file_src_dir)
    return sorted([x for x in f if "checklist" in x])


def get_generated_files() -> None:
    return listdir( generated_excel_dir )


def get_pathway_files() -> list:
    f = listdir(excel_file_src_dir)
    return sorted([x for x in f if x[0:2] == "pw"])

