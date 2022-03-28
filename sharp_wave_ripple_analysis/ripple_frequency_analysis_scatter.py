# Import OS libraries
import numpy as np
import matplotlib.pyplot as plt


# A function that takes in a list of ripple windows, and finds the centre of that window
def find_center_ripple(ripple_times):
    ripple_times = np.load(ripple_times)
    ripple_centres = []  # Create an empty list to append ripple centers to
    for ripple_window in ripple_times:
        ripple_centres.append(np.median(ripple_window))
    assert len(ripple_centres) == len(ripple_times), 'Number of ripple centres does not match numer of ripple windows'
    if len(ripple_centres) == 0:
        print("ERROR - List of centres is empty, check why.")
    return(ripple_centres)


# A function that takes in a list of ripple centers and calcs avg ripples per minute
def avg_calc_ripples_per_minute(ripple_centres):  # Assumes ripple_centers is in seconds
    bins = list(range(0, 3600, 60))  # Create bins per minute up to a total time in seconds. 3600 seconds is one hour
    counts, bin_edges = np.histogram(ripple_centres, bins=bins)
    return(np.average(counts))


# A function that takes in a list of ripple centers and calcs avg ripples per minute
def hist_calc_ripples_per_minute(ripple_centres):  # Assumes ripple_centers is in seconds
    bins = list(range(0, 3600, 60))  # Create bins per minute up to a total time in seconds. 3600 seconds is one hour
    counts, bin_edges = np.histogram(ripple_centres, bins=bins)
    return(counts)
