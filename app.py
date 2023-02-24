import os.path
import random
import streamlit as st
import pandas as pd
import pickle
from pathlib import Path

m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = 'data/extended_descriptors_output.pickle'
AUDIO_DIR = '/Users/francescopapaleo/Dropbox/Mac/Documents/git-box/streamlit/audio'

def load_essentia_analysis():
    with open(ESSENTIA_ANALYSIS_PATH, 'rb') as f:
        unpickled = []
        while True:
            try:
                unpickled.append(pickle.load(f))
            except EOFError:
                break
    df = pd.DataFrame(unpickled)
    # df.set_index('file_path', inplace=True)
    return df

st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')

audio_analysis = load_essentia_analysis()

st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('### 🔍 By style')
st.write('Style activation statistics:')
st.write(audio_analysis.describe())

audio_analysis_styles = audio_analysis.columns[6:]
style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
print(style_select)

if style_select:
    st.write(audio_analysis[style_select].describe())
    audio_analysis_srtd = audio_analysis.sort_values([style_select])
    audio_analysis_srtd(5)

# style_select_str = ', '.join(style_select)
style_range = st.slider(f'Select tracks with `{}` activations within range:', value=[0., 1.0])

# st.write('### 🔍 By BPM')
# bpm_range = st.slider('Select BPM range:', value=[int(audio_analysis['bpm'].min()), int(audio_analysis['bpm'].max())])

# print(bpm_range)
# print(style_range)

audio_analysis_srtd(5)
rsl_flt = audio_analysis_srtd.loc(lambda x: (x[style_select] >= style_range[0]) & (x[style_select] <= style_range[1]))


#  (lambda x: (x[style_select_str] >= style_range[0]) & (x[style_select_str] <= style_range[1]))


# st.write('### 🔍 By danceability')
# danceability_range = st.slider('Select danceability range:', value=[1.0, 7.0])

# st.write('## 🔀 Post-process')
# max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)

if st.button("RUN"):
    st.write('## 🔊 Results')
    mp3s = list(audio_analysis.index.sort_values())

    # if style_select:
    audio_analysis_query = audio_analysis.loc[mp3s][style_select][(audio_analysis[style_select] >= style_select_range[0]) & (audio_analysis[style_select] <= style_select_range[1])]
    sty_result = audio_analysis_query
    
    audio_analysis_query = audio_analysis.loc[mp3s]['bpm'][(audio_analysis['bpm'] >= bpm_range[0]) & (audio_analysis['bpm'] <= bpm_range[1])]
    bpm_result = set(audio_analysis_query.index)
    
    st.write(type(audio_analysis_query))
    
    intersection = bpm_result & style_res

    if max_tracks:
        mp3 = intersection[:max_tracks]
        st.write('Using top', len(intersection), 'tracks from the results.')

    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
    # Modify relative mp3 paths to make them accessible from the playlist folder.
        mp3_paths = [os.path.join('audio', mp3) for mp3 in intersection]
        object = f.write('\n'.join(mp3_path for mp3_path in mp3_paths))

        st.write(f'Stored M3U playlist (absolute filepaths) to `{m3u_filepaths_file}`.')

    st.write('Audio previews for the first 10 results:')
    for mp3_path in mp3_paths[:10]:
        st.audio(str(mp3_path), format="audio/mp3", start_time=0)




    # bpm_res = audio_analysis.loc[mp3s][(audio_analysis['bpm'] >= bpm_range[0]) & (audio_analysis['bpm'] <= bpm_range[1])]
    # set_bpm=set(bpm_res)
    # print('set bpm', set_bpm)

    

        # for style in style_select:
        #     result = result.loc[result[style] >= style_select_range[0]]
        # # st.write(result).describe()
        # mp3 = result.index

    # # rank by style activations
    # if style_rank:
    #     audio_analysis_query = audio_analysis.loc[mp3s][style_rank]
    #     audio_analysis_query['RANK'] = audio_analysis_query[style_rank[0]]
    #     for style in style_rank[1:]:
    #         audio_analysis_query['RANK'] *= audio_analysis_query[style]
    #     ranked = audio_analysis_query.sort_values(['RANK'], ascending=[False])
    #     ranked = ranked[['RANK'] + style_rank]
    #     mp3s = list(ranked.index)

    #     st.write('Applied ranking by audio style predictions.')
    #     # st.write(ranked)

    # filter by bpm

   
    

    # dnc_res = audio_analysis.loc[mp3s][(audio_analysis['danceability'] >= danceability_range[0]) & (audio_analysis['danceability'] <= danceability_range[1])].index
    # set_dance=set(dnc_res)

    # 

    # dnc_filt = mp3.intersection(intersection)    

    
