# README for `apple/mlx-whisper`

This is code for using the OpenAI's Whisper speech-to-text models on Apple Silicon adapted from https://simonwillison.net/2024/Aug/13/mlx-whisper/.

Install the `mlx-whisper` library using `pip`:

```shell
pip install mlx-whisper
```

Then install `ffmpeg`. Using HomeBrew:

```shell
brew install ffmpeg
```

For other platforms, see https://ffmpeg.org/download.html.

(The blog post doesn't mention `ffmpeg`. Most likely, Simon forgot he had it installed already.)

You'll need a speech MP3 file to use. You can download Martin Luther King's _I Have a Dream_ speech here, for example: https://archive.org/details/MLKDream

Put the `MLKDream_64kb.mp3` in this directory and then run the following script. If you want to use a different MP3 file, edit the script to specify its path:

```shell
python mlx-whisper-example.py
```

This example should download a 1.5GB model from Hugging Face and stash it in your `~/.cache/huggingface/hub/models--mlx-community--distil-whisper-large-v3` folder.

Calling `.transcribe(filepath)` without the `path_or_hf_repo` argument uses the much smaller (74.4 MB) `whisper-tiny-mlx` model.

See Simon's blog post above for more details and a discussion of how this compares to `whisper.cpp`.
