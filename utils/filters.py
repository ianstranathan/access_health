import parsing

def served_on_interval_filter(date_range, client, file_name) -> bool:
    if parsing.enrolled_during_time_interval(date_range, client):
        return True
    return False
