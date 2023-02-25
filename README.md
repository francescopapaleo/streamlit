# Streamlit Repository for Essentia Playlist Testing

## Main steps:

### 1. Pre-processing of the dataset MusAV

retrieving recursively a list of files over an agnostic folder structure and storing it in a json file. The function ```filewalker()``` and its call have been implemented in a way that checks the number of results and that doesn't re-compute the list if it already exists.

[Check Colab notebook with the full code for the descriptors extraction](https://colab.research.google.com/drive/1wfLR03x49FdYityigL_VLSRFJV6wRahp?usp=sharing)

### 2. Extracting Audio Descriptors with Essentia

These algorythms or pre-trained models have been used:

- BPM [RythmExtractor2013](https://essentia.upf.edu/reference/std_RhythmExtractor2013.html)
- Danceability [Standard mode](https://essentia.upf.edu/reference/std_Danceability.html)
- Style [Discogs-Effnet Model](https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb)
- Voice / Instrumental [MusicNN Model](https://essentia.upf.edu/models/classifiers/voice_instrumental/voice_instrumental-musicnn-mtt-2.pb)
- Arousal / Valence [Emomusic MOdel](https://essentia.upf.edu/models/classification-heads/emomusic/emomusic-musicnn-msd-2.pb)

### Possible improvement

Here it could be interesting to optimize the extraction. Maybe some embeddings could be shared among multiple models or different versions could be used in order to make the computation time shorter.

### Timing

First iteration took 6 hours for the entire dataset, different pipelines have been tested to optimize performance. The final version implemented in this colab notebook took 2 hours with a GPU runtime.

***to avoid disruptions during the computation of descriptors the data is stored on a json file at each cycle (i.e. after each file descriptors have been computed). In case of error or exception this would allow restarting the extraction from where it has stopped***

### 4. Setting up the GitHub repository for Streamlit integration

A GitHub repository has been set up to host the code necessary for the streamlit app.
The resulting app is accessible at this [Streamlit public address](https://essentia-playlist.streamlit.app/) 

### 5. Build a web interface to generate playlists based on the computed descriptors

***...Work in progress...***



### Main issues:

1. Impossible to deploy a web interface with streamlite using http
2. Still figuring out how to finalise the playlist generation and preview

***...even though the computation is done, there are still problems in file-paths handling and m3u generation...***