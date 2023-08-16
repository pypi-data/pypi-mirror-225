"""Example OctoAI service scaffold: Hello World."""
from octoai.service import Service
from octoai.types import Text


class HelloService(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Perform intialization."""
        print("Setting up.")

    def infer(self, prompt: Text) -> Text:
        """Perform inference."""
        return prompt
