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
    audio_analysis = pd.read_json(essentia_descriptors)
    activations = audio_analysis['activations_dict']            # extract the activations dict column
    activations_df = pd.DataFrame.from_records(activations)     # create a new dataframe for the dict
    audio_analysis = pd.concat([audio_analysis, activations_df], axis=1)    # concatenate the new activations with the original df
    audio_analysis = audio_analysis.drop('activations_dict', axis=1)    # drop the activations dict column
    return audio_analysis

audio_analysis = load_essentia_analysis()

# Visualize the data
st.write('# Audio analysis playlists example')
st.write(audio_analysis)
st.write(f'Using analysis data from `{essentia_descriptors}`.')
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

# Style filter
st.write('## 🔍 Filter by style activation')
# User inputs:
style_input = st.selectbox('Select a style:', list(audio_analysis.columns[5:]))
activ_value = st.slider('Activation level:', value=[0.1, 1.0])
# Filtering
style_col = audio_analysis[style_input]
audio_analysis_sorted = audio_analysis.sort_values(by=[style_input])
style_filter = audio_analysis_sorted[(audio_analysis_sorted[style_input] > activ_value[0]) &
                                      (audio_analysis_sorted[style_input] <= activ_value[1])]

res_style = style_filter

# BPM filter
st.write('## 🔍 Filter by BPM')
# User input:
bpm_range = st.slider('Select BPM range:', value=[20, 200])
bpm_col = audio_analysis['bpm']
bpm_filter = audio_analysis[(audio_analysis['bpm'] > bpm_range[0]) & 
                            (audio_analysis['bpm'] <= bpm_range[1])]
res_bpm = res_style.loc[res_style.index.isin(bpm_filter.index)]

# Danceability filter
st.write('## 🔍 Filter by danceability')
# User input:
danceability_range = st.slider('Select danceability range:', value=[0.0, 1.0])
danceability_col = audio_analysis['danceability']
danceability_filter = audio_analysis[(audio_analysis['danceability'] > danceability_range[0]) & 
                                     (audio_analysis['danceability'] <= danceability_range[1])]
res_danceability = res_bpm.loc[res_bpm.index.isin(danceability_filter.index)]

# # Valence/arousal filter
# st.write('## 🔍 Filter by valence/arousal')
# # User input:
# valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)
# valence_arousal_col = audio_analysis['valence-arousal']
# valence_arousal_filter = audio_analysis[(audio_analysis['valence-arousal'] > valence_arousal_range[0]) &
#                                         (audio_analysis['valence-arousal'] <= valence_arousal_range[1])]
# res_valence_arousal = res_danceability.loc[res_danceability.index.isin(valence_arousal_filter.index)]

# voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])

# We can select how many filters we want (ideally I would further develop the GUI)
post_all_filters = res_danceability

st.write('## 🔍 Results Stats')
st.write(post_all_filters.describe())


if st.button("RUN"):
    st.write('##Audio previews for the first 10 results:')
    mp3s = list(post_all_filters['file_id'].values)
    
    mp3_paths = [str(audio_root.joinpath(mp3)) for mp3 in mp3s]

    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
    # Modify relative mp3 paths to make them accessible from the playlist folder.
        f.write('\n'.join(str(mp3_path) for mp3_path in mp3_paths))
        st.write(f'Stored M3U playlist (absolute filepaths) to `{m3u_filepaths_file}`.')

    st.write('Audio previews for the first 10 results:')
    for mp3_path in mp3_paths[:10]:
        st.audio(str(mp3_path), format="audio/mp3", start_time=0)