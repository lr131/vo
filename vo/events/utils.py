import datetime

def get_current_season():
    today = datetime.date.today()
    current_year = today.year
    start_year = current_year if today.month >= 8 else current_year - 1
    end_year = current_year + 1 if today.month >= 8 else current_year

    return f"{start_year}/{end_year}"