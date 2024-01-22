import os
import io
import warnings
from PIL import Image
from dotenv import load_dotenv
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from show_me.image_generation.stability_config import StabilityConfig, get_stability_config


def generate_image(
    stabilityConfig: StabilityConfig, prompt: str, width: int, height: int
):
    load_dotenv()

    stability_api = client.StabilityInference(
        key=os.environ["STABILITY_KEY"],  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-xl-1024-v1-0",  # Set the engine to use for generation.
        # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
    )

    answers = stability_api.generate(
        prompt=prompt,
        width=width,
        height=height,
        sampler=stabilityConfig.sampler,
        steps=stabilityConfig.steps,
        seed=stabilityConfig.seed,
        cfg_scale=stabilityConfig.cfg_scale,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again."
                )
            if artifact.type == generation.ARTIFACT_IMAGE:
                return Image.open(io.BytesIO(artifact.binary))
    return None