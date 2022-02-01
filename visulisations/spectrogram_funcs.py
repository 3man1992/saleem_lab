"""In the context of time-frequency analysis, HeisenBerg's uncertainity
principal denotes that a function can't be both temporally and spatially localised.
Thus one can't achieve the perfect temporal and spatial resolution at the same time.
This is the flaw of the short-time Fourier transform. If one uses a wide window, a good
spatial frequency resolution at the cost of temporal resolution is caused. With a narrow
window one has the opporsite trade off. This happens in the short-time-fourier transform.

Thus the wavelet transform is used when transients are important.

I think this method uses the Inverse Fourier transform calc of CWT"""

#OS libaries
import ghostipy as gsp
import numpy as np
import matplotlib.pyplot as plt

def cwt(filtered_signal, fs):
    coefs_cwt, _, f_cwt, t_cwt, _ = gsp.cwt(data        = filtered_signal,
                                            fs          = fs,
                                            freq_limits = [1, 500],
                                            method      = 'full',
                                            n_workers   = 8,
                                            verbose     = True)
    psd_cwt = coefs_cwt.real**2 + coefs_cwt.imag**2
    psd_cwt /= np.max(psd_cwt)

    kwargs_dict = {}
    kwargs_dict['cmap'] = plt.cm.Spectral_r
    kwargs_dict['linewidth'] = 0
    kwargs_dict['vmin'] = 0
    kwargs_dict['vmax'] = 1
    kwargs_dict['rasterized'] = True
    kwargs_dict['shading'] = 'auto'

    return(t_cwt, f_cwt, psd_cwt, kwargs_dict)

def wsst(filtered_signal, fs):
    coefs_wsst, _, f_wsst, t_wsst, _ = gsp.wsst(data        = filtered_signal,
                                                fs          = fs,
                                                freq_limits =[1, 500],
                                                voices_per_octave=32)
    psd_wsst = coefs_wsst.real**2 + coefs_wsst.imag**2
    psd_wsst /= np.max(psd_wsst)
    return(t_wsst, f_wsst, psd_wsst)
