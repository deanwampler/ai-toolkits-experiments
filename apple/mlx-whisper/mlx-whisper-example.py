#!/usr/bin/env python

import mlx_whisper

# See the README about downloading the following MP3 
# or change this value to the path to a speech mp3 you already have.
recording = "./MLKDream_64kb.mp3" 
path_or_hf_repo="mlx-community/distil-whisper-large-v3"
# path_or_hf_repo="mlx-community/whisper-tiny-mlx"

result = mlx_whisper.transcribe(
    recording,
    path_or_hf_repo=path_or_hf_repo)
print(f"result.keys(): {result.keys()}")
print(f"result['language']: {result['language']}")
print(f"len(result['text']): {len(result['text'])}")
print(f"First 3000 characters: {result['text'][:3000]}")
# If you use MLK's speech, the output should start as follows:
# I have the pleasure to present to you, Dr. Martin Luther King, ...
