# Saleem Lab Repo

This github repo is a collection of knowledge gained during my PhD rotation in the Saleem Lab. Primarily this repo is a signal processing repository for analysing local field potential (LFP) data from the hippocampus.

Some useful aspects are:
+ A matlab (.mat) converter script into python dictionarys. This file is found within utils and is called auto_mat_to_python.py
+ A collection of sharp wave ripple extraction techniques found in the SWR dir
+ MUA activity calculations
+ An improved meta_data system for producing code across many sessions

Below is an example output from the MTA_power_spec script which utilises multi-taper analysis to produce a power spectral density estimation for a single channel from a tetrode recording.

<p align="center">
  <img width="594" alt="Screenshot 2022-01-19 at 17 11 33" src="https://user-images.githubusercontent.com/22481774/150185078-69f7e938-2b90-4b9a-908c-fb21c8ac0793.png">
</p>

Below is an example output from the MT_spectrogram script which utilises multi-taper analysis to produce a spectrogram for a single channel from a tetrode recording.

<p align="center">
  <img width="601" alt="Screenshot 2022-01-21 at 16 09 03" src="https://user-images.githubusercontent.com/22481774/150560602-ded88fba-0434-4d21-a260-2c598f3c338c.png">
</p>

Below are example raw traces of a sharp wave ripple detection algorithm compared to bandpass filtered signals. Each channel is from a single tetrode.

<p align="center">
  <img width="528" alt="Screenshot 2022-01-31 at 17 19 47" src="https://user-images.githubusercontent.com/22481774/151986847-94992946-ac9d-48a3-a4e9-1c3248012d6e.png">
</p>

Below is an example of MUA modulation relative to SWR time comparing the visual cortex and hpc.

<p align="center">
  <img width="1448" alt="Screenshot 2022-03-28 at 11 37 41" src="https://user-images.githubusercontent.com/22481774/160380807-9639d648-ba0b-41dd-aa9a-13eb1892e9be.png">
</p>

