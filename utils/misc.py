from datetime import datetime

#-- String q.o.l functions
def string_splitter_joiner(s: str, sp: str, j: str) -> str:
    return (j.join(list( map( lambda x: x.capitalize(), s.split(sp)))))

def capitalize_each_spaced_substring(s: str) -> str:
    return string_splitter_joiner(s, " ", " ")

def snake_case_to_standard(s: str) -> str:
    return string_splitter_joiner(s, "_", " ")

def standard_to_snake_case(s: str) -> str:
    return string_splitter_joiner(s, " ", "_")

def str_to_datetime(s: str)-> datetime:
    return datetime.strptime(s, '%m/%d/%Y')
