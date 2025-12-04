import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# # List speakers
# print(tts.speakers)

# Run TTS
# ❗ XTTS supports both, but many models allow only one of the `speaker` and
# `speaker_wav` arguments

def tts_to_file(txt:str, fname="output.wav"):
    print("starting")

    # TTS to a file, use a preset speaker
    tts.tts_to_file(
    text=txt,
    speaker="Craig Gutsy",
    language="en",
    file_path=fname
    )

    print("done")