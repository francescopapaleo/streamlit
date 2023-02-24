import os.path
import sys
from pathlib import Path
import random

import streamlit as st
import pandas as pd
import ast
import pickle

CURRENT_DIR = Path().absolute()
sys.path.append('data')
ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output.pickle'
m3u_filepaths_file = 'playlists/streamlit.m3u8'

def load_essentia_analysis():
    with open(ESSENTIA_ANALYSIS_PATH, "rb") as f:
        while True:
            try:
                file_buffer = yield pickle.load(f)
            except EOFError:
                break
            return file_buffer

audio_analysis = pd.DataFrame(load_essentia_analysis())

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
st.write(audio_analysis.describe())
st.write('Loaded audio analysis for', audio_analysis, 'tracks.')

style_input = st.selectbox('Select a style:', audio_analysis.columns[6:])
print(style_input)
activ_value = st.slider('Activation level:', value=[0.0, 1.0])
bpm_range = st.slider('Select BPM range:', value=[0, 200])
danceability_range = st.slider('Select danceability range:', value=[0.0, 1.0])
voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])
valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)

def filter_by_style(audio_analysis, style_input, activ_value):
    filt_audio_analysis = audio_analysis.filter(by=[style_input, activ_value])
    return filt_audio_analysis
    
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
    style_act = style_flt.loc[(style_flt[style_input] >= activ_value[0]) & (style_flt[style_input] <= activ_value[1])]
    bpm_flt = filter_by_bpm(style_act, bpm_range)
else:
    bpm_flt = filter_by_bpm(audio_analysis, bpm_range)

# st.write(type(style_act))
# st.write(bpm_flt)

# results = bpm_flt.to_dict

# st.write(bpm_flt.head(10))

# with open(m3u_filepaths_file, 'w') as f:
#     # Modify relative mp3 paths to make them accessible from the playlist folder.
#         for keys, file_path in results.items():
#             mp3_paths = [os.path.join('audio', mp3) for mp3 in bpm_flt]
#             object = f.write('\n'.join(mp3_path for mp3_path in mp3_paths))

# def filter_by_style(df, style_input, style_range):
#     return df.loc[(df[style_input] >= style_range[0]) & (df[style_input] <= style_range[1])]
