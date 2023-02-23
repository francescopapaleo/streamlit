import os.path
import sys
from pathlib import Path
import random

import streamlit as st
import pandas as pd

CURRENT_DIR = Path().absolute()
sys.path.append('./data')

from style_labels import style_400_keys

ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output_processed.json'

def load_essentia_analysis():
    return pd.read_json(ESSENTIA_ANALYSIS_PATH)

def filter_by_style(df, style_select):
    style_select = ' '.join(style_select).lower().replace(' ', '_')
    style_query = df.loc[(df['style_activations'].apply(lambda x: x[style_select] >= 0.5)).all(axis=1)]
    return style_query


def filter_by_bpm(df, bpm_range):
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

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis = load_essentia_analysis()
st.write(audio_analysis.describe())
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

style_select = st.multiselect('Select by style activations:', style_400_keys)
bpm_range = st.slider('Select BPM range:', value=[int(audio_analysis['bpm'].min()), int(audio_analysis['bpm'].max())])
danceability_range = st.slider('Select danceability range:', value=[0.0, 1.0])
voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])
# valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)

df = filter_by_style(audio_analysis, style_select)
df = filter_by_bpm(df, bpm_range)
df = filter_by_danceability(df, danceability_range)
df = filter_by_voice_instrumental(df, voice_instrumental_select)
# df = filter_by_valence_arousal(df, valence_arousal_range)

st.write(df)

# max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
# shuffle = st.checkbox('Random shuffle')

# if st.button("RUN"):
#         st.write('## 🔊 Results')
#         mp3s = list(style_query.index)

#         if shuffle:
#             random.shuffle(mp3s)

#         if max_tracks > 0:
#             mp3s = mp3s[:max_tracks]

#         with open(m3u_filepaths_file, 'w') as f:
#             for mp3 in mp3s:
#                 f.write(mp3 + '\n')

#         st.write('Wrote', len(mp3s), 'tracks to', m3u_filepaths_file)

#         with st.beta_expander("Results"):
#             for mp3 in mp3s:
#                 st.write(mp3)
            
#         st.audio(m3u_filepaths_file)
