# Playlist Generator based on audio features

### This repository has been created for a project during the SMC Master (2022/23)

The aim is to deploy feature extraction on a collection of audio files to prototype a playlist generator that leverages those data.

## STEPS

### 1. Pre-processing of the dataset MusAV

retrieving recursively a list of files over an agnostic folder structure and storing it in a json file. The function ```filewalker()``` and its call have been implemented in a way that checks the number of results and that doesn't re-compute the list if it already exists.

[Here a copy of the initial notebook with the full code for the descriptors extraction]()

### 2. Extracting Audio Descriptors with Essentia

Two algorythms belong to the traditional DSP set of algorythms included in Esssentia.

- BPM [RythmExtractor2013](https://essentia.upf.edu/reference/std_RhythmExtractor2013.html)
- Danceability [Standard mode](https://essentia.upf.edu/reference/std_Danceability.html)

Three others are pre-trained models distributed by Essentia used for this task: 

- Style [Discogs-Effnet Model](https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb)
- Voice / Instrumental [MusicNN Model](https://essentia.upf.edu/models/classifiers/voice_instrumental/voice_instrumental-musicnn-mtt-2.pb)
- Arousal / Valence [Emomusic MOdel](https://essentia.upf.edu/models/classification-heads/emomusic/emomusic-musicnn-msd-2.pb)

## 3. Setting up the GitHub repository for Streamlit integration

A GitHub repository has been set up to host the code necessary for the streamlit app.
The resulting app is accessible at this [Streamlit public address](https://essentia-playlist.streamlit.app/) 

### 4. Deploy a simple but functional web app

- the app is intended a simple demo and let the user set some filters based on the audio descriptors extracted
- the program output selectively the top 10 tracks in the collection and writes a playlist on a m3u file
- for copyright reason the preview of the files is not possible online

### 5. Possible improvements

Here it could be interesting to optimize the extraction. Maybe some embeddings could be shared among multiple models or different versions could be used in order to make the computation time shorter.


-------------------------------------------------------------------------------------------------------