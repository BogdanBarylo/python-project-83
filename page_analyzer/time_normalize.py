def get_normalized_time(date):
    only_date = date.date()
    date_string = only_date.strftime('%Y-%m-%d')
    return date_string
