!pip install speechbrain

from speechbrain.inference.separation import SepformerSeparation as separator
import torchaudio
from IPython.display import Audio

model = separator.from_hparams(source="speechbrain/sepformer-wham16k-enhancement", savedir='pretrained_models/sepformer-wham16k-enhancement')

audio_sources = model.separate_file(path='/content/drive/MyDrive/audio/noisy_audio2.wav')

import IPython.display as ipd
ipd.Audio("/content/drive/MyDrive/audio/noisy_audio2.wav")

torchaudio.save("converted_audio.wav", audio_sources[:, :, 0], 16000)

import IPython.display as ipd
ipd.Audio("converted_audio.wav")