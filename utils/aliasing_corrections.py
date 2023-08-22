
def get_allowable_aliases_funcs() -> list:
     return ["client_id", "base", "emergency", "hosptial", "missed appointments"]


def get_alias_func(t: str) -> callable:
     match t:
         case "client_id":
             return client_ids
         case "base":
             return base
         case "emergency":
             return emergency_department_visits
         case "hospital":
             return hosptial_admissions
         case "missed appointments":
             return missed_appointments


def client_ids(file_name: str) -> str:
     match file_name:
         case "initial_adult_checklist.csv":
             return {"client_id": "Client"}
         case "adult_checklist.csv":
             return {"client_id": "Client"}
         case "initial_maternal_checklist.csv":
             return {"client_id":"Client -"}
         case "maternal_checklist.csv":
             return {"client_id": "Client -"}
         case "initial_pregnancy_checklist.csv":
             return {"client_id": "Client Id"}
         case "pregnancy_checklist.csv":
             return {"client_id":"Client Id"}
                     
def base(fileName: str) -> dict:
     match fileName:
        case "initial_adult_checklist.csv":
            return {"client_id": "Client",    "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time", "chw": "Coordinator"}
        case "adult_checklist.csv":
            return {"client_id": "Client",    "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time", "chw": "Care Coordinator"}
            #return {"client_id": "Client",    "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time", "chw": "Care Coordinator", "rq": "Rq Status"}
        #-----------------------------------------------------------------------------------
        case "initial_maternal_checklist.csv":
            return {"client_id": "Client -",  "start_date": "Start Date 3-B", "start_time": "Start Time", "end_time": "End Time", "chw": "Coordinator"}
        case "maternal_checklist.csv":
            return {"client_id": "Client -",    "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time", "chw": "Coordinator", "rq": "RQ -"}
        #-----------------------------------------------------------------------------------
        case "initial_pregnancy_checklist.csv":
            return {"client_id": "Client Id", "start_date": "Start Date  3", "start_time": "Start Time  1", "end_time": "End Time  1", "chw": "Coordinator  -"}
        case "pregnancy_checklist.csv":
            return {"client_id": "Client Id", "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time", "chw": "Coordinator", "rq": "Rq"}
        #-----------------------------------------------------------------------------------
        case "initial_pediatric_checklist.csv":
            return {"client_id": "Client Id", "start_date": "Start Date  3", "start_time": "Start Time  1", "end_time": "End Time  1", "chw": "Coordinator  -"}
        case "pediatric_checklist.csv":
            return {"client_id": "Client Id", "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time",  "chw": "Care Coordinator", "rq": "Rq"}
        #-----------------------------------------------------------------------------------
        case _:
            return {"client_id": "Client Id", "start_date": "Start Date", "start_time": "Start Time", "end_time": "End Time"}

def base_checklist(fileName: str) -> dict:
    match fileName:
        case "initial_adult_checklist.csv":
            return {"client_id": "Client",    "date": "Start Date",     "zip_code": "Zip Code"}
        case "adult_checklist.csv":
            return {"client_id": "Client",    "date": "Start Date",     "zip_code": "Zip Code"}
        #-----------------------------------------------------------------------------------
        case "initial_maternal_checklist.csv":
            return {"client_id": "Client -",  "date": "Start Date 3-B", "zip_code": "Zip Code"}
        case "maternal_checklist.csv":
            return {"client_id": "Client -",    "date": "Start Date",     "zip_code": "Zip Code"}
        #-----------------------------------------------------------------------------------
        case "initial_pregnancy_checklist.csv":
            return {"client_id": "Client Id", "date": "Start Date  3",  "zip_code": "Zip Code"}
        case "pregnancy_checklist.csv":
            return {"client_id": "Client Id", "date": "Start Date",     "zip_code": "Zip Code"}
        #-----------------------------------------------------------------------------------
        case _:
            return {"client_id": "Client Id", "date": "Start Date",     "zip_code": "Zip Code"}

    
def health_behavior(fileName: str) -> dict:
     match fileName:
        case "adult_checklist.csv":
            return {"alcohol": "Alcohol Use", "tobacco": "Tobacco Use", "drugs": "Substance Use"}
        case "initial_adult_checklist.csv":
            return {"alcohol": "Alcohol", "tobacco": "Tobacco", "drugs": "Substances"}
        #-----------------------------------------------------------------------------------
        case "maternal_checklist.csv":
            return {"alcohol": "Do You Drink Alcohol", "tobacco": "Using Tobaco", "drugs": "Other Substance"}
        case "initial_maternal_checklist.csv":
            return {"alcohol": "Drinking Alcohol", "tobacco": "Using Tobacco Products", "drugs": "Using Other Substance"}
        #-----------------------------------------------------------------------------------
        case "pregnancy_checklist.csv":
            return {"alcohol": "Alcohol Use", "tobacco": "Tobacco Use", "drugs": "Substance Use"}
        case "initial_pregnancy_checklist.csv":
            return {"alcohol": "Drinking Alcohol  3", "tobacco": "Tobacco Products  3", "drugs": "Using Other Substance  3"}
            
        #-----------------------------------------------------------------------------------
        case _:
            return {"alcohol": "Alcohol Use", "tobacco": "Tobacco Use", "drugs": "Substance Use"}

def mental_health(fileName: str) -> dict:
     match fileName:
        case "adult_checklist.csv":
            return {"pleasure": "Little Pleasure"}
        case "maternal_checklist.csv":
            return {"pleasure": "Pleasure Doing Things"}
        #-----------------------------------------------------------------------------------
        case "pregnancy_checklist.csv":
            return {"pleasure": "Little Pleasure"}
        #-----------------------------------------------------------------------------------
        case _:
           return {"pleasure": "Little Pleasure"}

def emergency_department_visits(fileName: str) -> dict:
     match fileName:
         case "adult_checklist.csv":
            return {"ed_visit":"ED / ER Visit Since", "ed_val": "# of Visits"}
         case "initial_adult_checklist.csv":
            return {"ed_visit":"ED Visit 12m",        "ed_val": "# of ED Visits"}
        #----------------------------------------------------------
         case "maternal_checklist.csv":
             return {"ed_visit":"Emergency Room",   "ed_val": "Ed Visit Since Number"}
         case "initial_maternal_checklist.csv":
             return {"ed_visit":"Ed Visit 12m",     "ed_val": "Ed Visit 12m Number"}
         #-----------------------------------------------------------------------------------
         case "pregnancy_checklist.csv":
             return {"ed_visit":"Emergency Room",   "ed_val": "Ed Visit Since Number"}
         case "initial_pregnancy_checklist.csv":
             return {"ed_visit": "ED Visit 12m  3", "ed_val": "ER/ED Visits 12m   3"}
         #-----------------------------------------------------------------------------------
         case "pediatric_checklist.csv":
             return {"ed_visit":"ER / ED Visits Since", "ed_val": "# of Visits"}
         case "initial_pediatric_checklist.csv":
             return {"ed_visit": None, "ed_val": None}
         #-----------------------------------------------------------------------------------
         case _:
             return {"ed_visit":"Emergency Room"}

def hosptial_admissions(fileName: str) -> dict:
      match fileName:
         case "adult_checklist.csv":
            return {"hospital_visit":"Hospital Admits Since", "hospital_val": "# of Admits"}
         case "initial_adult_checklist.csv":
            return {"hospital_visit":"Hospital Visits 12m", "hospital_val": "# of Hosp Admits"}
        #----------------------------------------------------------
         case "maternal_checklist.csv":
             return {"hospital_visit": None, "hospital_val": "Hospital Visit Number"}
         case "initial_maternal_checklist.csv":
             return {"hospital_visit":"Hospital Visit 12m", "hospital_val": "Hospital Visit 12m Number"}
         #-----------------------------------------------------------------------------------
         case "pregnancy_checklist.csv":
             return {"hospital_visit":"Hospital Visit Since", "hospital_val": "# of Admits SInce"}
         case "initial_pregnancy_checklist.csv":
             return {"hospital_visit":"Hospital Visits 12m 3 (Logic)", "hospital_val": "Hospital Visits 12m 3 (#)"}
        

def gender_race_ethnicity(fileName: str) -> dict:
     match fileName:
        case "adult_checklist.csv":
            return {"gender": "Gender", "race" : "Race",    "ethnicity": "Ethnicity"}
        case "initial_adult_checklist.csv":
            return {"gender": "Gender", "race" : "Race",    "ethnicity": "Ethnicity"}
        #-----------------------------------------------------------------------------------
        case "maternal_checklist.csv":
            return {"race" : "Race  3", "ethnicity": "Ethnicity  3"}
        case "initial_maternal_checklist.csv":
            return {"race" : "Race  3", "ethnicity": "Ethnicity  3"}
        #-----------------------------------------------------------------------------------
        case "pregnancy_checklist.csv":
            return {"race" : "Race",    "ethnicity": "Ethnicity"}
      
        #-----------------------------------------------------------------------------------
        case _:
            return {"gender": "Gender", "race" : "Race",    "ethnicity": "Ethnicity"}
       
def health_self_rates(file_name:str) -> dict:
      match file_name:
         case "adult_checklist.csv":
             return {"health_self_rate": "Health Selfrate"}
         case "initial_adult_checklist.csv":
             return {"health_self_rate": "Health-selfrate"}
        #----------------------------------------------------------
         case "maternal_checklist.csv":
             return {"health_self_rate": "Health Selfrate"}
         case "initial_maternal_checklist.csv":
             return {"health_self_rate": "Health Selfrate"}
         #-----------------------------------------------------------------------------------
         case "pregnancy_checklist.csv":
             return {"health_self_rate": "Health Selfrate"}
         case "initial_pregnancy_checklist.csv":
             return {"health_self_rate": "Health-selfrate  3"}
         #-----------------------------------------------------------------------------------

def missed_appointments(file_name:str) -> dict:
    match file_name:
        case "adult_checklist.csv":
             return {"missed_appointments": "Number Missed Appointments"}
        case "initial_adult_checklist.csv":
             return {"health_self_rate": "Missed Appts Number"}
       
