######## THIS IS MY APP FILE ########

from collections import namedtuple

import os.path
import sys
from pathlib import Path
import random

import streamlit as st
import pandas as pd

CURRENT_DIR = Path().absolute()
sys.path.append('./data')


from style_labels import style_400_keys

m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output_processed.json'

def load_essentia_analysis():
    return pd.read_json(ESSENTIA_ANALYSIS_PATH)

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis = load_essentia_analysis()
st.write(audio_analysis.describe())
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

bpm = audio_analysis['bpm']
bpm_range = st.slider('Select BPM range:', value=[int(bpm.min()), int(bpm.max())])

bpm_query = audio_analysis.loc[(audio_analysis['bpm'] >= bpm_range[0]) & (audio_analysis['bpm'] <= bpm_range[1])]
bpm_index = bpm_query.sort_index()
st.write(bpm_index)

style = audio_analysis['style_activations']
style_select = st.multiselect('Select by style activations:', style_400_keys)
if style_select:
    style_query = audio_analysis
    for style_key in style_select:
        style_query = audio_analysis.loc[(audio_analysis['style_activations'].apply(lambda x: x[style_key] >= 0.5)).all(axis=1)]
    style_query = style_query.loc[style_query.index.isin(bpm_query.index)]
    st.write(style_query)

    max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
    shuffle = st.checkbox('Random shuffle')

    if st.button("RUN"):
        st.write('## 🔊 Results')
        mp3s = list(style_query.index)

        if shuffle:
            random.shuffle(mp3s)

        if max_tracks > 0:
            mp3s = mp3s[:max_tracks]

        with open(m3u_filepaths_file, 'w') as f:
            for mp3 in mp3s:
                f.write(mp3 + '\n')

        st.write('Wrote', len(mp3s), 'tracks to', m3u_filepaths_file)

        st.audio(m3u_filepaths_file)