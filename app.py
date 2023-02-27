import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------- Setting some paths -------------------------------- #
data_root = Path('data').resolve()
audio_root = Path('audio').resolve()
essentia_descriptors = Path(data_root / 'ext_desc_output.json')
m3u_filepaths_file = Path('playlists/m3u_playlist.m3u8')

# ---------------------------------- Load the data ------------------------------------ #
def load_essentia_analysis():
    audio_analysis = pd.read_json(essentia_descriptors)
    # extract the activations dict column
    activations = audio_analysis['activations_dict']
    activations_df = pd.DataFrame.from_records(
        activations)     # create a new dataframe for the dict
    # concatenate the new activations with the original df
    audio_analysis = pd.concat([audio_analysis, activations_df], axis=1)
    # drop the activations dict column
    audio_analysis = audio_analysis.drop('activations_dict', axis=1).set_index('file_id')
    audio_analysis = audio_analysis

    return audio_analysis

audio_analysis = load_essentia_analysis().describe()

# --------------------------------- Visualize the data ---------------------------------- #
st.write('# Audio analysis playlists example')
st.dataframe(audio_analysis)
st.write(f'Using analysis data from `{essentia_descriptors}`.')
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')


# ----------------------------------- Filter the data ----------------------------------- #
st.write('## 🔍 Filter by style activation')                                # Style filter
style_select = st.multiselect('Select a style:', list(audio_analysis.columns[5:]))   
if style_select:
    activ_value = st.slider('Activation level:', value=[0.1, 1.0])

st.write('## 🔍 Filter by BPM')                                             # BPM filter
bpm_range = st.slider('Select BPM range:', value=[20, 200]) 

st.write('## 🔍 Filter by danceability')                                # Danceability filter
danceability_range = st.slider('Select danceability range:', value=[0.5, 7.0])

st.write('## 🔍 Filter by voice/instrumental')                          # Voice/instrumental filter
voice_instrumental_select = st.selectbox('Select voice/instrumental:', ['', 'instrumental', 'voice'])

st.write('## 🔍 Filter by valence/arousal')                             # Valence/arousal filter
valence_arousal_range = st.slider('Select valence/arousal range:', -1.0, 1.0, (-1.0, 1.0), 0.1)

# -----------------------------------  Run the query ---------------------------------- #

if st.button("RUN"):
    # mp3s = list(audio_analysis['file_id'][i] for i in range(audio_analysis.shape[0]))
    mp3s = list(audio_analysis.index)
    
    if style_select:
        audio_analysis_query = audio_analysis.loc[mp3s][style_select]
        result = audio_analysis_query
    
        for style in style_select:
            result = result.loc[result[style] >= activ_value[0]]
            mp3s_style = result.index
    
    if bpm_range:
        bpm_query = audio_analysis.sort_values(by = ['bpm'], ascending = False)
        bpm_min = float(bpm_range[0])
        bpm_max = float(bpm_range[1])
        result_bpm = bpm_query['bpm'].loc[(bpm_query['bpm'] >= bpm_min) & (bpm_query['bpm'] <= bpm_max)]
        mp3s_bpm = list(result_bpm.index)

    if danceability_range:
        danceability_query = audio_analysis.sort_values(by = ['danceability'], ascending = False)
        danceability_min = float(danceability_range[0])
        danceability_max = float(danceability_range[1])
        result_danceability = danceability_query['danceability'].loc[(danceability_query['danceability'] >= danceability_min) & 
                                                                     (danceability_query['danceability'] <= danceability_max)]
        mp3s_danceability = list(result_danceability.index)

    if voice_instrumental_select != '':
        voice_instrumental_query = audio_analysis.sort_values(by = ['voice_instru'], ascending = False)
        if voice_instrumental_select == 'instrumental':
            result_voice_instrumental = voice_instrumental_query['voice_instru'].loc[(voice_instrumental_query['voice_instru'] > 0.5)]
        else:
            result_voice_instrumental = voice_instrumental_query['voice_instru'].loc[(voice_instrumental_query['voice_instru'] < 0.5)]
        mp3s_voice_instrumental = list(result_voice_instrumental.index)

# -----------------------------------  Show the results ------------------------------------- #

    st.write('## 🔍 Results Stats')
    results = set(mp3s_style) & set(mp3s_bpm) & set(mp3s_danceability) & set(mp3s_voice_instrumental)
    mp3_paths = [(audio_root).joinpath(mp3) for mp3 in results]

    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
        # Modify relative mp3 paths to make them accessible from the playlist folder.
        f.write('\n'.join(str(mp3_path) for mp3_path in mp3_paths))
        st.write(
            f'Stored M3U playlist (absolute filepaths) to `{m3u_filepaths_file}`.')
    
    st.write('Audio previews for the first 10 results:')
    for mp3_path in mp3_paths[:10]:
        st.audio(str(mp3_path), format="audio/mp3", start_time=0, )