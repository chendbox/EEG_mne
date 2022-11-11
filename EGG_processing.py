# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18TeETVGE5wsXCDNQOGph1LKuo7pVevJg
"""

!pip install mne

import mne
import matplotlib.pyplot as plt



#Read in raw data

fname = 'oddball_example_small-fif'

raw = mne.io.read_raw_fif(fname)

# helper information
dir(raw)

# helper information
raw.crop?

raw.filter?

# by default, MNE does not store raw and epochs objects in memory

raw = mne.io.read_raw_fif(fname, preload = True)

raw.filter(1, 20)

raw.plot()

eog_evoked = create_eog_epochs(raw).average()
eog_evoked.apply_baseline(baseline=(None, -0.2))
eog_evoked.plot_joint()

mne.preprocessing.create_eog_epochs(raw).average()



# there are many eog arefacts. We will use ICA to correct. Create ICA object and use its .fit method















ica = mne.preprocessing.ICA(n_components = 20, random_state = 42)

ica.fit(raw.copy().filter(8, 35))

ica.plot_components(outlines = 'skirt');

# store the 'bad' components in the ica object

ica.exclude = [1, 10, 14, 17, 18, 19]

bad_idx, scores = ica.find_bads_eog(raw, 'SO2', threshold = 2)
print(bad_idx)

# compare raw and adjusted data

raw.plot();

ica.apply(raw.copy(), exclude = ica.exclude).plot();

# epochs

# for epoching the data, we need event markers, usually, these are stored in the raw object, in mne, in a stimulus channel

events = mne.find_events(raw)

# events is an array*time in sampes, zero, trigger)

events

mne.viz.plot_events(events[:100]);

# for creating an mne.Epochs object, we require a dictionary of the intended condition names and the corresponding trigger numbers

event_ids = {'standard/stimulus': 200, 'target/stimulus': 100}

epochs = mne.Epochs(raw, events, event_id = event_ids)

epochs.plot();

epochs = ica.apply(epochs.load_data(), exclude = ica.exclude)

epochs.apply_baseline((None, 0))

# how does the epoched avtivity looks like?



epochs.info

epochs['target'].plot_image(picks = [13])

epochs['stimulus'].plot_image(picks = [13])

epochs['target'].plot_image(picks = [7])

# to ensure we have as many Oddball as standard trails, we can run...

epochs.equalize_event_counts(event_ids)

# standard = target



X = epochs.get_data()

X.shape

type(X)

epochs['target'].get_data().shape