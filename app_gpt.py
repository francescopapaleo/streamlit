import os.path
import sys
import streamlit as st
import pandas as pd
import pickle
from pathlib import Path


CURRENT_DIR = Path().absolute()
ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output.pickle'

sys.path.append('data')
m3u_filepaths_file = 'playlists/streamlit.m3u8'

def load_essentia_analysis():
    return pd.DataFrame(pd.read_pickle(ESSENTIA_ANALYSIS_PATH)).set_index('file_path')

audio_analysis = load_essentia_analysis()

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
st.write(audio_analysis)
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

def filter_audio(audio_analysis, style_input, activ_value, bpm_range, danceability_range, voice_instrumental_select, valence_arousal_range):
    result = audio_analysis.loc[:, style_input]
    result = result.loc[(result > activ_value[0]) & (result <= activ_value[1])]
    result = result.loc[(audio_analysis['bpm'] >= bpm_range[0]) & (audio_analysis['bpm'] <= bpm_range[1])]
    result = result.loc[(audio_analysis['danceability'] >= danceability_range[0]) & (audio_analysis['danceability'] <= danceability_range[1])]
    if voice_instrumental_select:
        result = result.loc[audio_analysis['voice_instrumental'] == voice_instrumental_select]
    result = result.loc[(audio_analysis['valence'] >= valence_arousal_range[0]) & (audio_analysis['valence'] <= valence_arousal_range[1]) & (audio_analysis['arousal'] >= valence_arousal_range[2]) & (audio_analysis['arousal'] <= valence_arousal_range[3])]
    return result

if st.button("RUN"):
    st.write('## 🔊 Results')
    filtered_audio = filter_audio(audio_analysis, style_input, activ_value, bpm_range, danceability_range, voice_instrumental_select, valence_arousal_range)
    st.write('Audio previews for the first 10 results:')
    for mp3 in filtered_audio.index[:10]:
        st.audio(os.path.join('audio', mp3), format="audio/mp3", start_time=0)
