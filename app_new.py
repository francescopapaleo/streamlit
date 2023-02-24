import os.path
import sys
from pathlib import Path

import pickle

import streamlit as st
import pandas as pd
import numpy as np

CURRENT_DIR = Path().absolute()
ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output.pickle'

sys.path.append('data')
m3u_filepaths_file = 'playlists/streamlit.m3u8'

def load_essentia_analysis():
    with open(ESSENTIA_ANALYSIS_PATH, 'rb') as f:
        unpickled = []
        while True:
            try:
                unpickled.append(pickle.load(f))
            except EOFError:
                break
    df = pd.DataFrame(unpickled)
    df.set_index('file_path', inplace=True)
    return df

audio_analysis = load_essentia_analysis()
st.write(audio_analysis.head())

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
st.write(audio_analysis)
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

style_input = st.selectbox('Select a style:', list(audio_analysis.columns[6:]))
print(style_input)
activ_value = st.slider('Activation level:', value=[0.0, 1.0])
bpm_range = st.slider('Select BPM range:', value=[0, 200])
danceability_range = st.slider('Select danceability range:', value=[0.0, 1.0])
voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])
valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)

def filter_by_style(audio_analysis, style_input, activ_value):
    st.write(style_input)
    result=audio_analysis.loc[:][style_input]
    result=result.loc[(result>activ_value[0]) & (result<=activ_value[1]) ]
    return result
    
def filter_by_bpm(df, bpm_range):
    st.write(df)
    if bpm_range:
        df = df.loc[(df['bpm'] >= bpm_range[0]) & (df['bpm'] <= bpm_range[1])]
    return df

def filter_by_danceability(df, danceability_range):
    if danceability_range:
        df = df.loc[(df['danceability'] >= danceability_range[0]) & (df['danceability'] <= danceability_range[1])]
    return df

def filter_by_voice_instrumental(df, voice_instrumental_select):
    if voice_instrumental_select:
        df = df.loc[df['voice_instrumental'] == voice_instrumental_select]
    return df

def filter_by_valence_arousal(df, valence_arousal_range):
    if valence_arousal_range:
        df = df.loc[(df['valence'] >= valence_arousal_range[0]) & (df['valence'] <= valence_arousal_range[1]) &
                    (df['arousal'] >= valence_arousal_range[2]) & (df['arousal'] <= valence_arousal_range[3])]
    return df

if st.button("RUN"):
    st.write('## 🔊 Results')
    style_flt = filter_by_style(audio_analysis, style_input, activ_value)

    st.write('Audio previews for the first 10 results:')
    for mp3 in style_flt.index[:10]:
        st.audio(os.path.join('audio', mp3), format="audio/mp3", start_time=0)