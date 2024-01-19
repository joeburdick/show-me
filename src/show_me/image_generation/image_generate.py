import os
import io
import warnings
from PIL import Image
from dotenv import load_dotenv
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from show_me.image_generation.stability_config import get_stability_config

def generate_image(prompt: str, width: int, height: int):
    load_dotenv()

    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'], # API Key reference.
        verbose=True, # Print debug messages.
        engine='stable-diffusion-xl-1024-v1-0', # Set the engine to use for generation.
        # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
    )

    config = get_stability_config()

    config['prompt'] = prompt
    config['width'] = width
    config['height'] = height

    answers = stability_api.generate(**config)

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    'Please modify the prompt and try again.')
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(str(artifact.seed)+ '.png') # Save our generated images with their seed number as the filename.