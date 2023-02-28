import essentia.standard as es
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from style_labels import style_400_keys # This is a list of 400 style labels based on the Discogs dataset

class AudioDescriptorsExtended:
    '''This class is used to compute audio descriptors for a given audio file.
        It uses the following models:
        - Tempo and Danceability: RhythmExtractor2013 and Danceability
        - Style: TensorflowPredictEffnetDiscogs
        - Voice/Instrumental: TensorflowPredictMusiCNN
        - Arousal/Valence: TensorflowPredictMusiCNN and TensorflowPredict2D
        '''

    def __init__(self):
        self.model_effnet = es.TensorflowPredictEffnetDiscogs(graphFilename='discogs-effnet-bs64-1.pb')
        self.model_vi = es.TensorflowPredictMusiCNN(graphFilename='voice_instrumental-musicnn-mtt-2.pb', output='model/dense/BiasAdd')
        self.model_av_emb = es.TensorflowPredictMusiCNN(graphFilename="msd-musicnn-1.pb", output='model/dense/BiasAdd')
        self.model_av = es.TensorflowPredict2D(graphFilename='emomusic-musicnn-msd-2.pb', output='model/Identity')

    def tempo_dance(self, path_to_file):
        audio = es.MonoLoader(filename=path_to_file, sampleRate=44100)()
        bpm, _, _, _, _ = es.RhythmExtractor2013()(audio)
        danceability, dfa = es.Danceability()(audio)
        return bpm, danceability

    def audio_16(self, path_to_file):
        audio_load_16 = es.MonoLoader(filename=path_to_file, sampleRate=16000)()
        return audio_load_16

    def style_ml(self, audio_load_16):
        activations = self.model_effnet(audio_load_16)
        activations_mean = np.mean(activations, axis=0, keepdims=True)
        activations_list = list(activations_mean.flatten())
        style_zip = dict(zip(style_400_keys, activations_list))
        return style_zip

    def vi_ml(self, audio_load_16):
        activations = self.model_vi(audio_load_16)
        v_i_mean = np.mean(activations, axis=0, keepdims=True)
        v_i_scaled = (v_i_mean - v_i_mean.min()) / (v_i_mean.max() - v_i_mean.min())
        v_i_mean_scaled = np.mean(v_i_scaled)
        return v_i_mean_scaled


    def av_ml(self, audio_load_16):
        embeddings = self.model_av_emb(audio_load_16)
        activations = self.model_av(embeddings)
        activations_mean = np.mean(activations, axis=0, keepdims=True)[0]
        valence = activations_mean[0]
        arousal = activations_mean[1]
        return valence, arousal

    def compute_descriptors(self, file_path):
        descriptors_dict = {}

        rel_path = os.path.relpath(file_path)
        audio_16 = self.audio_16(file_path)
        style_zip = self.style_ml(audio_16)
        v_i_mean_scaled = self.vi_ml(audio_16)
        valence, arousal = self.av_ml(audio_16)
        bpm, danceability = self.tempo_dance(file_path)

        descriptors_dict = {
            'file_path': rel_path,
            'bpm': str(bpm),
            'danceability': str(danceability),
            'style_activations': str(style_zip),
            'vi_scaled': str(v_i_mean_scaled),
            'valence': str(valence),
            'arousal': str(arousal)
        }

        return descriptors_dict