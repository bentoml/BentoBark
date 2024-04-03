from __future__ import annotations

import os
import typing as t
from pathlib import Path

import bentoml

SAMPLE_TEXT = "♪ In the jungle, the mighty jungle, the lion barks tonight ♪"

@bentoml.service(
    resources={
        "gpu": 1,
        "gpu_type": "nvidia-tesla-t4",
    },
    traffic={"timeout": 300},
)
class SunoBark:
    def __init__(self) -> None:
        import torch
        from transformers import AutoProcessor, BarkModel

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = AutoProcessor.from_pretrained("suno/bark")
        self.model = BarkModel.from_pretrained("suno/bark").to(self.device)

    
    @bentoml.api
    def generate(
            self,
            context: bentoml.Context,
            text: str = SAMPLE_TEXT,
            voice_preset: t.Optional[str] = None,
    ) -> t.Annotated[Path, bentoml.validators.ContentType('audio/*')]:
        import scipy

        voice_preset = voice_preset or None

        output_path = os.path.join(context.temp_dir, "output.wav")
        inputs = self.processor(text, voice_preset=voice_preset).to(self.device)
        audio_array = self.model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()

        sample_rate = self.model.generation_config.sample_rate
        scipy.io.wavfile.write(output_path, rate=sample_rate, data=audio_array)

        return Path(output_path)
