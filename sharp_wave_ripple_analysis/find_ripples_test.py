# started but not finished

# Import OS libaries
import numpy as np


def find_ripples(signal):
    """A pythonic implementation of FineRipples from Matlab
    =========================================================================
    Properties    Values
    -------------------------------------------------------------------------
    'Signal'      A 1d array of mV recordings from a single channel
    'Time'        A 1d array of times in seconds matching signal length
    'thresholds'  thresholds for ripple beginning/end and peak, in multiples
                  of the stdev (default = [2 5])
    'durations'   minimum inter-ripple interval, and minimum and maximum
                  ripple durations, in ms (default = [30 20 100])
    'baseline'    interval used to compute normalization (default = all)
    'restrict'    same as 'baseline' (for backwards compatibility)
    'frequency'   sampling rate (in Hz) (default = 1250Hz)
    'stdev'       reuse previously computed stdev
    'show'        plot results (default = 'off')
    'noise'       noisy ripple-band filtered channel used to exclude ripple-
                  like noise (events also present on this channel are
                  discarded)
    =========================================================================
    """

    # Parameters to the function
    frequency = 1250  # In Hertz - sampling rate of data

    # Set the window length
    window_length = round(frequency / 1250 * 11)

    # Square and normalise signal
    squared_signal = np.square(signal)
    window = np.ones(window_length, 1) / window_length
