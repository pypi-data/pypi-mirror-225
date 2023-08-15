
def strip_where_from_opt_filter(orig_str):
    """Hidden function to remove leading WHERE keyword if supplied in optional filter."""
    if orig_str.upper()[:5] == 'WHERE':
        return orig_str[5:].strip()
    else:
        return orig_str

