import os
from enum import Enum
from pathlib import Path
from queue import Queue
from tempfile import TemporaryDirectory, NamedTemporaryFile
from time import time
from typing import List, cast, Type

import filetype as filetype
import requests
from filetype.types.audio import Wav
from pydantic import Field, BaseModel
from pydub import AudioSegment
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, AltText
from starlette.datastructures import UploadFile
from yt_dlp import YoutubeDL

from pyconverters_deeptranscript.webhook import WebhookServer

DT_API_KEY = os.environ.get("DT_API_KEY")


class InputFormat(str, Enum):
    AudioFile = "AudioFile"
    YoutubeUrls = "YoutubeUrls"


class DeepTranscriptParameters(ConverterParameters):
    lang: str = Field(
        "en", description="Name of the 2-letter language of the documents"
    )
    input_format: InputFormat = Field(
        InputFormat.AudioFile,
        description="""Input format of the input file, among:<br/>
        <li>`AudioFile`: an audio file (wav, mp3, flac, etc...)<br/>
        <li>`YoutubeUrls`: A plain text file with a list of Youtube urls one by line.""",
    )
    duration: int = Field(300, description="Limit the duration (in seconds) of the audio (0 means no limit)")


class DeepTranscriptConverter(ConverterBase):
    """DeepTranscript converter ."""

    @staticmethod
    def process_audio_file(source, tmpdir, duration, docs):
        kind = filetype.guess(source.file)
        source.file.seek(0)
        if (
                kind is not None
                and kind.mime.startswith("audio")
                or kind.mime.startswith("video")
        ):
            tmp_file = NamedTemporaryFile(
                "w+b", suffix=".wav", dir=tmpdir, delete=False
            )
            try:
                if isinstance(kind, Wav):
                    inputs = source.file.read()
                    tmp_file.write(inputs)
                else:
                    codec = "opus" if kind.extension == "webm" else None
                    segment = AudioSegment.from_file(source.file, codec=codec, duration=duration)
                    # check audio export
                    segment.export(tmp_file, format="wav")
            except BaseException as err:
                raise err
            finally:
                tmp_file.close()
        wav_file = Path(tmp_file.name)
        doc = Document(identifier=wav_file.stem, title=wav_file.stem)
        doc.properties = {"fileName": source.filename}
        docs[wav_file.stem] = doc

    @staticmethod
    def entry2doc(entry, fileName):
        doc = Document(identifier=entry["id"], title=entry["title"])
        doc.properties = {"fileName": fileName}

        doc.metadata = {"url": entry["webpage_url"]}
        if "duration" in entry:
            doc.metadata["duration"] = entry["duration"]
        if "uploader" in entry:
            doc.metadata["uploader"] = entry["uploader"]
        if "channel" in entry:
            doc.metadata["channel"] = entry["channel"]
        if "playlist" in entry:
            doc.metadata["playlist"] = entry["playlist"]
        if entry.get("description", ""):
            doc.altTexts = [
                AltText(
                    name="description", text=entry["description"]
                )
            ]
        return doc

    @staticmethod
    def process_youtube_list(source, tmpdir, duration, docs):
        inputs = source.file.readlines()
        urls = []

        ffmpeg_options = ["-ar", "8000", "-ac", "1"]
        if duration is not None:
            ffmpeg_options.append("-t")
            ffmpeg_options.append(f"{duration}")
        for line in inputs:
            line = (
                str(line, "utf-8").strip() if isinstance(line, bytes) else line.strip()
            )
            if line:
                urls.append(line)
        if urls:
            ydl_opt = {
                "outtmpl": tmpdir + "/%(id)s.%(ext)s",
                "noplaylist": True,
                "id": True,
                "extractaudio": True,
                # 'audioformat': 'flac',
                "preferffmpeg": True,
                "format": "bestaudio/best",
                # 'download_archive': 'downloaded_songs.txt',
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                    }
                ],
                "postprocessor_args": {
                    "extractaudio+ffmpeg_o1": ffmpeg_options
                },
            }
            with YoutubeDL(ydl_opt) as ydl:
                for url in urls:
                    info = ydl.extract_info(url, download=False)
                    if info.get("_type", None) == "playlist":
                        for entry in info["entries"]:
                            doc = DeepTranscriptConverter.entry2doc(entry, source.filename)
                            docs[entry["id"]] = doc
                    else:
                        doc = DeepTranscriptConverter.entry2doc(info, source.filename)
                        docs[info["id"]] = doc
                ydl.download(urls)

    def convert(
            self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: DeepTranscriptParameters = cast(DeepTranscriptParameters, parameters)

        # Test DT token
        resp = requests.get(
            "https://app.deeptranscript.com/api/transcriptions",
            headers={
                "Authorization": f"Bearer {DT_API_KEY}",
            },
        )
        if resp.ok:
            pass
        else:
            resp.raise_for_status()

        webhook = WebhookServer()
        duration = None if params.duration == 0 else params.duration
        docs = {}
        with TemporaryDirectory() as tmpdir:
            tmp_dir = Path(tmpdir)
            if params.input_format == InputFormat.AudioFile:
                self.process_audio_file(source, tmpdir, duration, docs)
            else:
                self.process_youtube_list(source, tmpdir, duration, docs)

            if docs:
                wav_files = list(tmp_dir.glob("*.wav"))
                cb_queue = Queue()
                uids = []
                for wav_file in wav_files:
                    wav_url = f"{webhook.public_url}/files/{tmp_dir.name}/{wav_file.name}"
                    cb_url = f"{webhook.public_url}/callback"

                    resp = requests.post(
                        "https://app.deeptranscript.com/api/transcriptions/",
                        json={
                            "recording": wav_url,
                            "recordingFormat": "wav",
                            "callbackUrl": cb_url,
                            "language": params.lang,
                        },
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {DT_API_KEY}",
                        },
                    )
                    if resp.ok:
                        result = resp.json()
                        uid = result["uid"]
                        doc = docs[wav_file.stem]
                        doc.properties["uid"] = uid
                        uids.append(uid)
                        webhook.QUEUES[uid] = (cb_queue, tmp_dir)
                        cb_queue.put(wav_file)
                join_queue(cb_queue, 300)
                for uid in uids:
                    del webhook.QUEUES[uid]
                for doc in docs.values():
                    uid = doc.properties.get("uid", None)
                    if uid is not None:
                        txt_file = tmp_dir / f"{uid}.txt"
                        if txt_file.exists():
                            with txt_file.open("r") as fin:
                                doc.text = fin.read()
        return list(docs.values())

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepTranscriptParameters


class Pending(Exception):
    "Exception raised by Queue.put(block=0)/put_nowait()."
    pass


def join_queue(q: Queue, timeout=None):
    q.all_tasks_done.acquire()
    try:
        if timeout is None:
            while q.unfinished_tasks:
                q.all_tasks_done.wait()
        elif timeout < 0:
            raise ValueError("'timeout' must be a positive number")
        else:
            endtime = time() + timeout
            while q.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    raise Pending
                q.all_tasks_done.wait(remaining)
    finally:
        q.all_tasks_done.release()
