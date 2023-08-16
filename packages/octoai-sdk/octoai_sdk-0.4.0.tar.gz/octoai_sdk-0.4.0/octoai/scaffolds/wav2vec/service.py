"""Example OctoAI service scaffold: Wav2Vec."""
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from octoai.service import Service
from octoai.types import Audio, Text

"""
Wav2vec is a self-supervised learning algorithm for speech recognition.
"""


class Wav2VecService(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Download model weights to disk."""
        self.processor = Wav2Vec2Processor.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    def infer(self, audio: Audio) -> Text:
        """Perform inference with the model.

        The `Audio` type is a wrapper for binary audio files that provides a
        consistent API specification for your endpoint. The audio data is
        transferred over HTTP encoded as base64. This type provides support for
        encoding and decoding, reading audio data as numpy, creating audio files
        from numpy, and reading audio files from disk or remote URLs.

        The `Text` type is a simple wrapper for `str` that provides
        a consistent API specification for your endpoint. The text is
        transferred over HTTP without any additional encoding. This type
        supports typical string-like operations.

        See also the API reference at
        https://octoml.github.io/octoai-python-sdk/octoai.html#module-octoai.types
        """
        audio_array, sampling_rate = audio.to_numpy()
        input_values = self.processor(
            audio_array,
            sampling_rate=sampling_rate,
            return_tensors="pt",
            padding="longest",
        ).input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)

        return Text(text=transcription[0])
