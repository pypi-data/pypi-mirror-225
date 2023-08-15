POSTRGRES_NUMERIC_TYPES = ['double', 'float', 'bigint', 'int', 'smallint']

def strip_where_from_filter_if_exists(filter_string):
    """
    utility function to clean up the WHERE condition (in case the string begins with "WHERE ... ")
    """
    if filter_string.upper()[:5] == 'WHERE':
        return filter_string[5:].strip()
    else:
        return filter_string
