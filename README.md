# Streamlit Repository for Essentia Playlist Testing

## Main steps:

### 1. Pre-processing of the dataset MusAV
- retrieving recursively list of files over an agnostic folder structure
[Check Colab notebook](https://colab.research.google.com/drive/1KmjyiFMBxAGL1eM74tJ716AohOMRD1va?usp=sharing)

### 2. Computing Audio Descriptors with Essentia with only style-tags

- BPM [RythmExtractor2013](https://essentia.upf.edu/reference/std_RhythmExtractor2013.html)
- Danceability [Standard mode](https://essentia.upf.edu/reference/std_Danceability.html)
- Style [Discogs-Effnet Model](https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb)
- Voice / Instrumental [MusicNN Model](https://essentia.upf.edu/models/classifiers/voice_instrumental/voice_instrumental-musicnn-mtt-2.pb)
- Arousal / Valence [Emomusic MOdel](https://essentia.upf.edu/models/classification-heads/emomusic/emomusic-musicnn-msd-2.pb)

First iteration took 6 hours for the entire dataset, second iteration after small optimisation and usage of GPUs took around 2 hours.
Different pipelines have been tested to optimize performance:
- no difference has been noticed using csv, json files as index list
- no difference in performance between the use of dictionaries or lists
- no improvement in computing time when using Pool package for parallel processing

***to avoid disruptions during the computation of descriptors the data is stored on a json file at each cycle (i.e. after each file descriptors have been computed)***

### 3. Computing the same Audio Descriptors with Essentia
- another class is defined to compute the same descriptors but keep the 400 activations for the style

### 4. Setting up the GitHub repository for Streamlit integration

[Streamlit public address](https://esse-playlist.streamlit.app/) 

***...Still not working...***

### 5. Build a web interface to generate playlists based on the computed descriptors

***...Work in progress...***

### Main issues:

1. Impossible to deploy a web interface with streamlite using http
2. Still figuring out how to finalise the playlist generation and preview

***...even though the computation is done, there are still problems in file-paths handling and m3u generation...***