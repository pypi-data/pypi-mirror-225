import numpy as np

import autumn8
import base64


import base64
import tempfile
from subprocess import CalledProcessError, run
from typing import Optional
import pysubs2

import numpy as np
import static_ffmpeg
import torch
from transformers import (
    Pipeline,
    WhisperForConditionalGeneration,
    WhisperProcessor,
    pipeline,
)


TEN_HOURS = 36000


class WhisperFastLoading:
    def __init__(self):
        self.processor: Optional[WhisperProcessor] = None
        self.model: Optional[WhisperForConditionalGeneration] = None

        self.MODEL_NAME = "openai/whisper-large-v2"
        self.SAMPLE_RATE = 16000

        self.device = "cpu"
        self.processor = WhisperProcessor.from_pretrained(
            "openai/whisper-large-v2"
        )
        self.model = WhisperForConditionalGeneration.from_pretrained(
            self.MODEL_NAME
        ).to(self.device)
        self.model.config.forced_decoder_ids = None
        self.pipeline = None

    def preprocess(self, input, **kwargs):
        self.model.config.forced_decoder_ids = (
            self.processor.get_decoder_prompt_ids(
                language=kwargs.get("language", None), task=kwargs["task"]
            )
        )
        with tempfile.NamedTemporaryFile() as input_file:
            input_file.write(base64.decodebytes(str.encode(input)))
            static_ffmpeg.add_paths()  # blocks until files are downloaded
            # https://github.com/openai/whisper/blob/main/whisper/audio.py#LL43C32-L43C32
            cmd = [
                "ffmpeg",
                "-nostdin",
                "-threads",
                "0",
                "-i",
                input_file.name,
                "-f",
                "s16le",
                "-ac",
                "1",
                "-acodec",
                "pcm_s16le",
                "-ar",
                str(self.SAMPLE_RATE),
                "-",
            ]
            try:
                out = run(cmd, capture_output=True, check=True).stdout
            except CalledProcessError as e:
                raise RuntimeError(
                    f"Failed to load audio: {e.stderr.decode()}"
                ) from e
            array = (
                np.frombuffer(out, np.int16).flatten().astype(np.float32)
                / 32768.0
            )
            return array.copy()

    def inference(self, model_input, **kwargs):
        if self.pipeline is None:
            self.pipeline = pipeline(
                "automatic-speech-recognition",
                model=self.model,
                tokenizer=self.processor.tokenizer,
                feature_extractor=self.processor.feature_extractor,
                chunk_length_s=30,
                device=self.device,
            )

        return self.pipeline(
            model_input,
            batch_size=8,
            return_timestamps=kwargs["predict_timestamps"],
        )

    def postprocess(self, model_output, **kwargs):
        transcription = model_output
        if kwargs.get("predict_timestamps", False):
            transcription = model_output["chunks"]

        subtitles_format = kwargs["subtitles_format"]

        if kwargs.get("predict_timestamps", False) and subtitles_format in [
            "srt",
            "vtt",
        ]:
            subtitle_file = pysubs2.SSAFile()
            subtitle_file.events = [
                pysubs2.SSAEvent(
                    start=pysubs2.make_time(s=phrase["timestamp"][0]),
                    end=pysubs2.make_time(
                        s=phrase["timestamp"][1]
                        or TEN_HOURS  # in some cases, whisper doesn't detect the last timestamp range end - https://github.com/huggingface/transformers/issues/23231
                    ),
                    text=phrase["text"],
                )
                for phrase in transcription
            ]
            subtitle_file.format = subtitles_format

            return subtitle_file.to_string(format_=subtitles_format)

        return transcription

    def __call__(self, model_input, **kwargs):
        prep = self.preprocess(model_input, **kwargs)
        out = self.inference(prep, **kwargs)
        return self.postprocess(out, **kwargs)

    def to(self, device):
        self.device = device
        if device != "cpu":
            self.model.to("cuda")
        else:
            self.model.to(device)

    def eval(self):
        pass


def empty_pass(input, *args, **kwargs):
    return input


autumn8.lib.attach_model(
    WhisperFastLoading(),
    [],
    preprocess=empty_pass,
    postprocess=empty_pass,
    interns=[],
    externs=[
        "torch",
        "huggingface_hub",
        "transformers",
        "accelerate",
        "static_ffmpeg",
        "pysubs2",
    ],
)
