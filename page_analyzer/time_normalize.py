def get_normalized_time(date):
    if date is not None:
        only_date = date.date()
        date_string = only_date.strftime('%Y-%m-%d')
        return date_string
    else:
        return None
