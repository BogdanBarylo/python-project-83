def datetime_to_str(date):
    if date is None:
        return ''
    only_date = date.date()
    date_string = only_date.strftime('%Y-%m-%d')
    return date_string
