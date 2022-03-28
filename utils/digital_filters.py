import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import sosfiltfilt


# Create second order coeff
def butter_bandpass(lowcut, highcut, fs, order=4):
    "Set at 4th order to match paper by Ahmadi et al 2021"
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = signal.butter(N=order,
                        Wn=[low, high],
                        btype='bandpass',
                        output='sos',
                        fs=fs)
    return sos

#Filt filt function - no phase shift
def butter_bandpass_filter(data, lowcut, highcut, fs):
    #If one channel axis = 1, if more than one channel, axis 0
    sos = butter_bandpass(lowcut, highcut, fs)
    # filtered_data = sosfiltfilt(sos, data, axis=0) #Axis 0 for rows as timestamps go down
    filtered_data = sosfiltfilt(sos, data) #Trying to remove axis to what happens
    return(filtered_data)


def highpass_filtfilt(sig, sampling_freq, cut_off):
    """Set at 4th order to match paper by Ahmadi et al 2021
    Using highpass to avoid alaising associated with bandpass.
    Used for MUA filtering"""
    if len(sig) != 0:
        order = 4
        print("Length of signal going through filt filt:", len(sig))
        sos = signal.butter(N=order,
                            Wn=cut_off,
                            btype='highpass',
                            output='sos',
                            fs=sampling_freq)
    else:
        raise Exception("Can't filter an empty signal")
    return(sosfiltfilt(sos, sig))

#For testing filters
if __name__ == '__main__':
    #A function that plots syn data and filtering results
    def test_highvslow_pass():
        #Generate test signals for testing the filter function -------------------------
        t = np.linspace(0, 1, 1000, False)  # 1 second
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)

        #Generate synethic 50hz signal
        sig1 = np.sin(2*np.pi*50*t)
        ax1.plot(t, sig1)
        ax1.set_title('50 Hz sinusoid')
        ax1.axis([0, 1, -2, 2])
        ax1.set_ylabel('Amplitude')

        #Generate synethic 5hz signal
        sig2 = np.sin(2*np.pi*5*t)
        ax2.plot(t, sig2)
        ax2.set_title('5 Hz sinusoid')
        ax2.set_ylabel('Amplitude')
        ax2.axis([0, 1, -2, 2])

        #Generate synethic 50hz + 5Hz multiplexed signal
        sig3 = sig2 + sig1
        ax3.plot(t, sig3)
        ax3.set_title('50 + 5 Hz multiplexed sinusoids')
        ax3.set_ylabel('Amplitude')

        #Conduct highpass filter above 15hz
        sos = signal.butter(N = 10, Wn = 15, btype = 'highpass', output= 'sos', fs=1000)
        filtered = signal.sosfilt(sos, sig3)
        ax4.plot(t, filtered)
        ax4.set_title('After 15 Hz high-pass filter')
        ax4.axis([0, 1, -2, 2])
        ax4.set_ylabel('Amplitude')

        #Conduct lowpass filter above 15hz
        sos = signal.butter(N = 10, Wn = 15, btype = 'lowpass', output= 'sos', fs=1000)
        filtered = signal.sosfilt(sos, sig3)
        ax5.plot(t, filtered)
        ax5.set_title('After 15 Hz low-pass filter')
        ax5.set_xlabel('Time [seconds]')
        ax5.axis([0, 1, -2, 2])
        ax5.set_ylabel('Amplitude')

        #Plot
        plt.tight_layout()
        plt.show()
        #-------------------------------------------------------------------------------

    #Comment / uncomment to run
    # test_highvslow_pass()

    #Generate test signals for testing the band pass filter function -------------------------
    def test_band_pass():
        #Gen time
        t = np.linspace(0, 1, 1000, False)  # 1 second

        #Generate synethic 50hz signal
        sig1 = np.sin(2*np.pi*50*t)

        #Generate synethic 5hz signal
        sig2 = np.sin(2*np.pi*5*t)

        #Generate synethic 50hz + 5Hz multiplexed signal
        sig3 = sig2 + sig1

        #filter
        signal = test_highpass(sig3)

        #Plot
        fig, axs = plt.subplots(2, 1, sharex=True)
        axs[0].plot(t, signal)
        axs[1].plot(t, sig1)
        plt.show()

    test_band_pass()
