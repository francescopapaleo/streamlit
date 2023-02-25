import os
import sys
import streamlit as st
import pandas as pd
import pickle
from pathlib import Path

# Setting some paths
data_root = Path('data').resolve()
audio_root = Path('audio').resolve()
essentia_descriptors = Path(data_root / 'ext_desc_output.json')
m3u_filepaths_file = Path('playlists/m3u_playlist.m3u8')

# Load the data
def load_essentia_analysis():
    df = pd.read_json(essentia_descriptors)
    return df

audio_analysis = load_essentia_analysis()

# create a new DataFrame with one column per label
labels_df = pd.get_dummies(pd.DataFrame(audio_analysis['activations_dict'].tolist()).stack()).sum(level=0)

# join the label columns to the original DataFrame
df = pd.concat([audio_analysis, labels_df], axis=1)

# drop the original 'activations_list' column
audio_analysis = df.drop('activations_dict', axis=1, inplace=True)

# print the result

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{essentia_descriptors}`.')
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