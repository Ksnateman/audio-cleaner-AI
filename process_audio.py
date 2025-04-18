import os
import noisereduce as nr
import scipy.io.wavfile as wav
from pydub import AudioSegment
from demucs_model import separate_vocals

def convert_to_wav(input_path):
    if not input_path.endswith('.wav'):
        audio = AudioSegment.from_file(input_path)
        wav_path = input_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format="wav")
        return wav_path
    return input_path

def reduce_noise(audio_path, output_path):
    rate, data = wav.read(audio_path)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wav.write(output_path, rate, reduced_noise.astype(data.dtype))

def process_full_audio(input_path, final_output):
    wav_path = convert_to_wav(input_path)
    vocal_path = separate_vocals(wav_path)
    reduce_noise(vocal_path, final_output)
