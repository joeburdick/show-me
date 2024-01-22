from show_me.image_generation.image_generate import generate_image
from show_me.image_generation.stability_config import get_stability_config
from inky.auto import auto
from inky.mock import InkyMockImpression

configPath = 'config/stability_config.json'

def display_prompt(prompt):
    # display = auto()
    display = InkyMockImpression()

    display.DESATURATED_PALETTE =  [
        [0, 0, 0],
        [255, 255, 255],
        [0, 255, 0],
        [0, 0, 255],
        [255, 0, 0],
        [255, 255, 0],
        [255, 140, 0],
        [255, 255, 255]]
    
    display.SATURATED_PALETTE = [
        [57, 48, 57],
        [255, 255, 255],
        [58, 91, 70],
        [61, 59, 94],
        [156, 72, 75],
        [208, 190, 71],
        [177, 106, 73],
        [255, 255, 255]]
    
    config = get_stability_config(configPath)
    image = generate_image(config, prompt, display.width, display.height)
    display.set_image(image)
    display.show()
    display.wait_for_window_close()

display_prompt("A hipster in Portland Oregon fighting a Polar bear by the St John's Bridge")