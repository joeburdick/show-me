from show_me.image_generation.image_generate import generate_image
from show_me.image_generation.stability_config import get_stability_config
from inky.auto import auto
from inky.mock import InkyMockImpression

configPath = 'config/stability_config.json'

def display_prompt(prompt):
    # display = auto()
    display = InkyMockImpression()
    config = get_stability_config(configPath)
    image = generate_image(config, prompt, display.width, display.height)
    display.set_image(image)
    display.show()

display_prompt("A cute cat")