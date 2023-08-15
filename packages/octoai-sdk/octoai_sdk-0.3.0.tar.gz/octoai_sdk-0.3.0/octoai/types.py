"""
Type definitions to help communicate with endpoints.

These type definitions help with routine format conversions
that are necessary when transferring binary files (such as
images or audio) over HTTP. These type definitions can be useful
both when creating endpoints (implementing ``octoai.service.Service``
as directed by the ``octoai`` command-line interface) and when
communicating with live endpoints using the client SDK.
"""

import base64
import importlib
import os
import sys
from io import BytesIO
from types import ModuleType
from typing import Any, Dict, Tuple, Union

import httpx
from numpy.typing import ArrayLike
from PIL import Image as PImage
from pydantic import BaseModel, Field


def file_b64encode(file_bytes: bytes) -> str:
    """Encode binary file as a base64 string.

    :param file_bytes: contents of a binary file
    :type file_bytes: bytes
    :return: contents of a binary file encoded as a base64 string
    :rtype: str
    """
    return base64.b64encode(file_bytes).decode("ascii")


def file_b64decode(file_b64: str) -> bytes:
    """Decode a base64 string into a binary file.

    :param file_b64: contents of a binary file encoded as a base64 string
    :type file_b64: str
    :return: contents of a binary file
    :rtype: bytes
    """
    return base64.b64decode(bytes(file_b64, "ascii"))


def _import_soundfile() -> ModuleType:
    """Attempt to import the soundfile module."""
    if "soundfile" in sys.modules:
        return sys.modules["soundfile"]

    try:
        return importlib.import_module("soundfile")
    except OSError:
        raise Exception(
            "Can't import the 'soundfile' module. "
            "For Linux, try: sudo apt install libsndfile1. "
            "For Mac, try: brew install libsndfile."
        )


class Text(BaseModel):
    """Text type for models that accept or return text.

    The `Text` type is a simple wrapper for `str` that provides
    a consistent API specification for endpoints. This type
    supports typical string-like operations. The text is transferred
    over HTTP without any additional encoding.

    To create an instance of this type, call the constructor
    with your string value: `Text("mytext")`
    """

    text: str

    def __init__(self, text: str):
        super().__init__(text=text)

    def __add__(self, other: Union["Text", str]) -> "Text":
        """Concatenate."""
        try:
            return Text(self.text + other.text)  # type: ignore
        except AttributeError:
            return Text(self.text + other)  # type: ignore

    def __contains__(self, item: Union["Text", str]) -> bool:
        """Check inclusion."""
        try:
            return item.text in self.text  # type: ignore
        except AttributeError:
            return item in self.text  # type: ignore

    def __getitem__(self, index):
        """Get item."""
        return Text(self.text.__getitem__(index))

    def __mul__(self, other: int) -> "Text":
        """Repeat."""
        return Text(self.text * other)

    def __str__(self) -> str:
        """Convert to string."""
        return self.text


class Image(BaseModel):
    """Image helpers for models that accept or return images.

    The `Image` type is a wrapper for binary image files that provides a
    consistent API specification for your endpoint. The image data is
    transferred over HTTP encoded as base64. This type provides support for
    encoding and decoding, reading image data as Pillow, creating image files
    from Pillow, and reading image files from disk or remote URLs.

    To create an instance of this type, users can select the appropriate
    ``Image.from_...()`` method depending on the format of their input.

    :param BaseModel: base model
    :type BaseModel: :class:`BaseModel`
    :raises ValueError: ``from_file`` method failed to load image.
    :raises ValueError: ``from_url`` method was unable to reach the url.
    :return: base64 encoded image
    :rtype: str
    """

    image_b64: str = Field(description="base64-encoded image file")

    def __init__(self, image_b64: str):
        super().__init__(image_b64=image_b64)

    @classmethod
    def from_base64(cls, b64: str):
        """Create from base64 encoded string, such as that returned from an HTTP call.

        See also ``Image.from_endpoint_response()``.

        :param b64: contents of a binary image file as a base64 encoded string
        :type b64: str
        :return: Image object
        :rtype: :class:`Image`
        """
        return cls(image_b64=b64)

    @classmethod
    def from_endpoint_response(cls, resp_dict: Dict[str, Any], key: str):
        """Create from an endpoint response, such as an endpoint that produces images.

        :param resp_dict: a response from an OctoAI endpoint that produces images
        :type resp_dict: Dict[str, Any]
        :param key: the key name in the response that contains an encoded image
        :return: Image object
        :rtype: :class:`Image`
        """
        if key in resp_dict:
            return cls(image_b64=resp_dict[key]["image_b64"])
        elif "output" in resp_dict and key in resp_dict["output"]:
            return cls(image_b64=resp_dict["output"][key]["image_b64"])

        raise ValueError(f"{key} not in resp_dict")

    @classmethod
    def from_pil(cls, image_pil: PImage, format="JPEG"):
        """Create from Pillow image object.

        A file format is required since the Pillow image object is
        serialized to a binary image file. The default is "JPEG".

        :param image_pil: image in PIL format
        :type image_pil: PIL.Image
        :param format: target file format, defaults to "JPEG"
        :type format: str, optional
        :return: Image object
        :rtype: :class:`Image`
        """
        buffer = BytesIO()
        image_pil.save(buffer, format=format)
        return cls(image_b64=file_b64encode(buffer.getvalue()))

    @classmethod
    def from_file(cls, image_file: str):
        """Create from local file.

        :param image_file: path to local image file
        :type image_file: str
        :raises ValueError: image_file not found at provided path
        :return: Image object
        :rtype: :class:`Image`
        """
        if not os.path.isfile(image_file):
            raise ValueError(f"File {image_file} does not exist")

        with open(image_file, "rb") as fd:
            return cls(image_b64=file_b64encode(fd.read()))

    @classmethod
    def from_url(cls, image_url: str, follow_redirects=False):
        """Create from image URL.

        :param image_url: url leading to an image
        :type image_url: str
        :param follow_redirects: whether to follow URL redirects
        :type follow_redirects: bool
        :raises ValueError: there was an error reaching the target url
        :return: Image object
        :rtype: :class:`Image`
        """
        resp = httpx.get(image_url, follow_redirects=follow_redirects)
        if resp.status_code != 200:
            raise ValueError(f"status {resp.status_code} ({image_url})")

        return cls(image_b64=file_b64encode(resp.content))

    def is_valid(self):
        """Check if this is a valid image.

        :return: True if valid, False if invalid
        :rtype: bool
        """
        try:
            self.to_pil().verify()
            return True
        except Exception:
            return False

    def to_pil(self) -> PImage:
        """Convert to PIL Image.

        :return: Pillow image object
        :rtype: PIL.Image
        """
        return PImage.open(BytesIO(file_b64decode(self.image_b64)))

    def to_file(self, file_name: str):
        """Save image to disk.

        :param file_name: file path
        :type file_name: str
        """
        with open(file_name, "wb") as fd:
            fd.write(file_b64decode(self.image_b64))


class Audio(BaseModel):
    """Audio helpers for models that accept or return audio.

    The `Audio` type is a wrapper for binary audio files that provides a
    consistent API specification for endpoints. The audio data is
    transferred over HTTP encoded as base64. This type provides support for
    encoding and decoding, reading audio data as numpy, creating audio files
    from numpy, and reading audio files from disk or remote URLs.

    To create an instance of this type, users can select the appropriate
    ``Audio.from_...()`` method depending on the format of their input.

    :param BaseModel: base model
    :type BaseModel: :class:`BaseModel`
    :raises ValueError: ``from_file`` method failed to load file
    :raises ValueError: ``from_url`` method was unable to reach the url.
    :return: base64 encoded audio
    :rtype: str
    """

    audio_b64: str = Field(description="base64-encoded audio file")

    def __init__(self, audio_b64: str):
        super().__init__(audio_b64=audio_b64)

    @classmethod
    def from_base64(cls, b64: str):
        """Create from base64 encoded string, such as that returned from an HTTP call.

        See also ``Audio.from_endpoint_response()``.

        :param b64: contents of a binary audio file as a base64 encoded string
        :type b64: str
        :return: Audio object
        :rtype: :class:`Audio`
        """
        return cls(audio_b64=b64)

    @classmethod
    def from_endpoint_response(cls, resp_dict: Dict[str, Any], key: str):
        """Create from an endpoint response, such as an endpoint that produces audio.

        :param resp_dict: a response from an OctoAI endpoint that produces audio
        :type resp_dict: Dict[str, Any]
        :param key: the key name in the response that contains an encoded audio file
        :return: Audio object
        :rtype: :class:`Audio`
        """
        if key in resp_dict:
            return cls(audio_b64=resp_dict[key]["audio_b64"])
        elif "output" in resp_dict and key in resp_dict["output"]:
            return cls(audio_b64=resp_dict["output"][key]["audio_b64"])

        raise ValueError(f"{key} not in resp_dict")

    @classmethod
    def from_numpy(cls, data: ArrayLike, sample_rate: int, format="WAV"):
        """Create from a numpy array.

        The first dimension of the array should represent audio frames (samples),
        while the second dimension should represent audio channels.

        A file format and a sample rate are needed since the audio data is
        serialized to a binary audio file. The default format is "WAV", and the
        sample rate is required.

        :param data: numpy array with audio data (frames x channels)
        :type data: ArrayLike
        :param sample_rate: samples per second taken to create signal
        :type sample_rate: int
        :param format: target format, defaults to "WAV"
        :type format: str, optional
        :return: Audio object
        :rtype: :class:`Audio`
        """
        soundfile = _import_soundfile()
        buffer = BytesIO()
        soundfile.write(buffer, data=data, samplerate=sample_rate, format=format)
        return cls(audio_b64=file_b64encode(buffer.getvalue()))

    @classmethod
    def from_file(cls, audio_file: str):
        """Create from local file.

        :param audio_file: path to local audio file
        :type audio_file: str
        :raises ValueError: audio_file not found at provided path
        :return: Audio object
        :rtype: :class:`Audio`
        """
        if not os.path.isfile(audio_file):
            raise ValueError(f"File {audio_file} does not exist")

        with open(audio_file, "rb") as fd:
            return cls(audio_b64=file_b64encode(fd.read()))

    @classmethod
    def from_url(cls, audio_url: str, follow_redirects=False):
        """Create from audio URL.

        :param audio_url: url leading to an audio file
        :type audio_url: str
        :param follow_redirects: whether to follow URL redirects
        :type follow_redirects: bool
        :raises ValueError: there was an error reaching the target url
        :return: Audio object
        :rtype: :class:`Audio`
        """
        resp = httpx.get(audio_url, follow_redirects=follow_redirects)
        if resp.status_code != 200:
            raise ValueError(f"status {resp.status_code} ({audio_url})")

        return cls(audio_b64=file_b64encode(resp.content))

    def is_valid(self):
        """Check if this is a valid audio.

        :return: True if it's valid, false if not.
        :rtype: bool
        """
        try:
            self.to_numpy()
            return True
        except Exception:
            return False

    def to_numpy(self) -> Tuple[ArrayLike, int]:
        """Convert to numpy array.

        :return: numpy array representation (frames x channels)
        :rtype: Tuple[ArrayLike, int]
        """
        soundfile = _import_soundfile()
        fd = BytesIO(file_b64decode(self.audio_b64))
        data, sample_rate = soundfile.read(fd)
        return (data, sample_rate)

    def to_file(self, file_name: str):
        """Save to disk.

        :param file_name: file descriptor or path.
        :type file_name: str
        """
        with open(file_name, "wb") as fd:
            fd.write(file_b64decode(self.audio_b64))
