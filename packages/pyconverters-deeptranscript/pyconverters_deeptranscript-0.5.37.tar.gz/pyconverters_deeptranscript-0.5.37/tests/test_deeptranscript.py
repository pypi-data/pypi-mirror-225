from pathlib import Path
from typing import List
import pytest
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

from pyconverters_deeptranscript.deeptranscript import (
    DeepTranscriptConverter,
    DeepTranscriptParameters,
    InputFormat,
    WebhookServer
)


def test_deeptranscript():
    model = DeepTranscriptConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepTranscriptParameters


@pytest.mark.skip(reason="Not a test")
def test_deeptranscript_wav():
    model = DeepTranscriptConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepTranscriptParameters
    converter = DeepTranscriptConverter()
    parameters = DeepTranscriptParameters(input_format=InputFormat.AudioFile)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/2.wav")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "audio/wav"), parameters
        )
        assert len(docs) == 1
        doc0 = docs[0]
        assert doc0.text.startswith("On bed 7")
    WebhookServer().stop()


@pytest.mark.skip(reason="Not a test")
def test_deeptranscript_webm():
    model = DeepTranscriptConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepTranscriptParameters
    converter = DeepTranscriptConverter()
    parameters = DeepTranscriptParameters(lang="fr", input_format=InputFormat.AudioFile)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/ae26ccf4-ea2b-4bc7-b112-9bdb00931577.webm")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "audio/webm"), parameters
        )
        assert len(docs) == 1
        doc0 = docs[0]
        assert "personnes" in doc0.text
    WebhookServer().stop()


@pytest.mark.skip(reason="Not a test")
def test_deeptranscript_yt():
    model = DeepTranscriptConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepTranscriptParameters
    converter = DeepTranscriptConverter()
    parameters = DeepTranscriptParameters(input_format=InputFormat.YoutubeUrls)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/test.txt")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin), parameters
        )
        assert len(docs) == 1
        doc0 = docs[0]
        assert "business" in doc0.text
    WebhookServer().stop()


@pytest.mark.skip(reason="Not a test")
def test_deeptranscript_yt_playlist_index():
    converter = DeepTranscriptConverter()
    parameters = DeepTranscriptParameters(
        lang="fr", input_format=InputFormat.YoutubeUrls
    )
    testdir = Path(__file__).parent
    source = Path(testdir, "data/playlist_index.txt")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin), parameters
        )
        assert len(docs) == 2
    WebhookServer().stop()


@pytest.mark.skip(reason="Not a test")
def test_deeptranscript_yt_playlist():
    converter = DeepTranscriptConverter()
    parameters = DeepTranscriptParameters(
        lang="fr", input_format=InputFormat.YoutubeUrls, duration=60
    )
    testdir = Path(__file__).parent
    source = Path(testdir, "data/playlist.txt")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin), parameters
        )
        assert len(docs) == 3
    WebhookServer().stop()
