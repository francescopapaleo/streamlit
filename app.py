import os.path
import sys
from pathlib import Path
import random

import streamlit as st
import pandas as pd
import ast

CURRENT_DIR = Path().absolute()
sys.path.append('./data')

from style_labels import style_400_keys

ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_reformat.json'

def load_essentia_analysis():
    df = pd.read_json(ESSENTIA_ANALYSIS_PATH)
    # Convert style_activations column from string to dictionary
    df['style_activations'] = df['style_activations'].apply(lambda x: ast.literal_eval(x))
    df.to_json('data/extended_descriptors_reformat.json', indent=4)
    return df

def filter_by_style(df, style_input):
    style_query = df[['track_id', 'style_activations']].copy()
    style_query['activation'] = style_query['style_activations'].apply(lambda x: x.get(style_input, -1))
    style_query = style_query[style_query['activation'] >= 0.5]
    style_query = style_query.sort_values(by='activation', ascending=False)
    style_query = style_query.merge(df, on='track_id')
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

st.write(audio_analysis['style_activations'].describe())

style_input = st.selectbox('Select a style:', style_400_keys)
bpm_range = st.slider('Select BPM range:', value=[int(audio_analysis['bpm'].min()), int(audio_analysis['bpm'].max())])
danceability_range = st.slider('Select danceability range:', value=[0.0, 1.0])
voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])
valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)

style_query = filter_by_style(audio_analysis, style_select, track_idx)

df = filter_by_style(audio_analysis, style_input)
df = filter_by_bpm(df, bpm_range)
df = filter_by_danceability(df, danceability_range)
df = filter_by_voice_instrumental(df, voice_instrumental_select)
df = filter_by_valence_arousal(df, valence_arousal_range)


st.write(df)