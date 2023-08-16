# Helper function to get the time component based on the time_freq
def get_time_component(time_freq, dt):
    if time_freq == 'Y':
        return dt.year
    elif time_freq == 'M':
        return dt.year, dt.month
    elif time_freq == 'D':
        return dt.year, dt.month, dt.day
    else:
        raise ValueError("Invalid time frequency. Use 'Y', 'M', or 'D'.")
