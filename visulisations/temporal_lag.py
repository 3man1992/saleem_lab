import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

#Define tag lag calc func
def time_lag_coords(binned_data, channel):
    """A func that takes in binned MUA focusing on a given channel to return the time lag
    between the vc and the hpc. Runs both forwards and backwards to get positive and negative lags

    Returns:
        - x: Creates an x axis for plotting
        - temporal_coeffs: Creates an array of temporal coefficients of length bin_window * 2
        - arg_max_temporal_index: Which bin is the max temp coeff in
        - arg_max_value: What is the amplitude of the coeff"""

    # I need to refactor this can't have channel selection here
    #Variation 1
    visual_channels =      [0, 1,  2,  3, 4, 5,  6,  7]
    hippocampal_channels = [8, 9, 10, 11, 8, 9, 10, 11]

    # #Variation 2
    # visual_channels =      [4, 5, 6, 7, 8, 9, 10, 11]
    # hippocampal_channels = [0, 1, 2, 3, 0, 1, 2, 3]

    #Define how long before and after t to compare temporal lags
    bin_window = 50 #E.g 50 would set 50ms before and after t

    #Run correlation coefficients forwards and backwards by swapping x and ys
    dark_corrcoeffs_forward = sm.tsa.stattools.ccf(binned_data[:,visual_channels[channel]],
                                                   binned_data[:,hippocampal_channels[channel]])
    dark_corrcoeffs_back =    sm.tsa.stattools.ccf(binned_data[:,hippocampal_channels[channel]],
                                                   binned_data[:,visual_channels[channel]])

    #Creates plotting x axis
    x = np.arange(-bin_window, bin_window, 1) #Creates a window from -1s to 1s

    #Creates an array of temp coeffs from -bin_window < t < bin_window
    first_component = dark_corrcoeffs_back[1:bin_window]
    reversed_first_component = first_component[::-1]
    temporal_coeffs = list(reversed_first_component) + list(dark_corrcoeffs_forward[0:bin_window + 1])

    #Print if list is empty for some reason - bug
    if not temporal_coeffs: print('List of coeffs is empty for some reason, expected bug')

    #Locations the bin of the max temp coeff and the value its self
    argmax = np.argmax(np.asarray(temporal_coeffs)) #Return indice of highest coeff
    arg_max_temporal_index = x[argmax] #Return the bin of the argmax temp coeff
    arg_max_value = temporal_coeffs[argmax]
    print("The max coeff is", arg_max_value)

    #Unit Tests
    assert arg_max_value < 1 or arg_max_value > -1, "Temporal coefficient {} is out of logical range".format(arg_max_value)

    return(x, temporal_coeffs, arg_max_temporal_index, arg_max_value)

#Produce temporal coefficients bin index and argmax for scatter
def scatter_temp_coeff(binned_dark_data, binned_light_data, number_of_channels):
    """Runs through each channel and produces for dark and light conditions the bin of temp lag
    and the argmax of the temp coeff. Returned results input into scatter plot.

    Returns:
        - light lag values: the index of argmax for temp lag in light conditions
        - dark lag values: the index of argmax for temp lag in dark conditions
        - light lag max: the argmax of tempo coeff for light
        - dark lag max: the argmax of tempo coeff for light"""

    #Create empty dictionaries to fill for each channel
    light_lags = {}
    dark_lags  = {}
    light_arg_max = {}
    dark_arg_max = {}

    #Loop through channels, call temp lag func and add to dics
    for channel in range(number_of_channels):
        print('Comparing channel index: {}'.format(channel))

        #Dark
        dark_x, dark_temporal_coeffs, dark_arg_max_temporal_index, dark_arg_max_value     = time_lag_coords(binned_dark_data, channel)
        dark_lags[channel]  = dark_arg_max_temporal_index
        dark_arg_max[channel] = dark_arg_max_value

        #Light
        light_x, light_temporal_coeffs, light_arg_max_temporal_index, light_arg_max_value = time_lag_coords(binned_light_data, channel)
        light_lags[channel] = light_arg_max_temporal_index
        light_arg_max[channel] = light_arg_max_value

    #turn into a list of values for plotting
    light_lag_values = list(light_lags.values())
    dark_lag_values  = list(dark_lags.values())
    light_lag_max = list(light_arg_max.values())
    dark_lag_max = list(dark_arg_max.values())

    return (light_lag_values, light_lag_max, dark_lag_values, dark_lag_max)

#Not tested since copy from mains cript
#Plot time lag
def time_lag():
    #Plotting four channel comparisons
    fig, axs = plt.subplots(nrows = 2, ncols = 3, sharey = True)
    for channel in range(3):
        #Dark conditions
        dark_x, dark_y, arg_max_plot_x = time_lag_coords(binned_dark_data, channel)
        axs[0][channel].plot(dark_x, dark_y, 'k')
        axs[0][channel].axvline(0, color = 'k', linestyle ='--')
        axs[0][channel].axvline(arg_max_plot_x, color = 'r')
        axs[0][channel].margins(x=0)
        axs[0][channel].set_title('Channel: {}'.format(channel))
        axs[0][0].set_ylabel("Dark Conditions", size = 'large')

        #Light conditions
        light_x, light_y, arg_max_plot_xx = time_lag_coords(binned_light_data, channel)
        axs[1][channel].plot(light_x, light_y, 'k')
        axs[1][channel].axvline(0, color = 'k', linestyle ='--')
        axs[1][channel].axvline(arg_max_plot_xx, color = 'r')
        axs[1][channel].margins(x=0)
        axs[1][0].set_ylabel("Light Conditions", size = 'large')
    fig.tight_layout()
    fig.supylabel('Coeff')
    fig.supxlabel('Time (bins of 10mS)')
    fig.suptitle("Whole session: Temporal lag coefficients between HPC and VC across channels \n Positive lag is hpc preceding vc")
    plt.show()
    plt.savefig("/Users/freeman/Documents/saleem_folder/viz/temporal_coordination")

#Produce scatter for whole session comparing light and dark
def whole_session_plot(dark_mua, light_mua):
    binned_dark_data =  bin_mua(dark_mua, 60).to_numpy() #change second param for different bin size
    binned_light_data = bin_mua(light_mua, 60).to_numpy() #change second param for different bin size
    light_lag_values, light_lag_max, dark_lag_values, dark_lag_max = scatter_temp_coeff(binned_dark_data,
                                                                                        binned_light_data,
                                                                                        8)
    #Uncomment for plot
    # plt.scatter(light_lag_values, light_lag_max, color='r', label='light conditions')
    # plt.scatter(dark_lag_values, dark_lag_max, color='b', label='dark conditions')
    # plt.legend()
    # plt.xlabel('Time lag in 10ms')
    # plt.ylabel('Argmax coeff')
    # plt.axvline(x=0, color='k', linestyle ='--')
    # plt.show()
    return (light_lag_values, light_lag_max, dark_lag_values, dark_lag_max)
