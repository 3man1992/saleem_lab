# Saleem Lab Repo

This github repo is a collection of knowledge gained during my PhD rotation in the Saleem Lab. Primarily this repo is a signal processing repository for analysing local field potential (LFP) data from the hippocampus.

Below is an example output from the MTA_power_spec script which utilises multi-taper analysis to produce a power spectral density estimation for a single channel from a tetrode recording.

<p align="center">
  <img width="594" alt="Screenshot 2022-01-19 at 17 11 33" src="https://user-images.githubusercontent.com/22481774/150185078-69f7e938-2b90-4b9a-908c-fb21c8ac0793.png">
</p>

Below is an example output from the MT_spectrogram script which utilises multi-taper analysis to produce a spectrogram for a single channel from a tetrode recording.

<p align="center">
  <img width="601" alt="Screenshot 2022-01-21 at 16 09 03" src="https://user-images.githubusercontent.com/22481774/150560602-ded88fba-0434-4d21-a260-2c598f3c338c.png">
</p>


Error message handling:
+ ValueError: 'n_tapers' of 5 is greater than the 1 that satisfied the minimum energy concentration criteria of 0.5. -> Change the number of tapers used to the recommended number
+ ValueError: None of the tapers satisfied the minimum energy concentration criteria of 0.95 -> min_lambda parameter can be changed (though what does this mean for the analyis)
