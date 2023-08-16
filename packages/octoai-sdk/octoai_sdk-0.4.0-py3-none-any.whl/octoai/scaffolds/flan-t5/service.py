"""Example OctoAI service scaffold: Flan-T5-Small."""
from transformers import T5ForConditionalGeneration, T5Tokenizer

from octoai.service import Service
from octoai.types import Text

"""
Flan-T5 is an instruction-finetuned version of T5, a text-to-text
transformer language model.
"""


class T5Service(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Download model weights to disk."""
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

    def infer(self, prompt: Text) -> Text:
        """Perform inference with the model.

        The `Text` type is a simple wrapper for `str` that provides
        a consistent API specification for your endpoint. The text is
        transferred over HTTP without any additional encoding. This type
        supports typical string-like operations.

        See also the API reference at
        https://octoml.github.io/octoai-python-sdk/octoai.html#module-octoai.types
        """
        inputs = self.tokenizer(prompt.text, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return Text(response[0])
