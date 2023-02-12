import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from tensorflow.keras.models import load_model
from keras.models import load_model

fs = 44100
seconds = 2
filename = "prediction.wav"
class_names = ["Wake word NOT Detected", "Wake word Detected" ]
model = load_model("saved_model\\WWD.h5")
print("Prediction started: \n")
i = 0
while True:
    print("Say Now:")
    myrecording = sd.rec(int(seconds *fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, myrecording)
    audio, sample_rate = librosa.load(filename)
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfcc_processed = np.mean(mfcc.T, axis=0)
    prediction = model.predict(np.expand_dims(mfcc_processed, axis=0))
    if prediction[:, 1] > 0.80:
        print(f"Wake Word has been Detected!({i})")
        print(f"Confidence: {prediction[:, 1]}")
        i += 1
    else:
        print("Wake word not detected!")
        print(f"Confidence: {prediction[:, 0]}")