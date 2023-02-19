import os.path
import random
import streamlit as st
import pandas
import pathlib

m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = '/Users/francescopapaleo/Dropbox/Mac/Documents/git-box/streamlit/data_test/descriptors_output.json'

def load_essentia_analysis():
    return pandas.read_json(ESSENTIA_ANALYSIS_PATH)

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis = load_essentia_analysis()

st.dataframe(audio_analysis)
audio_analysis_preview = audio_analysis.columns
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

# Select two columns and their weights
column1 = st.selectbox('Select the first column', audio_analysis.columns)
weight1 = st.slider('Select the weight of the first column', 0, 100, 50)

column2 = st.selectbox('Select the second column', audio_analysis.columns)
weight2 = st.slider('Select the weight of the second column', 0, 100, 50)

# Calculate the weighted average of the two columns
weighted_average = (audio_analysis[column1] * weight1/100) + (audio_analysis[column2] * weight2/100)
st.write('Weighted average:', weighted_average)

# Add the weighted average as a new column to the DataFrame
# audio_analysis_with_weighted_average = audio_analysis.assign(weighted_average=weighted_average)

# Sort the DataFrame by the weighted average column
# sorted_audio = audio_analysis_with_weighted_average.sort

# st.write('## Select a playlist')
# playlist = st.selectbox('Playlist', ['Random', 'Lowest energy', 'Highest energy', 'Lowest danceability', 'Highest danceability', 'Lowest valence', 'Highest valence', 'Lowest tempo', 'Highest tempo', 'Lowest loudness', 'Highest loudness', 'Lowest speechiness', 'Highest speechiness', 'Lowest acousticness', 'Highest acousticness', 'Lowest instrumentalness', 'Highest instrumentalness', 'Lowest liveness', 'Highest liveness'])