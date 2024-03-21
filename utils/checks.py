d = {'Income': [], 'People In Household': [], 'First': [], 'Last': [], 'Client Id': [], 'Client Type': [], 'Client Created Date': [], 'Referral Date': [], 'Referral In-detail': [], 'Enrollment Date': [], 'Enrollment Status': [], 'Discharged Date': [], 'Program': [], 'Race': [], 'Zip Code': [], 'Funder': [], 'Ethnicity': [], 'Gender': [], 'Age': [], 'Coordinator': [], 'Education': [], 'G': [], 'i': [], 'b': [], 's': [], ' ': [], 'c': [], 'l': [], 'e': [], 'n': [], 't': [], 'r': [], 'o': [], 'd': []}

d_keys = list( d.keys())

should_be = ["Income",       "People In Household", "First",           "Last",              "Client Id",       "Client Type", "Client Created Date",
            "Referral Date", "Referral In-detail",  "Enrollment Date", "Enrollment Status", "Discharged Date", "Program",     "Race",
            "Zip Code",      "Funder", "Ethnicity", "Gender",          "Age",               "Coordinator",     "Client Type", "Education"]


f = list( filter( lambda x: x not in d_keys, should_be))
print( f)
