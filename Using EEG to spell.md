# Using EEG to spell

### Method 1 (called "P300 spelling")

* Start with a keyboard on the screen, perhaps white letters on black ground.
* Each letter may flash, for instance letters may turn black on green ground. Flash stays for 600 ms or so.
* For operation mode, flash letters randomly without replacement. Do a couple of rounds of flashing (5 seem to be enough). This means, every letter will be flashed 5 times. Have a 30 ms delay between the flash onsets.
* Then, take EEG time series. Do band pass filter (0.5 Hz - 20 Hz). For each letter, retrieve the times of the flash onset (which where set by the computer during the flash phase). Cut EEG into pieces, 600ms staring from flash onset. One gets one EEG piece of 600 ms for each flash a couple of pieces for each letter. Average all time series per letter.  End up with one feature vector per letter.
* Complications: feature vectors big, got more then one time series per letter (several electrodes). Solution: down-sample time series, concatenate series from single electrodes into one feature vector.
* Finally, look which of these averages shows evoked potential. This is going to be the letter you wanted. How? Do calibration first: During calibration, ask subject to focus one given letter, and do the above procedure. Do this a couple of times. Use this data (feature vectors for all letters, and the labels that you instructed) to train a classifier (SVM, LDA or something similar). Get classifier that can take feature vector and give prob that you looked at the letter. 
* In operation mode, use classifier for each feature vector, to find prob that this letter was looked at. Output the letter with highest prob.
* Check first paragraph of https://www.tandfonline.com/doi/full/10.1080/2326263X.2017.1410418 to get some references.

Further materials:

Whole P300 data gathering and analysis: https://eeg-notebooks.readthedocs.io/en/latest/visual_p300.html

### Method 2 (probably the one we want to use for binary choice!)

Based on https://www.pnas.org/content/112/44/E6058

* Each latter is flashed continuously with a unique frequency.
* Do a power spectrum of the EEG, see which of the frequencies is strongest.
* This should be quicker.
* Note: refresh rate of monitor makes it difficult. It might be 60 Hz, then should use some 8 Hz and 12 Hz because otherwise it would not work somehow.

Code for python for powerspectrum: https://raphaelvallat.com/bandpower.html

Get data from here: https://figshare.com/articles/MAMEM_EEG_SSVEP_Dataset_III_14_channels_11_subjects_5_frequencies_presented_simultaneously_/3413851/1

### Method 3

Based on https://www.pnas.org/content/101/51/17849

* Using beta in motor cortex to identify which hand is to be moved
* Much harder, subjects need to train a lot.
* If they are trained, it will work very good!

### Ref

Chen, X., Wang, Y., Nakanishi, M., Gao, X., Jung, T. P., & Gao, S. (2015). High-speed spelling with a noninvasive brain–computer interface. *Proceedings of the national academy of sciences*, *112*(44), E6058-E6067.

Wolpaw, J. R., & McFarland, D. J. (2004). Control of a two-dimensional movement signal by a noninvasive brain-computer interface in humans. *Proceedings of the national academy of sciences*, *101*(51), 17849-17854.

Speier, W., Arnold, C., Chandravadia, N., Roberts, D., Pendekanti, S., & Pouratian, N. (2018). Improving P300 spelling rate using language models and predictive spelling. *Brain-Computer Interfaces*, *5*(1), 13-22.